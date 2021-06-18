import pandas as pd

class SensorCorrection:
	"""
	ms - moisture sensor calibration factors
	ts - temperature sensor calibration factors
	"""
	def __init__(self, path):
		self.ms = pd.read_excel(path + 'moisture_sensor_calibration_factors.xlsx', sheet_name='Sheet1', index_col=0)
		self.ts = pd.read_excel(path + 'temperature_sensor_calibration_factors.xlsx', sheet_name='Sheet1', index_col=0)

	def moisture_sensor_correction(self, TS, MS, read_temp, read_vol):
		"""
		V1L - low moisture, low temperature
		V1H - low moisture, high temperature
		V2L - high moisture, low temperature
		V2H - high moisture, high temperature
		"""
		sensor = self.ms.loc[MS]
		pos = (read_temp - sensor['T1']) / (sensor['T2'] - sensor['T1'])
		VxL = sensor['V1L'] + (sensor['V1H'] - sensor['V1L']) * pos
		VxH = sensor['V2L'] + (sensor['V2H'] - sensor['V2L']) * pos
		slope = (sensor['wH%'] - sensor['wL%']) / (VxH - VxL)
		w_grav = slope * (read_vol - VxH) + sensor['wH%']
		return w_grav

	def tempertaure_sensor_correction(self, TS, mes_val):
		sensor = self.ts.loc[TS]
		temp = sensor['a'] * mes_val + sensor['b']
		return temp
