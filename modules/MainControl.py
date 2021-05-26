import pandas as pd
import os
from modules.SensorCorrection import SensorCorrection
from modules.PlotMeasurementFigures import PlotMeasurementFigures
from modules.DataProcessor import DataProcessor
from modules.DirectoryGenerator import DirectoryGenerator
from modules.MiscCalculations import TempDistSolver, ThermalConductivity

class LargeTestControl:
    """
    An instance of this class is initiated together with teh program.
    """
    def __init__(self, sample_data, formatter):
        self.sample_data = sample_data
        self.formatter = formatter
        self.sample = None
        self.plotter = PlotMeasurementFigures(self.sample_data)
        self.data_processor = None
        self.df = None
        self.dfs = None
        self.phase_directories = None
        self.data_input = sample_data.test_info['data_input']
        self.data_output = sample_data.test_info['data_output']
        self.fignames = sample_data.fignames

        self.measurement_folder = '02_measurement_data\\'
        self.comsol_folder = '03_comsol_model\\'
        self.calib_folder = '04_calib_data\\'

    def load_dataset(self, sample):
        self.sample = sample
        sample_name = self.sample['sample_name'] + '\\'

        # Load sample in plotter:
        self.plotter.load_sample_into_plotter(self.sample)

        # Sample thermal conductivity (dry thermal conductivity and moist thermal conductivity)
        porosity = self.sample['sample_props']['porosity']
        ks = self.sample['sample_props']['ks']
        rhos = self.sample['sample_props']['rhos']
        w_grav = self.sample['sample_props']['w_grav']

        thermal = ThermalConductivity(porosity, ks, rhos, w_grav)
        kdry, kmoist = thermal.calculate_thermal_conductivity()

        # Initialize two zone solver
        zone_solver = TempDistSolver()

        # Data input directories:
        sample_data_dir = self.data_input + sample_name + self.measurement_folder
        comsol_data_dir = self.data_input + sample_name + self.comsol_folder
        calib_data_dir = self.data_input + sample_name + self.calib_folder

        # Directory generator:
        directory_generator = DirectoryGenerator(self.sample_data, self.sample, self.data_output)
        directory_generator.large_test_directories()
        self.phase_directories = directory_generator.return_phase_directories()

        # Calibration fit figures (optional):
        # calibration_figures = PlotCalibrationFigures(data_path, sample)
        # calibration_figures.plot_calibration_figure()

        # Plot formatter
        self.styler_color = 'light'

        # Column names:
        columns = self.sample['columns']
        temperature_columns_main = self.sample['temperature_columns_main']
        temperature_columns_moist = self.sample['temperature_columns_moist']
        temperature_columns_ext = self.sample['temperature_columns_ext']
        moisture_columns = self.sample['moisture_columns']
        temperature_columns = temperature_columns_main + temperature_columns_ext  # this is only for temperature correction

        # Loading dataframes:
        self.df = pd.DataFrame(columns=columns)
        files = os.listdir(sample_data_dir)
        for index, file in enumerate(files):
            if file.endswith('csv'):
                filename, extension = os.path.splitext(file)
                # Separating filename to extract phase number
                keyword = 'phase'
                sample_name, keyword, phase_number = filename.partition(keyword)
                if len(phase_number) == 1:
                    # Normal case: phase consist of single file
                    df_loc = pd.read_csv(sample_data_dir + file, index_col=0, names=columns)
                    self.df = pd.concat([self.df, df_loc])
                elif index == len(files) - 1:
                    # Phase consists of multiple files, but this is the very last file
                    df_loc = pd.read_csv(sample_data_dir + file, index_col=0, names=columns)
                    self.df = pd.concat([self.df, df_loc])
                else:
                    # When multiple files, one of the phase files.
                    # Retrieving phase number for the next file:
                    filename_next, extension_next = os.path.splitext(files[index + 1])
                    sample_name_next, keyword_next, phase_number_next = filename_next.partition(keyword)
                    if len(phase_number_next) == 1:
                        # This is the last file of the phase
                        df_loc = pd.read_csv(sample_data_dir + file, index_col=0, names=columns)
                        self.df = pd.concat([self.df, df_loc])
                    else:
                        df_loc = pd.read_csv(sample_data_dir + file, index_col=0, names=columns)
                        last_index = pd.to_datetime(df_loc.index[-1])
                        df_loc = df_loc.append(pd.Series(name=last_index + pd.Timedelta(minutes=1)))
                        self.df = pd.concat([self.df, df_loc])
            else:
                pass

        # Measurement corrections:
        def corrector_func(self):
            corrector = SensorCorrection(calib_data_dir)
            for name in temperature_columns:
                self.df[name] = self.df[name].apply(lambda mes_val: corrector.tempertaure_sensor_correction(name, mes_val))
            for temp_name, moist_name in zip(temperature_columns_moist, moisture_columns):
                self.df[moist_name] = self.df.apply(lambda line: corrector.moisture_sensor_correction(temp_name,
                                                                                            moist_name,
                                                                                            line[temp_name],
                                                                                            line[moist_name]), axis=1)

        # corrector_func()

        # Plot figures
        """
		Options to select from:
		- plot_all_measurements()   -> plots a 4 row, 3 column figure
		- plot_temperature_series()   -> plots temperature series separately
		- plot_moisture_series()   -> plots separately moisture figures series
		- plot_temperature_gradient()   -> plots temperature gradient separately
		- plot_moisture_gradient()   -> plots separately moisture figure gradient
		"""

        self.df.index = pd.to_datetime(self.df.index)
        self.add_hours_column_to_df()
        self.add_cold_end_temp_column()
        self.add_hot_end_temp_column()

        # Initiate DataProcessor instance for data manipulation:
        self.data_processor = DataProcessor(self.sample)
        self.data_processor.delete_flawed_data(self.df)

        # Generating dfs from comsol solutions
        # comsol_processor = ComsolProcessor(sample, comsol_path)
        # comsol_dfs = comsol_processor.generate_comsol_df()
        comsol_dfs = []

    def add_hours_column_to_df(self):
        start_time = self.df.index[0]

        def calc_hour_diff(time_point):
            diff = time_point - start_time
            return diff.days * 24 + diff.seconds / 3600

        self.df['hours'] = self.df.index.to_series().apply(calc_hour_diff)

    def add_cold_end_temp_column(self):
        self.df['cold_end'] = self.df[self.sample['cold_end_sensors']['sensors']].mean(axis=1)

    def add_hot_end_temp_column(self):
        self.df['hot_end'] = self.df[self.sample['hot_end_sensors']['sensors']].mean(axis=1)

    # Combined plot calls:
    def con_SN_combined_master(self, phases, xscale):
        if phases == 'master':
            dfs = [self.df]
            phase_dirs = self.phase_directories[0:1]
        else:
            self.dfs = self.generate_phase_dfs()
            dfs = self.dfs
            phase_dirs = self.phase_directories

        print('\n')
        print('Currently printing con_SN_combined_master')

        for df, direc in zip(dfs, phase_dirs):
            print(f'Currently printing in {direc}')
            self.plotter.plot_SN_combined_master(df=df,
                                                 phase_directory=direc,
                                                 folder=self.sample_data.folders['01_combined_plots'],
                                                 sizer=self.formatter.paper_4x3_full_width,        # changed this to pres!!
                                                 styler=self.formatter.styler[self.styler_color],
                                                 xscale=xscale)

        print('Done')

    def con_SN_combined_temperature_series(self, phases):
        """
        Plots combined (3x1) temperature series figure (with hours and datetime).
        This function is called from MainApp by app_SN_combined_temperature_series.
        """
        if phases == 'master':
            dfs = [self.df]
            phase_dirs = self.phase_directories[0:1]
        else:
            dfs = self.dfs
            phase_dirs = self.phase_directories

        print('\n')
        print('Currently printing con_SN_combined_temperature_series')

        for df, direc in zip(dfs, phase_dirs):
            # this iterates one or multiple times
            self.plotter.plot_SN_combined_temperature_series(df=df,
                                                             phase_directory=direc,
                                                             folder=self.sample_data.folders['01_combined_plots'],
                                                             sizer=self.formatter.std_paper_3x1_full_width,
                                                             styler=self.formatter.styler[self.styler_color])
            self.plotter.plot_SN_combined_temperature_series(df=df,
                                                             phase_directory=direc,
                                                             folder=self.sample_data.folders['01_combined_plots'],
                                                             sizer=self.formatter.std_paper_3x1_full_width,
                                                             styler=self.formatter.styler[self.styler_color],
                                                             xaxis_type='datetime')

        print('Done')

    def con_SN_combined_temperature_gradient(self, phases, xscale):
        """
        Plots combined (3x1) temperature gradient figure.
        This function is called from MainApp by app_SN_combined_temperature_gradient.
        """
        if phases == 'master':
            dfs = [self.df]
            phase_dirs = self.phase_directories[0:1]
        else:
            dfs = self.dfs
            phase_dirs = self.phase_directories

        print('\n')
        print('Currently printing con_SN_combined_temperature_gradient')

        for df, direc in zip(dfs, phase_dirs):
            # this iterates one or multiple times
            self.plotter.plot_SN_combined_temperature_gradient(df=df,
                                                               phase_directory=direc,
                                                               folder=self.sample_data.folders['01_combined_plots'],
                                                               sizer=self.formatter.std_paper_3x1_partial_width,
                                                               styler=self.formatter.styler[self.styler_color],
                                                               xscale=xscale)

        print('Done')

    def con_SN_combined_moisture_series(self, phases):
        """
        Plots combined (3x1) moisture series gradient figure.
        This function is called from MainApp by app_SN_combined_moisture_series.
        """

        if phases == 'master':
            dfs = [self.df]
            phase_dirs = self.phase_directories[0:1]
        else:
            dfs = self.dfs
            phase_dirs = self.phase_directories

        print('\n')
        print('Currently printing con_SN_combined_moisture_series')

        for df, direc in zip(dfs, phase_dirs):
            # this iterates one or multiple times
            self.plotter.plot_SN_combined_moisture_series(df=df,
                                                          phase_directory=direc,
                                                          folder=self.sample_data.folders['01_combined_plots'],
                                                          sizer=self.formatter.std_paper_3x1_full_width,
                                                          styler=self.formatter.styler[self.styler_color])
            self.plotter.plot_SN_combined_moisture_series(df=df,
                                                          phase_directory=direc,
                                                          folder=self.sample_data.folders['01_combined_plots'],
                                                          sizer=self.formatter.std_paper_3x1_full_width,
                                                          styler=self.formatter.styler[self.styler_color],
                                                          xaxis_type='datetime')

        print('Done')

    def con_SN_combined_moisture_gradient(self, phases, xscale):
        """
        Plots combined (3x1) moisture gradient figure.
        This function is called from MainApp by app_SN_combined_moisture_gradient.
        """
        if phases == 'master':
            dfs = [self.df]
            phase_dirs = self.phase_directories[0:1]
        else:
            dfs = self.dfs
            phase_dirs = self.phase_directories

        print('\n')
        print('Currently printing con_SN_combined_moisture_gradient')

        for df, direc in zip(dfs, phase_dirs):
            self.plotter.plot_SN_combined_moisture_gradients(df=df,
                                                             phase_directory=direc,
                                                             folder=self.sample_data.folders['01_combined_plots'],
                                                             sizer=self.formatter.std_paper_3x1_partial_width,
                                                             styler=self.formatter.styler[self.styler_color],
                                                             xscale=xscale)

        print('Done')

    def con_SN_combined_series_moist_vs_temp(self, phases):
        """
        Plots combined (3x1) moisture vs temperature series.
        This function is called from MainApp by app_SN_combined_series_moist_vs_temp.
        """
        if phases == 'master':
            dfs = [self.df]
            phase_dirs = self.phase_directories[0:1]
        else:
            dfs = self.dfs
            phase_dirs = self.phase_directories

        print('\n')
        print('Currently printing con_SN_combined_series_moist_vs_temp')

        for df, direc in zip(dfs, phase_dirs):
            # this iterates one or multiple times
            self.plotter.plot_SN_combined_series_moist_vs_temp(
                df=df,
                phase_directory=direc,
                folder=self.sample_data.folders['08_time_series_moisture_vs_temperature'],
                sizer=self.formatter.std_paper_3x1_full_width,
                styler=self.formatter.styler[self.styler_color])
            self.plotter.plot_SN_combined_series_moist_vs_temp(
                df=df,
                phase_directory=direc,
                folder=self.sample_data.folders['08_time_series_moisture_vs_temperature'],
                sizer=self.formatter.std_paper_3x1_full_width,
                styler=self.formatter.styler[self.styler_color],
                xaxis_type='datetime')

        print('Done')

    # Separate plot function calls:
    def con_SN_separate_temperature_series(self, phases):
        """
        Plots separate figures for every direction for temperature series.
        This function is called from MainApp by app_SN_separate_temperature_series.
        """
        if phases == 'master':
            dfs = [self.df]
            phase_dirs = self.phase_directories[0:1]
        else:
            dfs = self.dfs
            phase_dirs = self.phase_directories

        print('\n')
        print('Currently printing con_SN_separate_temperature_series')

        for df, direc in zip(dfs, phase_dirs):
            self.plotter.plot_SN_separate_temperature_series(
                df=df,
                phase_directory=direc,
                folder=self.sample_data.folders['02_time_series_temperature'],
                sizer=self.formatter.paper_full_width,
                styler=self.formatter.styler[self.styler_color])
            self.plotter.plot_SN_separate_temperature_series(
                df=df,
                phase_directory=direc,
                folder=self.sample_data.folders['02_time_series_temperature'],
                sizer=self.formatter.paper_full_width,
                styler=self.formatter.styler[self.styler_color],
                xaxis_type='datetime')

        print('Done')

    def con_SN_separate_temperature_gradient(self, phases, xscale):
        """
        Plots separate figures for every direction for temperature gradient.
        This function is called from MainApp by app_SN_separate_temperature_gradient.
        """
        if phases == 'master':
            dfs = [self.df]
            phase_dirs = self.phase_directories[0:1]
        else:
            dfs = self.dfs
            phase_dirs = self.phase_directories

        print('\n')
        print('Currently printing con_SN_separate_temperature_gradient')

        for df, direc in zip(dfs, phase_dirs):
            self.plotter.plot_SN_separate_temperature_gradient(
                df=df,
                phase_directory=direc,
                folder=self.sample_data.folders['04_gradient_temperature'],
                sizer=self.formatter.std_paper_1x1_partial_width,
                styler=self.formatter.styler[self.styler_color],
                xscale=xscale)

        print('Done')

    def con_SN_separate_moisture_series(self, phases):
        """
        Plots separate figures for every direction for moisture series.
        This function is called from MainApp by app_SN_separate_moisture_series.
        """
        if phases == 'master':
            dfs = [self.df]
            phase_dirs = self.phase_directories[0:1]
        else:
            dfs = self.dfs
            phase_dirs = self.phase_directories

        print('\n')
        print('Currently printing con_SN_separate_moisture_series')

        for df, direc in zip(dfs, phase_dirs):
            self.plotter.plot_SN_separate_moisture_series(
                df=df,
                phase_directory=direc,
                folder=self.sample_data.folders['03_time_series_moisture'],
                sizer=self.formatter.paper_full_width,
                styler=self.formatter.styler[self.styler_color])
            self.plotter.plot_SN_separate_moisture_series(
                df=df,
                phase_directory=direc,
                folder=self.sample_data.folders['03_time_series_moisture'],
                sizer=self.formatter.paper_full_width,
                styler=self.formatter.styler[self.styler_color],
                xaxis_type='datetime')

        print('Done')

    def con_SN_separate_moisture_gradient(self, phases, xscale):
        """
        Plots separate figures for every direction for moisture gradient.
        This function is called from MainApp by app_SN_separate_moisture_gradient.
        """
        if phases == 'master':
            dfs = [self.df]
            phase_dirs = self.phase_directories[0:1]
        else:
            dfs = self.dfs
            phase_dirs = self.phase_directories

        print('\n')
        print('Currently printing con_SN_separate_moisture_gradient')

        for df, direc in zip(dfs, phase_dirs):
            # this iterates one or multiple times
            self.plotter.plot_SN_separate_moisture_gradient(df=df,
                                                            phase_directory=direc,
                                                            folder=self.sample_data.folders['05_gradient_moisture'],
                                                            sizer=self.formatter.std_paper_1x1_partial_width,
                                                            styler=self.formatter.styler[self.styler_color],
                                                            xscale=xscale)

        print('Done')

    # Short period plot function calls:
    def con_SN_last_24h_plots(self, phases):
        """
        Plots separate and combined temperature and moisture series for the last 24h our period.
        This function is called from MainApp by app_last_24h_plots.
        """
        if phases == 'master':
            dfs = [self.df]
            phase_dirs = self.phase_directories[0:1]
        else:
            dfs = self.dfs
            phase_dirs = self.phase_directories

        print('\n')
        print('Currently printing con_last_24h_plots')

        for df, direc in zip(dfs, phase_dirs):
            df = self.data_processor.create_24h_subset(df)
            self.plotter.plot_SN_separate_temperature_series(df=df,
                                                             phase_directory=direc,
                                                             folder=self.sample_data.folders['06_last_24_hours'],
                                                             sizer=self.formatter.paper_full_width,
                                                             styler=self.formatter.styler[self.styler_color],
                                                             xaxis_type='datetime',
                                                             last_day=True)
            self.plotter.plot_SN_separate_moisture_series(df=df,
                                                          phase_directory=direc,
                                                          folder=self.sample_data.folders['06_last_24_hours'],
                                                          sizer=self.formatter.paper_full_width,
                                                          styler=self.formatter.styler[self.styler_color],
                                                          xaxis_type='datetime',
                                                          last_day=True)
            self.plotter.plot_SN_combined_temperature_series(df=df,
                                                             phase_directory=direc,
                                                             folder=self.sample_data.folders['06_last_24_hours'],
                                                             sizer=self.formatter.std_paper_3x1_full_width,
                                                             styler=self.formatter.styler[self.styler_color],
                                                             xaxis_type='datetime',
                                                             last_day=True)
            self.plotter.plot_SN_combined_moisture_series(df=df,
                                                          phase_directory=direc,
                                                          folder=self.sample_data.folders['06_last_24_hours'],
                                                          sizer=self.formatter.std_paper_3x1_full_width,
                                                          styler=self.formatter.styler[self.styler_color],
                                                          xaxis_type='datetime',
                                                          last_day=True)

        print('Done')

    def con_SN_hot_end_temperature(self, phases):
        if phases == 'master':
            dfs = [self.df]
            phase_dirs = self.phase_directories[0:1]
        else:
            dfs = self.dfs
            phase_dirs = self.phase_directories

        print('\n')
        print('Currently printing hot end temperature')

        for df, direc in zip(dfs, phase_dirs):
            df = self.data_processor.create_10perc_subset(df)
            self.plotter.plot_SN_hot_end_temperature(df=df,
                                                     phase_directory=direc,
                                                     folder=self.sample_data.folders['09_tracking_individual_sensors'],
                                                     sizer=self.formatter.paper_full_width,
                                                     styler=self.formatter.styler[self.styler_color])

        print('Done')

    def plot_everything(self, phases, xscale):
        # Combined plots:
        self.con_SN_combined_master(phases=phases, xscale=xscale)
        self.con_SN_combined_temperature_series(phases=phases)
        self.con_SN_combined_temperature_gradient(phases=phases, xscale=xscale)
        self.con_SN_combined_moisture_series(phases=phases)
        self.con_SN_combined_moisture_gradient(phases=phases, xscale=xscale)
        self.con_SN_combined_series_moist_vs_temp(phases=phases)

        # Separate plots:
        self.con_SN_separate_temperature_series(phases=phases)
        self.con_SN_separate_temperature_gradient(phases=phases, xscale=xscale)
        self.con_SN_separate_moisture_series(phases=phases)
        self.con_SN_separate_moisture_gradient(phases=phases, xscale=xscale)
        self.con_SN_last_24h_plots(phases=phases)
        self.con_SN_hot_end_temperature(phases=phases)

        # main df -> PHASE_MASTER       subfolder stay the same
        # any other PHASE?_phase_name   subfolder stay the same

    def generate_phase_dfs(self):
        """
        The function generates a list wiht of phased dfs. The first element in teh list is the master phase while the
        following are each particular phase based on start and end datetimes.
        :return: list with all phase dfs as follows: [MASTER_PHASE, PHASE1, PHASE2..]
        """
        dfs = [self.df]
        for phase in self.sample['phases']:
            df_loc = self.df.loc[phase['start']:phase['end']]
            dfs.append(df_loc)
        return dfs


