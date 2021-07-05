import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.dates import DateFormatter
from matplotlib.ticker import FormatStrFormatter
import pandas as pd
import numpy as np
from math import ceil, floor
from modules.ComsolModel import ComsolModel
from modules.MiscCalculations import TempDistSolver, ThermalConductivity
from typing import Dict, List, Type, Union
import os
from copy import deepcopy

# TEST 222

# message
# another message
# yooooooo
# yooooo

# new line from precision PC
# another line coming form Precision

#plt.style.use('dark_background')

colors = {
	'red': '#FF7A7A',
	'orange': '#FFBF70',
	'yellow': '#FBFF84',
	'green': '#9CFF89',
	'blue': '#6BF3FF',
	'light_purple': '#70A7FF',
	'dark_purple': '#927FFF',
	'pink': 'FF92FF'}

my_pallete = [
	colors['red'],
	colors['yellow'],
	colors['green'],
	colors['blue'],
	colors['orange'],
	colors['light_purple'],
	colors['dark_purple'],
	colors['pink'],
]


# http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/

color_palette = ['#FDEF54', '#3598FE', '#EF3C77', '#08CF96']

#mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=color_pallete)

#E69F00 orange
#56B4E9 light blue
#009E73 green
#F0E442	yellow
#0072B2 dark blue
#D55E00 red
#CC79A7 pink

# http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/

#print(plt.rcParams['axes.prop_cycle'].by_key()['color'])

# Seaborn color-blind color cycle:
	#0072B2
	#009E73
	#D55E00
	#CC79A7
	#F0E442
	#56B4E9

# seaborn-colorblind
# seaborn-deep
# dark_background


