import ffmpeg
import pathlib as pl
import os
import matplotlib.pyplot as plt
import numpy as np
import platform

class metavid:
	def __init__(self, filename):
		self.filename = pl.Path(filename)
		self.stream = ffmpeg.input(os.fspath(self.filename))

	def export(self, filename=None):
		if not filename:
			filename_lite = self.filename.stem
			filename = pl.Path(filename_lite+'_output.mp4')
		else:
			filename = pl.Path(filename)
		filename = os.fspath(filename)
		system = platform.system()
		if system == 'Darwin':
			print('using macOS hardware acceleration')
			self.stream = ffmpeg.output(self.stream,filename,vcodec='h264_videotoolbox')
		else:
			self.stream = ffmpeg.output(self.stream, filename)
		ffmpeg.run(self.stream)
		return self

	def hflip(self):
		self.stream = ffmpeg.hflip(self.stream)
		return self

	def get_scene_transitions(self):
		self.stream = ffmpeg.filter(self.stream,'select','gt(scene,0.05)')
		self.stream = ffmpeg.filter(self.stream,'metadata','print',file=self.filename.stem+'_transitions.txt')
		return self

	def overlay_plot(self,image,time_range=[0,10]):
		image_stream = ffmpeg.input(os.fspath(image))
		self.stream = ffmpeg.overlay(
			self.stream,
			image_stream,
			enable=f'between(t,{time_range[0]},{time_range[1]})'
		)
		return self