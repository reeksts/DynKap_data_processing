import numpy as np
import pandas as pd
import os
import shutil

class DataProcessor:
	def __init__(self, sample):
		self.sample = sample
		# load data here

	def generate_df(self):
		pass

		# this function should return df

	def generate_dfs(self):
		pass

	def generate_averaged_df(self):
		pass

	def temperature_sensor_calibration(self):
		pass

		# this function should return df with averaged values
		# options should probably be every 6min, every 10min, every 30min, every 60min

	def delete_flawed_data(self, df):
		for data_chunk in self.sample['del_data']:
			start_time = data_chunk['start']
			end_time = data_chunk['end']
			sensor = data_chunk['sensor']
			df[sensor][start_time:end_time] = df[sensor][start_time:end_time].apply(lambda val: np.nan)

	def create_24h_subset(self, df):
		diff = pd.Timedelta(hours=24)
		end_time = df.index[-1]
		start_time = end_time - diff
		df = df[start_time:end_time]
		return df

	def create_10perc_subset(self, df):
		last_temp = df['hot_end'].values[-1]
		min_temp = last_temp*0.9
		start_time = None
		for index_val, temp_val in zip(df.index, df['hot_end']):
			if temp_val >= min_temp:
				start_time = index_val
				break
		df = df.loc[start_time:]

		# adjust the 'hours' column
		min_hour = df['hours'][0]
		print(min_hour)
		df['hours'] = df['hours'].apply(lambda val: val-min_hour)

		return df


class DataUpdater:
	def __init__(self):
		self.source_folder_list = [
			'C:\\Users\\karlisr\\OneDrive\\LargeMoistureCell\\',
			'C:\\Users\\karlisr\\OneDrive\\SmallMoistureCell\\']

		self.target_folder_list = [
			'C:\\Users\\karlisr\\OneDrive - NTNU\\3_PostDoc_Sintef\\01_laboratory_work\\01_large_test\\',
			'C:\\Users\\karlisr\\OneDrive - NTNU\\3_PostDoc_Sintef\\01_laboratory_work\\02_small_test\\']

	def update_data(self):
		for source_folder, target_folder in zip(self.source_folder_list, self.target_folder_list):
			for root, dirs, files in os.walk(source_folder):
				for file in files:
					if len(file) != 0:
						# Getting sample name:
						sample_name = file.split('_')[0]

						# Check if the file exists, copy or replace:
						sample_folder_raw = os.path.join(
							target_folder, '01_measurement_data', sample_name, '01_raw_data')
						sample_folder_csv = os.path.join(
							target_folder, '01_measurement_data', sample_name, '02_measurement_data')
						if file not in os.listdir(sample_folder_raw):
							shutil.copy(os.path.join(root, file), sample_folder_raw)
							# Should convert from .lvm to .csv here
							shutil.copy(os.path.join(sample_folder_raw, file), sample_folder_csv)
							name, ext = os.path.splitext(os.path.join(sample_folder_csv, file))
							os.rename(os.path.join(sample_folder_csv, file), name + '.csv')


						else:
							src_mod_time = os.stat(os.path.join(root, file)).st_mtime
							trg_mod_time = os.stat(os.path.join(sample_folder_raw, file)).st_mtime
							if src_mod_time - trg_mod_time > 1:
								shutil.copy(os.path.join(root, file), sample_folder_raw)
								# Should convert from .lvm to .csv here
								shutil.copy(os.path.join(sample_folder_raw, file), sample_folder_csv)

	def convert_data(self):
		pass



