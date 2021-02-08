import matplotlib.pyplot as plt
import pandas as pd

class PlotCalibrationFigures:
	def __init__(self, data_path, sample):
		self.sample = sample

		self.calib_data = pd.read_excel(data_path + 'moisture_sensor_calibration_data.xlsx', sheet_name='Sheet2')
		self.calib_data_from_testing = pd.read_excel(data_path + 'moitsure_sensor_calibration_data_during_testing.xlsx',
													 sheet_name='Sheet1')

		self.sensor_names = ['MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6', 'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12']
		self.temp_names = ['30degC', '40degC', '50degC', '60degC', '70degC']

	def plot_calibration_figure(self):
		nrows = 4
		ncols = 3
		fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(20, 20))
		fig.subplots_adjust(hspace=0.3)

		sensor_counter = 0
		for row in range(nrows):
			for column in range(ncols):
				subset = self.calib_data[self.calib_data['sensor'] == self.sensor_names[sensor_counter]]
				for temp in self.temp_names:
					subsubset = subset[subset['temp'] == temp]
					ax[row, column].plot(subsubset['vol'],
										 subsubset['w%'],
										 label=temp,
										 marker='o')
					ax[row, column].plot(self.calib_data_from_testing[self.sensor_names[sensor_counter]],
										 self.calib_data_from_testing['w%'],
										 linestyle='none',
										 marker='o',
										 mec='black')

					ax[row, column].set_xlabel('Voltage, mV')
					ax[row, column].set_ylabel('Moisture, %')
					ax[row, column].set_title(self.sensor_names[sensor_counter])
					ax[row, column].legend()
					#ax[row, column].set_xlim([450, 570])



				sensor_counter += 1
		plt.savefig('moisture_figure.png', dpi=300)
		plt.show()