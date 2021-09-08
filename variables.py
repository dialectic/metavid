import ffmpeg
import pathlib as pl
import matplotlib.pyplot as plt
import numpy as np
from metastimuli_video import *

# make a plot

np.random.seed(19680801)
x = np.arange(0.0, 50.0, 2.0)
y = x ** 1.3 + np.random.rand(*x.shape) * 30.0
s = np.random.rand(*x.shape) * 800 + 500

plt.scatter(x, y, s, c="g", alpha=0.5, marker=r'$\clubsuit$',
            label="Luck")
plt.xlabel("Leprechauns")
plt.ylabel("Gold")
plt.legend(loc='upper left')
plt.savefig("lucky.png", transparent=True)

# overlay it on video

mv = metavid('variables.mp4')
# mv.overlay_plot(
# 	"lucky.png", # image file
# 	[0,22] # time range (seconds)
# )
# mv.export()

# extract scene transitions

mv = metavid('variables.mp4')
mv.get_scene_transitions()
mv.export('scene_transitioned.mp4')