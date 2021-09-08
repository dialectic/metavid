import ffmpeg
import pathlib as pl
import matplotlib.pyplot as plt
import numpy as np
from metavid import metavid
import pickle

# extract scene transitions

mv = metavid('variables.mp4')
mv.get_scene_transitions() # this saves into mv.timestamps

# import projected atoms arrays

mv.load_atoms('chi_pred.pkl')

# make plots and overlay

mv.overlay_all_plots(
	starting_scene_i=1 # so first (i=0) scene doesn't get a plot
)

# run video processing and export video

# mv.export()