import pandas as pd


class SampleData:
	def __init__(self):
		self.fignames = {'time series temp - up': 'time_series_temp_up',
						 'time series temp - right': 'time_series_temp_right',
						 'time series temp - down': 'time_series_temp_down',
						 'time series moist - up': 'time_series_moist_up',
						 'time series moist - right': 'time_series_moist_right',
						 'time series moist - down': 'time_series_moist_down',
						 'gradient temp - up': 'gradient_temp_up',
						 'gradient temp - right': 'gradient_temp_right',
						 'gradient temp - down': 'gradient_temp_down',
						 'gradient moist - up': 'gradient_moist_up',
						 'gradient moist - right': 'gradient_moist_right',
						 'gradient moist - down': 'gradient_moist_down',
						 'time series temp': 'time_series_temp',
						 'gradient temp': 'gradient_temp',
						 'time series moist': 'time_series_moisture',
						 'gradient moist': 'gradient_moisture'}

		self.SN1 = {'dir': 'C:\\Users\\karlisr\\OneDrive - NTNU\\3_PostDoc_Sintef\\01_laboratory_work\\01_large_test\\'
						   '07_testing_data\\01_Sample_1_Vassfjell_4%_fines_Pallet_1\\',
					'timestamps': [[pd.Timestamp(2020, 10, 30, 15, 40), '30 degC core'],
								   [pd.Timestamp(2020, 10, 31, 17, 10), '40 degC core'],
								   [pd.Timestamp(2020, 11, 1, 15, 10), '45 degC core'],
								   [pd.Timestamp(2020, 11, 2, 7, 50), '50 degC core'],
								   [pd.Timestamp(2020, 11, 3, 20, 20), '20 degC core'],
								   [pd.Timestamp(2020, 11, 4, 10, 10), '50 degC core'],
								   [pd.Timestamp(2020, 11, 7, 15, 10), '60 degC core']],
					'core_sensors': ['X1', 'X2'],
					'wall_sensors': ['K1', 'K2', 'K3'],
					'del_data': []}


		self.SN2 = {'dir': 'C:\\Users\\karlisr\\OneDrive - NTNU\\3_PostDoc_Sintef\\01_laboratory_work\\01_large_test\\'
						   '07_testing_data\\02_Sample_2_Vassfjell_4%_fines_Pallet_2\\',
					'timestamps': [[pd.Timestamp(2021, 1, 19, 14, 30), '154W core'],
								   [pd.Timestamp(2021, 1, 26, 8, 00), '174W core'],
								   [pd.Timestamp(2021, 2, 1, 8, 00), '194W core'],
								   [pd.Timestamp(2021, 2, 5, 8, 00), '214W core']],
					'periods': [{'start': 'timestamp', 'end': 'timestamp', 'name': 'name'},
								{'start': 'timestamp', 'end': 'timestamp', 'name': 'name'},
								{'start': 'timestamp', 'end': 'timestamp', 'name': 'name'},
								{'start': 'timestamp', 'end': 'timestamp', 'name': 'name'},
								{'start': 'timestamp', 'end': 'timestamp', 'name': 'name'}],
					'core_sensors': ['X1', 'X2'],
					'wall_sensors': ['K2', 'X3'],
					'del_data': [{'sensor': 'R1', 'start': '', 'end': ''}]}
