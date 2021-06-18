import numpy as np
import pandas as pd
import os
import shutil


class DataProcessor:
	def __init__(self, large_test_data, small_test_data):
		self.large_test_data = large_test_data
		self.small_test_data = small_test_data
		self.test_setups = [
			self.large_test_data,
			self.small_test_data,
		]

		self.measurement_folder = '02_measurement_data'
		self.comsol_folder = '03_comsol_model'
		self.calib_folder = '04_calib_data'
		self.corrected_df_folder = '01_calibrated_datasets'

		self.source_folder_list = [
			'C:\\Users\\karlisr\\OneDrive\\LargeMoistureCell',
			#'C:\\Users\\karlisr\\OneDrive\\SmallMoistureCell',
		]

		self.target_folder_list = [
			'C:\\Users\\karlisr\\OneDrive - NTNU\\3_PostDoc_Sintef\\01_laboratory_work\\'
			'01_large_test\\01_measured_samples',
			#'C:\\Users\\karlisr\\OneDrive - NTNU\\3_PostDoc_Sintef\\01_laboratory_work\\'
			#'02_small_test\\01_measured_samples',
		]


	@staticmethod
	def load_single_file(sample_data_dir, file):

		def combine_datetime(x):
			"""Combines date and time cells into one"""
			return x[0] + ' ' + x[1]

		df_loc = pd.read_csv(
			os.path.join(sample_data_dir, file),
			skiprows=5,
			header=None,
			delim_whitespace=True)
		df_loc[0] = df_loc.iloc[:, 0:2].apply(combine_datetime, axis=1)
		df_loc.drop(df_loc.columns[1], axis=1, inplace=True)
		df_loc.index = df_loc[0]
		df_loc.index = pd.to_datetime(df_loc.index)
		df_loc.drop(df_loc.columns[0], axis=1, inplace=True)

		return df_loc

	@staticmethod
	def add_hours_column_to_df(df_loc):
		start_time = df_loc.index[0]

		def calc_hour_diff(time_point):
			diff = time_point - start_time

			return diff.days * 24 + diff.seconds / 3600

		df_loc['hours'] = df_loc.index.to_series().apply(calc_hour_diff)

		return df_loc

	@staticmethod
	def add_cold_end_temp_column(active_sample, df_loc):
		df_loc['cold_end'] = df_loc[active_sample['cold_end_sensors']['sensors']].mean(axis=1)

		return df_loc

	@staticmethod
	def add_hot_end_temp_column(active_sample, df_loc):
		df_loc['hot_end'] = df_loc[active_sample['hot_end_sensors']['sensors']].mean(axis=1)

		return df_loc

	@staticmethod
	def nan_out_low_moisture_vals(active_sample, df_loc):
		def f(x):
			if x < 300:
				x = np.nan
			return x

		for column in active_sample['moisture_columns']:
			df_loc[column] = df_loc[column].apply(f)

		return df_loc

	@staticmethod
	def normalize_moisture_values(active_sample, df_loc):
		def normalized_vals(moist_val, min_val, max_val):
			if moist_val != np.nan:
				moist_val = (moist_val - min_val) / (max_val - min_val)
			return moist_val

		for sensor in active_sample['moisture_columns']:
			# find min and max values:
			min_val = np.nanmin(df_loc[sensor])
			max_val = np.nanmax(df_loc[sensor])

			df_loc[sensor + '_norm'] = df_loc[sensor].apply(lambda x: normalized_vals(x, min_val, max_val))

		return df_loc

	@staticmethod
	def delete_flawed_data(active_sample, df_loc):
		for data_chunk in active_sample['del_data']:
			start_time = data_chunk['start']
			end_time = data_chunk['end']
			sensor = data_chunk['sensor']
			df_loc[sensor][start_time:end_time] = df_loc[sensor][start_time:end_time].apply(lambda val: np.nan)

		return df_loc

	def generate_phase_dfs(self, active_sample, active_test, df_loc):
		"""
		The function generates a list with of phased dfs. The first element in the list is the master phase while the
		following are each particular phase based on start and end datetimes.

		:return: list with all phase dfs as follows: [MASTER_PHASE, PHASE1, PHASE2..]
		"""
		# Get pahse dates:
		phase_datetimes = self.generate_df(active_sample, active_test, return_phases_times=True)
		# Find how many phases:
		phase_count = len(phase_datetimes)

		dfs = [df_loc]
		phase_number = '1'
		for phase in range(phase_count):
			df_subset = df_loc.loc[phase_datetimes[phase_number][0]:phase_datetimes[phase_number][1]]
			dfs.append(df_subset)
			phase_number = str(int(phase_number) + 1)
		return dfs

	@staticmethod
	def create_24h_subset(df):
		diff = pd.Timedelta(hours=24)
		end_time = df.index[-1]
		start_time = end_time - diff
		df = df[start_time:end_time]
		return df

	def generate_df(self, active_sample, active_test, return_phases_times=False):
		"""
		The functions loads all phase datasets and concatenate them together.

		:param - active_sample: active sample
		:param - active_test: current test setup
		:param - return_phases_times: if set tu True, this function will only return phase times
		:return - df, phases: df - full uncalibrated dataframe; phases - start and end datetime of each phase.
		"""

		# Get sample data directory:
		sample_name = active_sample['sample_name']
		active_test_dir = active_test.test_info['sample_dir']
		sample_data_dir = os.path.join(active_test_dir, sample_name, self.measurement_folder)

		# Loading dataframes:
		df = pd.DataFrame()
		files = os.listdir(sample_data_dir)

		phase_datetimes = {}

		for index, file in enumerate(files):
			if file.endswith('csv'):
				filename, extension = os.path.splitext(file)
				# Separating filename to extract phase number
				keyword = 'phase'
				sample_name, keyword, phase_number = filename.partition(keyword)
				if len(phase_number) == 1:
					# Normal case: phase consist of single file
					# Both, start and end of phase index can be extracted
					df_loc = self.load_single_file(sample_data_dir, file)
					df = pd.concat([df, df_loc])
					phase_datetimes[phase_number] = [df_loc.index[0], df_loc.index[-1]]
				elif index == len(files) - 1:
					# Phase consists of multiple files, but this is the very last file
					# End datetime of phase can be extracted
					df_loc = self.load_single_file(sample_data_dir, file)
					df = pd.concat([df, df_loc])
					phase_datetimes[phase_number.split('-')[0]].append(df_loc.index[-1])
				else:
					# When multiple files, one of the phase files.
					# Retrieving phase number for the next file:
					filename_next, extension_next = os.path.splitext(files[index + 1])
					sample_name_next, keyword_next, phase_number_next = filename_next.partition(keyword)
					if len(phase_number_next) == 1:
						# This is the last file of the phase
						df_loc = self.load_single_file(sample_data_dir, file)
						df = pd.concat([df, df_loc])
						phase_datetimes[phase_number.split('-')[0]].append(df_loc.index[-1])
					else:
						# This is not teh last file of the phase
						df_loc = self.load_single_file(sample_data_dir, file)
						last_index = pd.to_datetime(df_loc.index[-1])
						df_loc = df_loc.append(pd.Series(name=last_index + pd.Timedelta(seconds=1)))
						df = pd.concat([df, df_loc])
						if phase_number not in active_sample:
							# Adds a list with phase start time
							phase_datetimes[phase_number.split('-')[0]] = [df_loc.index[0]]

		df.index.name = None
		df.columns = active_sample['columns']

		if not return_phases_times:
			return df

		else:
			return phase_datetimes

	def generate_corrected_dfs(self, override_dfs):
		""""
		This function is executed together with teh update function.
		The function will iterate through both test setups and update corrected dfs if there is any new date
		for any of the samples.
		"""

		# This function should be executed together with update files function.
		# This way it would ensure that any time I update the files, I also add new data
		# to corrected dataset

		corrected_df_folder = '01_calibrated_datasets'

		# Iterate through all samples:
		for active_test in self.test_setups:
			active_test_dir = active_test.test_info['sample_dir']
			for active_sample in active_test.samples:
				sample_name = active_sample['sample_name']
				corrected_df_name = sample_name + '_calibrated_df.csv'
				corrected_df_dir = os.path.join(
					active_test_dir,
					sample_name,
					self.measurement_folder,
					corrected_df_folder)
				temperature_sensor_columns = active_sample['temperature_columns']

				corr_coef_dir = os.path.join(active_test_dir, sample_name, self.calib_folder)
				corr_coef_filename = 'temperature_sensor_calibration_factors.csv'
				corr_coef_data = pd.read_csv(
					os.path.join(corr_coef_dir, corr_coef_filename),
					header=0,
					index_col=0)

				def correcting_data(x, column):
					a = corr_coef_data['a'][column]
					b = corr_coef_data['b'][column]
					return x * a + b

				if override_dfs:
					# load all phase files into df
					corrected_df = self.generate_df(active_sample, active_test)

					for column in temperature_sensor_columns:
						corrected_df.loc[:, column].apply(lambda x: correcting_data(x, column))

					# Do preprocessing:
					corrected_df = self.add_hours_column_to_df(corrected_df)
					corrected_df = self.add_cold_end_temp_column(active_sample, corrected_df)
					corrected_df = self.add_hot_end_temp_column(active_sample, corrected_df)

					if active_test is self.large_test_data:
						corrected_df = self.nan_out_low_moisture_vals(active_sample, corrected_df)
						corrected_df = self.normalize_moisture_values(active_sample, corrected_df)
						corrected_df = self.delete_flawed_data(active_sample, corrected_df)

					corrected_df.to_csv(os.path.join(corrected_df_dir, corrected_df_name))

				else:
					if corrected_df_name not in os.listdir(corrected_df_dir):
						# load all phase files into df
						corrected_df = self.generate_df(active_sample, active_test)

						for column in temperature_sensor_columns:
							corrected_df.loc[:, column].apply(lambda x: correcting_data(x, column))

						# Do preprocessing:
						corrected_df = self.add_hours_column_to_df(corrected_df)
						corrected_df = self.add_cold_end_temp_column(active_sample, corrected_df)
						corrected_df = self.add_hot_end_temp_column(active_sample, corrected_df)

						if active_test is self.large_test_data:
							corrected_df = self.nan_out_low_moisture_vals(active_sample, corrected_df)
							corrected_df = self.normalize_moisture_values(active_sample, corrected_df)
							corrected_df = self.delete_flawed_data(active_sample, corrected_df)

						corrected_df.to_csv(os.path.join(corrected_df_dir, corrected_df_name))

					else:
						corrected_df = pd.read_csv(
							os.path.join(corrected_df_dir, corrected_df_name),
							index_col=0,
							header=0)
						corrected_df = corrected_df[active_sample['columns']]
						corrected_df.index = pd.to_datetime(corrected_df.index)
						corr_df_last_index = corrected_df.index[-1]
						sample_data_dir = os.path.join(
							active_test_dir,
							sample_name,
							self.measurement_folder)
						phase_files = []
						for file in os.listdir(sample_data_dir):
							if os.path.isfile(os.path.join(sample_data_dir, file)):
								phase_files.append(file)
						phase_files.sort()

						df_loc = self.load_single_file(sample_data_dir, phase_files[-1])
						origin_df_last_index = df_loc.index[-1]
						if origin_df_last_index > corr_df_last_index:
							# Load whole df and make a slice:
							df = self.generate_df(active_sample, active_test)
							df_subset = df[df.index > corr_df_last_index]
							for column in temperature_sensor_columns:
								df_subset.loc[:, column] = df_subset.loc[:, column].apply(lambda x: correcting_data(x, column))

							# Concatenate new data to old:
							corrected_df = pd.concat([corrected_df, df_subset])

							# Do preprocessing:
							corrected_df = self.add_hours_column_to_df(corrected_df)
							corrected_df = self.add_cold_end_temp_column(active_sample, corrected_df)
							corrected_df = self.add_hot_end_temp_column(active_sample, corrected_df)

							if active_test is self.large_test_data:
								corrected_df = self.nan_out_low_moisture_vals(active_sample, corrected_df)
								corrected_df = self.normalize_moisture_values(active_sample, corrected_df)
								corrected_df = self.delete_flawed_data(active_sample, corrected_df)

							# Save corrected df:
							corrected_df.to_csv(os.path.join(corrected_df_dir, corrected_df_name))

	def load_corrected_df(self, active_sample, active_test):
		"""
		Load dataframe with correceted values.
		Any necessary preprocessing has already been done for this dataframe.

		:param active_sample - current sample to be plotted.
		:param active_test - current test setup to be processed.
		:return: df - master dataframe used for any plot.
		"""

		sample_name = active_sample['sample_name']
		active_test_dir = active_test.test_info['sample_dir']
		corrected_df_dir = os.path.join(
			active_test_dir,
			sample_name,
			self.measurement_folder,
			self.corrected_df_folder)
		corrected_df_name = sample_name + '_calibrated_df.csv'

		df = pd.read_csv(
			os.path.join(corrected_df_dir,
						 corrected_df_name),
			index_col=0,
			header=0)

		df.index = pd.to_datetime(df.index)

		return df

	def generate_averaged_dfs(self):
		pass

	@staticmethod
	def create_10perc_subset(df):
		"""
		The function creates a subset from the current dataframe.
		The subset is the last 10% temperature increase.
		The last value of teh dataset is teh last value of teh input df. The first value is defined as
		the last*0.9. Then the df subset is limited to this range.

		:param df: Current data set
		:return: a subset of the current df
		"""
		last_temp = df['hot_end'].values[-1]
		min_temp = last_temp*0.9
		start_time = None
		for index_val, temp_val in zip(df.index, df['hot_end']):
			if temp_val >= min_temp:
				start_time = index_val
				break
		df = df.loc[start_time:]

		return df

	def update_data(self):
		for source_folder, target_folder in zip(self.source_folder_list, self.target_folder_list):
			for root, dirs, files in os.walk(source_folder):
				for file in files:
					if len(file) != 0:
						# Getting sample name:
						sample_name = file.split('_')[0]

						# Check if the file exists, copy or replace:
						sample_folder_raw = os.path.join(
							target_folder, sample_name, '01_raw_data')
						sample_folder_csv = os.path.join(
							target_folder, sample_name, '02_measurement_data')

						if file not in os.listdir(sample_folder_raw):
							# Executed when new file is added
							shutil.copy(os.path.join(root, file), sample_folder_raw)
							# Should convert from .lvm to .csv here
							shutil.copy(os.path.join(sample_folder_raw, file), sample_folder_csv)
							name, ext = os.path.splitext(os.path.join(sample_folder_csv, file))
							os.rename(os.path.join(sample_folder_csv, file), name + '.csv')


						else:
							# Executed when file already exists
							src_mod_time = os.stat(os.path.join(root, file)).st_mtime
							trg_mod_time = os.stat(os.path.join(sample_folder_raw, file)).st_mtime
							if src_mod_time - trg_mod_time > 1:
								shutil.copy(os.path.join(root, file), sample_folder_raw)
								shutil.copy(os.path.join(sample_folder_raw, file), sample_folder_csv)
								# Updating csv version of the file:
								name, ext = os.path.splitext(os.path.join(sample_folder_csv, file))
								csv_name = file.split('.')[0] + '.csv'
								if csv_name not in os.listdir(sample_folder_csv):
									os.rename(os.path.join(sample_folder_csv, file), name + '.csv')
								else:
									os.remove(os.path.join(sample_folder_csv, csv_name))
									os.rename(os.path.join(sample_folder_csv, file), name + '.csv')
