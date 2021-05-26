import pandas as pd


class SampleDataSmall:
	def __init__(self):
		self.test_info = {'test_name': 'Small moisture cell',
						  'data_input': 'C:\\Users\\karlisr\\OneDrive - NTNU\\3_PostDoc_Sintef\\01_laboratory_work\\'
										'02_small_test\\01_measurement_data\\',
						  'data_output': 'C:\\Users\\karlisr\\OneDrive - NTNU\\3_PostDoc_Sintef\\01_laboratory_work\\'
										 '02_small_test\\02_measurement_figures\\'}

		self.fignames = {'time series': 'time_series',
						 'gradient temp': 'gradient_temp',
						 'animated series': 'animated_series',
						 'animated gradient': 'animated_gradient'}

		self.folders = {'01_time_series_plots': '01_time_series_plots\\',
						'02_temperature_gradient_plots': '02_temperature_gradient_plots\\',
						'03_animated_plots': '03_animated_plots\\'}

		self.temp_directions = ['temp']
		self.moist_directions = []

		self.SS1 = {'sample_name': 'SS1',
					'columns': ['top', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'bot', 'ext', 'power'],
					'timestamps': [[pd.Timestamp(2021, 5, 19, 8, 0), '5.3W hot end']],
					'phases': [{'start': 'timestamp', 'end': 'timestamp', 'name': '5.3W_hot_end'}],
					'hot_end_sensors': {'sensors': ['top'],
									    'locations': [0.1]},
					'cold_end_sensors': {'sensors': ['bot'],
									     'locations': [25]},
					'sensors': {'temp': {'sensors': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'],
										 'locations': [3.4, 6.4, 9.4, 12.4, 15.4, 18.4, 21.4]}},
					'del_data': [{'sensor': '',
								  'start': '',
								  'end': ''}],
					'comsol_files': [],
					'sample_props': {'porosity': 0.4,  # this is dummy data
									 'ks': 2.66,  # this is dummy data
									 'rhos': 3.02,  # this is dummy data
									 'w_grav': 3.0}}  # this is dummy data

		self.SS2 = {'sample_name': 'SS2',
					'columns': ['top', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'bot', 'ext', 'power']}
		self.SS3 = {'sample_name': 'SS3',
					'columns': ['top', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'bot', 'ext', 'power']}
		self.SS4 = {'sample_name': 'SS4',
					'columns': ['top', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'bot', 'ext', 'power']}
		self.SS5 = {'sample_name': 'SS5',
					'columns': ['top', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'bot', 'ext', 'power']}
		self.SS6 = {'sample_name': 'SS6',
					'columns': ['top', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'bot', 'ext', 'power']}
		self.SS7 = {'sample_name': 'SS7',
					'columns': ['top', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'bot', 'ext', 'power']}
		self.SS8 = {'sample_name': 'SS8',
					'columns': ['top', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'bot', 'ext', 'power']}
		self.SS9 = {'sample_name': 'SS9',
					'columns': ['top', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'bot', 'ext', 'power']}
		self.SS10 = {'sample_name': 'SS10',
					 'columns': ['top', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'bot', 'ext', 'power']}

		self.samples = [self.SS1,
						self.SS2,
						self.SS3,
						self.SS4,
						self.SS5,
						self.SS6,
						self.SS7,
						self.SS8,
						self.SS9,
						self.SS10]