class PlotMeasurementFigures:
	"""
	An instance of this class is initiated only when the user presses any of the plot buttons.
	That means that an instance is created with a particular sample.
	There might be a flaw when printing multiple samples.
	Shouldn't the plotter object be initiated together with the program?
	SImply initiated with sample_data instead of particular sample?
	This object does not load data ot r do any sorts of that kind of manipulation...
	"""
	def __init__(self, ):
		# Sample data placeholders:
		self.sample = None
		self.test_data = None
		self.timestamps = []
		self.comsol_path = None
		self.fignames = None
		self.temp_directions = list()
		self.moist_directions = list()

	def load_sample_into_plotter(self, test_data, active_sample, phase_datetimes):
		"""
		The function picks the corresponding sample that is selected by user.

		:param test_data - this is whole test data instance (large_test_data, small_test_data)
		:param active_sample: the current sample being prepared for plotting
		:param phase_datetimes: dictionary of phase datetimes.
		"""
		self.test_data = test_data
		self.sample = active_sample
		self.fignames = self.test_data.fignames
		self.timestamps = []

		phase_count = len(phase_datetimes)
		phase_number = '1'
		for phase in range(phase_count):
			phase_name = active_sample['phase_names'][phase]
			self.timestamps.append([phase_datetimes[phase_number][1], phase_name])
			phase_number = str(int(phase_number) + 1)

		# These directions are loaded for each sample because the amount of sensors and location is changing:
		self.temp_directions.clear()
		self.moist_directions.clear()
		for direction in self.test_data.temp_directions:
			self.temp_directions.append(self.sample['sensors'][direction])

		for direction in self.test_data.moist_directions:
			self.moist_directions.append(self.sample['sensors'][direction])

		# Sample thermal conductivity (dry thermal conductivity and moist thermal conductivity)
		porosity = self.sample['sample_props']['porosity']
		ks = self.sample['sample_props']['ks']
		rhos = self.sample['sample_props']['rhos']
		w_grav = self.sample['sample_props']['w_grav']

		thermal = ThermalConductivity(porosity, ks, rhos, w_grav)
		self.kdry, self.kmoist = thermal.calculate_thermal_conductivity()

		# Initialize two zone solver
		self.zone_solver = TempDistSolver()

	# Combined plot calls:
	def plot_SN_combined_master(
			self,
			df: pd.DataFrame,
			phase_directory: str,
			folder: str,
			sizer,
			styler,
			xscale,
			title: bool = False,
			comsol_model: bool = False,
			power_line: bool = True,
			save_fig: bool = True,
			show_fig: bool = False,
			xaxis_type: str = 'hours',
			last_day: bool = False):

		# initializer:
		fig, ax = plt.subplots(nrows=4, ncols=3, figsize=sizer['figsize'], sharey='row')
		fig.patch.set_facecolor(styler['facecolor'])
		fig.subplots_adjust(wspace=sizer['wspace'], hspace=sizer['hspace'])
		max_col_ind = ax.shape[1]-1
		max_row_ind = ax.shape[0]-1

		power_sensor = ['power']

		# TEMPERATURE SERIES:
		column = 0
		for temp_direction in self.temp_directions:
			curr_col_ind = column
			curr_row_ind = max_row_ind
			self.executor_time_series(
				df,
				ax[0, column],
				max_col_ind,
				curr_col_ind,
				max_row_ind,
				curr_row_ind,
				temp_direction,
				power_sensor,
				sizer,
				styler,
				title,
				power_line,
				xaxis_type,
				last_day,
				data_type='temperature')
			column += 1

		# TEMPERATURE GRADIENTS:
		column = 0
		for temp_direction in self.temp_directions:
			curr_col_ind = column
			curr_row_ind = max_row_ind
			self.executor_gradients(
				df,
				ax[1, column],
				max_col_ind,
				curr_col_ind,
				max_row_ind,
				curr_row_ind,
				temp_direction,
				sizer,
				styler,
				xscale,
				comsol_model,
				data_type='temperature')
			column += 1

		# MOISTURE SERIES:
		column = 0
		for moist_direction in self.moist_directions:
			curr_col_ind = column
			curr_row_ind = max_row_ind
			self.executor_time_series(df,
									  ax[2, column],
									  max_col_ind,
									  curr_col_ind,
									  max_row_ind,
									  curr_row_ind,
									  moist_direction,
									  power_sensor,
									  sizer,
									  styler,
									  title,
									  power_line,
									  xaxis_type,
									  last_day,
									  data_type='moisture')
			column += 1

		# MOISTURE GRADIENTS:
		column = 0
		for moist_direction in self.moist_directions:
			curr_col_ind = column
			curr_row_ind = max_row_ind
			self.executor_gradients(
				df,
				ax[3, column],
				max_col_ind,
				curr_col_ind,
				max_row_ind,
				curr_row_ind,
				moist_direction,
				sizer,
				styler,
				xscale,
				comsol_model,
				data_type='moisture')
			column += 1

		# save show options:
		if save_fig:
			fig.savefig(os.path.join(phase_directory, folder, 'all_plots'),
						dpi=300,
						bbox_inches='tight',
						facecolor=fig.get_facecolor())

		if show_fig:
			plt.show()

		plt.close()

	def plot_SN_combined_temperature_series(
			self,
			df,
			phase_directory,
			folder,
			sizer,
			styler,
			title=False,
			power_line=True,
			save_fig=True,
			show_fig=False,
			xaxis_type='hours',
			last_day=False):

		save_name = self.fignames['time series temp']

		# subversion configuration:
		if xaxis_type == 'datetime' and not last_day:
			savename_ext = '_with_datetime'
		elif xaxis_type == 'datetime' and last_day:
			savename_ext = '_last_24h'
		else:
			savename_ext = ''

		# initializer:
		fig, ax = plt.subplots(
			nrows=3,
			ncols=1,
			figsize=sizer['figsize'],
			#sharex='col',
		)
		fig.patch.set_facecolor(styler['facecolor'])
		max_col_ind = 0
		max_row_ind = len(ax) - 1
		power_sensor = ['power']

		row = 0
		for temp_direction in self.temp_directions:
			curr_col_ind = 0
			curr_row_ind = row
			self.executor_time_series(
				df,
				ax[row],
				max_col_ind,
				curr_col_ind,
				max_row_ind,
				curr_row_ind,
				temp_direction,
				power_sensor,
				sizer,
				styler,
				title,
				power_line,
				xaxis_type,
				last_day,
				data_type='temperature')
			row += 1

		plt.tight_layout(pad=sizer['tight_layout_pad'], h_pad=sizer['tight_layout_h_pad'])

		# save show options:
		if save_fig:
			fig.savefig(os.path.join(phase_directory, folder, save_name + savename_ext),
						dpi=300,
						facecolor=fig.get_facecolor())

		if show_fig:
			plt.show()

		plt.close()

	def plot_SN_combined_temperature_gradient(
			self,
			df,
			phase_directory,
			folder,
			sizer,
			styler,
			xscale,
			comsol_model=False,
			save_fig=True,
			show_fig=False):

		"""
		Plots combined (3x1) temperature gradient figure.
		This function is called from MainApp by con_SN_combined_temperature_gradient.
		"""
		save_name = self.fignames['gradient temp']

		# initializer:
		fig, ax = plt.subplots(nrows=3, ncols=1, figsize=sizer['figsize'], sharex='col')
		fig.patch.set_facecolor(styler['facecolor'])
		plt.tight_layout()
		fig.subplots_adjust(hspace=sizer['hspace'])
		max_col_ind = 0
		max_row_ind = len(ax) - 1

		row = 0
		for direction in self.temp_directions:
			curr_col_ind = 0
			curr_row_ind = row
			self.executor_gradients(df,
									ax[row],
									max_col_ind,
									curr_col_ind,
									max_row_ind,
									curr_row_ind,
									direction,
									sizer,
									styler,
									xscale,
									comsol_model,
									data_type='temperature')
			row += 1

		# save show options:
		if save_fig:
			fig.savefig(os.path.join(phase_directory, folder, save_name),
						dpi=300,
						bbox_inches='tight',
						facecolor=fig.get_facecolor())

		if show_fig:
			plt.show()

		plt.close()

	def plot_SN_combined_moisture_series(
			self,
			df,
			phase_directory,
			folder,
			sizer,
			styler,
			title=False,
			power_line=True,
			save_fig=True,
			show_fig=False,
			xaxis_type='hours',
			last_day=False):
		"""


		Plots combined (3x1) moisture series gradient figure.
		This function is called from MainApp by con_SN_combined_moisture_series.
		"""

		save_name = self.fignames['time series moist']

		# subversion configuration:
		if xaxis_type == 'datetime' and not last_day:
			savename_ext = '_with_datetime'
		elif xaxis_type == 'datetime' and last_day:
			savename_ext = '_last_24h'
		else:
			savename_ext = ''

		# initializer:
		fig, ax = plt.subplots(nrows=3, ncols=1, figsize=sizer['figsize'], sharex='col')
		fig.patch.set_facecolor(styler['facecolor'])
		max_col_ind = 0
		max_row_ind = len(ax) - 1
		power_sensor = ['power']

		row = 0
		for moist_direction in self.moist_directions:
			curr_col_ind = 0
			curr_row_ind = row
			self.executor_time_series(df,
									  ax[row],
									  max_col_ind,
									  curr_col_ind,
									  max_row_ind,
									  curr_row_ind,
									  moist_direction,
									  power_sensor,
									  sizer,
									  styler,
									  title,
									  power_line,
									  xaxis_type,
									  last_day,
									  data_type='moisture')
			row += 1

		plt.tight_layout(pad=sizer['tight_layout_pad'], h_pad=sizer['tight_layout_h_pad'])

		# save show options:
		if save_fig:
			fig.savefig(os.path.join(phase_directory, folder, save_name + savename_ext),
						dpi=300,
						facecolor=fig.get_facecolor())

		if show_fig:
			plt.show()

		plt.close()

	def plot_SN_combined_moisture_gradients(
			self,
			df,
			phase_directory,
			folder,
			sizer,
			styler,
			xscale,
			comsol_model=False,
			save_fig=True,
			show_fig=False):

		save_name = self.fignames['gradient moist']

		# initializer:
		fig, ax = plt.subplots(nrows=3, ncols=1, figsize=sizer['figsize'], sharex='col')
		fig.patch.set_facecolor(styler['facecolor'])
		fig.subplots_adjust(hspace=sizer['hspace'])
		max_col_ind = 0
		max_row_ind = len(ax) - 1

		row = 0
		for direction in self.moist_directions:
			curr_col_ind = 0
			curr_row_ind = row
			self.executor_gradients(df,
									ax[row],
									max_col_ind,
									curr_col_ind,
									max_row_ind,
									curr_row_ind,
									direction,
									sizer,
									styler,
									xscale,
									comsol_model,
									data_type='moisture')
			row += 1

		# save show options:
		if save_fig:
			fig.savefig(os.path.join(phase_directory, folder, save_name),
						dpi=300,
						bbox_inches='tight',
						facecolor=fig.get_facecolor())

		if show_fig:
			plt.show()

		plt.close()

	def plot_SN_combined_series_moist_vs_temp(
			self,
			df,
			phase_directory,
			folder,
			sizer,
			styler,
			normalized=False,
			title=False,
			power_line=True,
			save_fig=True,
			show_fig=False,
			xaxis_type='hours',
			last_day=False):

		"""
		Plots combined (3x1) moisture vs temperature series.
		This function is called from MainApp by app_SN_combined_series_moist_vs_temp.

		:type show_fig:
		:param save_fig:
		:param power_line:
		:param title:
		:param styler:
		:param sizer:
		:param df - current dataframe to plotted. This can be master dataframe or any of the phase dataframes.
		:param phase_directory - phase directory (master or phaseXX) directory where the plot will be saved.
		:param folder - folder to save in located in the phase_directory.
		:param normalized - if True, the function will plot normalized values of moisture sensors. Those are generated
							that end with _norm.
		"""
		save_name = self.fignames['moist vs temp']

		# primary save extension:
		if not normalized:
			primary_savename_ext = ''
		else:
			primary_savename_ext = '_normalized'

		# secondary save extension:
		if xaxis_type == 'datetime' and not last_day:
			secondary_savename_ext = '_with_datetime'
		elif xaxis_type == 'datetime' and last_day:
			secondary_savename_ext = '_last_24h'
		else:
			secondary_savename_ext = ''

		# initializer:
		fig, ax = plt.subplots(nrows=3, ncols=1, figsize=sizer['figsize'], sharex='col')
		fig.patch.set_facecolor(styler['facecolor'])
		max_col_ind = 0
		max_row_ind = len(ax) - 1



		row = 0
		for moist_direction in self.moist_directions:
			# switch to '_norm' columns:
			if normalized:
				moist_direction = deepcopy(moist_direction)
				for idx in range(len(moist_direction['sensors'])):
					moist_direction['sensors'][idx] += '_norm'

			curr_col_ind = 0
			curr_row_ind = row
			self.executor_time_series(
				df,
				ax[row],
				max_col_ind,
				curr_col_ind,
				max_row_ind,
				curr_row_ind,
				moist_direction,
				moist_direction['temp_sensors'],
				sizer=sizer,
				styler=styler,
				title=title,
				power_line=power_line,
				xaxis_type=xaxis_type,
				last_day=last_day,
				data_type='moisture')
			row += 1

		plt.tight_layout(pad=sizer['tight_layout_pad'], h_pad=sizer['tight_layout_h_pad'])

		# save show options:
		if save_fig:
			fig.savefig(
				os.path.join(phase_directory, folder, save_name + primary_savename_ext + secondary_savename_ext),
				dpi=300,
				facecolor=fig.get_facecolor())

		if show_fig:
			plt.show()

		plt.close()

	# Separate plot function calls:
	def plot_SN_separate_temperature_series(
			self,
			df,
			phase_directory,
			folder,
			sizer,
			styler,
			title=False,
			power_line=True,
			save_fig=True,
			show_fig=False,
			xaxis_type='hours',
			last_day=False):

		"""
		Plots separate figures for every direction for temperature series.
		This function is called from MainApp by con_SN_separate_temperature_series.
		"""

		save_names = [self.fignames['time series temp - up'],
					  self.fignames['time series temp - right'],
					  self.fignames['time series temp - down']]

		# subversion configuration:
		if xaxis_type == 'datetime' and not last_day:
			savename_ext = '_with_datetime'
		elif xaxis_type == 'datetime' and last_day:
			savename_ext = '_last_24h'
		else:
			savename_ext = ''


		counter = 0
		for temp_direction in self.temp_directions:
			# initializer:
			fig, ax = plt.subplots(figsize=sizer['figsize'])
			fig.patch.set_facecolor(styler['facecolor'])
			max_col_ind = 0
			curr_col_ind = 0
			max_row_ind = 0
			curr_row_ind = 0
			power_sensor = ['power']

			self.executor_time_series(df,
									  ax,
									  max_col_ind,
									  curr_col_ind,
									  max_row_ind,
									  curr_row_ind,
									  temp_direction,
									  power_sensor,
									  sizer,
									  styler,
									  title,
									  power_line,
									  xaxis_type,
									  last_day,
									  data_type='temperature')

			# save show options:
			if save_fig:
				fig.savefig(os.path.join(phase_directory, folder, save_names[counter] + savename_ext),
							dpi=300,
							bbox_inches='tight',
							facecolor=fig.get_facecolor())

			if show_fig:
				plt.show()

			counter += 1

			plt.close()

	def plot_SN_separate_temperature_gradient(
			self,
			df,
			phase_directory,
			folder,
			sizer,
			styler,
			xscale,
			comsol_model=False,
			save_fig=True,
			show_fig=False):

		"""
		Plots separate figures for every direction for temperature gradient.
		This function is called from MainApp by con_SN_separate_temperature_gradient.
		"""

		save_names = [self.fignames['gradient temp - up'],
					  self.fignames['gradient temp - right'],
					  self.fignames['gradient temp - down']]

		counter = 0
		for direction in self.temp_directions:
			# initializer:
			fig, ax = plt.subplots(figsize=sizer['figsize'])
			fig.patch.set_facecolor(styler['facecolor'])
			max_col_ind = 0
			curr_col_ind = 0
			max_row_ind = 0
			curr_row_ind = 0

			self.executor_gradients(
				df,
				ax,
				max_col_ind,
				curr_col_ind,
				max_row_ind,
				curr_row_ind,
				direction,
				sizer,
				styler,
				xscale,
				comsol_model,
				data_type='temperature')

			# save show options:
			if save_fig:
				fig.savefig(os.path.join(phase_directory, folder, save_names[counter]),
							dpi=300,
							bbox_inches='tight',
							facecolor=fig.get_facecolor())

			if show_fig:
				plt.show()

			counter += 1

			plt.close()

	def plot_SN_separate_moisture_series(
			self,
			df,
			phase_directory,
			folder,
			sizer,
			styler,
			title=False,
			power_line=True,
			save_fig=True,
			show_fig=False,
			xaxis_type='hours',
			last_day=False):

		"""
		Plots separate figures for every direction for moisture series.
		This function is called from MainApp by con_SN_separate_moisture_series.
		"""

		save_names = [self.fignames['time series moist - up'],
					  self.fignames['time series moist - right'],
					  self.fignames['time series moist - down']]

		# subversion configuration:
		if xaxis_type == 'datetime' and not last_day:
			savename_ext = '_with_datetime'
		elif xaxis_type == 'datetime' and last_day:
			savename_ext = '_last_24h'
		else:
			savename_ext = ''

		counter = 0
		for moist_direction in self.moist_directions:
			# initializer:
			fig, ax = plt.subplots(figsize=sizer['figsize'])
			fig.patch.set_facecolor(styler['facecolor'])
			max_col_ind = 0
			curr_col_ind = 0
			max_row_ind = 0
			curr_row_ind = 0
			power_sensor = ['power']

			self.executor_time_series(
				df,
				ax,
				max_col_ind,
				curr_col_ind,
				max_row_ind,
				curr_row_ind,
				moist_direction,
				power_sensor,
				sizer,
				styler,
				title,
				power_line,
				xaxis_type,
				last_day,
				data_type='moisture')

			# save show options:
			if save_fig:
				fig.savefig(os.path.join(phase_directory, folder, save_names[counter] + savename_ext),
							dpi=300,
							facecolor=fig.get_facecolor())

			if show_fig:
				plt.show()

			counter += 1

			plt.close()

	def plot_SN_separate_moisture_gradient(
			self,
			df,
			phase_directory,
			folder,
			sizer,
			styler,
			xscale,
			comsol_model=False,
			save_fig=True,
			show_fig=False):

		"""
		Plots separate figures for every direction for moisture gradient.
		This function is called from MainApp by con_SN_separate_moisture_gradient.
		"""

		save_names = [self.fignames['gradient moist - up'],
					  self.fignames['gradient moist - right'],
					  self.fignames['gradient moist - down']]

		counter = 0
		for direction in self.moist_directions:
			# initializer:
			fig, ax = plt.subplots(figsize=sizer['figsize'])
			fig.patch.set_facecolor(styler['facecolor'])
			max_col_ind = 0
			curr_col_ind = 0
			max_row_ind = 0
			curr_row_ind = 0

			self.executor_gradients(
				df,
				ax,
				max_col_ind,
				curr_col_ind,
				max_row_ind,
				curr_row_ind,
				direction,
				sizer,
				styler,
				xscale,
				comsol_model,
				data_type='moisture')

			# save show options:
			if save_fig:
				fig.savefig(os.path.join(phase_directory, folder, save_names[counter]),
							dpi=300,
							facecolor=fig.get_facecolor())

			if show_fig:
				plt.show()

			counter += 1

			plt.close()


	def plot_SN_separate_series_moist_vs_temp(
			self,
			df,
			phase_directory,
			folder,
			sizer,
			styler,
			normalized=False,
			title=False,
			power_line=True,
			save_fig=True,
			show_fig=False,
			xaxis_type='hours',
			last_day=False):

		"""
		Plots combined (3x1) moisture vs temperature series.
		This function is called from MainApp by app_SN_combined_series_moist_vs_temp.

		:type show_fig:
		:param save_fig:
		:param power_line:
		:param title:
		:param styler:
		:param sizer:
		:param df - current dataframe to plotted. This can be master dataframe or any of the phase dataframes.
		:param phase_directory - phase directory (master or phaseXX) directory where the plot will be saved.
		:param folder - folder to save in located in the phase_directory.
		:param normalized - if True, the function will plot normalized values of moisture sensors. Those are generated
							that end with _norm.
		"""
		save_names = [self.fignames['time series moist - up'],
					  self.fignames['time series moist - right'],
					  self.fignames['time series moist - down']]

		# primary save extension:
		if not normalized:
			primary_savename_ext = ''
		else:
			primary_savename_ext = '_normalized'

		# secondary save extension:
		if xaxis_type == 'datetime' and not last_day:
			secondary_savename_ext = '_with_datetime'
		elif xaxis_type == 'datetime' and last_day:
			secondary_savename_ext = '_last_24h'
		else:
			secondary_savename_ext = ''

		counter = 0
		for moist_direction in self.moist_directions:
			# initializer:
			fig, ax = plt.subplots(figsize=sizer['figsize'])
			fig.patch.set_facecolor(styler['facecolor'])
			max_col_ind = 0
			curr_col_ind = 0
			max_row_ind = 0
			curr_row_ind = 0
			power_sensor = ['power']

			# switch to '_norm' columns:
			if normalized:
				moist_direction = deepcopy(moist_direction)
				for idx in range(len(moist_direction['sensors'])):
					moist_direction['sensors'][idx] += '_norm'

			self.executor_time_series(
				df,
				ax,
				max_col_ind,
				curr_col_ind,
				max_row_ind,
				curr_row_ind,
				moist_direction,
				moist_direction['temp_sensors'],
				sizer=sizer,
				styler=styler,
				title=title,
				power_line=power_line,
				xaxis_type=xaxis_type,
				last_day=last_day,
				data_type='moisture')


			plt.tight_layout(pad=sizer['tight_layout_pad'], h_pad=sizer['tight_layout_h_pad'])

			# save show options:
			if save_fig:
				fig.savefig(
					os.path.join(phase_directory, folder, save_names[counter] + primary_savename_ext + secondary_savename_ext),
					dpi=300,
					facecolor=fig.get_facecolor())

			if show_fig:
				plt.show()

			counter += 1

			plt.close()

	def plot_SN_hot_end_temperature(
			self,
			df,
			phase_directory,
			folder,
			sizer,
			styler,
			title=False,
			power_line=True,
			save_fig=True,
			show_fig=False,
			xaxis_type='hours',
			last_day=False):

		save_name = self.fignames['hot end temp']

		# subversion configuration:
		if xaxis_type == 'datetime' and not last_day:
			savename_ext = '_with_datetime'
		elif xaxis_type == 'datetime' and last_day:
			savename_ext = '_last_24h'
		else:
			savename_ext = ''

		# initializer:
		fig, ax = plt.subplots(figsize=sizer['figsize'])
		fig.patch.set_facecolor(styler['facecolor'])
		max_col_ind = 0
		curr_col_ind = 0
		max_row_ind = 0
		curr_row_ind = 0
		power_sensor = ['power']
		sensor_dict = {'sensors': ['hot_end']}

		self.executor_time_series(df,
								  ax,
								  max_col_ind,
								  curr_col_ind,
								  max_row_ind,
								  curr_row_ind,
								  sensor_dict,
								  power_sensor,
								  sizer,
								  styler,
								  title,
								  power_line,
								  xaxis_type,
								  last_day,
								  data_type='single')



		# save show options:
		if save_fig:
			fig.savefig(os.path.join(phase_directory, folder, save_name + savename_ext),
						dpi=300,
						bbox_inches='tight',
						facecolor=fig.get_facecolor())

		if show_fig:
			plt.show()

		plt.close()

	def plot_SS_combined_master(self):
		pass

	def plot_SS_time_series(
			self,
			df,
			phase_directory,
			folder,
			sizer,
			styler,
			title=False,
			power_line=True,
			save_fig=True,
			show_fig=False,
			xaxis_type='hours',
			last_day=False):

		save_name = self.fignames['time series']

		# subversion save name configuration:
		if xaxis_type == 'datetime' and not last_day:
			savename_ext = '_with_datetime'
		elif xaxis_type == 'datetime' and last_day:
			savename_ext = '_last_24h'
		else:
			savename_ext = ''

		# initializer:
		fig, ax = plt.subplots(figsize=sizer['figsize'])
		fig.patch.set_facecolor(styler['facecolor'])
		max_col_ind = 0
		curr_col_ind = 0
		max_row_ind = 0
		curr_row_ind = 0
		power_sensor = ['power']

		temp_direction = self.temp_directions[0]

		self.executor_time_series(
			df,
			ax,
			max_col_ind,
			curr_col_ind,
			max_row_ind,
			curr_row_ind,
			temp_direction,
			power_sensor,
			sizer=sizer,
			styler=styler,
			title=title,
			power_line=power_line,
			xaxis_type=xaxis_type,
			last_day=last_day,
			data_type='temperature')

		# save show options:
		if save_fig:
			fig.savefig(os.path.join(phase_directory, folder, save_name + savename_ext),
						dpi=300,
						bbox_inches='tight',
						facecolor=fig.get_facecolor())

		if show_fig:
			plt.show()

		plt.close()

	def plot_SS_temperature_gradient(
			self,
			df,
			phase_directory,
			folder,
			sizer,
			styler,
			xscale,
			comsol_model=False,
			save_fig=True,
			show_fig=False):

		save_name = self.fignames['gradient temp']

		counter = 0
		for direction in self.temp_directions:
			# initializer:
			fig, ax = plt.subplots(figsize=sizer['figsize'])
			fig.patch.set_facecolor(styler['facecolor'])
			max_col_ind = 0
			curr_col_ind = 0
			max_row_ind = 0
			curr_row_ind = 0

			self.executor_gradients(
				df,
				ax,
				max_col_ind,
				curr_col_ind,
				max_row_ind,
				curr_row_ind,
				direction,
				sizer,
				styler,
				xscale,
				comsol_model,
				data_type='temperature')

			# save show options:
			if save_fig:
				fig.savefig(os.path.join(phase_directory, folder, save_name),
							dpi=300,
							facecolor=fig.get_facecolor())

			if show_fig:
				plt.show()

			counter += 1

			plt.close()

	def executor_time_series(
			self,
			df: pd.DataFrame,
			ax: plt.Axes,
			max_col_ind: int,
			curr_col_ind: int,
			max_row_ind: int,
			curr_row_ind: int,
			primary_axis_sensors: Dict,
			secondary_axis_sensors: List,
			sizer,
			styler,
			title: bool,
			power_line: bool,
			xaxis_type,
			last_day,
			data_type):

		"""
		:param df: current dataset to be plotted
		:param ax: current axis in the plot
		:param max_col_ind: maximum column index in subplot
		:param curr_col_ind: current column index in subplot
		:param max_row_ind: maximum row index in subplot
		:param curr_row_ind: current row index in the subplot
		:param primary_axis_sensors: dictionary containing particular direction information (sensors, locations)
		:param secondary_axis_sensors: list containing only sensor names (multiple ('R1', 'R2',..) or one ('power'))
		:param sizer: sizer object to adjust the size of plot
		:param styler: styler object to adjust the style of plot elements
		:param title: bool value, if True add title to the plot
		:param power_line: bool value, if True add power measurement on secondary axis
		:param xaxis_type: type of xaxis selected in gui - 'linear' or 'log'
		:param last_day: bool value, if True plot only last 24h
		:param data_type: string value to select datatype: 'temperature', 'moisture'
		"""

		# configuration based on data type input:
		if data_type == 'temperature':
			yticks, ylim = self.generate_yaxis_ticks_temp_series(df, ['hot_end', 'cold_end'])
			ylabel = 'Temperature, °C'
		elif data_type == 'moisture':
			yticks, ylim = self.generate_yaxis_ticks_temp_series(df, primary_axis_sensors['sensors'])
			if '_norm' in primary_axis_sensors['sensors'][0]:
				ylabel = 'Normalized moisture'
			else:
				ylabel = 'Moisture, mV'
		elif data_type == 'single':
			yticks, ylim = self.generate_yaxis_ticks_temp_series(df, ['hot_end'])
			ylabel = 'Temperature, °C'
		else:
			ylim = []
			yticks = []
			ylabel = []

		# styler:
		ax.set_facecolor(styler['axis_facecolor'])

		# primary axis plot input setup:
		if xaxis_type == 'hours':
			x_vals = df['hours']
			x_label = 'Time, hours'
			xticks, xlim = self.generate_xaxis_ticks_hours(df)
		elif xaxis_type == 'datetime':
			x_vals = df.index
			x_label = 'Time, daytime'
			xticks, xlim = self.generate_xaxis_ticks_datetime(df, last_day)
		else:
			x_vals = None
			x_label = None
			xticks, xlim = None, None

		plot_list = []

		# plot on primary axis:
		for sensor in primary_axis_sensors['sensors']:
			plot = ax.plot(
				x_vals,
				df[sensor],
				label=sensor.split('_')[0],
				lw=sizer['line_width'],
				marker=None,
				linestyle='solid')
			plot_list.append(plot[0])

		# plot core and wall temperature if plotting temperature series
		if data_type == 'temperature':
			plot = ax.plot(
				x_vals,
				df['cold_end'],
				label='cold end',
				lw=1.5,
				color='black',
				linestyle='dashed')
			plot_list.append(plot[0])
			plot = ax.plot(
				x_vals,
				df['hot_end'],
				label='hot end',
				lw=1.5,
				color='black',
				linestyle='dotted')
			plot_list.append(plot[0])

		'''
		# configuration:
		if curr_row_ind == max_row_ind:
			ax.set_xlabel(
				x_label,
				size=sizer['label_size'],
				color=styler['label_color'],
				labelpad=sizer['labelpad'])
		if title:
			ax.set_title(primary_axis_sensors['direction_name'])
		'''

		twinx_config = False
		if secondary_axis_sensors[0] == 'power' and power_line is True:
			# This filters out of power is plotted on secondary axis
			# Only this option is linked to the power selection in gui
			ax_twinx = ax.twinx()
			twinx_config = True
			twinx_ylabel = 'Power, W'
			yticks_sec, ylim_sec = self.generate_yaxis_ticks_temp_series(df, secondary_axis_sensors)

			# plot data:
			plot = ax_twinx.plot(
				x_vals,
				df['power'],
				label='power',
				lw=sizer['line_width'],
				color='dimgrey',
				marker=None,
				linestyle='solid')
			plot_list.append(plot[0])

		elif power_line is False:
			# This is true for plots when power_line is False:
			ax_twinx = None		 # dummy
			twinx_ylabel = None	 # dummy
			yticks_sec = None	 # dummy
			ylim_sec = None		 # dummy
		else:
			# Other data is plotted here (for now only temperature for moist vs temp plots)
			ax_twinx = ax.twinx()
			twinx_config = True
			twinx_ylabel = 'Temperature, °C'
			yticks_sec, ylim_sec = self.generate_yaxis_ticks_temp_series(df, secondary_axis_sensors)

			for sensor in secondary_axis_sensors:
				if xaxis_type == 'hours':
					plot = ax_twinx.plot(
						df['hours'],
						df[sensor],
						label=sensor,
						lw=sizer['line_width'],
						marker=None,
						linestyle='--')
					plot_list.append(plot[0])
				elif xaxis_type == 'datetime':
					plot = ax_twinx.plot_date(
						df.index,
						df[sensor],
						label=sensor,
						lw=sizer['line_width'],
						marker=None,
						linestyle='--')
					plot_list.append(plot[0])

		# legend configuration
		labels = [plot.get_label() for plot in plot_list]
		if len(labels) <= 8:
			ncols = 1
		else:
			ncols = 2

		if twinx_config:
			# legend:
			legend = ax_twinx.legend(
				plot_list,
				labels,
				ncol=ncols,
				loc=sizer['legend_loc'],
				bbox_to_anchor=sizer['legend_bbox_to_anchor'],
				borderaxespad=sizer['legend_borderaxespad'],
				fontsize=sizer['legend_size'],
				handlelength=sizer['legend_handlelength'],
				labelcolor=styler['legend_text_color'],
				edgecolor=styler['legend_edge_color'],
				frameon=False,
				labelspacing=sizer['legend_labelspacing'])
			legend.get_frame().set_linewidth(sizer['legend_frame_width'])
			legend.get_frame().set_alpha(None)
			legend.get_frame().set_facecolor(styler['legend_face_color_rgba'])

			if curr_col_ind == max_col_ind:
				ax_twinx.set_ylabel(
					twinx_ylabel,
					size=sizer['label_size'],
					color=styler['label_color'])
				ax_twinx.set_yticks(yticks_sec)
			else:
				ax_twinx.set_yticks([])

			ax_twinx.set_ylim(ylim_sec)
			ax_twinx.tick_params(
				direction='in',
				width=sizer['tick_width'],
				labelsize=sizer['tick_size'],
				length=sizer['tick_length'],
				color=styler['tick_color'],
				labelcolor=styler['tick_label_color'])
			ax_twinx.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
			ax.tick_params(
				axis='both',
				direction='in',
				width=sizer['tick_width'],
				top=True,
				labelsize=sizer['tick_size'],
				length=sizer['tick_length'],
				color=styler['tick_color'],
				labelcolor=styler['tick_label_color'])
			ax.tick_params(axis='x', which='major', pad=2)

			# spines:
			for spine in ['top', 'bottom', 'left', 'right']:
				ax_twinx.spines[spine].set_visible(False)

		else:
			# These options are executed if nothing is plotted on the secondary axis
			legend = ax.legend(
				plot_list,
				labels,
				ncol=ncols,
				loc=sizer['legend_loc'],
				bbox_to_anchor=sizer['legend_bbox_to_anchor'],
				borderaxespad=sizer['legend_borderaxespad'],
				fontsize=sizer['legend_size'],
				handlelength=sizer['legend_handlelength'],
				labelcolor=styler['legend_text_color'],
				edgecolor=styler['legend_edge_color'],
				frameon=False,
				labelspacing=sizer['legend_labelspacing'])
			legend.get_frame().set_linewidth(sizer['legend_frame_width'])
			legend.get_frame().set_alpha(None)
			legend.get_frame().set_facecolor(styler['legend_face_color_rgba'])
			ax.tick_params(
				axis='both',
				direction='in',
				width=sizer['tick_width'],
				right=True,
				top=True,
				labelsize=sizer['tick_size'],
				length=sizer['tick_length'],
				color=styler['tick_color'],
				labelcolor=styler['tick_label_color'])

		# configuration:
		ax.set_xlim(xlim)
		ax.set_xticks(xticks)
		if xaxis_type == 'hours':
			ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
		elif xaxis_type == 'datetime' and last_day:
			ax.xaxis.set_major_formatter(DateFormatter('%d-%m  %H:%M'))
		else:
			ax.xaxis.set_major_formatter(DateFormatter('%d-%m'))

		if curr_col_ind == 0:
			ax.set_ylabel(ylabel,
						  size=sizer['label_size'],
						  color=styler['label_color'])
		ax.set_ylim(ylim)
		ax.set_yticks(yticks)
		for spine in ['top', 'bottom', 'left', 'right']:
			ax.spines[spine].set_linewidth(sizer['spine_width'])
			ax.spines[spine].set_color(styler['spine_color'])
		plt.setp(ax.get_xticklabels(), rotation=sizer['tick_rotation'], ha='right')
		if yticks[-1] == 1:
			ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
		else:
			ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

	def executor_gradients(
			self,
			df,
			ax,
			max_col_ind,
			curr_col_ind,
			max_row_ind,
			curr_row_ind,
			direction,
			sizer,
			styler,
			xscale,
			comsol_model,
			data_type):

		hot_end_temp = None
		cold_end_temp = None
		max_date = df.index.max()
		min_date = df.index.min()

		for timestamp in self.timestamps:
			if min_date <= timestamp[0] <= max_date:
				if data_type == 'temperature':
					# Get hot end temperature value (single value) as ndarray:
					hot_end_temp = [
						self.calculate_mean(df, timestamp[0],
						self.sample['hot_end_sensors']['sensors']).mean()]
					# Get sensor temperature values (multiple values) as ndarray:
					sensors_temps = self.calculate_mean(df, timestamp[0], direction['sensors']).values.tolist()
					# Get cold end temperature value as pandas Series:
					cold_end_temp = [
						self.calculate_mean(df, timestamp[0],
						self.sample['cold_end_sensors']['sensors']).mean()]
					power = self.calculate_mean(df, timestamp[0], 'power')
					# Concatenated temperatures into single ndarray.
					grad_values = hot_end_temp + sensors_temps + cold_end_temp
					# Get sensor locations and add wall and core locs:
					sensor_loc = direction['locations'].copy()
					sensor_loc.insert(0, self.sample['hot_end_sensors']['locations'][0])
					sensor_loc.append(self.sample['cold_end_sensors']['locations'][0])
					label = timestamp[1]
				elif data_type == 'moisture':
					if len(direction['sensors']) != 0:
						grad_values = self.calculate_mean(df, timestamp[0], direction['sensors'])
						sensor_loc = direction['locations'].copy()
						label = timestamp[1]
					else:
						grad_values = []
						sensor_loc = []
						label = ''
				else:
					grad_values = 0
					sensor_loc = 0
					label = 0

				# plot data:
				ax.plot(
					sensor_loc,
					grad_values,
					label=label,
					linestyle='solid',
					lw=sizer['line_width'],
					marker='o',
					ms=sizer['marker_size'],
					mew=sizer['marker_edge_width'],
					mfc=sizer['marker_face_color'])

		# data type configuration:
		if data_type == 'temperature':
			yticks, ylim = self.generate_yaxis_ticks_temp_gradient(hot_end_temp, cold_end_temp)
			ylabel = 'Temperature, °C'
		elif data_type == 'moisture':
			yticks = [450, 500, 550]
			ylim = [450, 550]
			ylabel = 'Moisture, mV'
		else:
			yticks = 0
			ylim = 0
			ylabel = 0

		# styler:
		ax.set_facecolor(styler['axis_facecolor'])

		# configuration:
		legend = ax.legend(
			loc='upper right',
			fontsize=sizer['legend_size'],
			handlelength=sizer['legend_handlelength'],
			labelcolor=styler['legend_text_color'],
			edgecolor=styler['legend_edge_color'])
		legend.get_frame().set_linewidth(sizer['legend_frame_width'])
		legend.get_frame().set_alpha(None)
		legend.get_frame().set_facecolor(styler['legend_face_color_rgba'])
		if curr_row_ind == max_row_ind:
			ax.set_xlabel(
				'Distance from core, cm',
				size=sizer['label_size'],
				color=styler['label_color'],
				labelpad=sizer['labelpad'])
		if curr_col_ind == 0:
			ax.set_ylabel(ylabel,
						  size=sizer['label_size'],
						  color=styler['label_color'])

		if xscale == 'log':
			ax.set_xscale(xscale)
			ax.set_xlim([0.1, 27])
		else:  						# this means xscale=='linear'
			ax.set_xlim([-1, 27])

		ax.set_ylim(ylim)
		ax.set_yticks(yticks)
		ax.tick_params(
			axis='both',
			direction='in',
			width=sizer['tick_width'],
			right=True,
			top=True,
			labelsize=sizer['tick_size'],
			length=sizer['tick_length'],
			color=styler['tick_color'],
			labelcolor=styler['tick_label_color'])
		for spine in ['top', 'bottom', 'left', 'right']:
			ax.spines[spine].set_linewidth(sizer['spine_width'])
			ax.spines[spine].set_color(styler['spine_color'])
		ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
		ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))

		# comsol model data:
		if comsol_model:
			model = ComsolModel(self.comsol_path)
			for model in model.comsol_models_dfs:
				ax.plot(
					model['loc'],
					model['temp'],
					lw=sizer['line_width'],
					linestyle='--',
					color='dimgrey')

		'''
		# theoretical model fit:
		if data_type == 'temperature':
			temp_dist = self.zone_solver.two_zone_solver(self.kdry, self.kmoist,
														 float(wall_temp), float(core_temp), power)
		'''

	@staticmethod
	def calculate_mean(df, timestamp, sensors):
		"""
		The function returns mean values of given columns.
		Returned value is Pandas Series with one or multiple values.
		"""
		end_time = timestamp
		time_delta = pd.Timedelta(30, unit='m')
		start_time = end_time - time_delta
		mask = (df.index >= start_time) & (df.index <= end_time)
		mean_values = df[mask][sensors].mean()

		return mean_values

	@staticmethod
	def step_size_ticks(range_diff):
		if 0 < range_diff <= 1:
			step = 0.2
		elif 1 < range_diff <= 10:
			step = 1
		elif 10 < range_diff <= 20:
			step = 2
		elif 20 < range_diff <= 50:
			step = 5
		elif 50 < range_diff <= 100:
			step = 10
		elif 100 < range_diff <= 200:
			step = 20
		elif 200 < range_diff <= 500:
			step = 50
		else:
			step = None

		return step

	@staticmethod
	def generate_xaxis_ticks_datetime(df, last_day):
		"""
		This function return xlim and xticks for datetime plots:
		If last_day==True, then the function return date_range of every second hour.
		If last_day==False, function returns date_range based on the total length of the dataframe.
		"""

		def round_down_day(t):
			return t.replace(microsecond=0, second=0, minute=0, hour=0)

		def round_up_day(t):
			one_day = pd.Timedelta(days=1)
			t.replace(microsecond=0, second=0, minute=0, hour=0)
			t += one_day
			return t

		def round_hour_down(t):
			return t.replace(microsecond=0, second=0, minute=0)

		def round_hour_up(t):
			if t.hour == 23:
				return t.replace(microsecond=0, second=0, minute=0, hour=0, day=t.day + 1)
			else:
				return t.replace(microsecond=0, second=0, minute=0, hour=t.hour + 1)

		def roundup_periods(hours, period):
			return int(ceil(hours / period))

		if last_day:
			start_time = round_hour_down(df.index[0])
			end_time = round_hour_up(df.index[-1])
			periods = 13
			freq = '2H'
		else:
			start_time = round_down_day(df.index[0])
			end_time = round_up_day(df.index[-1])
			diff = end_time - start_time
			total_hours = diff.days * 24 + diff.seconds / 3600
			if total_hours <= 144:  # up to 6 days
				period = 6
				freq = '6H'
			elif 144 < total_hours <= 432:  # from 6 to 18 days
				period = 12
				freq = '12H'
			elif 432 < total_hours <= 864:  # from 18 to 36 days
				period = 24
				freq = '24H'
			else:  # more than 36 days
				period = 48
				freq = '48H'
			periods = roundup_periods(total_hours, period)
			periods += 1

		xticks = pd.date_range(start=start_time, periods=periods, freq=freq)
		xlim = [start_time, end_time]

		return xticks, xlim

	@staticmethod
	def generate_xaxis_ticks_hours(df):
		"""
		This function returns:
		- x axis values to plot
		- labels for x axis
		"""
		max_hour = df['hours'][-1]
		min_hour = df['hours'][0]

		total_hours = (max_hour - min_hour)

		def roundup_hours(max_hour, period):
			return int(ceil(max_hour / period) * period)

		def rounddown_hours(min_hour, period):
			return int(floor(min_hour / period) * period)

		if total_hours <= 72:
			period = 6
			max_hour = roundup_hours(max_hour, period)
			min_hour = rounddown_hours(min_hour, period)
		elif 72 < total_hours <= 144:
			period = 12
			max_hour = roundup_hours(max_hour, period)
			min_hour = rounddown_hours(min_hour, period)
		elif 144 < total_hours <= 288:
			period = 24
			max_hour = roundup_hours(max_hour, period)
			min_hour = rounddown_hours(min_hour, period)
		else:
			period = 48
			max_hour = roundup_hours(max_hour, period)
			min_hour = rounddown_hours(min_hour, period)

		xticks = np.arange(min_hour, max_hour + period, period)
		offset = (max_hour - min_hour) * 0.02
		xlim = [xticks[0] - offset, xticks[-1] + offset]

		return xticks, xlim

	def generate_yaxis_ticks_temp_series(self, df, sensors: List):
		"""
		The function generate yticks and ylim values based on temperature, moisture or power column(s)

		Step size is determined based on the range (max - min):
			range 0 - 1: 0.2
			range 1 - 10: 1
			range 10 - 20: 2
			range 20 - 50: 5
			range 50 - 100: 10
			range 100 - 200: 20
			range 200 - 500: 50

		:param df: active dataframe (master or phase)
		:param sensors: list with one or multiple entry
		:return: yticks and ylim
		"""

		max_val = np.nanmax(df[sensors])
		min_val = np.nanmin(df[sensors])
		step = self.step_size_ticks(max_val - min_val)


		def roundup_max(val):
			return int(ceil(val / step) * step)

		def rounddown_min(val):
			return int(floor(val / step) * step)

		max_val = roundup_max(max_val)
		min_val = rounddown_min(min_val)
		offset = (max_val - min_val) * 0.03

		ylim = [min_val - offset, max_val + offset]
		yticks = np.arange(min_val, max_val + step, step)

		return yticks, ylim

	@staticmethod
	def generate_yaxis_ticks_temp_gradient(hot_end_temp: List, cold_end_temp: List):
		"""
		The function generates yticks and ylim for temperature gradient plot.
		The maximum and minimum values are derived from the cold and hot end temperatures.
		"""
		max_val = np.nanmax(hot_end_temp)
		min_val = np.nanmin(cold_end_temp)

		def roundup_max(val):
			return int(ceil(val / 10) * 10)

		def rounddown_min(val):
			return int(floor(val / 10) * 10)

		max_val = roundup_max(max_val)
		min_val = rounddown_min(min_val)
		offset = max_val * 0.03

		ylim = [min_val - offset, max_val + offset]
		yticks = np.arange(min_val, max_val + 10, 10)

		return yticks, ylim

