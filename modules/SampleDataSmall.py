import pandas as pd


class SampleDataSmall:
	def __init__(self):
		self.SN2 = {'sample_name': 'SS1',
					'path': 'C:\\Users\\karlisr\\OneDrive - NTNU\\3_PostDoc_Sintef\\01_laboratory_work\\01_small_test\\',
					'timestamps': [[pd.Timestamp(2021, 1, 19, 14, 30), '154W core'],
								   [pd.Timestamp(2021, 1, 26, 8, 00), '174W core'],
								   [pd.Timestamp(2021, 2, 1, 8, 00), '194W core'],
								   [pd.Timestamp(2021, 2, 5, 8, 00), '214W core'],
								   [pd.Timestamp(2021, 2, 15, 8, 00), '288W core']],
					'phases': [{'start': 'timestamp', 'end': 'timestamp', 'name': '154W_core'},
							   {'start': 'timestamp', 'end': 'timestamp', 'name': '174W_core'},
							   {'start': 'timestamp', 'end': 'timestamp', 'name': '196W_core'},
							   {'start': 'timestamp', 'end': 'timestamp', 'name': '217W_core'},
							   {'start': 'timestamp', 'end': 'timestamp', 'name': '290W_core'}],
					'core_sensors': {'sensors': ['X1', 'X2'],
									 'locations': [0, 26]},
					'wall_sensors': {'sensors': ['K2', 'X3'],
									 'locations': [0, 26]},
					'sensors': {'temp': {'sensors': ['U1', 'U2', 'U3', 'U4', 'U5', 'U6'],
										 'locations': [4, 8, 12, 16, 20, 24],
										 'direction_name': 'Direction - up'},
					'del_data': [{'sensor': 'R1',
								  'start': pd.Timestamp(2021, 2, 6, 12, 40),
								  'end': pd.Timestamp(2021, 2, 8, 17, 40)}],
					'comsol_files': ['comsol_model_288W.csv']}