class SmallTestControl:
    """
    An instance of this class is initiated together with teh program.
    """
    def __init__(self, sample_data, formatter):
        self.sample_data = sample_data
        self.formatter = formatter
        self.sample = None
        self.plotter = PlotMeasurementFigures(self.sample_data)
        self.df = None
        self.dfs = None
        self.phase_directories = None
        self.data_input = sample_data.test_info['data_input']
        self.data_output = sample_data.test_info['data_output']
        self.fignames = sample_data.fignames

        self.measurement_folder = '02_measurement_data\\'
        self.comsol_folder = '03_comsol_model\\'
        self.calib_folder = '04_calib_data\\'

    def load_dataset(self, sample):
        self.sample = sample
        sample_name = self.sample['sample_name'] + '\\'

        # Load sample in plotter:
        self.plotter.load_sample_into_plotter(self.sample)

        # Data input directories:
        sample_data_dir = self.data_input + sample_name + self.measurement_folder
        comsol_data_dir = self.data_input + sample_name + self.comsol_folder
        calib_data_dir = self.data_input + sample_name + self.calib_folder

        # Directory generator:
        directory_generator = DirectoryGenerator(self.sample_data, self.sample, self.data_output)
        directory_generator.small_test_directories()
        self.phase_directories = directory_generator.return_phase_directories()

        # Plot formatter
        self.styler_color = 'light'

        # Column names:
        columns = self.sample['columns']

        # Loading dataframes:
        self.df = pd.DataFrame()
        files = os.listdir(sample_data_dir)

        def f(x):
            return x[0] + ' ' + x[1]

        for index, file in enumerate(files):
            if file.endswith('csv'):
                filename, extension = os.path.splitext(file)
                # Separating filename to extract phase number
                keyword = 'phase'
                sample_name, keyword, phase_number = filename.partition(keyword)
                if len(phase_number) == 1:
                    # Normal case: phase consist of single file
                    df_loc = pd.read_csv(
                        sample_data_dir + file, skiprows=5, header=None, delim_whitespace=True)

                    df_loc[0] = df_loc.iloc[:, 0:2].apply(f, axis=1)
                    df_loc.drop(df_loc.columns[1], axis=1, inplace=True)
                    df_loc.index = df_loc[0]
                    df_loc.index = pd.to_datetime(df_loc.index)
                    df_loc.drop(df_loc.columns[0], axis=1, inplace=True)
                    self.df = pd.concat([self.df, df_loc])
                elif index == len(files) - 1:
                    # Phase consists of multiple files, but this is the very last file
                    df_loc = pd.read_csv(
                        sample_data_dir + file, skiprows=5, header=None, delim_whitespace=True)
                    df_loc[0] = df_loc.iloc[:, 0:2].apply(f, axis=1)
                    df_loc.drop(df_loc.columns[1], axis=1, inplace=True)
                    df_loc.index = df_loc[0]
                    df_loc.index = pd.to_datetime(df_loc.index)
                    df_loc.drop(df_loc.columns[0], axis=1, inplace=True)
                    self.df = pd.concat([self.df, df_loc])
                else:
                    # When multiple files, one of the phase files.
                    # Retrieving phase number for the next file:
                    filename_next, extension_next = os.path.splitext(files[index+1])
                    sample_name_next, keyword_next, phase_number_next = filename_next.partition(keyword)
                    if len(phase_number_next) == 1:
                        # This is the last file of the phase
                        df_loc = pd.read_csv(
                            sample_data_dir + file, skiprows=5, header=None, delim_whitespace=True)
                        df_loc[0] = df_loc.iloc[:, 0:2].apply(f, axis=1)
                        df_loc.drop(df_loc.columns[1], axis=1, inplace=True)
                        df_loc.index = df_loc[0]
                        df_loc.index = pd.to_datetime(df_loc.index)
                        df_loc.drop(df_loc.columns[0], axis=1, inplace=True)
                        self.df = pd.concat([self.df, df_loc])
                    else:
                        # This is not the last file of the phase (NaN line added)
                        df_loc = pd.read_csv(
                            sample_data_dir + file, skiprows=5, header=None, delim_whitespace=True)
                        df_loc[0] = df_loc.iloc[:, 0:2].apply(f, axis=1)
                        df_loc.drop(df_loc.columns[1], axis=1, inplace=True)
                        df_loc.index = df_loc[0]
                        df_loc.index = pd.to_datetime(df_loc.index)
                        df_loc.drop(df_loc.columns[0], axis=1, inplace=True)
                        last_index = pd.to_datetime(df_loc.index[-1])
                        df_loc = df_loc.append(pd.Series(name=last_index + pd.Timedelta(minutes=1)))
                        self.df = pd.concat([self.df, df_loc])
            else:
                pass

        self.df.columns = self.sample['columns']
        self.add_hours_column_to_df()
        self.add_cold_end_temp_column()
        self.add_hot_end_temp_column()

    def add_hours_column_to_df(self):
        start_time = self.df.index[0]

        def calc_hour_diff(time_point):
            diff = time_point - start_time
            return diff.days * 24 + diff.seconds / 3600

        self.df['hours'] = self.df.index.to_series().apply(calc_hour_diff)

    def add_cold_end_temp_column(self):
        self.df['cold_end'] = self.df[self.sample['cold_end_sensors']['sensors']].mean(axis=1)

    def add_hot_end_temp_column(self):
        self.df['hot_end'] = self.df[self.sample['hot_end_sensors']['sensors']].mean(axis=1)

    def con_SS_temperature_series(self, phases):
        if phases == 'master':
            dfs = [self.df]
            phase_dirs = self.phase_directories[0:1]
        else:
            dfs = self.dfs
            phase_dirs = self.phase_directories

        print('\n')
        print('Currently printing SS temperature series')

        for df, direc in zip(dfs, phase_dirs):
            # this iterates one or multiple times (master or phases)
            self.plotter.plot_SS_time_series(
                df=df,
                phase_directory=direc,
                folder=self.sample_data.folders['01_time_series_plots'],
                sizer=self.formatter.paper_full_width,
                styler=self.formatter.styler[self.styler_color])
            self.plotter.plot_SS_time_series(
                df=df,
                phase_directory=direc,
                folder=self.sample_data.folders['01_time_series_plots'],
                sizer=self.formatter.paper_full_width,
                styler=self.formatter.styler[self.styler_color],
                xaxis_type='datetime')

        print('Done')

    def con_SS_temperature_gradient(self, phases, xscale):
        if phases == 'master':
            dfs = [self.df]
            phase_dirs = self.phase_directories[0:1]
        else:
            dfs = self.dfs
            phase_dirs = self.phase_directories

        print('\n')
        print('Currently printing SS temperature gradient')

        for df, direc in zip(dfs, phase_dirs):
            self.plotter.plot_SS_temperature_gradient(df=df,
                                                      phase_directory=direc,
                                                      folder=self.sample_data.folders['02_temperature_gradient_plots'],
                                                      sizer=self.formatter.std_paper_1x1_partial_width,
                                                      styler=self.formatter.styler[self.styler_color],
                                                      xscale=xscale)

        print('Done')


class HydraulicTestControl:
    def __init__(self, sample_data, formatter):
        self.sample_data = sample_data
        self.formatter = formatter


class RetentionTestControl:
    def __init__(self, sample_data, formatter):
        self.sample_data = sample_data
        self.formatter = formatter


class ThermalTestControl:
    def __init__(self, sample_data, formatter):
        self.sample_data = sample_data
        self.formatter = formatter


class DrainageTestControl:
    def __init__(self, sample_data, formatter):
        self.sample_data = sample_data
        self.formatter = formatter


class GradationTestControl:
    def __init__(self, sample_data, formatter):
        self.sample_data = sample_data
        self.formatter = formatter





