import ffmpeg
import pathlib as pl
import matplotlib.pyplot as plt
import numpy as np
from metastimuli_video import *

# extract scene transitions

mv = metavid('variables.mp4')
mv.get_scene_transitions() # this saves into mv.timestamps

# import projected atom arrays

# should import from Dane's work but generating for now
np.random.seed(19680801)
n_atoms = 9
atoms = np.random.rand(2,n_atoms) * 10.0

# make plots

for i in range(0,n_atoms):
	plt.scatter(atoms[0,:],atoms[1,:], c="g", marker=r'$\clubsuit$')
	plt.scatter(atoms[0,i],atoms[1,i], c="r", marker=r'$\clubsuit$')
	plt.savefig(f'lucky_{i}.png', transparent=True)

# overlay on video

# mv = metavid('variables.mp4')
for i in range(0,n_atoms):
	mv.overlay_plot_i(
		f'lucky_{i}.png', # image file
		i # atom index
	)
mv.export()

# mv = metavid('variables.mp4')
# mv.timestamps_extract('variables_transitions.txt')