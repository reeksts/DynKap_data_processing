import numpy as np
import pandas as pd

class DataProcessor:
	def __init__(self, sample):
		self.sample = sample
		# load data here

	def generate_df(self):
		pass

		# this function should return df

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

