import os


class DirectoryGenerator:
	def __init__(self, sample):
		general_path = sample['path']  	# this is a general path to large_test
		figure_output_dir = '08_measurement_figures\\'
		figure_output_path = general_path + figure_output_dir
		sample_name = sample['sample_name']

		# child subdirectories:
		combined_plots = '01_combined_plots\\'
		time_series_temperature = '02_time_series_temperature\\'
		time_series_moisture = '03_time_series_moisture\\'
		gradient_temperature = '04_gradient_temperature\\'
		gradient_moisture = '05_gradient_moisture\\'
		child_subdirectories = [combined_plots, time_series_temperature, time_series_moisture,
								gradient_temperature, gradient_moisture]

		# Generate sample parent directory:
		parent_dir = 'Sample_' + sample_name + '\\'
		if not os.path.exists(figure_output_path + parent_dir):
			os.mkdir(figure_output_path + parent_dir)

		# Generate sample child directories:
		child_dir_names = []
		phase_num = 1
		for phases in sample['phases']:
			child_dir = 'PHASE' + str(phase_num) + '_' + phases['name'] + '\\'
			if not os.path.exists(figure_output_path + parent_dir + child_dir):
				os.mkdir(figure_output_path + parent_dir + child_dir)
				child_dir_names.append(child_dir)
			phase_num += 1
		phase_master = 'PHASE_MASTER\\'
		if not os.path.exists(figure_output_path + parent_dir + phase_master):
			os.mkdir(figure_output_path + parent_dir + phase_master)
			child_dir_names.append(phase_master)

		# Generate sample child subdirectories:
		for child_dir in child_dir_names:
			for child_sub_dir in child_subdirectories:
				if not os.path.exists(figure_output_path + parent_dir + child_dir + child_sub_dir):
					os.mkdir(figure_output_path + parent_dir + child_dir + child_sub_dir)
