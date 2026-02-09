import argparse
import importlib
from itertools import product

import numpy as np
import math
from tqdm import tqdm
import matplotlib.pyplot as plt

from src.antialiasing import antialiasing_factor

def eval_point(scene, point):
# Receives a point and returns a color based on the first primitive it's inside of

    # Check if it's a special colored scene (like mandelbrot_colored_scene)
    if hasattr(scene, 'get_point_color'):
        color = scene.get_point_color(point)
        return [color.r, color.g, color.b]

    # Set background color
    final_color = list(scene.background.as_list())
    # If point is inside any primitive, set pixel color to that primitive's color
    for primitive, color in scene:
        inside = primitive.in_out(point)
        if inside:
            # Simple shading: use the red channel as intensity
            final_color = [color.r, color.g, color.b]
            break  # Stop at the first primitive that contains the point
    return final_color

def rotate_point(x, y, center_x, center_y, angle_degrees):
# Function that rotates a point (x,y) around the center
    
    # Negate angle to make positive angles counter-clockwise (standard convention)
    angle_rad = math.radians(angle_degrees)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    # Translate to origin
    dx = x - center_x
    dy = y - center_y
    
    # Rotate
    rotated_x = dx * cos_a - dy * sin_a
    rotated_y = dx * sin_a + dy * cos_a
    
    # Translate back
    return rotated_x + center_x, rotated_y + center_y

def main(args):
    xmin, xmax, ymin, ymax = args.window
    width, height = args.resolution

    # create tensor for image: RGB
    image = np.zeros((height, width, 3))

    # Find coordinates for each pixel
    x_coords = [xmin + (xmax - xmin) * (i + 0.5) / width for i in range(width)]
    y_coords = [ymin + (ymax - ymin) * (j + 0.5) / height for j in range(height)]

    # load scene from file args.scene
    scene = importlib.import_module(args.scene).Scene()

    # Calculate image center for rotation
    center_x = (xmin + xmax) / 2
    center_y = (ymin + ymax) / 2

    # for each pixel, determine if it is inside any primitive in the scene
    # use cartesian product for efficiency
    for j, i in tqdm(product(range(height), range(width)), total=height*width):
        point = (x_coords[i], y_coords[j])

        if args.filter == 'none':
            # No anti-aliasing, just evaluate the center point to find the color
            # Apply rotation if specified
            if args.angle != 0:
                # We invert the angle sign because this is the inverse transformation
                rotated_point = rotate_point(point[0], point[1], center_x, center_y, -args.angle)
            else:
                rotated_point = point
            image[j, i] = eval_point(scene, rotated_point)
        else:
            # Anti-aliasing: sample multiple points within the pixel and weighted average
            weighted_colors = []
            weights = []
            
            for _ in range(args.n_samples):
                # Randomly sample a point within the pixel
                random_number_1 = np.random.rand() - 0.5
                random_number_2 = np.random.rand() - 0.5
                offset_x = random_number_1 * (xmax - xmin) / width
                offset_y = random_number_2 * (ymax - ymin) / height
                sample_point = (point[0] + offset_x, point[1] + offset_y)
                
                # Apply rotation if specified
                if args.angle != 0:
                    rotated_sample_point = rotate_point(sample_point[0], sample_point[1], center_x, center_y, args.angle)
                else:
                    rotated_sample_point = sample_point
                
                # Get filter weight and color
                filter_weight = antialiasing_factor(random_number_1, random_number_2, args.filter, args.sd)
                color = eval_point(scene, rotated_sample_point)
                
                # Store color and weight separately
                weighted_colors.append(np.array(color) * filter_weight)
                weights.append(filter_weight)

            # Proper weighted average: sum(color*weight) / sum(weight)
            if sum(weights) > 0:
                weighted_average = np.sum(weighted_colors, axis=0) / np.sum(weights)
            else:
                # fallback to center point (with rotation if specified)
                if args.angle != 0:
                    rotated_point = rotate_point(point[0], point[1], center_x, center_y, args.angle)
                else:
                    rotated_point = point
                weighted_average = eval_point(scene, rotated_point)
                
            # Ensure values are in [0, 1] range for matplotlib
            image[j, i] = np.clip(weighted_average, 0, 1)
        

    # save image as png using matplotlib
    plt.imsave(args.output, image, vmin=0, vmax=1, origin='lower')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Raster module main function")
    parser.add_argument('-s', '--scene', type=str, help='Scene name', default='mickey_scene')
    parser.add_argument('-w', '--window', type=float, nargs=4, help='Window: xmin xmax ymin ymax', default=[0, 8.0, 0, 6.0])
    parser.add_argument('-r', '--resolution', type=int, nargs=2, help='Resolution: width height', default=[800, 600])
    parser.add_argument('-o', '--output', type=str, help='Output file name', default='output.png')
    parser.add_argument('-f', '--filter', type=str, choices=['none', 'box', 'hat', 'gaussian'], help='Anti-aliasing filter type', default='none')
    parser.add_argument('-n', '--n_samples', type=int, help='Number of samples per pixel for anti-aliasing', default=10)
    parser.add_argument('--sd', type=float, help='Standard deviation for Gaussian filter', default=0.25)
    parser.add_argument('-a', '--angle', type=float, help='Rotation angle in degrees (rotates image content around center)', default=0.0)
    args = parser.parse_args()

    main(args)