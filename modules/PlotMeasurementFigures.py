import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import FormatStrFormatter
import pandas as pd
import numpy as np
from math import ceil, floor
from modules.FigureFormatting import FigureFormatting
from modules.ComsolModel import ComsolModel

plt.style.use('seaborn-colorblind')


# seaborn-colorblind
# seaborn-deep
# dark_background


class PlotMeasurementFigures:
	def __init__(self, df, timestamps, fignames, save_path, comsol_path, sample):
		self.df = df
		self.timestamps = timestamps
		self.fignames = fignames
		self.save_path = save_path
		self.comsol_path = comsol_path
		self.sample = sample
		self.temp_sensor_loc = [0, 4, 8, 12, 16, 20, 24, 26]
		self.moist_sensor_loc = [4, 8, 12, 16]
		self.direction_up = [['U1', 'U2', 'U3', 'U4', 'U5', 'U6'],
							 ['MS1', 'MS2', 'MS3', 'MS4'],
							 'Direction - up']
		self.direction_right = [['R1', 'R2', 'R3', 'R4', 'R5', 'R6'],
								['MS5', 'MS6', 'MS7', 'MS8'],
								'Direction - right']
		self.direction_down = [['D1', 'D2', 'D3', 'D4', 'D5', 'D6'],
							   ['MS9', 'MS10', 'MS11', 'MS12'],
							   'Direction - down']
		self.directions = [self.direction_up, self.direction_right, self.direction_down]
		self.formatter = FigureFormatting()
		self.add_hours_column_to_df()

	def plot_all_measurements(self,
							  folder,
							  formatter,
							  title=False,
							  comsol_model=True,
							  power_line=True,
							  save_fig=True,
							  show_fig=False,
							  xaxis_type='hours',
							  last_day=False):

		# initializer:
		fig, axes = plt.subplots(nrows=4, ncols=3, figsize=formatter['figsize'], sharey='row')
		plt.tight_layout()
		fig.subplots_adjust(wspace=formatter['wspace'], hspace=formatter['hspace'])
		max_col_ind = axes.shape[1]-1
		max_row_ind = axes.shape[0]-1

		# TEMPERATURE SERIES:
		column = 0
		for direction in self.directions:
			curr_col_ind = column
			curr_row_ind = max_row_ind
			self.executor_temperature_series(axes[0, column],
											 max_col_ind,
											 curr_col_ind,
											 max_row_ind,
											 curr_row_ind,
											 direction,
											 formatter,
											 title,
											 power_line,
											 xaxis_type,
											 last_day)
			column += 1

		# TEMPERATURE GRADIENTS:
		column = 0
		for direction in self.directions:
			curr_col_ind = column
			curr_row_ind = max_row_ind
			self.executor_temperature_gradient(axes[1, column],
											   max_col_ind,
											   curr_col_ind,
											   max_row_ind,
											   curr_row_ind,
											   direction,
											   formatter,
											   comsol_model)
			column += 1

		# MOISTURE SERIES:
		column = 0
		for direction in self.directions:
			curr_col_ind = column
			curr_row_ind = max_row_ind
			self.executor_moisture_series(axes[2, column],
										  max_col_ind,
										  curr_col_ind,
										  max_row_ind,
										  curr_row_ind,
										  direction,
										  formatter,
										  power_line,
										  xaxis_type,
										  last_day)
			column += 1

		# MOISTURE GRADIENTS:
		column = 0
		for direction in self.directions:
			curr_col_ind = column
			curr_row_ind = max_row_ind
			self.executor_moisture_gradient(axes[3, column],
											max_col_ind,
											curr_col_ind,
											max_row_ind,
											curr_row_ind,
											direction,
											formatter)
			column += 1

		# save show options:
		if save_fig:
			fig.savefig(self.save_path + folder + 'all_plots', dpi=300, bbox_inches='tight')

		if show_fig:
			plt.show()

		plt.close()

	def plot_temperature_series(self,
								folder,
								formatter,
								title=False,
								power_line=True,
								save_fig=True,
								show_fig=False,
								xaxis_type='hours',
								last_day=False):

		save_names = [self.fignames['time series temp - up'],
					  self.fignames['time series temp - right'],
					  self.fignames['time series temp - down']]

		# subversion configuration:
		if xaxis_type == 'datetime' and last_day:
			savename_ext = '_with_datetime'
		elif xaxis_type == 'datetime' and last_day:
			savename_ext = '_last_24h'
		else:
			savename_ext = ''

		counter = 0
		for direction in self.directions:
			# initializer:
			fig, ax = plt.subplots(figsize=formatter['figsize'], sharex='col')
			plt.tight_layout()
			max_col_ind = 0
			curr_col_ind = 0
			max_row_ind = 0
			curr_row_ind = 0

			self.executor_temperature_series(ax,
											 max_col_ind,
											 curr_col_ind,
											 max_row_ind,
											 curr_row_ind,
											 direction,
											 formatter,
											 title,
											 power_line,
											 xaxis_type,
											 last_day)

			# save show options:
			if save_fig:
				fig.savefig(self.save_path + folder + save_names[counter] + savename_ext, dpi=300, bbox_inches='tight')

			if show_fig:
				plt.show()

			counter += 1

			plt.close()

	def plot_temperature_gradient(self,
								  folder,
								  formatter,
								  comsol_model=True,
								  save_fig=True,
								  show_fig=False):
		save_names = [self.fignames['gradient temp - up'],
					  self.fignames['gradient temp - right'],
					  self.fignames['gradient temp - down']]

		counter = 0
		for direction in self.directions:
			# initializer:
			fig, ax = plt.subplots(figsize=formatter['figsize'])
			plt.tight_layout()
			max_col_ind = 0
			curr_col_ind = 0
			max_row_ind = 0
			curr_row_ind = 0

			self.executor_temperature_gradient(ax,
											   max_col_ind,
											   curr_col_ind,
											   max_row_ind,
											   curr_row_ind,
											   direction,
											   formatter,
											   comsol_model)

			# save show options:
			if save_fig:
				fig.savefig(self.save_path + folder + save_names[counter], dpi=300, bbox_inches='tight')

			if show_fig:
				plt.show()

			counter += 1

			plt.close()

	def plot_moisture_series(self,
							 folder,
							 formatter,
							 power_line=True,
							 save_fig=True,
							 show_fig=False,
							 xaxis_type='hours',
							 last_day=False):

		save_names = [self.fignames['time series moist - up'],
					  self.fignames['time series moist - right'],
					  self.fignames['time series moist - down']]

		# subversion configuration:
		if xaxis_type == 'datetime' and last_day == False:
			savename_ext = '_with_datetime'
		elif xaxis_type == 'datetime' and last_day == True:
			savename_ext = '_last_24h'
		else:
			savename_ext = ''

		counter = 0
		for direction in self.directions:
			# initializer:
			fig, ax = plt.subplots(figsize=formatter['figsize'])
			plt.tight_layout()
			max_col_ind = 0
			curr_col_ind = 0
			max_row_ind = 0
			curr_row_ind = 0

			self.executor_moisture_series(ax,
										  max_col_ind,
										  curr_col_ind,
										  max_row_ind,
										  curr_row_ind,
										  direction,
										  formatter,
										  power_line,
										  xaxis_type,
										  last_day)

			# save show options:
			if save_fig:
				fig.savefig(self.save_path + folder + save_names[counter] + savename_ext, dpi=300, bbox_inches='tight')

			if show_fig:
				plt.show()

			counter += 1

			plt.close()

	def plot_moisture_gradient(self,
							   folder,
							   formatter,
							   save_fig=True,
							   show_fig=False):

		save_names = [self.fignames['gradient moist - up'],
					  self.fignames['gradient moist - right'],
					  self.fignames['gradient moist - down']]

		counter = 0
		for direction in self.directions:
			# initializer:
			fig, ax = plt.subplots(figsize=formatter['figsize'])
			plt.tight_layout()
			max_col_ind = 0
			curr_col_ind = 0
			max_row_ind = 0
			curr_row_ind = 0

			self.executor_moisture_gradient(ax,
											max_col_ind,
											curr_col_ind,
											max_row_ind,
											curr_row_ind,
											direction,
											formatter)

			# save show options:
			if save_fig:
				fig.savefig(self.save_path + folder + save_names[counter], dpi=300, bbox_inches='tight')

			if show_fig:
				plt.show()

			counter += 1

			plt.close()

	def plot_all_temperature_series(self,
									folder,
									formatter,
									title=False,
									power_line=True,
									save_fig=True,
									show_fig=False,
									xaxis_type='hours',
									last_day=False):

		save_name = self.fignames['time series temp']

		# subversion configuration:
		if xaxis_type == 'datetime' and last_day == False:
			savename_ext = '_with_datetime'
		elif xaxis_type == 'datetime' and last_day == True:
			savename_ext = '_last_24h'
		else:
			savename_ext = ''

		# initializer:
		fig, ax = plt.subplots(nrows=3, ncols=1, figsize=formatter['figsize'], sharex='col')
		plt.tight_layout()
		fig.subplots_adjust(hspace=formatter['hspace'])
		max_col_ind = 0
		max_row_ind = len(ax) - 1

		row = 0
		for direction in self.directions:
			curr_col_ind = 0
			curr_row_ind = row
			self.executor_temperature_series(ax[row],
											 max_col_ind,
											 curr_col_ind,
											 max_row_ind,
											 curr_row_ind,
											 direction,
											 formatter,
											 title,
											 power_line,
											 xaxis_type,
											 last_day)
			row += 1

		# save show options:
		if save_fig:
			plt.tight_layout()
			fig.savefig(self.save_path + folder + save_name + savename_ext, dpi=300, bbox_inches='tight')

		if show_fig:
			plt.show()

		plt.close()

	def plot_all_temperature_gradients(self,
									   folder,
									   formatter,
									   comsol_model=True,
									   save_fig=True,
									   show_fig=False):

		save_name = self.fignames['gradient temp']

		# initializer:
		fig, ax = plt.subplots(nrows=3, ncols=1, figsize=formatter['figsize'], sharex='col')
		plt.tight_layout()
		fig.subplots_adjust(hspace=formatter['hspace'])
		max_col_ind = 0
		max_row_ind = len(ax) - 1

		row = 0
		for direction in self.directions:
			curr_col_ind = 0
			curr_row_ind = row
			self.executor_temperature_gradient(ax[row],
											   max_col_ind,
											   curr_col_ind,
											   max_row_ind,
											   curr_row_ind,
											   direction,
											   formatter,
											   comsol_model)
			row += 1

		# save show options:
		if save_fig:
			fig.savefig(self.save_path + folder + save_name, dpi=300, bbox_inches='tight')

		if show_fig:
			plt.show()

		plt.close()

	def plot_all_moisture_series(self,
								 folder,
								 formatter,
								 power_line=True,
								 save_fig=True,
								 show_fig=False,
								 xaxis_type='hours',
								 last_day=False):

		save_name = self.fignames['time series moist']

		# subversion configuration:
		if xaxis_type == 'datetime' and last_day == False:
			savename_ext = '_with_datetime'
		elif xaxis_type == 'datetime' and last_day == True:
			savename_ext = '_last_24h'
		else:
			savename_ext = ''

		# initializer:
		fig, ax = plt.subplots(nrows=3, ncols=1, figsize=formatter['figsize'], sharex='col')
		plt.tight_layout()
		fig.subplots_adjust(hspace=formatter['hspace'])
		max_col_ind = 0
		max_row_ind = len(ax) - 1

		row = 0
		for direction in self.directions:
			curr_col_ind = 0
			curr_row_ind = row
			self.executor_moisture_series(ax[row],
										  max_col_ind,
										  curr_col_ind,
										  max_row_ind,
										  curr_row_ind,
										  direction,
										  formatter,
										  power_line,
										  xaxis_type,
										  last_day)
			row += 1

		# save show options:
		if save_fig:
			fig.savefig(self.save_path + folder + save_name + savename_ext, dpi=300, bbox_inches='tight')

		if show_fig:
			plt.show()

		plt.close()

	def plot_all_moisture_gradients(self,
									folder,
									formatter,
									save_fig=True,
									show_fig=False,):

		save_name = self.fignames['gradient moist']

		# initializer:
		fig, ax = plt.subplots(nrows=3, ncols=1, figsize=formatter['figsize'], sharex='col')
		plt.tight_layout()
		fig.subplots_adjust(hspace=formatter['hspace'])
		max_col_ind = 0
		max_row_ind = len(ax) - 1

		row = 0
		for direction in self.directions:
			curr_col_ind = 0
			curr_row_ind = row
			self.executor_moisture_gradient(ax[row],
											max_col_ind,
											curr_col_ind,
											max_row_ind,
											curr_row_ind,
											direction,
											formatter)
			row += 1

		# save show options:
		if save_fig:
			fig.savefig(self.save_path + folder + save_name, dpi=300, bbox_inches='tight')

		if show_fig:
			plt.show()

		plt.close()

	def executor_temperature_series(self,
									ax,
									max_col_ind,
									curr_col_ind,
									max_row_ind,
									curr_row_ind,
									direction,
									formatter,
									title,
									power_line,
									xaxis_type,
									last_day):
		# ticks:
		yticks_temp_ser, ylim_temp_ser = self.generate_yaxis_ticks_temp_series()
		yticks_sec, ylim_sec = self.generate_yaxis_sec_ticks_series()

		if last_day:
			df = self.create_df_subset()
		else:
			df = self.df

		# plot data:
		if xaxis_type == 'hours':
			for sensor in direction[0]:
				ax.plot(df['hours'],
						df[sensor],
						label=sensor,
						lw=formatter['line_width'],
						marker=None,
						linestyle='solid')
			# configuration:
			if curr_row_ind == max_row_ind:
				ax.set_xlabel('Time, hours', size=formatter['label_size'], labelpad=formatter['labelpad'])
			xticks, xlim = self.generate_xaxis_ticks_hours()

		elif xaxis_type == 'datetime':
			for sensor in direction[0]:
				ax.plot_date(df.index,
							 df[sensor],
							 label=sensor,
							 lw=formatter['line_width'],
							 marker=None,
							 linestyle='solid')
			# configuration:
			if curr_row_ind == max_row_ind:
				ax.set_xlabel('Time, daytime', size=formatter['label_size'], labelpad=formatter['labelpad'])
			xticks, xlim = self.generate_xaxis_ticks_datetime(df, last_day)

		else:
			xlim = 0
			xticks = 0

		# configuration:
		if title:
			ax.set_title(direction[2])
		legend = ax.legend(loc='lower right',
						   fontsize=formatter['legend_size'],
						   handlelength=formatter['legend_length'])
		legend.get_frame().set_linewidth(formatter['legend_frame_width'])
		legend.get_frame().set_edgecolor(formatter['legend_edge_color'])
		legend.remove()

		# power line on plots
		if power_line:
			ax2_temp_series = ax.twinx()
			if xaxis_type == 'hours':
				ax2_temp_series.plot(df['hours'],
									 df['power'],
									 label='power',
									 lw=formatter['line_width'],
									 color='dimgrey',
									 marker=None,
									 linestyle='solid')
			elif xaxis_type == 'datetime':
				ax2_temp_series.plot_date(df.index,
										  df['power'],
										  label='power',
										  lw=formatter['line_width'],
										  color='dimgrey',
										  marker=None,
										  linestyle='solid')
			legend2 = ax2_temp_series.legend(loc='lower left',
								   			 fontsize=formatter['legend_size'],
								   			 handlelength=formatter['legend_length'])
			legend2.get_frame().set_linewidth(formatter['legend_frame_width'])
			legend2.get_frame().set_edgecolor(formatter['legend_edge_color'])
			ax2_temp_series.add_artist(legend)
			if curr_col_ind == max_col_ind:
				ax2_temp_series.set_ylabel('Power, W', size=formatter['label_size'])
				ax2_temp_series.set_yticks(yticks_sec)
			else:
				ax2_temp_series.set_yticks([])
			ax2_temp_series.set_ylim(ylim_sec)
			ax2_temp_series.tick_params(direction='in', width=formatter['tick_width'],
										labelsize=formatter['tick_size'], length=formatter['tick_length'])
			ax2_temp_series.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
			for spine in ['top', 'bottom', 'left', 'right']:
				ax2_temp_series.spines[spine].set_visible(False)
			ax.tick_params(axis='both', direction='in', width=formatter['tick_width'], top=True,
						   labelsize=formatter['tick_size'], length=formatter['tick_length'])

		else:
			ax.add_artist(legend)
			ax.tick_params(axis='both', direction='in', width=formatter['tick_width'], right=True, top=True,
						   labelsize=formatter['tick_size'], length=formatter['tick_length'])

		# configuration:
		ax.set_xlim(xlim)
		ax.set_xticks(xticks)
		if xaxis_type == 'hours':
			ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
		elif xaxis_type == 'datetime' and last_day:
			ax.xaxis.set_major_formatter(DateFormatter('%m-%d  %H:%M'))
		else:
			ax.xaxis.set_major_formatter(DateFormatter('%m-%d'))

		if curr_col_ind == 0:
			ax.set_ylabel('Temperature, °C', size=formatter['label_size'])
		ax.set_ylim(ylim_temp_ser)
		for spine in ['top', 'bottom', 'left', 'right']:
			ax.spines[spine].set_linewidth(formatter['spine_width'])
		plt.setp(ax.get_xticklabels(), rotation=formatter['tick_rotation'], ha='right')
		ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

	def executor_temperature_gradient(self,
									  ax,
									  max_col_ind,
									  curr_col_ind,
									  max_row_ind,
									  curr_row_ind,
									  direction,
									  formatter,
									  comsol_model):
		core_temps = []
		wall_temps = []
		for timestamp in self.timestamps:
			# precalculation:
			core_temp = pd.Series(self.calculate_mean(timestamp[0], self.sample['core_sensors']).mean())
			sensors_temp = self.calculate_mean(timestamp[0], direction[0])
			wall_temp = pd.Series(self.calculate_mean(timestamp[0], self.sample['wall_sensors']).mean())
			mean_temp_values = core_temp.append(sensors_temp)
			mean_temp_values = mean_temp_values.append(wall_temp)
			core_temps.append(core_temp.values)
			wall_temps.append(wall_temp.values)

			# plot data:
			ax.plot(self.temp_sensor_loc,
					mean_temp_values,
					label=timestamp[1],
					linestyle='solid',
					lw=formatter['line_width'],
					marker='o',
					ms=formatter['marker_size'],
					mew=formatter['marker_edge_width'],
					mfc=formatter['marker_face_color'])

		# ticks
		yticks_temp_grad, ylim_temp_grad = self.generate_yaxis_ticks_temp_gradient(core_temps, wall_temps)

		# configuration:
		legend = ax.legend(loc='lower right',
						   fontsize=formatter['legend_size'],
						   handlelength=formatter['legend_length'])
		legend.get_frame().set_linewidth(formatter['legend_frame_width'])
		legend.get_frame().set_edgecolor(formatter['legend_edge_color'])
		if curr_row_ind == max_row_ind:
			ax.set_xlabel('Distance from core, cm', size=formatter['label_size'], labelpad=formatter['labelpad'])
		if curr_col_ind == 0:
			ax.set_ylabel('Temperature, °C', size=formatter['label_size'])
		ax.set_xlim([-1, 27])
		ax.set_xticks(self.temp_sensor_loc)
		ax.set_ylim(ylim_temp_grad)
		ax.set_yticks(yticks_temp_grad)
		ax.tick_params(axis='both', direction='in', width=formatter['tick_width'], right=True, top=True,
					   labelsize=formatter['tick_size'], length=formatter['tick_length'])
		for spine in ['top', 'bottom', 'left', 'right']:
			ax.spines[spine].set_linewidth(formatter['spine_width'])
		ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
		ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))

		# comsol model data:
		if comsol_model:
			model = ComsolModel(self.comsol_path)
			for model in model.comsol_models_dfs:
				ax.plot(model['loc'],
						model['temp'],
						lw=formatter['line_width'],
						linestyle='--',
						linewidth=2,
						color='dimgrey')

	def executor_moisture_series(self,
								 ax,
								 max_col_ind,
								 curr_col_ind,
								 max_row_ind,
								 curr_row_ind,
								 direction,
								 formatter,
								 power_line,
								 xaxis_type,
								 last_day):
		# ticks:
		yticks_sec, ylim_sec = self.generate_yaxis_sec_ticks_series()
		# y ticks should be genetrated here...
		if last_day:
			df = self.create_df_subset()
		else:
			df = self.df

		# plot data:
		if xaxis_type == 'hours':
			for sensor in direction[1]:
				ax.plot(df['hours'],
						df[sensor],
						label=sensor,
						lw=formatter['line_width'],
						marker=None,
						linestyle='solid')
			# configuration:
			if curr_row_ind == max_row_ind:
				ax.set_xlabel('Time, hours', size=formatter['label_size'], labelpad=formatter['labelpad'])
			xticks, xlim = self.generate_xaxis_ticks_hours()

		elif xaxis_type == 'datetime':
			for sensor in direction[1]:
				ax.plot(df.index,
						df[sensor],
						label=sensor,
						lw=formatter['line_width'],
						marker=None,
						linestyle='solid')
			# configuration:
			if curr_row_ind == max_row_ind:
				ax.set_xlabel('Time, daytime', size=formatter['label_size'], labelpad=formatter['labelpad'])
			xticks, xlim = self.generate_xaxis_ticks_datetime(df, last_day)

		else:
			xlim = 0
			xticks = 0

		# configuration:
		# should a title statement be added here??
		legend = ax.legend(loc='lower right',
						   fontsize=formatter['legend_size'],
						   handlelength=formatter['legend_length'])
		legend.get_frame().set_linewidth(formatter['legend_frame_width'])
		legend.get_frame().set_edgecolor(formatter['legend_edge_color'])
		legend.remove()

		# power line on plots
		if power_line:
			ax2_moist_series = ax.twinx()
			if xaxis_type == 'hours':
				ax2_moist_series.plot(df['hours'],
									  df['power'],
									  label='power',
									  lw=formatter['line_width'],
									  color='dimgrey',
									  marker=None,
									  linestyle='solid')
			elif xaxis_type == 'datetime':
				ax2_moist_series.plot_date(df.index,
										   df['power'],
										   label='power',
										   lw=formatter['line_width'],
										   color='dimgrey',
										   marker=None,
										   linestyle='solid')
			ax2_moist_series.legend(loc='lower left',
									fontsize=formatter['legend_size'],
									handlelength=formatter['legend_length'])
			legend2 = ax2_moist_series.legend(loc='lower left',
											  fontsize=formatter['legend_size'],
											  handlelength=formatter['legend_length'])
			legend2.get_frame().set_linewidth(formatter['legend_frame_width'])
			legend2.get_frame().set_edgecolor(formatter['legend_edge_color'])
			ax2_moist_series.add_artist(legend)
			if curr_col_ind == max_col_ind:
				ax2_moist_series.set_ylabel('Power, W', size=formatter['label_size'])
				ax2_moist_series.set_yticks(yticks_sec)
			else:
				ax2_moist_series.set_yticks([])
			ax2_moist_series.set_ylim(ylim_sec)
			ax2_moist_series.tick_params(direction='in', width=formatter['tick_width'],
										 labelsize=formatter['tick_size'], length=formatter['tick_length'])
			ax2_moist_series.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
			for spine in ['top', 'bottom', 'left', 'right']:
				ax2_moist_series.spines[spine].set_visible(False)
			ax.tick_params(axis='both', direction='in', width=formatter['tick_width'], top=True,
						   labelsize=formatter['tick_size'], length=formatter['tick_length'])
		else:
			ax.add_artist(legend)
			ax.tick_params(axis='both', direction='in', width=formatter['tick_width'], right=True, top=True,
						   labelsize=formatter['tick_size'], length=formatter['tick_length'])

		# configuration:
		ax.set_xlim(xlim)
		ax.set_xticks(xticks)
		if xaxis_type == 'hours':
			ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
		elif xaxis_type == 'datetime' and last_day:
			ax.xaxis.set_major_formatter(DateFormatter('%m-%d  %H:%M'))
		else:
			ax.xaxis.set_major_formatter(DateFormatter('%m-%d'))
		if curr_col_ind == 0:
			ax.set_ylabel('Moisture, w%', size=formatter['label_size'])
		for spine in ['top', 'bottom', 'left', 'right']:
			ax.spines[spine].set_linewidth(formatter['spine_width'])
		plt.setp(ax.get_xticklabels(), rotation=formatter['tick_rotation'], ha='right')
		ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

	def executor_moisture_gradient(self,
								   ax,
								   max_col_ind,
								   curr_col_ind,
								   max_row_ind,
								   curr_row_ind,
								   direction,
								   formatter):
		for timestamp in self.timestamps:
			# precalculation:
			mean_moisture = self.calculate_mean(timestamp[0], direction[1])

			# plot data:
			ax.plot(self.moist_sensor_loc,
					mean_moisture,
					label=timestamp[1],
					linestyle = 'solid',
					lw=formatter['line_width'],
					marker='o',
					ms=formatter['marker_size'],
					mew=formatter['marker_edge_width'],
					mfc=formatter['marker_face_color'])

		# configuration:
		legend = ax.legend(loc='lower right',
						   fontsize=formatter['legend_size'],
						   handlelength=formatter['legend_length'])
		legend.get_frame().set_linewidth(formatter['legend_frame_width'])
		legend.get_frame().set_edgecolor(formatter['legend_edge_color'])
		if curr_row_ind == max_row_ind:
			ax.set_xlabel('Distance from core, cm', size=formatter['label_size'], labelpad=formatter['labelpad'])
		if curr_col_ind == 0:
			ax.set_ylabel('Moisture, w%', size=formatter['label_size'])
		ax.set_xlim([-1, 27])
		ax.set_xticks(self.temp_sensor_loc)
		ax.tick_params(axis='both', direction='in', width=formatter['tick_width'], right=True, top=True,
					   labelsize=formatter['tick_size'], length=formatter['tick_length'])
		for spine in ['top', 'bottom', 'left', 'right']:
			ax.spines[spine].set_linewidth(formatter['spine_width'])
		ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
		ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))

	def calculate_mean(self, timestamp, direction_sensors):
		end_time = timestamp
		time_delta = pd.Timedelta(30, unit='m')
		start_time = end_time - time_delta
		mask = (self.df.index >= start_time) & (self.df.index <= end_time)
		mean_values = self.df[mask][direction_sensors].mean()

		return mean_values

	def generate_xaxis_ticks_datetime(self, df, last_day):
		"""
		This function return xlim and xticks for datetime plots:
		If last_day==True, then the function return date_range of every hour.
		If last_day==False, function returns date_range based on the total length of the dataframe.
		"""

		def round_down(t):
			return t.replace(microsecond=0, second=0, minute=0, hour=0)

		def round_up(t):
			return t.replace(microsecond=0, second=0, minute=0, hour=0, day=t.day + 1)

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
			periods = 26
			freq = '2H'
		else:
			start_time = round_down(df.index[0])
			end_time = round_up(df.index[-1])
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

	def generate_xaxis_ticks_hours(self):
		"""
		This function returns:
		- x axis values to plot
		- labels for x axis
		"""
		total_hours = self.df['hours'][-1]

		def roundup_hours(total_hours, period):
			return int(ceil(total_hours / period) * period)

		if total_hours <= 72:
			period = 6
			hours_roundup = roundup_hours(total_hours, period)
		elif 72 < total_hours <= 144:
			period = 12
			hours_roundup = roundup_hours(total_hours, period)
		elif 144 < total_hours <= 288:
			period = 24
			hours_roundup = roundup_hours(total_hours, period)
		else:
			period = 48
			hours_roundup = roundup_hours(total_hours, period)

		xticks = np.arange(0, hours_roundup + period, period)
		max_val = xticks[-1]
		offset = max_val * 0.02
		xlim = [xticks[0] - offset, xticks[-1] + offset]

		return xticks, xlim

	def generate_yaxis_ticks_temp_series(self):
		max_val = max(self.df['U1'].max(), self.df['R1'].max(), self.df['D1'].max())
		min_val = min(self.df['U6'].min(), self.df['R6'].min(), self.df['D6'].min())

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

	def generate_yaxis_ticks_temp_gradient(self, core_temps, wall_temps):
		max_val = max(core_temps)
		min_val = min(wall_temps)

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

	def generate_yaxis_sec_ticks_series(self):
		max_val = self.df['power'].max()

		def roundup_max(val, step):
			return int(ceil(val / step) * step)

		if max_val <= 200:
			step = 40
			max_val = roundup_max(max_val, step)
		else:
			step = 50
			max_val = roundup_max(max_val, step)

		offset = max_val * 0.03

		ylim = [0 - offset, max_val + offset]
		yticks = np.arange(0, max_val + step, step)

		return yticks, ylim

	def add_hours_column_to_df(self):
		start_time = self.df.index[0]

		def calc_hour_diff(time_point):
			diff = time_point - start_time
			return diff.days * 24 + diff.seconds / 3600

		self.df['hours'] = self.df.index.to_series().apply(calc_hour_diff)

	def create_df_subset(self):
		diff = pd.Timedelta(hours=24)
		end_time = self.df.index[-1]
		start_time = end_time - diff
		df = self.df[start_time:end_time]
		return df
