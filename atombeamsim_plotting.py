import atombeamsim
from analyze import *

import numpy as np
import matplotlib.pyplot as plt

with open('angle_array_80deg.npy', 'rb') as f:
    angle_array_80deg = np.load(f)

with open('angle_array_100deg.npy', 'rb') as f:
    angle_array_100deg = np.load(f)

with open('angle_array_smooth.npy', 'rb') as f:
    angle_array_smooth = np.load(f)

angle_array_array = [angle_array_80deg, angle_array_100deg, angle_array_smooth]
label_array = ['80 deg', '100 deg', 'Smooth']

t_profiles.plot_theta_polar(angle_array_array, label_array)
t_profiles.plot_theta_distribution(angle_array_array, label_array)
