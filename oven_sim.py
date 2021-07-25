import numpy as np
import matplotlib.pyplot as plt

def get_vertices(tolerance, diameter, length, sheets):
	sheet_width = length/sheets
	error = np.random.normal(0, tolerance, size=sheets)
	center = diameter/2
	num_vertices = sheets + 1
	vertices = []
	x_coord = 0
	for sheet_n in range(sheets):
		count = 0
		while count < 2:
			if count == 1:
				x_coord += sheet_width
			y_coord = error[sheet_n]
			vertices.append((x_coord, y_coord))
			count += 1
	x_coord = 0
	upper_vertices = []
	for sheet_n in range(sheets):
		count = 0
		while count < 2:
			if count == 1:
				x_coord += sheet_width
			y_coord = diameter + error[sheet_n]
			upper_vertices.append((x_coord, y_coord))
			count += 1
	upper_vertices.reverse()
	vertices.extend(upper_vertices)
	return vertices


def get_exit_angle_array(trajectory_array, success_array):
    theta_array = []
    for i in range(len(success_array)):
        if success_array[i]:
            coords1 = trajectory_array[0][i][-2][1]
            coords2 = trajectory_array[0][i][-1][1]
            del_x = coords2[0]-coords1[0]
            del_y = coords2[1]-coords1[1]
            theta_array.append(np.arctan(del_y/del_x))
    return theta_array
