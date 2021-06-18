import pandas as pd


class SampleDataLarge:
	def __init__(self):
		self.test_info = {'test_name': 'LargeMoistureCell',
						  'sample_dir': 'C:\\Users\\karlisr\\OneDrive - NTNU\\3_PostDoc_Sintef\\'
										'01_laboratory_work\\01_large_test\\01_measured_samples'}


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
						 'gradient moist': 'gradient_moisture',
						 'moist vs temp': 'moist_vs_temp',
						 'moist vs temp - up': 'moist_vs_temp_up',
						 'moist vs temp - right': 'moist_vs_temp_right',
						 'moist vs temp - down': 'moist_vs_temp_down',
						 'hot end temp': 'hot_end_temp'}

		self.folders = {'01_combined_plots': '01_combined_plots',
           				'02_time_series_temperature': '02_time_series_temperature',
           				'03_time_series_moisture': '03_time_series_moisture',
           				'04_gradient_temperature': '04_gradient_temperature',
           				'05_gradient_moisture': '05_gradient_moisture',
           				'06_last_24_hours': '06_last_24_hours',
						'07_animated_plots': '07_animated_plots',
						'08_time_series_moisture_vs_temperature': '08_time_series_moisture_vs_temperature',
						'09_tracking_individual_sensors': '09_tracking_individual_sensors'}

		self.plot_folders = [self.folders['01_combined_plots'],
							 self.folders['02_time_series_temperature'],
							 self.folders['03_time_series_moisture'],
							 self.folders['04_gradient_temperature'],
							 self.folders['05_gradient_moisture'],
							 self.folders['06_last_24_hours'],
							 self.folders['07_animated_plots'],
							 self.folders['08_time_series_moisture_vs_temperature'],
							 self.folders['09_tracking_individual_sensors']]


		self.temp_directions = ['temp_up', 'temp_right', 'temp_down']
		self.moist_directions = ['moist_up', 'moist_right', 'moist_down']

		self.SN0 = {'sample_name': 'SN0',
					'columns': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6',
								'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
								'U7', 'U8', 'U9', 'U10',
								'D1', 'D2', 'D3', 'D4', 'D5', 'D6',
								'C1', 'C2', 'W1', 'D7', 'D8', 'D9', 'D10',
								'X1', 'W2', 'X3',
								'MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6', 'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12',
								'power'],
					'temperature_columns_main': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6',
												 'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
												 'D1', 'D2', 'D3', 'D4', 'D5', 'D6'],
					'temperature_columns_moist': ['U1', 'U2', 'U3', 'U4',
												  'R1', 'R2', 'R3', 'R4',
												  'D1', 'D2', 'D3', 'D4'],
					'temperature_columns_ext': ['X1', 'X2', 'X3', 'K1', 'K2', 'K3'],
					'moisture_columns': ['MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6',
										 'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12'],
					'power_column': ['power'],
					'timestamps': [[pd.Timestamp(2021, 4, 4, 17, 00), '50W  power'],
								   [pd.Timestamp(2021, 4, 7, 11, 00), '70W power'],
								   [pd.Timestamp(2021, 4, 12, 9, 00), '90W power']],
					'phases': [{'start': 'timestamp', 'end': 'timestamp', 'name': '50W_core'},
								{'start': 'timestamp', 'end': 'timestamp', 'name': '70W_core'}],
					'core_sensors': {'sensors': ['C1', 'C2'],
									 'locations': [0, 26]},
					'wall_sensors': {'sensors': ['W1', 'W2'],
									 'locations': [0, 26]},
					'sensors': {'temp_up': {'sensors': ['U3', 'U5', 'U7', 'U8', 'U9', 'U10'],
											     'locations': [4, 8, 12, 16, 20, 24],
											     'direction_name': 'Direction - up'},
									 'temp_right': {'sensors': ['R1', 'R2', 'R3', 'R4', 'R5', 'R6'],
													'locations': [4, 8, 12, 16, 20, 24],
													'direction_name': 'Direction - right'},
									 'temp_down': {'sensors': ['D3', 'D5', 'D7', 'D8', 'D9', 'D10'],
												   'locations': [4, 8, 12, 16, 20, 24],
												   'direction_name': 'Direction - down'},
									 'moist_up': {'sensors': [],
												  'locations': [],
												  'direction_name': ''},
									 'moist_right': {'sensors': [],
													 'locations': [],
													 'direction_name': ''},
									 'moist_down': {'sensors': [],
													'locations': [],
													'direction_name': ''}},
					'other_sensors': [['Core at 5cm', 'U1'],
									  ['Core at 5cm', 'U2'],
									  ['Wall at 5cm', 'U4'],
									  ['Core at 25cm', 'U6'],
									  ['Core at 25cm', 'D1'],
									  ['Core at 65cm', 'D2'],
									  ['Core at 65cm', 'D4'],
									  ['Core at 85cm', 'D6'],
									  ['Cable', 'X1']],
					'del_data': [],
					'comsol_files': [],
					'sample_props': {'porosity': 0.4,       # this is dummy data
									 'ks': 2.66,			# this is dummy data
									 'rhos': 3.02,			# this is dummy data
									 'w_grav': 3.0}}		# this is dummy data

		self.SN1 = {'sample_name': 'SN1',
					'timestamps': [[pd.Timestamp(2020, 10, 30, 15, 40), '30 degC core'],
								   [pd.Timestamp(2020, 10, 31, 17, 10), '40 degC core'],
								   [pd.Timestamp(2020, 11, 1, 15, 10), '45 degC core'],
								   [pd.Timestamp(2020, 11, 2, 7, 50), '50 degC core'],
								   [pd.Timestamp(2020, 11, 3, 20, 20), '20 degC core'],
								   [pd.Timestamp(2020, 11, 4, 10, 10), '50 degC core'],
								   [pd.Timestamp(2020, 11, 7, 15, 10), '60 degC core']],
					'phases': [{'start': 'timestamp', 'end': 'timestamp', 'name': 'name'},
								{'start': 'timestamp', 'end': 'timestamp', 'name': 'name'},
								{'start': 'timestamp', 'end': 'timestamp', 'name': 'name'},
								{'start': 'timestamp', 'end': 'timestamp', 'name': 'name'},
								{'start': 'timestamp', 'end': 'timestamp', 'name': 'name'}],
					'sensors': {'temp_up': {'sensors': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6'],
											'locations': [4, 8, 12, 16, 20, 24],
											'direction_name': 'Direction - up'},
								'temp_right': {'sensors': ['R1', 'R2', 'R3', 'R4', 'R5', 'R6'],
											   'locations': [4, 8, 12, 16, 20, 24],
											   'direction_name': 'Direction - right'},
								'temp_down': {'sensors': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6'],
											  'locations': [4, 8, 12, 16, 20, 24],
											  'direction_name': 'Direction - down'},
								'moist_up': {'sensors': ['MS1', 'MS2', 'MS3', 'MS4'],
											 'locations': [4, 8, 12, 16],
											 'direction_name': 'Direction - up'},
								'moist_right': {'sensors': ['MS5', 'MS6', 'MS7', 'MS8'],
												'locations': [4, 8, 12, 16],
												'direction_name': 'Direction - right'},
								'moist_down': {'sensors': ['MS9', 'MS10', 'MS11', 'MS12'],
											   'locations': [4, 8, 12, 16],
											   'direction_name': 'Direction - down'}},
					'core_sensors': {'sensors': ['X1', 'X2'],
									 'locations': [0, 26]},
					'wall_sensors': {'sensors': ['K1', 'K2', 'K3'],
									 'locations': [0, 26]},
					'del_data': [],
					'comsol_files': ['comsol_model_288W.csv']}

		self.SN2 = {'sample_name': 'SN2',
					'columns': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6',
							    'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
								'D1', 'D2', 'D3', 'D4', 'D5', 'D6',
								'X1', 'X2', 'X3', 'K1', 'K2', 'K3',
								'MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6',
								'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12',
								'power'],
					'temperature_columns_main': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6',
												 'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
												 'D1', 'D2', 'D3', 'D4', 'D5', 'D6'],
					'temperature_columns_moist': ['U1', 'U2', 'U3', 'U4',
												  'R1', 'R2', 'R3', 'R4',
												  'D1', 'D2', 'D3', 'D4'],
					'temperature_columns_ext': ['X1', 'X2', 'X3', 'K1', 'K2', 'K3'],
					'moisture_columns': ['MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6',
										 'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12'],
					'power_column': ['power'],
					'timestamps': [[pd.Timestamp(2021, 1, 19, 14, 33), '154W core'],
								   [pd.Timestamp(2021, 1, 26, 14, 5), '174W core'],
								   [pd.Timestamp(2021, 2, 1, 10, 29), '194W core'],
								   [pd.Timestamp(2021, 2, 6, 9, 17), '214W core'],
								   [pd.Timestamp(2021, 2, 23, 13, 7), '288W core']],
					'phases': [{'start': pd.Timestamp(2021, 1, 14, 9, 56), 'end': pd.Timestamp(2021, 1, 19, 14, 33),
								 'name': '154W_core'},
								{'start': pd.Timestamp(2021, 1, 19, 14, 34), 'end': pd.Timestamp(2021, 1, 26, 14, 5),
								 'name': '174W_core'},
								{'start': pd.Timestamp(2021, 1, 26, 14, 6), 'end': pd.Timestamp(2021, 2, 1, 10, 29),
								 'name': '196W_core'},
								{'start': pd.Timestamp(2021, 2, 1, 10, 30), 'end': pd.Timestamp(2021, 2, 6, 9, 17),
								 'name': '217W_core'},
								{'start': pd.Timestamp(2021, 2, 6, 9, 18), 'end': pd.Timestamp(2021, 2, 23, 13, 7),
								 'name': '290W_core'}],
					'hot_end_sensors': {'sensors': ['X1', 'X2'],
									    'locations': [0.1]},
					'cold_end_sensors': {'sensors': ['K2', 'X3'],
									     'locations': [26]},
					'sensors': {'temp_up': {'sensors': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6'],
											'locations': [4, 8, 12, 16, 20, 24],
											'direction_name': 'Direction - up'},
								'temp_right': {'sensors': ['R1', 'R2', 'R3', 'R4', 'R5', 'R6'],
											'locations': [4, 8, 12, 16, 20, 24],
											'direction_name': 'Direction - right'},
								'temp_down': {'sensors': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6'],
											'locations': [4, 8, 12, 16, 20, 24],
											'direction_name': 'Direction - down'},
								'moist_up': {'sensors': ['MS1', 'MS2', 'MS3', 'MS4'],
											 'temp_sensors': ['U1', 'U2', 'U3', 'U4'],
											 'locations': [4, 8, 12, 16],
											 'direction_name': 'Direction - up'},
								'moist_right': {'sensors': ['MS5', 'MS6', 'MS7', 'MS8'],
												'temp_sensors': ['R1', 'R2', 'R3', 'R4'],
											    'locations': [4, 8, 12, 16],
											    'direction_name': 'Direction - right'},
								'moist_down': {'sensors': ['MS9', 'MS10', 'MS11', 'MS12'],
											   'temp_sensors': ['D1', 'D2', 'D3', 'D4'],
											   'locations': [4, 8, 12, 16],
											   'direction_name': 'Direction - down'}},
					'other_sensors': [],
					'failed_sensors': [],
					'del_data': [{'sensor': 'R1',
								  'start': pd.Timestamp(2021, 2, 6, 12, 40),
								  'end': pd.Timestamp(2021, 2, 8, 17, 40)}],
					'comsol_files': ['comsol_model_288W.csv'],
					'sample_props': {'porosity': 0.4,
									 'ks': 2.66,
									 'rhos': 3.02,
									 'w_grav': 3.0}}

		self.SN3 = {'sample_name': 'SN3',
					'columns': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6',
								'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
								'U7', 'U8', 'U9', 'U10',
								'D1', 'D2', 'D3', 'D4', 'D5', 'D6',
								'C1', 'C2', 'W1', 'D7', 'D8', 'D9', 'D10',
								'X1', 'W2', 'X2',
								'MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6',
								'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12',
								'power'],
					'temperature_columns': [
						'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'U10',
						'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
						'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
						'C1', 'C2', 'W1', 'W2', 'X1', 'X2'],
					'temperature_columns_main': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6',
												 'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
												 'D1', 'D2', 'D3', 'D4', 'D5', 'D6'],
					'temperature_columns_moist': ['U1', 'U2', 'U3', 'U4',
												  'R1', 'R2', 'R3', 'R4',
												  'D1', 'D2', 'D3', 'D4'],
					'temperature_columns_ext': ['C1', 'C2', 'X1', 'X2', 'W1', 'W2'],
					'moisture_columns': ['MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6',
										 'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12'],
					'power_column': ['power'],
					'phase_names': ['170W'],
					'hot_end_sensors': {'sensors': ['C1', 'C2'],
										'locations': [0.1]},
					'cold_end_sensors': {'sensors': ['W1', 'W2'],
										 'locations': [26]},
					'sensors': {'temp_up': {'sensors': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'U10'],
											'locations': [1.3, 2.7, 4, 6, 8, 10, 12, 16, 20, 24],
											'direction_name': 'Direction - up'},
								'temp_right': {'sensors': ['R1', 'R2', 'R3', 'R4', 'R5', 'R6'],
											   'locations': [4, 8, 12, 16, 20, 24],
											   'direction_name': 'Direction - right'},
								'temp_down': {'sensors': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10'],
											  'locations': [1.3, 2.7, 4, 6, 8, 10, 12, 16, 20, 24],
											  'direction_name': 'Direction - down'},
								'moist_up': {'sensors': ['MS1', 'MS2', 'MS3', 'MS4'],
											 'temp_sensors': ['U3', 'U5', 'U7', 'U8'],
											 'locations': [4, 8, 12, 16],
											 'direction_name': 'Direction - up'},
								'moist_right': {'sensors': ['MS5', 'MS6', 'MS7', 'MS8'],
												'temp_sensors': ['R1', 'R2', 'R3', 'R4'],
												'locations': [4, 8, 12, 16],
												'direction_name': 'Direction - right'},
								'moist_down': {'sensors': ['MS9', 'MS10', 'MS11', 'MS12'],
											   'temp_sensors': ['D3', 'D5', 'D7', 'D8'],
											   'locations': [4, 8, 12, 16],
											   'direction_name': 'Direction - down'}},
					'other_sensors': [],
					'failed_sensors': ['M5'],
					'del_data': [],
					'comsol_files': [],
					'sample_props': {'porosity': 0.4,
									 'ks': 2.66,
									 'rhos': 3.02,
									 'w_grav': 3.0}}

		self.SN4 = {'sample_name': 'SN4',
					'columns': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6',
								'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
								'U7', 'U8', 'U9', 'U10',
								'D1', 'D2', 'D3', 'D4', 'D5', 'D6',
								'C1', 'C2', 'W1', 'D7', 'D8', 'D9', 'D10',
								'X1', 'W2', 'X2',
								'MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6',
								'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12',
								'power'],
					'temperature_columns': [
						'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'U10',
						'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
						'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
						'C1', 'C2', 'W1', 'W2', 'X1', 'X2'],
					'temperature_columns_main': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6',
												 'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
												 'D1', 'D2', 'D3', 'D4', 'D5', 'D6'],
					'temperature_columns_moist': ['U1', 'U2', 'U3', 'U4',
												  'R1', 'R2', 'R3', 'R4',
												  'D1', 'D2', 'D3', 'D4'],
					'temperature_columns_ext': ['C1', 'C2', 'X1', 'X2', 'W1', 'W2'],
					'moisture_columns': ['MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6',
										 'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12'],
					'power_column': ['power'],
					'phase_names': ['230W_core', '320W_core'],
					'hot_end_sensors': {'sensors': ['C1', 'C2'],
										'locations': [0.1]},
					'cold_end_sensors': {'sensors': ['W1', 'W2'],
										 'locations': [26]},
					'sensors': {'temp_up': {'sensors': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'U10'],
											'locations': [1.3, 2.7, 4, 6, 8, 10, 12, 16, 20, 24],
											'direction_name': 'Direction - up'},
								'temp_right': {'sensors': ['R1', 'R2', 'R3', 'R4', 'R5', 'R6'],
											   'locations': [4, 8, 12, 16, 20, 24],
											   'direction_name': 'Direction - right'},
								'temp_down': {'sensors': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10'],
											  'locations': [1.3, 2.7, 4, 6, 8, 10, 12, 16, 20, 24],
											  'direction_name': 'Direction - down'},
								'moist_up': {'sensors': ['MS1', 'MS2', 'MS3', 'MS4'],
											 'temp_sensors': ['U3', 'U5', 'U7', 'U8'],
											 'locations': [4, 8, 12, 16],
											 'direction_name': 'Direction - up'},
								'moist_right': {'sensors': ['MS5', 'MS6', 'MS7', 'MS8'],
												'temp_sensors': ['R1', 'R2', 'R3', 'R4'],
												'locations': [4, 8, 12, 16],
												'direction_name': 'Direction - right'},
								'moist_down': {'sensors': ['MS9', 'MS10', 'MS11', 'MS12'],
											   'temp_sensors': ['D3', 'D5', 'D7', 'D8'],
											   'locations': [4, 8, 12, 16],
											   'direction_name': 'Direction - down'}},
					'other_sensors': [],
					'failed_sensors': [],
					'del_data': [],
					'comsol_files': [],
					'sample_props': {'porosity': 0.4,
									 'ks': 2.66,
									 'rhos': 3.02,
									 'w_grav': 3.0}}

		self.SN5 = {'sample_name': 'SN5',
					'columns': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6',
								'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
								'U7', 'U8', 'U9', 'U10',
								'D1', 'D2', 'D3', 'D4', 'D5', 'D6',
								'C1', 'C2', 'W1', 'D7', 'D8', 'D9', 'D10',
								'X1', 'W2', 'X2',
								'MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6',
								'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12',
								'power'],
					'temperature_columns': [
						'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'U10',
						'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
						'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
						'C1', 'C2', 'W1', 'W2', 'X1', 'X2'],
					'temperature_columns_main': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6',
												 'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
												 'D1', 'D2', 'D3', 'D4', 'D5', 'D6'],
					'temperature_columns_moist': ['U1', 'U2', 'U3', 'U4',
												  'R1', 'R2', 'R3', 'R4',
												  'D1', 'D2', 'D3', 'D4'],
					'temperature_columns_ext': ['C1', 'C2', 'X1', 'X2', 'W1', 'W2'],
					'moisture_columns': ['MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6',
										 'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12'],
					'power_column': ['power'],
					'phase_names': ['230W_core'],
					'hot_end_sensors': {'sensors': ['C1', 'C2'],
										'locations': [0.1]},
					'cold_end_sensors': {'sensors': ['W1', 'W2'],
										 'locations': [26]},
					'sensors': {'temp_up': {'sensors': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'U10'],
											'locations': [1.3, 2.7, 4, 6, 8, 10, 12, 16, 20, 24],
											'direction_name': 'Direction - up'},
								'temp_right': {'sensors': ['R1', 'R2', 'R3', 'R4', 'R5', 'R6'],
											   'locations': [4, 8, 12, 16, 20, 24],
											   'direction_name': 'Direction - right'},
								'temp_down': {'sensors': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10'],
											  'locations': [1.3, 2.7, 4, 6, 8, 10, 12, 16, 20, 24],
											  'direction_name': 'Direction - down'},
								'moist_up': {'sensors': ['MS1', 'MS2', 'MS3', 'MS4'],
											 'temp_sensors': ['U3', 'U5', 'U7', 'U8'],
											 'locations': [4, 8, 12, 16],
											 'direction_name': 'Direction - up'},
								'moist_right': {'sensors': ['MS5', 'MS6', 'MS7', 'MS8'],
												'temp_sensors': ['R1', 'R2', 'R3', 'R4'],
												'locations': [4, 8, 12, 16],
												'direction_name': 'Direction - right'},
								'moist_down': {'sensors': ['MS9', 'MS10', 'MS11', 'MS12'],
											   'temp_sensors': ['D3', 'D5', 'D7', 'D8'],
											   'locations': [4, 8, 12, 16],
											   'direction_name': 'Direction - down'}},
					'other_sensors': [],
					'failed_sensors': [],
					'del_data': [],
					'comsol_files': [],
					'sample_props': {'porosity': 0.4,
									 'ks': 2.66,
									 'rhos': 3.02,
									 'w_grav': 3.0}}

		self.SN6 = {
			'sample_name': 'SN6',
			'columns': [
				'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'R1', 'R2',
				'R3', 'R4', 'R5', 'R6', 'U7', 'U8', 'U9', 'U10',
				'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'C1', 'C2',
				'W1', 'D7', 'D8', 'D9', 'D10', 'X1', 'W2', 'X2',
				'MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6',
				'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12',
				'power'
			],
			'temperature_columns': [
				'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'U10',
				'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
				'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
				'C1', 'C2', 'W1', 'W2', 'X1', 'X2',
			],
			'temperature_columns_main': [
				'U1', 'U2', 'U3', 'U4', 'U5', 'U6',
				'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
				'D1', 'D2', 'D3', 'D4', 'D5', 'D6',
			],
			'temperature_columns_moist': [
				'U1', 'U2', 'U3', 'U4',
				'R1', 'R2', 'R3', 'R4',
				'D1', 'D2', 'D3', 'D4',
			],
			'temperature_columns_ext': ['C1', 'C2', 'X1', 'X2', 'W1', 'W2'],
			'moisture_columns': [
				'MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6',
				'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12',
			],
			'power_column': ['power'],
			'phase_names': ['170W_core'],
			'hot_end_sensors': {
				'sensors': ['C1', 'C2'],
				'locations': [0.1],
			},
			'cold_end_sensors': {
				'sensors': ['W1', 'W2'],
				'locations': [26],
			},
			'sensors': {
				'temp_up': {
					'sensors': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'U10'],
					'locations': [1.3, 2.7, 4, 6, 8, 10, 12, 16, 20, 24],
					'direction_name': 'Direction - up',
				},
				'temp_right': {
					'sensors': ['R1', 'R2', 'R3', 'R4', 'R5', 'R6'],
					'locations': [4, 8, 12, 16, 20, 24],
					'direction_name': 'Direction - right',
				},
				'temp_down': {
					'sensors': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10'],
					'locations': [1.3, 2.7, 4, 6, 8, 10, 12, 16, 20, 24],
					'direction_name': 'Direction - down',
				},
				'moist_up': {
					'sensors': ['MS1', 'MS2', 'MS3', 'MS4'],
					'temp_sensors': ['U3', 'U5', 'U7', 'U8'],
					'locations': [4, 8, 12, 16],
					'direction_name': 'Direction - up',
				},
				'moist_right': {
					'sensors': ['MS5', 'MS6', 'MS7', 'MS8'],
					'temp_sensors': ['R1', 'R2', 'R3', 'R4'],
					'locations': [4, 8, 12, 16],
					'direction_name': 'Direction - right',
				},
				'moist_down': {
					'sensors': ['MS9', 'MS10', 'MS11', 'MS12'],
					'temp_sensors': ['D3', 'D5', 'D7', 'D8'],
					'locations': [4, 8, 12, 16],
					'direction_name': 'Direction - down',
				},
			},
			'other_sensors': [],
			'failed_sensors': [],
			'del_data': [],
			'comsol_files': [],
			'sample_props': {
				'porosity': 0.4,
				'ks': 2.66,
				'rhos': 3.02,
				'w_grav': 3.0
			}
		}

		self.SN7 = {
			'sample_name': 'SN7',
			'columns': [
				'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'R1', 'R2',
				'R3', 'R4', 'R5', 'R6', 'U7', 'U8', 'U9', 'U10',
				'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'C1', 'C2',
				'W1', 'D7', 'D8', 'D9', 'D10', 'X1', 'W2', 'X2',
				'MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6',
				'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12',
				'power'
			],
			'temperature_columns': [
				'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'U10',
				'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
				'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
				'C1', 'C2', 'W1', 'W2', 'X1', 'X2',
			],
			'temperature_columns_main': [
				'U1', 'U2', 'U3', 'U4', 'U5', 'U6',
				'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
				'D1', 'D2', 'D3', 'D4', 'D5', 'D6',
			],
			'temperature_columns_moist': [
				'U1', 'U2', 'U3', 'U4',
				'R1', 'R2', 'R3', 'R4',
				'D1', 'D2', 'D3', 'D4',
			],
			'temperature_columns_ext': ['C1', 'C2', 'X1', 'X2', 'W1', 'W2'],
			'moisture_columns': [
				'MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6',
				'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12',
			],
			'power_column': ['power'],
			'phase_names': ['170W_core'],
			'hot_end_sensors': {
				'sensors': ['C1', 'C2'],
				'locations': [0.1],
			},
			'cold_end_sensors': {
				'sensors': ['W1', 'W2'],
				'locations': [26],
			},
			'sensors': {
				'temp_up': {
					'sensors': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'U10'],
					'locations': [1.3, 2.7, 4, 6, 8, 10, 12, 16, 20, 24],
					'direction_name': 'Direction - up',
				},
				'temp_right': {
					'sensors': ['R1', 'R2', 'R3', 'R4', 'R5', 'R6'],
					'locations': [4, 8, 12, 16, 20, 24],
					'direction_name': 'Direction - right',
				},
				'temp_down': {
					'sensors': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10'],
					'locations': [1.3, 2.7, 4, 6, 8, 10, 12, 16, 20, 24],
					'direction_name': 'Direction - down',
				},
				'moist_up': {
					'sensors': ['MS1', 'MS2', 'MS3', 'MS4'],
					'temp_sensors': ['U3', 'U5', 'U7', 'U8'],
					'locations': [4, 8, 12, 16],
					'direction_name': 'Direction - up',
				},
				'moist_right': {
					'sensors': ['MS5', 'MS6', 'MS7', 'MS8'],
					'temp_sensors': ['R1', 'R2', 'R3', 'R4'],
					'locations': [4, 8, 12, 16],
					'direction_name': 'Direction - right',
				},
				'moist_down': {
					'sensors': ['MS9', 'MS10', 'MS11', 'MS12'],
					'temp_sensors': ['D3', 'D5', 'D7', 'D8'],
					'locations': [4, 8, 12, 16],
					'direction_name': 'Direction - down',
				},
			},
			'other_sensors': [],
			'failed_sensors': [],
			'del_data': [],
			'comsol_files': [],
			'sample_props': {
				'porosity': 0.4,
				'ks': 2.66,
				'rhos': 3.02,
				'w_grav': 3.0
			}
		}

		self.SN8 = {'sample_name': 'SN8'}
		self.SN9 = {'sample_name': 'SN9'}
		self.SN10 = {'sample_name': 'SN10'}

		self.samples = [
			self.SN3,
			self.SN4,
			self.SN5,
			self.SN6,
			self.SN7,
			#self.SN8,
			#self.SN9,
			#self.SN10,
		]
