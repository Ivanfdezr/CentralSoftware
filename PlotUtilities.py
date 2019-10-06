import numpy as np
from mpl_toolkits import mplot3d
import matplotlib as mpl
import matplotlib.pylab as plt
from matplotlib import cm
from matplotlib.colors import LightSource
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection


Colors = {}
for i,color in enumerate(mpl.rcParams['axes.prop_cycle']):
	Colors['C'+str(i)] = color['color']
Colors['CW'] = '#FFFFFF'


class ZoomPan:
	def __init__(self):
		self.press = None
		self.cur_xlim = None
		self.cur_ylim = None
		self.x0 = None
		self.y0 = None
		self.x1 = None
		self.y1 = None
		self.xpress = None
		self.ypress = None


	def get_xyz_from_cursor(self,event, ax, w):
		"""
		Get coordinates clicked by user
		"""
		if ax.M is None:
			return {}

		xd, yd = event.xdata, event.ydata
		xd=0.0
		
		p = (xd, yd)
		edges = ax.tunit_edges()
		ldists = [(mplot3d.proj3d.line2d_seg_dist(p0, p1, p), i) for i, (p0, p1) in enumerate(edges)]
		#ldists.sort()

		# nearest edge
		edgei = ldists[0][1]

		p0, p1 = edges[edgei]

		# scale the z value to match
		x0, y0, z0 = p0
		x1, y1, z1 = p1
		d0 = np.hypot(x0-xd, y0-yd)
		d1 = np.hypot(x1-xd, y1-yd)
		dt = d0+d1
		z = d1/dt * z0 + d0/dt * z1

		x, y, z = mplot3d.proj3d.inv_transform(xd, yd, z, ax.M)
		
		i = np.where( min(abs(w._verts3d[2]-z))==abs(w._verts3d[2]-z) )[0][0]
		x = w._verts3d[0][i]
		y = w._verts3d[1][i]
		z = w._verts3d[2][i]	
		
		return x, y, z


	def zoom3D_factory(self, ax, curve, base_scale = 1.1):
		def zoom3D(event):
			curr_xlim = np.array(ax.get_xlim())
			curr_ylim = np.array(ax.get_ylim())
			curr_zlim = np.array(ax.get_zlim())
			
			x,y,z = self.get_xyz_from_cursor(event, ax, curve)
			
			##
			##
			if event.button == 'down':
				ax.set_xlim( (curr_xlim-x)*base_scale+x )
				ax.set_ylim( (curr_ylim-y)*base_scale+y )
				ax.set_zlim( (curr_zlim-z)*base_scale+z )
				#ax.dist += 1
				#ax.eye = np.array(ax.eye)*1.1
			elif event.button == 'up':
				ax.set_xlim( (curr_xlim-x)/base_scale+x )
				ax.set_ylim( (curr_ylim-y)/base_scale+y )
				ax.set_zlim( (curr_zlim-z)/base_scale+z )
				#ax.dist -= 1
				#ax.eye = np.array(ax.eye)/1.1
			
			ax.figure.canvas.draw()


		fig = ax.get_figure() # get the figure of interest
		# attach the call back
		fig.canvas.mpl_connect('scroll_event',zoom3D)

		#return the function
		return zoom3D

		
	def point3D_factory(self,ax,dot,curve):
		def move_dot(event):
			##
			try:
				x,y,z = self.get_xyz_from_cursor(event,ax,curve)
				dot.set_data([x],[y])
				dot.set_3d_properties([z])
				ax.figure.canvas.draw()
			except TypeError:
				pass
			
		fig = ax.get_figure()
		fig.canvas.mpl_connect('motion_notify_event', move_dot)
		return move_dot
		

	def zoom2D_factory(self, ax, base_scale = 1.1):
		def zoom2D(event):
			cur_xlim = ax.get_xlim()
			cur_ylim = ax.get_ylim()

			xdata = event.xdata # get event x location
			ydata = event.ydata # get event y location

			if event.button == 'up':
				# deal with zoom in
				scale_factor = 1 / base_scale
			elif event.button == 'down':
				# deal with zoom out
				scale_factor = base_scale
			else:
				# deal with something that should never happen
				scale_factor = 1
				##

			new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
			new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

			relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
			rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

			ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
			ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
			ax.figure.canvas.draw()

		fig = ax.get_figure() # get the figure of interest
		fig.canvas.mpl_connect('scroll_event', zoom2D)

		return zoom2D


	def pan2D_factory(self, ax):
		def onPress(event):
			if event.inaxes != ax: return
			self.cur_xlim = ax.get_xlim()
			self.cur_ylim = ax.get_ylim()
			self.press = self.x0, self.y0, event.xdata, event.ydata
			self.x0, self.y0, self.xpress, self.ypress = self.press

		def onRelease(event):
			self.press = None
			ax.figure.canvas.draw()

		def onMotion(event):
			if self.press is None: return
			if event.inaxes != ax: return
			dx = event.xdata - self.xpress
			dy = event.ydata - self.ypress
			self.cur_xlim -= dx
			self.cur_ylim -= dy
			ax.set_xlim(self.cur_xlim)
			ax.set_ylim(self.cur_ylim)

			ax.figure.canvas.draw()

		fig = ax.get_figure() # get the figure of interest

		# attach the call back
		fig.canvas.mpl_connect('button_press_event',onPress)
		fig.canvas.mpl_connect('button_release_event',onRelease)
		fig.canvas.mpl_connect('motion_notify_event',onMotion)

		#return the function
		return onMotion


	def zoomYD_factory(self, ax, ylims, base_scale=1.1):
		def zoomYD(event):
			#cur_xlim = ax.get_xlim()
			cur_ylim = ax.get_ylim()

			#xdata = event.xdata # get event x location
			ydata = event.ydata # get event y location

			if event.button == 'up':
				# deal with zoom in
				scale_factor = 1 / base_scale
			elif event.button == 'down':
				# deal with zoom out
				scale_factor = base_scale
			else:
				# deal with something that should never happen
				scale_factor = 1
				##

			#new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
			new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

			#relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
			rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

			#ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
			ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
			ylims[0], ylims[1] = ax.get_ylim()

			ax.figure.canvas.draw()

		fig = ax.get_figure() # get the figure of interest
		fig.canvas.mpl_connect('scroll_event', zoomYD)

		return zoomYD

	# ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
	def panYD_factory(self, ax, ylims=None, yselection=None, yselectionfunction=None): 
		
		self.note = ax.annotate( '', [0,0] )

		def onPress(event):
			if event.inaxes != ax: return
			self.cur_xlim = ax.get_xlim()
			if event.button==1:
				self.cur_ylim = ax.get_ylim()
				self.press = self.y0, event.ydata
				self.y0, self.ypress = self.press
			elif event.button==3:
				if isinstance(yselection,list):
					yselection.append(event.ydata)
				if not isinstance(yselectionfunction,type(None)):
					yselectionfunction(event.ydata)

		def onRelease(event):
			self.press = None
			ax.figure.canvas.draw()

		def onMotion(event):
			
			#self.note.set_y( event.ydata )
			#self.note.set_text( str(round(event.ydata,1)) )
			#self.note.draw()

			if self.press is None: return
			if event.inaxes != ax: return
			#dx = event.xdata - self.xpress
			dy = event.ydata - self.ypress
			#self.cur_xlim -= dx
			self.cur_ylim -= dy
			#ax.set_xlim(self.cur_xlim)
			ax.set_ylim(self.cur_ylim)
			if isinstance(ylims,list):
				ylims[0], ylims[1] = ax.get_ylim()

			ax.figure.canvas.draw()

		fig = ax.get_figure() # get the figure of interest

		# attach the call back
		fig.canvas.mpl_connect('button_press_event',onPress)
		fig.canvas.mpl_connect('button_release_event',onRelease)
		fig.canvas.mpl_connect('motion_notify_event',onMotion)

		#return the function
		return onMotion


	# def pressYD_factory(self, ax, yselection=None, yselectionfunction=None, mousebutton=1): 
		
	# 	self.note = ax.annotate( '', [0,0] )

	# 	def onPress(event):
	# 		if event.inaxes != ax: return
	# 		if event.button==mousebutton:
	# 			if isinstance(yselection,list):
	# 				yselection.append(event.ydata)
	# 			if not isinstance(yselectionfunction,type(None)):
	# 				yselectionfunction(event.ydata)
	
	
	
