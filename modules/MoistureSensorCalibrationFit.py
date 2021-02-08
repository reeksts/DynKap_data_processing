import pandas as pd
import matplotlib.pyplot as plt

class MoistureSensorCalibrationFit:
	def __init__(self):
		self.ms = pd.read_excel('moisture_sensor_calibratoin_full_data.xlsx', sheet_name='Sheet1')
		#self.sensor_names = ['MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6', 'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12']
		self.sensor_names = ['MS1']
		self.temperatures = ['30degC', '40degC', '50degC', '60degC', '70degC']

	def plot_figures(self):
		for sensor in self.sensor_names:
			sensor_df = self.ms[self.ms['sensor'] == sensor]

			# initializer:
			fig, ax = plt.subplots(figsize=(12, 6))

			for temp in self.temperatures:
				temp_df = sensor_df[sensor_df['temp'] == temp]
				x_vals = temp_df['vol'].values
				y_vals = temp_df['w%'].values
				ax.plot(x_vals,
						y_vals,
						label=temp,
						marker='o')

			# configuration:
			ax.set_ylabel('Moisture content, %', size=10)
			ax.set_xlabel('Measured voltage, mV', size=10)
			ax.tick_params(axis='both', direction='in', width=1.5, right=True, top=True)
			for j in ['top', 'bottom', 'left', 'right']:
				ax.spines[j].set_linewidth(1.5)


			plt.show()





moist = MoistureSensorCalibrationFit()
moist.plot_figures()
