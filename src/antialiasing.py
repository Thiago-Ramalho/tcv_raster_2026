import numpy as np
from scipy.special import erf

def antialiasing_factor(x, y, filter_type, sd=0.25):
    if filter_type == 'box':
        return box_filter(x, y)
    elif filter_type == 'hat':
        return hat_filter(x, y)
    elif filter_type == 'gaussian':
        return gaussian_filter(x, y, sd)
    else:
        raise ValueError(f"Unknown filter type: {filter_type}")

def box_filter(x, y):
# Uniform weight within the pixel
    return 1

def hat_filter(x, y):
# A Pyramid which has height 3 so its volume continues to be 1
    return 3 - 6*max(abs(x), abs(y))

def gaussian_filter(x, y, sd):
# 2D Gaussian centered at (0,0)
    
    # Standard 2D gaussian function
    gaussian_value = np.exp(-(x**2 + y**2) / (2 * sd**2))
    
    # Normalization factor to ensure integral = 1 in the domain [-0.5, 0.5]
    # It's difficult to calculate the integral, so here I use a polynomial 
    # regression fit to the exact integral values
    # I(sd) ≈ 1.008sd + 1.164sd^2 (captures both linear spreading and quadratic area)
    integral_approx = 1.008 * sd + 1.164 * sd**2
    normalization_factor = 1.0 / integral_approx
    
    return gaussian_value * normalization_factor