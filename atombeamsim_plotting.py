import atombeamsim
from analyze import *

import numpy as np
import matplotlib.pyplot as plt

with open('angle_array.npy', 'rb') as f:
    angle_array = np.load(f)

t_profiles.plot_theta_polar(angle_array)
t_profiles.plot_theta_distribution(angle_array)
