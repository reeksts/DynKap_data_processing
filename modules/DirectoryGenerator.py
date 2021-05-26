import os


class DirectoryGenerator:
	def __init__(self, sample_data, sample, output_dir):
		self.sample_data = sample_data
		self.sample = sample
		self.output_dir = output_dir

	def large_test_directories(self):
		"""
		Generates folder structure as follows:
		- Parent directory (sample sample name SN or SS)
			- Child directory (phase names - master, phase1, phase2)
				- Child subdirectories (plot types - series, gardient, animated)

		"""
		sample_name = self.sample['sample_name']
		self.sample = self.sample

		# child subdirectories:
		combined_plots = self.sample_data.folders['01_combined_plots']
		time_series_temperature = self.sample_data.folders['02_time_series_temperature']
		time_series_moisture = self.sample_data.folders['03_time_series_moisture']
		gradient_temperature = self.sample_data.folders['04_gradient_temperature']
		gradient_moisture = self.sample_data.folders['05_gradient_moisture']
		last_24_hours = self.sample_data.folders['06_last_24_hours']
		animated_plots = self.sample_data.folders['07_animated_plots']
		moist_vs_temp = self.sample_data.folders['08_time_series_moisture_vs_temperature']
		individual_sensors = self.sample_data.folders['09_tracking_individual_sensors']
		child_subdirectories = [combined_plots,
								time_series_temperature,
								time_series_moisture,
								gradient_temperature,
								gradient_moisture,
								last_24_hours,
								animated_plots,
								moist_vs_temp,
								individual_sensors]

		# Generate sample parent directory:
		parent_dir = sample_name + '\\'
		if not os.path.exists(self.output_dir + parent_dir):
			os.mkdir(self.output_dir + parent_dir)

		# Generate sample child directories (MASTER, PHASE1, PHASE2.. etc):
		child_dir_names = []
		phase_num = 1
		for phases in self.sample['phases']:
			child_dir = 'PHASE' + str(phase_num) + '_' + phases['name'] + '\\'
			if not os.path.exists(self.output_dir + parent_dir + child_dir):
				os.mkdir(self.output_dir + parent_dir + child_dir)
			phase_num += 1
			child_dir_names.append(child_dir)
		phase_master = 'PHASE_MASTER\\'
		if not os.path.exists(self.output_dir + parent_dir + phase_master):
			os.mkdir(self.output_dir + parent_dir + phase_master)
		child_dir_names.append(phase_master)

		# Generate sample child subdirectories (01_combined.., 02_time_series.., etc):
		for child_dir in child_dir_names:
			for child_sub_dir in child_subdirectories:
				if not os.path.exists(self.output_dir + parent_dir + child_dir + child_sub_dir):
					os.mkdir(self.output_dir + parent_dir + child_dir + child_sub_dir)

	def small_test_directories(self):
		sample_name = self.sample['sample_name']
		self.sample = self.sample

		# child subdirectories:
		time_series_plots = self.sample_data.folders['01_time_series_plots']
		temperature_gradient_plots = self.sample_data.folders['02_temperature_gradient_plots']
		animated_gradient = self.sample_data.folders['03_animated_plots']
		child_subdirectories = [time_series_plots,
								temperature_gradient_plots,
								animated_gradient]

		# Generate sample parent directory:
		parent_dir = sample_name + '\\'
		if not os.path.exists(self.output_dir + parent_dir):
			os.mkdir(self.output_dir + parent_dir)

		# Generate sample child directories (MASTER, PHASE1, PHASE2.. etc):
		child_dir_names = ['PHASE_MASTER\\']
		phase_num = 1
		for phases in self.sample['phases']:
			child_dir = 'PHASE' + str(phase_num) + '_' + phases['name'] + '\\'
			child_dir_names.append(child_dir)
			if not os.path.exists(self.output_dir + parent_dir + child_dir):
				os.mkdir(self.output_dir + parent_dir + child_dir)
			phase_num += 1
		phase_master = 'PHASE_MASTER\\'
		if not os.path.exists(self.output_dir + parent_dir + phase_master):
			os.mkdir(self.output_dir + parent_dir + phase_master)

		# Generate sample child subdirectories (01_combined.., 02_time_series.., etc):
		for child_dir in child_dir_names:
			for child_sub_dir in child_subdirectories:
				if not os.path.exists(self.output_dir + parent_dir + child_dir + child_sub_dir):
					os.mkdir(self.output_dir + parent_dir + child_dir + child_sub_dir)

	def return_phase_directories(self):
		phase_directories = [self.output_dir + self.sample['sample_name'] + '\\' + 'PHASE_MASTER\\']
		phase_num = 1
		for phases in self.sample['phases']:
			child_dir = self.output_dir + self.sample['sample_name'] + '\\' + 'PHASE' + str(phase_num) + '_' + phases['name'] + '\\'
			phase_directories.append(child_dir)
			phase_num += 1
		return phase_directories
