import ffmpeg
import pathlib as pl
import matplotlib.pyplot as plt
import numpy as np
from metavid import metavid
import pickle

# extract scene transitions

i=2
mv = metavid('variables.mp4')
mv.get_scene_transitions() # this saves into mv.timestamps
mv.load_atoms(f'tools/pickle_{i}.pkl')
# import projected atoms arrays



# make plots and overlay
filename_s=f'testFigs_fresh{i}/straight{i}'
filename_b=f'testFigs_fresh{i}/spline{i}'
filename_a=f'testFigs_fresh{i}/color{i}'
mv.overlay_all_plots(
	starting_scene_i=1, fig_type = 1, filename_base=filename_s, file_type = 'pdf'# so first (i=0) scene doesn't get a plot
)
mv = metavid('variables.mp4')
mv.get_scene_transitions() # this saves into mv.timestamps
mv.load_atoms(f'tools/pickle_{i}.pkl')

mv.overlay_all_plots(
	starting_scene_i=1, fig_type = 2, filename_base=filename_b, file_type = 'pdf'# so first (i=0) scene doesn't get a plot
)
mv = metavid('variables.mp4')
mv.get_scene_transitions() # this saves into mv.timestamps
mv.load_atoms(f'tools/pickle_{i}.pkl')

mv.overlay_all_plots(
	starting_scene_i=1, fig_type = 3, filename_base=filename_a, file_type = 'pdf'# so first (i=0) scene doesn't get a plot
)

# run video processing and export video

# mv.export()