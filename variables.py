import ffmpeg
import pathlib as pl
import matplotlib.pyplot as plt
import numpy as np
from metastimuli_video import *
import pickle

# extract scene transitions

mv = metavid('variables.mp4')
mv.get_scene_transitions() # this saves into mv.timestamps

# import projected atom arrays

atoms = pickle.load(open( "chi_pred.pkl", "rb" )).transpose()
n_atoms = np.shape(atoms)[1]

# make plots

for i in range(0,n_atoms):
	plt.scatter(atoms[0,:],atoms[1,:], c="g", marker='o')
	plt.scatter(atoms[0,i],atoms[1,i], c="r", marker='o')
	plt.savefig(f'lucky_{i}.png', transparent=True)

# overlay on video

# mv = metavid('variables.mp4')
for i in range(0,n_atoms):
	mv.overlay_plot_i(
		f'lucky_{i}.png', # image file
		i # atom index
	)
# mv.export()

# mv = metavid('variables.mp4')
# mv.timestamps_extract('variables_transitions.txt')