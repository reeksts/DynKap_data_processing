import os


class DirectoryGenerator:
	def __init__(self):
		pass

	@staticmethod
	def directory_generator(active_test, active_sample):
		"""
		Generates sample directory structure as follows:
		- Generate sample parent directory: (SN1(SS1), SN2(SS2), SN3(SS3), ..., etc)
			- Generate sample child directories: (01_raw_data, 02_measurement_data, ..., etc)
				- Generate child subdirectories (MASTER, PHASE1, PHASE2, ..., etc)
					- Generate child subdirectory subdirectories (01_combined.., 02_time_series, ..., etc):
		:return: phase_directories
		"""

		plot_folders = active_test.plot_folders
		sample_name = active_sample['sample_name']
		sample_dir = active_test.test_info['sample_dir']

		# child folder names:
		raw_data_folder = '01_raw_data'
		measurement_data_folder = '02_measurement_data'
		comsol_model_folder = '03_comsol_model'
		calib_data_folder = '04_calib_data'
		moisture_weight_measurements_folder = '05_moisture_weight_measurements'
		other_folder = '06_other'
		pics_folder = '07_pics'
		measurement_figures_folder = '08_measurement_figures'
		child_folders = [
			raw_data_folder,
			measurement_data_folder,
			comsol_model_folder,
			calib_data_folder,
			moisture_weight_measurements_folder,
			other_folder,
			pics_folder,
			measurement_figures_folder
		]

		# Generate sample parent directory: (SN1(SS1), SN2(SS2), ..., etc)
		parent_directory = os.path.join(sample_dir, sample_name)
		if not os.path.exists(parent_directory):
			os.mkdir(parent_directory)

		# Generate sample child directories: (01_raw_data, 02_measurement_data, ..., etc)
		for folder in child_folders:
			child_subdirectory = os.path.join(parent_directory, folder)
			if not os.path.exists(child_subdirectory):
				os.mkdir(child_subdirectory)

				# inner 01_calibrated_datasets folder generation:
				if folder == '02_measurement_data':
					inner_child_subdirectory = os.path.join(parent_directory, folder, '01_calibrated_datasets')
					if not os.path.exists(inner_child_subdirectory):
						os.mkdir(inner_child_subdirectory)



		# Generate child subdirectories (MASTER, PHASE1, PHASE2, ..., etc)
		if 'phase_names' in active_sample:
			phase_folders = ['PHASE_MASTER']
			phase_directories = []
			phase_num = 1
			for phase in active_sample['phase_names']:
				subdirectory_folders = 'PHASE' + str(phase_num) + '_' + phase
				phase_num += 1
				phase_folders.append(subdirectory_folders)

			measurement_figures_directory = os.path.join(
				sample_dir,
				sample_name,
				measurement_figures_folder
			)
			for new_phase_name in phase_folders:
				phase_directories.append(os.path.join(measurement_figures_directory, new_phase_name))

				# check if particular phase (except MASTER) exists:
				if 'MASTER' not in new_phase_name:
					# Break down the phase_name into phase_number and phase_tag:
					new_phase_number, new_phase_tag = new_phase_name.split('_', 1)
					# Check if such phase number exists:
					current_phase_folders = os.listdir(measurement_figures_directory)

					exists = False
					for phase_folder in current_phase_folders:
						if new_phase_number in phase_folder:
							exists = True
					if not exists:
						os.mkdir(os.path.join(measurement_figures_directory, new_phase_name))
					else:
						for phase_folder in current_phase_folders:
							if new_phase_number in phase_folder:
								current_phase_tag = phase_folder.split('_', 1)[1]
								if new_phase_tag != current_phase_tag:
									os.rename(
										os.path.join(measurement_figures_directory, phase_folder),
										os.path.join(measurement_figures_directory, new_phase_name),
									)

				elif 'MASTER' in new_phase_name:
					if not os.path.exists(os.path.join(measurement_figures_directory, new_phase_name)):
						os.mkdir(os.path.join(measurement_figures_directory, new_phase_name))

				for plot in plot_folders:
					if not os.path.exists(os.path.join(measurement_figures_directory, new_phase_name, plot)):
						os.mkdir(os.path.join(measurement_figures_directory, new_phase_name, plot))

			return phase_directories
