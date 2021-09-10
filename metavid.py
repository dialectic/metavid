import ffmpeg
import pathlib as pl
import os
import matplotlib.pyplot as plt
import numpy as np
import platform
import re
import pickle
from scipy.interpolate import make_interp_spline


class metavid:
	def __init__(self, filename):
		self.filename = pl.Path(filename)
		self.stream = ffmpeg.input(os.fspath(self.filename))
		self.vstream = self.stream.video
		self.astream = self.stream.audio
		self.timestamps = [] # populate with get_scene_transitions
		self.plot_filenames = []

	def run(self, *streams, filename='_dummy.mp4'):
		print(streams)
		system = platform.system()
		if system == 'Darwin':
			print('using macOS hardware acceleration')
			stream = ffmpeg.output(*streams,filename=filename,vcodec='h264_videotoolbox')
		else:
			stream = ffmpeg.output(*streams,filename=filename)
		ffmpeg.run(stream)
		return self

	def export(self, filename=None):
		if not filename:
			filename_lite = self.filename.stem
			filename = pl.Path(filename_lite+'_output.mp4')
		else:
			filename = pl.Path(filename)
		filename = os.fspath(filename)
		self.run(self.astream, self.vstream, filename=filename)
		return self

	def load_atoms(self,filename):
		# loads atoms array from filename pickle file of shape:
		# (n_atoms,2)
		filename = pl.Path(filename)
		self.atoms = pickle.load(open( filename, "rb" )).transpose()
		self.n_atoms = np.shape(self.atoms)[1]
		return self

	def get_scene_transitions(self,force=False):
		# saves metadata timestamps of transitions
		transitions_file = self.filename.stem+'_transitions.txt'
		if not pl.Path(transitions_file).is_file() or force:
			vstream = ffmpeg.filter(self.vstream,'select','gt(scene,0.04)')
			vstream = ffmpeg.filter(vstream,'metadata','print',file=transitions_file)
			self.run(vstream)
		self.timestamps_extract(transitions_file)
		self.n_scenes = 1+len(self.timestamps)
		return self

	def plot(self,filename_base='plots/plot', splinify = True):
		if not len(self.atoms) > 0:
			raise Exception('load atoms first with load_atoms method')
		(pl # make dir if not exist
			.Path(filename_base)
			.parents[0]
			.mkdir(parents=True, exist_ok=True)
		)
		self.plot_filenames = [] # re-initialize
		for i in range(0,self.n_atoms):
			if splinify:
				frame1 = plt.gca()
				# Olive Spline
				# Coordinates
				olvBaseX = self.atoms[0,:]
				olvBaseY = self.atoms[1,:]
				olvSize = olvBaseX.size
				olvBaseT = np.linspace(0, olvSize-1, olvSize)
				
				#Spline
				olvSpline = make_interp_spline(olvBaseT,[olvBaseX,olvBaseY], axis=1, k=2)
				olvSplineT = np.linspace(0, olvSize-1, 500)
				olvSplineCoord = olvSpline(olvSplineT)
				plt.plot(
					olvSplineCoord[0,:],
					olvSplineCoord[1,:], 
					c="darkslateblue", linewidth = 4
					)
	            
	            # Gray Spline
				# Coordinates
				gryBaseX = self.atoms[0,0:i+1]
				grySize = gryBaseX.size
				grySplineT = np.linspace(0, grySize-1, 500)
				# Spline
				grySplineCoord = olvSpline(grySplineT)
				plt.plot(
					grySplineCoord[0,:],
					grySplineCoord[1,:],
					c="tab:gray", linewidth = 4
					)
			else:
				plt.plot(
					self.atoms[0,:],
					self.atoms[1,:], 
					c="tab:olive", marker='o'
					)
				plt.plot(
					self.atoms[0,0:i+1],
					self.atoms[1,0:i+1], 
					c="silver", marker='o'
					)
			plt.plot(
				self.atoms[0,i],
				self.atoms[1,i], 
				c="white", marker='o', markersize=10, linestyle = 'none'
				)
			plt.plot(
				self.atoms[0,i],
				self.atoms[1,i], 
				c="tab:blue", marker='o', markersize=6
				)
			if i>0:
				plt.plot(
					self.atoms[0,0:i],
					self.atoms[1,0:i], 
					c="olive", marker='o', markersize=6, linestyle = 'none'
					)
					
			frame1.axes.xaxis.set_visible(False)
			frame1.axes.yaxis.set_visible(False)
			self.plot_filenames.append( # store filenames
				pl.Path(f'{filename_base}_{i}.png')
			)
			plt.savefig( # save transparent png
				self.plot_filenames[i], 
				transparent=True
			)
			frame1.clear()
		return self

	def overlay_plot(self,image,time_range=[0,10]):
		# overlays a single image on self.vstream over time_range
		image_stream = ffmpeg.input(os.fspath(image))
		self.vstream = ffmpeg.overlay(
			self.vstream,
			image_stream,
			enable=f'between(t,{time_range[0]},{time_range[1]})'
		)
		return self

	def overlay_plot_i(self,image,atom_index):
		# overlays a single image on self.vstream over time range corresponding to atom_index
		time_range = self.time_range_i(atom_index)
		self.overlay_plot(image,time_range)

	def overlay_all_plots(self,starting_scene_i=0):
		# overlays all atom plots on scenes starting with index starting_scene_i
		if not len(self.plot_filenames) > 0:
			self.plot()
		scene_atom_i = range( # scene index for atom
			starting_scene_i,
			self.n_atoms+starting_scene_i
		)
		for i in range(0,self.n_atoms):
			i_scene = scene_atom_i[i]
			self.overlay_plot_i(
				self.plot_filenames[i], # image filename
				i_scene # atom index
			)
		return self

	def time_range_i(self,atom_index):
		if not self.timestamps:
			raise Exception('no timestamps yet: run get_scene_transitions first')
		else:
			if atom_index == 0:
				low = 0.0
			else:
				low = self.timestamps[atom_index]
			if atom_index+1 < len(self.timestamps):
				high = self.timestamps[atom_index+1]
			else:
				high = self.timestamps[-1]
			return [low,high]

	def timestamps_extract(self,tfile):
		# extracts timestamps from tfile from metadata filter in get_scene_transitions method
		self.timestamps = []
		for line in open(tfile):
			match = re.search('pts_time:([+-]?([0-9]*[.])?[0-9]+)', line)
			if match:
				print(match.group(1))
				self.timestamps.append(match.group(1))
		return self
