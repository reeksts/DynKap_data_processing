import tkinter as tk
from tkinter import ttk
from app.StyleConfiguration import StyleConfiguration
from typing import List

from modules.FigureFormatting import FigureFormatting
from modules.DataProcessor import DataProcessor
from modules.DirectoryGenerator import DirectoryGenerator
from modules.PlotMeasurementFigures import PlotMeasurementFigures

from sample_data.SampleDataSmall import SampleDataSmall
from sample_data.SampleDataLarge import SampleDataLarge
from sample_data.SampleDataHydraulicConductivity import SampleDataHydraulicConductivity
from sample_data.SampleDataWaterRetention import SampleDataWaterRetention
from sample_data.SampleDataThermalConductivity import SampleDataThermalConductivity
from sample_data.SampleDataWaterDrainage import SampleDataWaterDrainage
from sample_data.SampleDataParticleGradation import SampleDataParticleGradation

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# new message


class MainApp(tk.Tk):
    def __init__(self):
        """
        # notation:
            # SN - refers to the large test
            # SS - refers to the small test

        # FRAME LAYOUT:
        # self.main_frame (top)
            # self.test_setup_plot_options_frame (top)
                # self.test_setup_sample_frame (left)
                    # self.test_setup_frame (top)
                    # self.sample_frame (top)
                # self.plot_options_frame (left)
            # self.plot_control_container_frame
                # self.LargeTestPlotControl (class frame, grid)
                    # SN_master_controller_frame (top)
                    # SN_combined_separate_plots_frame (top)
                        # SN_combined_plots_frame (left)
                        # SN_combined_plots_frame (left)
                    # SN_last_24h_plots_frame (top)
                # self.SmallTestPlotControl (class frame, grid)

        """

        super().__init__()
        self.title('Plot figures')

        # Sample data:
        self.large_test_data = SampleDataLarge()
        self.large_sample_names = [sample['sample_name'] for sample in self.large_test_data.samples]
        self.small_test_data = SampleDataSmall()
        self.small_sample_names = [sample['sample_name'] for sample in self.small_test_data.samples]
        self.hydraulic_sample_data = SampleDataHydraulicConductivity()
        self.hydraulic_samples = [sample['sample_name'] for sample in self.hydraulic_sample_data.samples]
        self.retention_sample_data = SampleDataWaterRetention()
        self.retention_samples = [sample['sample_name'] for sample in self.retention_sample_data.samples]
        self.thermal_sample_data = SampleDataThermalConductivity()
        self.thermal_samples = [sample['sample_name'] for sample in self.thermal_sample_data.samples]
        self.drainage_sample_data = SampleDataWaterDrainage()
        self.drainage_samples = [sample['sample_name'] for sample in self.drainage_sample_data.samples]
        self.gradation_sample_data = SampleDataParticleGradation()
        self.gradation_samples = [sample['sample_name'] for sample in self.gradation_sample_data.samples]

        # Initiating module objects:
        self.formatter = FigureFormatting()
        self.data_processor = DataProcessor(
            self.large_test_data,
            self.small_test_data)
        self.plotter = PlotMeasurementFigures()
        self.directory_generator = DirectoryGenerator()

        self.active_test = self.large_test_data

        # Place holders:
        self.df = None
        self.dfs = None

        # Adding main frame:
        self.main_frame = ttk.Frame(self, style='Standard.TFrame', padding=10)
        self.main_frame.grid(row=0, column=0)

        # Adding section frames:
        self.test_setup_plot_options_frame = ttk.Frame(self.main_frame, style='Standard.TFrame')
        self.test_setup_plot_options_frame.pack(side='top', fill='x')
        self.test_setup_sample_frame = ttk.Frame(self.test_setup_plot_options_frame, style='Standard.TFrame')
        self.test_setup_sample_frame.pack(side='left', fill='both')
        self.plot_options_frame = ttk.Frame(self.test_setup_plot_options_frame, style='Standard.TFrame')
        self.plot_options_frame.pack(side='left', fill='both', expand=True, padx=(10, 0))

        self.plot_control_container_frame = ttk.Frame(self.main_frame, style='Standard.TFrame')
        self.plot_control_container_frame.pack(side='top', fill='both', expand=True)           # check if fill='both' necessary
        self.plot_control_container_frame.rowconfigure(0, weight=1)
        self.plot_control_container_frame.columnconfigure(0, weight=1)
        self.frame_pages = dict()

        for page_class in [LargeTestPlotControl,
                           SmallTestPlotControl,
                           HydraulicConductivityPlotControl,
                           WaterRetentionPlotControl,
                           ThermalConductivityPlotControl,
                           WaterDrainagePlotControl,
                           ParticleGradationPlotControl]:
            page = page_class(self.plot_control_container_frame, self)
            self.frame_pages[page_class] = page
            page.grid(row=0, column=0, sticky='nsew')

        frame = self.frame_pages[LargeTestPlotControl]
        frame.tkraise()


        # Test setup section widgets:
        self.test_setup_frame = ttk.Frame(self.test_setup_sample_frame, style='Standard.TFrame')
        self.test_setup_frame.pack(side='top', fill='x')
        self.test_setup_label_frame = ttk.Frame(self.test_setup_frame, style='DarkFrame.TFrame')
        self.test_setup_label_frame.pack(side='top', fill='x')
        self.test_setup_label = ttk.Label(
            self.test_setup_label_frame,
            text='Test setup:',
            style='ExtraLargeLabel.TLabel',
        )
        self.test_setup_label.pack(side='left', padx=(10, 0), pady=(5, 5))

        self.test_type_var = tk.StringVar(value='large')
        self.large_test_radiobutton_frame = ttk.Frame(self.test_setup_frame, style='Standard.TFrame')
        self.large_test_radiobutton_frame.pack(side='top', fill='x')
        self.large_test_radiobutton = ttk.Radiobutton(
            self.large_test_radiobutton_frame,
            style='Standard.TRadiobutton',
            value='large',
            variable=self.test_type_var,
            takefocus=False,
            command=self.switch_frames,
        )
        self.large_test_radiobutton.pack(side='left', pady=(10, 0), padx=(20, 0))
        self.large_test_radiobutton_text = ttk.Label(
            self.large_test_radiobutton_frame,
            style='LeftAligned.TLabel',
            text='Large moisture transfer test',
        )
        self.large_test_radiobutton_text.pack(side='left', padx=(5, 5), pady=(10, 0))

        self.small_test_radiobutton_frame = ttk.Frame(self.test_setup_frame, style='Standard.TFrame')
        self.small_test_radiobutton_frame.pack(side='top', fill='x')
        self.small_test_radiobutton = ttk.Radiobutton(
            self.small_test_radiobutton_frame,
            style='Standard.TRadiobutton',
            value='small',
            variable=self.test_type_var,
            takefocus=False,
            command=self.switch_frames,
        )
        self.small_test_radiobutton.pack(side='left', pady=(10, 0), padx=(20, 0))
        self.small_test_radiobutton_text = ttk.Label(
            self.small_test_radiobutton_frame,
            style='LeftAligned.TLabel',
            text='Small moisture transfer test',
        )
        self.small_test_radiobutton_text.pack(side='left', padx=(5, 5), pady=(10, 0))

        self.hydraulic_test_radiobutton_frame = ttk.Frame(self.test_setup_frame, style='Standard.TFrame')
        self.hydraulic_test_radiobutton_frame.pack(side='top', fill='x')
        self.hydraulic_test_radiobutton = ttk.Radiobutton(
            self.hydraulic_test_radiobutton_frame,
            style='Standard.TRadiobutton',
            value='hydraulic',
            variable=self.test_type_var,
            takefocus=False,
            command=self.switch_frames,
        )
        self.hydraulic_test_radiobutton.pack(side='left', pady=(10, 0), padx=(20, 0))
        self.hydraulic_test_radiobutton_text = ttk.Label(
            self.hydraulic_test_radiobutton_frame,
            style='LeftAligned.TLabel',
            text='Hydraulic conductivity test',
        )
        self.hydraulic_test_radiobutton_text.pack(side='left', padx=(5, 5), pady=(10, 0))

        self.retention_test_radiobutton_frame = ttk.Frame(self.test_setup_frame, style='Standard.TFrame')
        self.retention_test_radiobutton_frame.pack(side='top', fill='x')
        self.retention_test_radiobutton = ttk.Radiobutton(
            self.retention_test_radiobutton_frame,
            style='Standard.TRadiobutton',
            value='retention',
            variable=self.test_type_var,
            takefocus=False,
            command=self.switch_frames,
        )
        self.retention_test_radiobutton.pack(side='left', pady=(10, 0), padx=(20, 0))
        self.retention_test_radiobutton_text = ttk.Label(
            self.retention_test_radiobutton_frame,
            style='LeftAligned.TLabel',
            text='Water retention test',
        )
        self.retention_test_radiobutton_text.pack(side='left', padx=(5, 5), pady=(10, 0))

        self.thermal_test_radiobutton_frame = ttk.Frame(self.test_setup_frame, style='Standard.TFrame')
        self.thermal_test_radiobutton_frame.pack(side='top', fill='x')
        self.thermal_test_radiobutton = ttk.Radiobutton(
            self.thermal_test_radiobutton_frame,
            style='Standard.TRadiobutton',
            value='thermal',
            variable=self.test_type_var,
            takefocus=False,
            command=self.switch_frames,
        )
        self.thermal_test_radiobutton.pack(side='left', pady=(10, 0), padx=(20, 0))
        self.thermal_test_radiobutton_text = ttk.Label(
            self.thermal_test_radiobutton_frame,
            style='LeftAligned.TLabel',
            text='Thermal conductivity test',
        )
        self.thermal_test_radiobutton_text.pack(side='left', padx=(5, 5), pady=(10, 0))

        self.drainage_test_radiobutton_frame = ttk.Frame(self.test_setup_frame, style='Standard.TFrame')
        self.drainage_test_radiobutton_frame.pack(side='top', fill='x')
        self.drainage_test_radiobutton = ttk.Radiobutton(
            self.drainage_test_radiobutton_frame,
            style='Standard.TRadiobutton',
            value='drainage',
            variable=self.test_type_var,
            takefocus=False,
            command=self.switch_frames,
        )
        self.drainage_test_radiobutton.pack(side='left', pady=(10, 0), padx=(20, 0))
        self.drainage_test_radiobutton_text = ttk.Label(
            self.drainage_test_radiobutton_frame,
            style='LeftAligned.TLabel',
            text='Water drainage test',
        )
        self.drainage_test_radiobutton_text.pack(side='left', padx=(5, 5), pady=(10, 0))

        self.gradation_test_radiobutton_frame = ttk.Frame(self.test_setup_frame, style='Standard.TFrame')
        self.gradation_test_radiobutton_frame.pack(side='top', fill='x')
        self.gradation_test_radiobutton = ttk.Radiobutton(
            self.gradation_test_radiobutton_frame,
            style='Standard.TRadiobutton',
            value='gradation',
            variable=self.test_type_var,
            takefocus=False,
            command=self.switch_frames,
        )
        self.gradation_test_radiobutton.pack(side='left', pady=(10, 0), padx=(20, 0))
        self.gradation_test_radiobutton_text = ttk.Label(
            self.gradation_test_radiobutton_frame,
            style='LeftAligned.TLabel',
            text='Particle gradation test',
        )
        self.gradation_test_radiobutton_text.pack(side='left', padx=(5, 5), pady=(10, 0))

        self.sample_frame = ttk.Frame(self.test_setup_sample_frame, style='Standard.TFrame')
        self.sample_frame.pack(side='top', fill='x', pady=(20, 0))
        self.sample_label_frame = ttk.Frame(self.sample_frame, style='DarkFrame.TFrame')
        self.sample_label_frame.pack(side='top', fill='x')
        self.samples_label = ttk.Label(
            self.sample_label_frame,
            text='Samples:',
            style='ExtraLargeLabel.TLabel',
        )
        self.samples_label.pack(side='left', padx=(10, 0), pady=(5, 5))
        self.samples_combobox = ttk.Combobox(
            self.sample_frame,
            style='Standard.TCombobox',
            values=self.large_sample_names,
            state='readonly',
        )
        self.samples_combobox.current(len(self.active_test.samples)-1)
        self.samples_combobox.pack(side='top', fill='x', padx=(10, 10), pady=(10, 0))

        # Plot options section widgets:
        self.plot_options_label_frame = ttk.Frame(self.plot_options_frame, style='DarkFrame.TFrame')
        self.plot_options_label_frame.pack(side='top', fill='x')
        self.plot_options_label = ttk.Label(
            self.plot_options_label_frame,
            style='ExtraLargeLabel.TLabel',
            text='Options:',
        )
        self.plot_options_label.pack(side='left', padx=(10, 0), pady=(5, 5))

        self.file_update_option_frame = ttk.Frame(self.plot_options_frame, style='Standard.TFrame')
        self.file_update_option_frame.pack(side='top', fill='x', padx=(20, 10))
        self.file_update_label = ttk.Label(
            self.file_update_option_frame,
            style='LeftAligned.TLabel',
            text='Update files:',
        )
        self.file_update_label.pack(side='left', padx=(5, 0), pady=(10, 0))
        self.file_update_button = ttk.Button(
            self.file_update_option_frame,
            style='Standard.TButton',
            text='update',
            width=6,
            takefocus=False,
            command=self.update_files,
        )
        self.file_update_button.pack(side='left', padx=(10, 0), pady=(10, 0))
        self.update_dfs_var = tk.IntVar()
        self.file_update_checkbox = ttk.Checkbutton(
            self.file_update_option_frame,
            style='Standard.TCheckbutton',
            variable=self.update_dfs_var)
        self.file_update_checkbox.pack(side='left', padx=(10, 0), pady=(10, 0))

        self.comsol_option_frame = ttk.Frame(self.plot_options_frame, style='Standard.TFrame')
        self.comsol_option_frame.pack(side='top', fill='x', padx=(20, 10))
        self.comsol_option_checkbox = ttk.Checkbutton(self.comsol_option_frame, style='Standard.TCheckbutton')
        self.comsol_option_checkbox.pack(side='left', padx=(5, 0), pady=(10, 0))
        self.comsol_option_text = ttk.Label(
            self.comsol_option_frame,
            style='LeftAligned.TLabel',
            text='Comsol model',
        )
        self.comsol_option_text.pack(side='left', padx=(5, 0), pady=(10, 0))

        self.power_line_option_frame = ttk.Frame(self.plot_options_frame, style='Standard.TFrame')
        self.power_line_option_frame.pack(side='top', fill='x', padx=(20, 10))
        self.power_line_option_checkbox = ttk.Checkbutton(self.power_line_option_frame, style='Standard.TCheckbutton')
        self.power_line_option_checkbox.pack(side='left', padx=(5, 0), pady=(10, 0))
        self.power_line_option_text = ttk.Label(
            self.power_line_option_frame,
            style='LeftAligned.TLabel',
            text='Power line',
        )
        self.power_line_option_text.pack(side='left', padx=(5, 0), pady=(10, 0))

        self.xscale_option_frame = ttk.Frame(self.plot_options_frame, style='Standard.TFrame')
        self.xscale_option_frame.pack(side='top', fill='x', padx=(20, 10))
        self.xscale_text_option = ttk.Label(
            self.xscale_option_frame,
            style='LeftAligned.TLabel',
            text='xscale:',
        )
        self.xscale_text_option.grid(row=0, column=0, padx=(5, 0), pady=(10, 0))
        self.xscale_var = tk.StringVar(value='linear')
        self.log_radiobutton = ttk.Radiobutton(
            self.xscale_option_frame,
            style='Standard.TRadiobutton',
            value='log',
            variable=self.xscale_var,
            takefocus=False
        )
        self.log_radiobutton.grid(row=0, column=1, padx=(5, 0), pady=(10, 0))
        self.log_text = ttk.Label(
            self.xscale_option_frame,
            style='LeftAligned.TLabel',
            text='log'
        )
        self.log_text.grid(row=0, column=2, sticky='W', padx=(5, 0), pady=(10, 0))
        self.linear_radiobutton = ttk.Radiobutton(
            self.xscale_option_frame,
            style='Standard.TRadiobutton',
            value='linear',
            variable=self.xscale_var,
            takefocus=False
        )
        self.linear_radiobutton.grid(row=1, column=1, sticky='W', padx=(5, 0), pady=(5, 0))
        self.linear_text = ttk.Label(
            self.xscale_option_frame,
            style='LeftAligned.TLabel',
            text='linear'
        )
        self.linear_text.grid(row=1, column=2, padx=(5, 0), pady=(5, 0))

        self.output_style_frame = ttk.Frame(self.plot_options_frame, style='Standard.TFrame')
        self.output_style_frame.pack(side='top', fill='x', padx=(20, 10))
        self.output_style_text = ttk.Label(
            self.output_style_frame,
            style='LeftAligned.TLabel',
            text='output style:'
        )
        self.output_style_text.grid(row=0, column=0, padx=(5, 0), pady=(10, 0))
        self.sizer_var = tk.StringVar(value='paper')
        self.paper_radiobutton = ttk.Radiobutton(
            self.output_style_frame,
            style='Standard.TRadiobutton',
            value='paper',
            variable=self.sizer_var,
            takefocus=False
        )
        self.paper_radiobutton.grid(row=0, column=1, padx=(5, 0), pady=(10, 0))
        self.paper_text = ttk.Label(
            self.output_style_frame,
            style='LeftAligned.TLabel',
            text='paper'
        )
        self.paper_text.grid(row=0, column=2, sticky='W', padx=(5, 0), pady=(10, 0))
        self.presentation_radiobutton = ttk.Radiobutton(
            self.output_style_frame,
            style='Standard.TRadiobutton',
            value='presentation',
            variable=self.sizer_var,
            takefocus=False
        )
        self.presentation_radiobutton.grid(row=1, column=1, sticky='W', padx=(5, 0), pady=(5, 0))
        self.presentation_text = ttk.Label(
            self.output_style_frame,
            style='LeftAligned.TLabel',
            text='presentation'
        )
        self.presentation_text.grid(row=1, column=2, padx=(5, 0), pady=(5, 0))

        self.data_density_frame = ttk.Frame(self.plot_options_frame, style='Standard.TFrame')
        self.data_density_frame.pack(side='top', fill='x', padx=(20, 10))
        self.data_density_text = ttk.Label(
            self.data_density_frame,
            style='LeftAligned.TLabel',
            text='data density:'
        )
        self.data_density_text.grid(row=0, column=0, padx=(5, 0), pady=(10, 0))
        self.data_density_var = tk.StringVar(value='1minute')
        self.one_minute_radiobutton = ttk.Radiobutton(
            self.data_density_frame,
            style='Standard.TRadiobutton',
            value='1minute',
            variable=self.data_density_var,
            takefocus=False
        )
        self.one_minute_radiobutton.grid(row=0, column=1, padx=(5, 0), pady=(10, 0))
        self.one_minute_text = ttk.Label(
            self.data_density_frame,
            style='LeftAligned.TLabel',
            text='measured (1 min)'
        )
        self.one_minute_text.grid(row=0, column=2, sticky='W', padx=(5, 0), pady=(10, 0))
        self.six_minute_radiobutton = ttk.Radiobutton(
            self.data_density_frame,
            style='Standard.TRadiobutton',
            value='6minute',
            variable=self.data_density_var,
            takefocus=False
        )
        self.six_minute_radiobutton.grid(row=1, column=1, padx=(5, 0), pady=(10, 0))
        self.six_minute_text = ttk.Label(
            self.data_density_frame,
            style='LeftAligned.TLabel',
            text='6-min averaged'
        )
        self.six_minute_text.grid(row=1, column=2, sticky='W', padx=(5, 0), pady=(10, 0))
        self.ten_minute_radiobutton = ttk.Radiobutton(
            self.data_density_frame,
            style='Standard.TRadiobutton',
            value='10minute',
            variable=self.data_density_var,
            takefocus=False
        )
        self.ten_minute_radiobutton.grid(row=2, column=1, padx=(5, 0), pady=(10, 0))
        self.ten_minute_text = ttk.Label(
            self.data_density_frame,
            style='LeftAligned.TLabel',
            text='10-min averaged'
        )
        self.ten_minute_text.grid(row=2, column=2, sticky='W', padx=(5, 0), pady=(10, 0))

    def switch_frames(self):
        if self.test_type_var.get() == 'large':
            self.active_test = self.large_test_data
            self.samples_combobox['values'] = self.large_sample_names
            self.samples_combobox.current(len(self.active_test.samples)-1)
            frame = self.frame_pages[LargeTestPlotControl]
            frame.tkraise()
        elif self.test_type_var.get() == 'small':
            self.active_test = self.small_test_data
            self.samples_combobox['values'] = self.small_sample_names
            self.samples_combobox.current(len(self.active_test.samples)-1)
            frame = self.frame_pages[SmallTestPlotControl]
            frame.tkraise()
        elif self.test_type_var.get() == 'hydraulic':
            self.active_test = self.hydraulic_sample_data
            self.samples_combobox['values'] = self.hydraulic_samples
            self.samples_combobox.current(0)
            frame = self.frame_pages[HydraulicConductivityPlotControl]
            frame.tkraise()
        elif self.test_type_var.get() == 'retention':
            self.active_test = self.retention_sample_data
            self.samples_combobox['values'] = self.retention_samples
            self.samples_combobox.current(0)
            frame = self.frame_pages[WaterRetentionPlotControl]
            frame.tkraise()
        elif self.test_type_var.get() == 'thermal':
            self.active_test = self.thermal_sample_data
            self.samples_combobox['values'] = self.thermal_samples
            self.samples_combobox.current(0)
            frame = self.frame_pages[ThermalConductivityPlotControl]
            frame.tkraise()
        elif self.test_type_var.get() == 'drainage':
            self.active_test = self.drainage_sample_data
            self.samples_combobox['values'] = self.drainage_samples
            self.samples_combobox.current(0)
            frame = self.frame_pages[WaterDrainagePlotControl]
            frame.tkraise()
        elif self.test_type_var.get() == 'gradation':
            self.active_test = self.gradation_sample_data
            self.samples_combobox['values'] = self.gradation_samples
            self.samples_combobox.current(0)
            frame = self.frame_pages[ParticleGradationPlotControl]
            frame.tkraise()

    def update_files(self):
        # Before updating, make sure that all samples have their folders generated.
        for test_data in [self.large_test_data, self.small_test_data]:
            for sample in test_data.samples:
                self.directory_generator.directory_generator(test_data, sample)

        # Get value form update override checkbox:
        if self.update_dfs_var.get() == 1:
            override_dfs = True
        else:
            override_dfs = False

        # Update data (pull data from OneDrive)
        self.data_processor.update_data()

        # Update dfs: executed only for sample with new data (tho teh check for data is done on all samples)
        self.data_processor.generate_corrected_dfs(override_dfs=override_dfs)

    def preprocessing_before_plotting(self, active_sample, phases):
        # Directory generator:
        phase_directories = self.directory_generator.directory_generator(self.active_test, active_sample)

        # Loading corrected dataframe:
        self.df = self.data_processor.load_corrected_df(active_sample, self.active_test)

        # Get phase datetimes:
        phase_datetimes = self.data_processor.generate_df(active_sample, self.active_test, return_phases_times=True)

        if phases == 'master':
            dfs = [self.df]
            phase_dirs = phase_directories[0:1]
        else:
            self.dfs = self.data_processor.generate_phase_dfs(active_sample, self.active_test, self.df)
            dfs = self.dfs
            phase_dirs = phase_directories

        # Loading sample into plotter for preprocessing
        self.plotter.load_sample_into_plotter(self.active_test, active_sample, phase_datetimes)

        # Getting sizer and styler values:
        sizer_val = self.sizer_var.get()
        if self.sizer_var.get() == 'paper':
            styler_val = 'light'
        else:
            styler_val = 'dark'

        return dfs, phase_dirs, sizer_val, styler_val

    # Master plot function calls:
    def app_SN_plot_all_active_sample(self, sample_list: List, phases):
        """
        Plots all figures for selected sample.
        User inputs for this function:
            - comsol model (for gradient plots)
            - power line (for series plots)
            - xscale (for gradient plots)
            - output style

        :param sample_list: list of samples to be ploted. This function can execute a single active sample as
                            [sample] or all samples as [sample1, smaple2, sample3, ..]
        :param phases:
        """

        for sample in sample_list:
            sample_name = sample['sample_name']
            print(f'processing: {sample_name}')
            dfs, phase_dirs, sizer_val, styler_val = self.preprocessing_before_plotting(sample, phases=phases)

            self.app_SN_combined_master(dfs, phase_dirs, sizer_val, styler_val)
            self.app_SN_combined_temperature_series(dfs, phase_dirs, sizer_val, styler_val)
            self.app_SN_combined_temperature_gradient(dfs, phase_dirs, sizer_val, styler_val)
            self.app_SN_combined_moisture_series(dfs, phase_dirs, sizer_val, styler_val)
            self.app_SN_combined_moisture_gradient(dfs, phase_dirs, sizer_val, styler_val)
            self.app_SN_combined_series_moist_vs_temp(dfs, phase_dirs, sizer_val, styler_val)
            self.app_SN_separate_temperature_series(dfs, phase_dirs, sizer_val, styler_val)
            self.app_SN_separate_temperature_gradient(dfs, phase_dirs, sizer_val, styler_val)
            self.app_SN_separate_moisture_series(dfs, phase_dirs, sizer_val, styler_val)
            self.app_SN_separate_moisture_gradient(dfs, phase_dirs, sizer_val, styler_val)
            self.app_SN_separate_series_moist_vs_temp(dfs, phase_dirs, sizer_val, styler_val)
            self.app_SN_last_24h_plots(dfs, phase_dirs, sizer_val, styler_val)
            self.app_SN_hot_end_temperature(dfs, phase_dirs, sizer_val, styler_val)

    def app_SN_plot_all_active_test(self):
        active_test_samples = self.active_test.samples
        self.app_SN_plot_all_active_sample(active_test_samples, phases='phases')

    def app_SN_SS_plot_all_both_tests(self):
        if self.active_test is self.large_test_data:
            self.app_SN_plot_all_active_test()
            self.active_test = self.small_test_data
            self.app_SS_plot_all_active_test()
            self.active_test = self.large_test_data
        else:
            self.active_test = self.large_test_data
            self.app_SN_plot_all_active_test()
            self.active_test = self.small_test_data
            self.app_SS_plot_all_active_test()

    # Combined plot calls:
    def app_SN_combined_master(self, dfs, phase_dirs, sizer_val, styler_val):     # need to implement other options
        """
        Plots the 4x3 figure:
        User inputs for this function:
            - comsol model (for gradient plots)     NOT IMPLEMENTED!
            - power line (for series plots)         NOT IMPLEMENTED!
            - xscale (for gradient plots)
            - sizer
        """

        print('Currently plotting con_SN_combined_master')

        for df, direc in zip(dfs, phase_dirs):
            self.plotter.plot_SN_combined_master(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['01_combined_plots'],
                sizer=self.formatter.sizer[sizer_val]['4x3_full_width'],
                styler=self.formatter.styler[styler_val],
                xscale=self.xscale_var.get()
            )

        print('Done\n')

    def app_SN_combined_temperature_series(self, dfs, phase_dirs, sizer_val, styler_val):      # need to implement other options
        """
        Plots combined (3x1) temperature series figure (with hours and datetime).
        User inputs for this function:
            - power line        NOT IMPLEMENTED!
        """

        print('Currently plotting plot_SN_combined_temperature_series')

        for df, direc in zip(dfs, phase_dirs):
            # this iterates one or multiple times
            self.plotter.plot_SN_combined_temperature_series(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['01_combined_plots'],
                sizer=self.formatter.sizer[sizer_val]['3x1_full_width'],
                styler=self.formatter.styler[styler_val]
            )
            self.plotter.plot_SN_combined_temperature_series(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['01_combined_plots'],
                sizer=self.formatter.sizer[sizer_val]['3x1_full_width'],
                styler=self.formatter.styler[styler_val],
                xaxis_type='datetime'
            )

        print('Done\n')

    def app_SN_combined_temperature_gradient(self, dfs, phase_dirs, sizer_val, styler_val):        # need to implement other options
        """
        Plots combined (3x1) temperature gradient figure.
        User inputs for this function:
            - comsol model      NOT IMPLEMENTED!
            - xscale
        """

        print('Currently plotting plot_SN_combined_temperature_gradient')

        for df, direc in zip(dfs, phase_dirs):
            # this iterates one or multiple times
            self.plotter.plot_SN_combined_temperature_gradient(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['01_combined_plots'],
                sizer=self.formatter.sizer[sizer_val]['3x1_partial_width'],
                styler=self.formatter.styler[styler_val],
                xscale=self.xscale_var.get()
            )

        print('Done\n')

    def app_SN_combined_moisture_series(self, dfs, phase_dirs, sizer_val, styler_val):
        """
        Plots combined (3x1) moisture series gradient figure.
        User inputs for this function:
            - power line        NOT IMPLEMENTED!
            - output style      NOT IMPLEMENTED!
        """

        print('Currently plotting plot_SN_combined_moisture_series')

        for df, direc in zip(dfs, phase_dirs):
            # this iterates one or multiple times
            self.plotter.plot_SN_combined_moisture_series(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['01_combined_plots'],
                sizer=self.formatter.sizer[sizer_val]['3x1_full_width'],
                styler=self.formatter.styler[styler_val]
            )
            self.plotter.plot_SN_combined_moisture_series(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['01_combined_plots'],
                sizer=self.formatter.sizer[sizer_val]['3x1_full_width'],
                styler=self.formatter.styler[styler_val],
                xaxis_type='datetime'
            )

        print('Done\n')

    def app_SN_combined_moisture_gradient(self, dfs, phase_dirs, sizer_val, styler_val):
        """
        Plots combined (3x1) moisture gradient figure.
        User inputs for this function:
            - comsol model      NOT IMPLEMENTED!
            - xscale
            - output style      NOT IMPLEMENTED!
        """

        print('Currently plotting plot_SN_combined_moisture_gradients')

        for df, direc in zip(dfs, phase_dirs):
            self.plotter.plot_SN_combined_moisture_gradients(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['01_combined_plots'],
                sizer=self.formatter.sizer[sizer_val]['3x1_partial_width'],
                styler=self.formatter.styler[styler_val],
                xscale=self.xscale_var.get()
            )

        print('Done\n')

    def app_SN_combined_series_moist_vs_temp(self, dfs, phase_dirs, sizer_val, styler_val):
        """
        Plots combined (3x1) moisture vs temperature series.
        User inputs for this function:
            - output style      NOT IMPLEMENTED!
        """

        print('Currently plotting plot_SN_combined_series_moist_vs_temp')

        for df, direc in zip(dfs, phase_dirs):
            # this iterates one or multiple times
            self.plotter.plot_SN_combined_series_moist_vs_temp(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['08_time_series_moisture_vs_temperature'],
                sizer=self.formatter.sizer[sizer_val]['3x1_full_width'],
                styler=self.formatter.styler[styler_val],
            )
            self.plotter.plot_SN_combined_series_moist_vs_temp(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['08_time_series_moisture_vs_temperature'],
                sizer=self.formatter.sizer[sizer_val]['3x1_full_width'],
                styler=self.formatter.styler[styler_val],
                xaxis_type='datetime',
            )
            self.plotter.plot_SN_combined_series_moist_vs_temp(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['08_time_series_moisture_vs_temperature'],
                sizer=self.formatter.sizer[sizer_val]['3x1_full_width'],
                styler=self.formatter.styler[styler_val],
                normalized=True,
            )

        print('Done\n')

    # Separate plot function calls:
    def app_SN_separate_temperature_series(self, dfs, phase_dirs, sizer_val, styler_val):
        """
        Plots separate figures for every direction for temperature series.
        User input for this function:
            - power line        NOT IMPLEMENTED!
            - output style      NOT IMPLEMENTED!
        """

        print('Currently plotting plot_SN_separate_temperature_series')

        for df, direc in zip(dfs, phase_dirs):
            self.plotter.plot_SN_separate_temperature_series(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['02_time_series_temperature'],
                sizer=self.formatter.sizer[sizer_val]['1x1_full_width'],
                styler=self.formatter.styler[styler_val]
            )
            self.plotter.plot_SN_separate_temperature_series(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['02_time_series_temperature'],
                sizer=self.formatter.sizer[sizer_val]['1x1_full_width'],
                styler=self.formatter.styler[styler_val],
                xaxis_type='datetime'
            )

        print('Done\n')

    def app_SN_separate_temperature_gradient(self, dfs, phase_dirs, sizer_val, styler_val):
        """
        Plots separate figures for every direction for temperature gradient.
        User input for this function:
            - comsol model      NOT IMPLEMENTED!
            - xscale
            - output style      NOT IMPLEMENTED!
        """

        print('Currently plotting con_SN_separate_temperature_gradient')

        for df, direc in zip(dfs, phase_dirs):
            self.plotter.plot_SN_separate_temperature_gradient(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['04_gradient_temperature'],
                sizer=self.formatter.sizer[sizer_val]['1x1_partial_width'],
                styler=self.formatter.styler[styler_val],
                xscale=self.xscale_var.get()
            )

        print('Done\n')

    def app_SN_separate_moisture_series(self, dfs, phase_dirs, sizer_val, styler_val):
        """
        Plots separate figures for every direction for moisture series.
        User input for this function:
            - power line        NOT IMPLEMENTED!
        """

        print('Currently printing plot_SN_separate_moisture_series')

        for df, direc in zip(dfs, phase_dirs):
            self.plotter.plot_SN_separate_moisture_series(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['03_time_series_moisture'],
                sizer=self.formatter.sizer[sizer_val]['1x1_full_width'],
                styler=self.formatter.styler[styler_val]
            )
            self.plotter.plot_SN_separate_moisture_series(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['03_time_series_moisture'],
                sizer=self.formatter.sizer[sizer_val]['1x1_full_width'],
                styler=self.formatter.styler[styler_val],
                xaxis_type='datetime'
            )

        print('Done\n')

    def app_SN_separate_moisture_gradient(self, dfs, phase_dirs, sizer_val, styler_val):
        """
        Plots separate figures for every direction for moisture gradient.
        User input for this function:
            - comsol model      NOT IMPLEMENTED!
            - xscale
            - output style      NOT IMPLEMENTED!
        """

        print('Currently plotting plot_SN_separate_moisture_gradient')

        for df, direc in zip(dfs, phase_dirs):
            # this iterates one or multiple times
            self.plotter.plot_SN_separate_moisture_gradient(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['05_gradient_moisture'],
                sizer=self.formatter.sizer[sizer_val]['1x1_partial_width'],
                styler=self.formatter.styler[styler_val],
                xscale=self.xscale_var.get()
            )

        print('Done\n')

    def app_SN_separate_series_moist_vs_temp(self, dfs, phase_dirs, sizer_val, styler_val):
        """
        :param dfs:
        :param phase_dirs:
        :param sizer_val:
        :param styler_val:
        :return:
        """

        print('Currently plotting app_SN_separate_series_moist_vs_temp')

        for df, direc in zip(dfs, phase_dirs):
            # this iterates one or multiple times
            self.plotter.plot_SN_separate_series_moist_vs_temp(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['08_time_series_moisture_vs_temperature'],
                sizer=self.formatter.sizer[sizer_val]['1x1_full_width'],
                styler=self.formatter.styler[styler_val],
                normalized=True,
            )

        print('Done\n')

    # Animated plot calls:
    def app_SN_animated_gradient_plot(self):
        """
        Plots animated temperature and moisture gradient.
        """
        print('this option is yet to be implemented')

    def app_SN_animated_series_plot(self):
        """
         Plots animated temperature and moisture series.
        """
        print('this option is yet to be implemented')

    # Short period plot calls:
    def app_SN_last_24h_plots(self, dfs, phase_dirs, sizer_val, styler_val):
        """
        Plots figures for the last 24h our period.
        This produces separate and combined plots for temperature and moisture series.
        User input for this function:
            - power line        NOT IMPLEMENTED!
        """

        print('Currently plotting con_last_24h_plots')

        for df, direc in zip(dfs, phase_dirs):
            df = self.data_processor.create_24h_subset(df)
            self.plotter.plot_SN_separate_temperature_series(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['06_last_24_hours'],
                sizer=self.formatter.sizer[sizer_val]['1x1_full_width'],
                styler=self.formatter.styler[styler_val],
                xaxis_type='datetime',
                last_day=True
            )
            self.plotter.plot_SN_separate_moisture_series(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['06_last_24_hours'],
                sizer=self.formatter.sizer[sizer_val]['1x1_full_width'],
                styler=self.formatter.styler[styler_val],
                xaxis_type='datetime',
                last_day=True
            )
            self.plotter.plot_SN_combined_temperature_series(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['06_last_24_hours'],
                sizer=self.formatter.sizer[sizer_val]['3x1_full_width'],
                styler=self.formatter.styler[styler_val],
                xaxis_type='datetime',
                last_day=True,
            )
            self.plotter.plot_SN_combined_moisture_series(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['06_last_24_hours'],
                sizer=self.formatter.sizer[sizer_val]['3x1_full_width'],
                styler=self.formatter.styler[styler_val],
                xaxis_type='datetime',
                last_day=True,
            )

        print('Done\n')

    def app_SN_hot_end_temperature(self, dfs, phase_dirs, sizer_val, styler_val):
        """
        Plots figures for the last 24h our period.
        This produces separate and combined plots for temperature and moisture series.
        User input for this function:
            - power line        NOT IMPLEMENTED!
        """

        print('Currently plotting con_SN_hot_end_temperature')

        for df, direc in zip(dfs, phase_dirs):
            df = self.data_processor.create_10perc_subset(df)
            self.plotter.plot_SN_hot_end_temperature(
                df=df,
                phase_directory=direc,
                folder=self.large_test_data.folders['09_tracking_individual_sensors'],
                sizer=self.formatter.sizer[sizer_val]['1x1_full_width'],
                styler=self.formatter.styler[styler_val]
            )

        print('Done\n')

    # Small moisture cell plot functions:
    def app_SS_plot_all_active_sample(self, sample_list: List, phases):

        for sample in sample_list:
            sample_name = sample['sample_name']
            print(f'processing: {sample_name}')
            dfs, phase_dirs, sizer_val, styler_val = self.preprocessing_before_plotting(sample, phases=phases)

            self.app_SS_temperature_series(dfs, phase_dirs, sizer_val, styler_val)
            self.app_SS_temperature_gradient(dfs, phase_dirs, sizer_val, styler_val)

    def app_SS_plot_all_active_test(self):
        active_test_samples = self.active_test.samples
        self.app_SS_plot_all_active_sample(active_test_samples, phases='phases')

    def app_SS_temperature_series(self, dfs, phase_dirs, sizer_val, styler_val):

        print('Currently printing plot_SS_time_series')

        for df, direc in zip(dfs, phase_dirs):
            # this iterates one or multiple times (master or phases)
            self.plotter.plot_SS_time_series(
                df=df,
                phase_directory=direc,
                folder=self.small_test_data.folders['01_time_series_plots'],
                sizer=self.formatter.sizer[sizer_val]['1x1_full_width'],
                styler=self.formatter.styler[styler_val]
            )
            self.plotter.plot_SS_time_series(
                df=df,
                phase_directory=direc,
                folder=self.small_test_data.folders['01_time_series_plots'],
                sizer=self.formatter.sizer[sizer_val]['1x1_full_width'],
                styler=self.formatter.styler[styler_val],
                xaxis_type='datetime'
            )

        print('Done\n')

    def app_SS_temperature_gradient(self, dfs, phase_dirs, sizer_val, styler_val):

        print('Currently printing plot_SS_temperature_gradient')

        for df, direc in zip(dfs, phase_dirs):
            self.plotter.plot_SS_temperature_gradient(
                df=df,
                phase_directory=direc,
                folder=self.small_test_data.folders['02_temperature_gradient_plots'],
                sizer=self.formatter.sizer[sizer_val]['1x1_partial_width'],
                styler=self.formatter.styler[styler_val],
                xscale=self.xscale_var.get()
            )

        print('Done\n')

    def SS_animated_temperature_series(self):
        print('button 17')

    def SS_animated_temperature_gradient(self):
        print('button 18')

    def retrieve_active_sample(self):
        selected_sample = self.samples_combobox.get()
        for sample in self.active_test.samples:
            if selected_sample == sample['sample_name']:
                return [sample]


class LargeTestPlotControl(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style='Standard.TFrame')
        self.parent = parent
        self.controller = controller

        # Large test section subframes:
        self.SN_master_controller_frame = ttk.Frame(self, style='Standard.TFrame')
        self.SN_master_controller_frame.pack(side='top', fill='x', pady=(20, 0))
        self.SN_master_controller_frame.grid_columnconfigure(0, weight=1)
        self.SN_master_controller_frame.grid_columnconfigure(1, weight=1)
        self.SN_master_controller_frame.grid_columnconfigure(2, weight=1)
        self.SN_master_controller_frame.grid_columnconfigure(3, weight=1)
        self.SN_combined_separate_plots_frame = ttk.Frame(self, style='Standard.TFrame')
        self.SN_combined_separate_plots_frame.pack(side='top', fill='x', pady=(20, 0))
        self.SN_combined_plots_frame = ttk.Frame(self.SN_combined_separate_plots_frame, style='Standard.TFrame')
        self.SN_combined_plots_frame.pack(side='left', fill='y')
        self.SN_combined_plots_frame.grid_columnconfigure(1, weight=1)
        self.SN_separate_plots_frame = ttk.Frame(self.SN_combined_separate_plots_frame, style='Standard.TFrame')
        self.SN_separate_plots_frame.pack(side='left', fill='both', expand=True, padx=(10, 0))
        self.SN_separate_plots_frame.grid_columnconfigure(1, weight=1)
        self.SN_animated_last_24h_plots_frame = ttk.Frame(self, style='Standard.TFrame')
        self.SN_animated_last_24h_plots_frame.pack(side='top', fill='x', pady=(20, 0))
        self.SN_animated_plots_frame = ttk.Frame(self.SN_animated_last_24h_plots_frame, style='Standard.TFrame')
        self.SN_animated_plots_frame.pack(side='left', fill='y')
        self.SN_animated_plots_frame.grid_columnconfigure(1, weight=1)
        self.SN_last_24h_plots_frame = ttk.Frame(self.SN_animated_last_24h_plots_frame, style='Standard.TFrame')
        self.SN_last_24h_plots_frame.pack(side='left', fill='both', expand=True, padx=(10, 0))
        self.SN_last_24h_plots_frame.grid_columnconfigure(1, weight=1)

        # Master control section widgets:
        self.master_controller_label_frame = ttk.Frame(self.SN_master_controller_frame, style='DarkFrame.TFrame')
        self.master_controller_label_frame.grid(row=0, column=0, columnspan=4, sticky='nsew')
        self.master_control_label = ttk.Label(
            self.master_controller_label_frame,
            text='Master control:',
            style='ExtraLargeLabel.TLabel'
        )
        self.master_control_label.pack(side='left', padx=(10, 0), pady=(5, 5))

        self.plot_all_active_sample_label = ttk.Label(
            self.SN_master_controller_frame,
            style='LeftAligned.TLabel',
            text='plot master phase:'
        )
        self.plot_all_active_sample_label.grid(row=1, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.plot_all_active_sample_button = ttk.Button(
            self.SN_master_controller_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SN_plot_all_active_sample(
                self.controller.retrieve_active_sample(),
                phases='master'
            )
        )
        self.plot_all_active_sample_button.grid(row=1, column=1, sticky='w', padx=(20, 0), pady=(10, 0))

        self.plot_all_phase_plots_label = ttk.Label(
            self.SN_master_controller_frame,
            style='LeftAligned.TLabel',
            text='plot all phases:'
        )
        self.plot_all_phase_plots_label.grid(row=2, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.plot_all_phase_plots_button = ttk.Button(
            self.SN_master_controller_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SN_plot_all_active_sample(
                self.controller.retrieve_active_sample(),
                phases='phases'
            )
        )
        self.plot_all_phase_plots_button.grid(row=2, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        self.plot_all_active_test_label = ttk.Label(
            self.SN_master_controller_frame,
            style='LeftAligned.TLabel',
            text='plot all (active test):'
        )
        self.plot_all_active_test_label.grid(row=1, column=2, sticky='w', padx=(20, 0), pady=(10, 0))
        self.plot_all_active_test_button = ttk.Button(
            self.SN_master_controller_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=controller.app_SN_plot_all_active_test
        )
        self.plot_all_active_test_button.grid(row=1, column=3, sticky='w', padx=(20, 0), pady=(10, 0))

        self.plot_all_both_tests_label = ttk.Label(
            self.SN_master_controller_frame,
            style='LeftAligned.TLabel',
            text='plot all (both tests):'
        )
        self.plot_all_both_tests_label.grid(row=2, column=2, sticky='w', padx=(20, 0), pady=(10, 0))
        self.plot_all_both_test_button = ttk.Button(
            self.SN_master_controller_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=controller.app_SN_SS_plot_all_both_tests
        )
        self.plot_all_both_test_button.grid(row=2, column=3, sticky='w', padx=(20, 5), pady=(10, 0))

        # Combined plots section widgets:
        self.combined_plots_label_frame = ttk.Frame(
            self.SN_combined_plots_frame,
            style='DarkFrame.TFrame'
        )
        self.combined_plots_label_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.combined_plots_label = ttk.Label(
            self.combined_plots_label_frame,
            text='Combined plots:',
            style='ExtraLargeLabel.TLabel'
        )
        self.combined_plots_label.pack(side='left', padx=(10, 0), pady=(5, 5))

        self.plot_all_combined_label = ttk.Label(
            self.SN_combined_plots_frame,
            style='LeftAligned.TLabel',
            text='combined plot:'
        )
        self.plot_all_combined_label.grid(row=1, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.plot_all_combined_button = ttk.Button(
            self.SN_combined_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SN_combined_master(
                *self.controller.preprocessing_before_plotting(
                    self.controller.retrieve_active_sample()[0],
                    phases='master',
                )
            )
        )
        self.plot_all_combined_button.grid(row=1, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        self.temperature_series_combined_label = ttk.Label(
            self.SN_combined_plots_frame,
            style='LeftAligned.TLabel',
            text='temperature series:'
        )
        self.temperature_series_combined_label.grid(row=2, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.temperature_series_combined_button = ttk.Button(
            self.SN_combined_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SN_combined_temperature_series(
                *self.controller.preprocessing_before_plotting(
                    self.controller.retrieve_active_sample()[0],
                    phases='master',
                )
            )
        )
        self.temperature_series_combined_button.grid(row=2, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        self.temperature_gradient_combined_label = ttk.Label(
            self.SN_combined_plots_frame,
            style='LeftAligned.TLabel',
            text='temperature gradient:'
        )
        self.temperature_gradient_combined_label.grid(row=3, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.temperature_gradient_combined_button = ttk.Button(
            self.SN_combined_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SN_combined_temperature_gradient(
                *self.controller.preprocessing_before_plotting(
                    self.controller.retrieve_active_sample()[0],
                    phases='master',
                )
            )
        )
        self.temperature_gradient_combined_button.grid(row=3, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        self.moisture_series_combined_label = ttk.Label(
            self.SN_combined_plots_frame,
            style='LeftAligned.TLabel',
            text='moisture series:')
        self.moisture_series_combined_label.grid(row=4, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.moisture_series_combined_button = ttk.Button(
            self.SN_combined_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SN_combined_moisture_series(
                *self.controller.preprocessing_before_plotting(
                    self.controller.retrieve_active_sample()[0],
                    phases='master',
                )
            )
        )
        self.moisture_series_combined_button.grid(row=4, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        self.moisture_gradient_combined_label = ttk.Label(
            self.SN_combined_plots_frame,
            style='LeftAligned.TLabel',
            text='moisture gradient:'
        )
        self.moisture_gradient_combined_label.grid(row=5, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.moisture_gradient_combined_button = ttk.Button(
            self.SN_combined_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SN_combined_moisture_gradient(
                *self.controller.preprocessing_before_plotting(
                    self.controller.retrieve_active_sample()[0],
                    phases='master',
                )
            )
        )
        self.moisture_gradient_combined_button.grid(row=5, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        self.moist_vs_temp_series_combined_label = ttk.Label(
            self.SN_combined_plots_frame,
            style='LeftAligned.TLabel',
            text='moisture vs temperature:'
        )
        self.moist_vs_temp_series_combined_label.grid(row=6, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.moist_vs_temp_series_combined_button = ttk.Button(
            self.SN_combined_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SN_combined_series_moist_vs_temp(
                *self.controller.preprocessing_before_plotting(
                    self.controller.retrieve_active_sample()[0],
                    phases='master',
                )
            )
        )
        self.moist_vs_temp_series_combined_button.grid(row=6, column=1, sticky='w', padx=(20, 5), pady=(10, 0))


        # Separate plots:
        self.separate_plots_label_frame = ttk.Frame(
            self.SN_separate_plots_frame,
            style='DarkFrame.TFrame'
        )
        self.separate_plots_label_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.separate_plots_label = ttk.Label(
            self.separate_plots_label_frame,
            text='Separate plots:',
            style='ExtraLargeLabel.TLabel'
        )
        self.separate_plots_label.pack(side='left', padx=(10, 0), pady=(5, 5))

        self.temperature_series_separate_label = ttk.Label(
            self.SN_separate_plots_frame,
            style='LeftAligned.TLabel',
            text='temperature series:'
        )
        self.temperature_series_separate_label.grid(row=1, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.temperature_series_separate_button = ttk.Button(
            self.SN_separate_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SN_separate_temperature_series(
                *self.controller.preprocessing_before_plotting(
                    self.controller.retrieve_active_sample()[0],
                    phases='master',
                )
            )
        )
        self.temperature_series_separate_button.grid(row=1, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        self.temperature_gradient_separate_label = ttk.Label(
            self.SN_separate_plots_frame,
            style='LeftAligned.TLabel',
            text='temperature gradient:'
        )
        self.temperature_gradient_separate_label.grid(row=2, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.temperature_gradient_separate_button = ttk.Button(
            self.SN_separate_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SN_separate_temperature_gradient(
                *self.controller.preprocessing_before_plotting(
                    self.controller.retrieve_active_sample()[0],
                    phases='master',
                )
            )
        )
        self.temperature_gradient_separate_button.grid(row=2, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        self.moisture_series_separate_label = ttk.Label(
            self.SN_separate_plots_frame,
            style='LeftAligned.TLabel',
            text='moisture series:'
        )
        self.moisture_series_separate_label.grid(row=3, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.moisture_series_separate_button = ttk.Button(
            self.SN_separate_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SN_separate_moisture_series(
                *self.controller.preprocessing_before_plotting(
                    self.controller.retrieve_active_sample()[0],
                    phases='master',
                )
            )
        )
        self.moisture_series_separate_button.grid(row=3, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        self.moisture_gradient_separate_label = ttk.Label(
            self.SN_separate_plots_frame,
            style='LeftAligned.TLabel',
            text='moisture gradient:'
        )
        self.moisture_gradient_separate_label.grid(row=4, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.moisture_gradient_separate_button = ttk.Button(
            self.SN_separate_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SN_separate_moisture_gradient(
                *self.controller.preprocessing_before_plotting(
                    self.controller.retrieve_active_sample()[0],
                    phases='master',
                )
            )
        )
        self.moisture_gradient_separate_button.grid(row=4, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        self.moist_vs_temp_series_separate_label = ttk.Label(
            self.SN_separate_plots_frame,
            style='LeftAligned.TLabel',
            text='moisture vs temperature:'
        )
        self.moist_vs_temp_series_separate_label.grid(row=5, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.moist_vs_temp_series_separate_button = ttk.Button(
            self.SN_separate_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SN_separate_series_moist_vs_temp(
                *self.controller.preprocessing_before_plotting(
                    self.controller.retrieve_active_sample()[0],
                    phases='master',
                )
            )
        )
        self.moist_vs_temp_series_separate_button.grid(row=5, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        # Animated plots control:
        self.animated_plots_label_frame = ttk.Frame(
            self.SN_animated_plots_frame,
            style='DarkFrame.TFrame'
        )
        self.animated_plots_label_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.animated_plots_label = ttk.Label(
            self.animated_plots_label_frame,
            text='Animated plots:',
            style='ExtraLargeLabel.TLabel'
        )
        self.animated_plots_label.pack(side='left', padx=(10, 0), pady=(5, 5))

        self.animated_gradient_label = ttk.Label(
            self.SN_animated_plots_frame,
            style='LeftAligned.TLabel',
            text='animated gradient:'
        )
        self.animated_gradient_label.grid(row=1, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.animated_gradient_button = ttk.Button(
            self.SN_animated_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=controller.app_SN_animated_gradient_plot
        )
        self.animated_gradient_button.grid(row=1, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        self.animated_gradient_series_label = ttk.Label(
            self.SN_animated_plots_frame,
            style='LeftAligned.TLabel',
            text='animated series:')
        self.animated_gradient_series_label.grid(row=2, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.animated_gradient_series_button = ttk.Button(
            self.SN_animated_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=controller.app_SN_animated_series_plot
        )
        self.animated_gradient_series_button.grid(row=2, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        # Short period plots:
        self.short_term_plots_label_frame = ttk.Frame(
            self.SN_last_24h_plots_frame,
            style='DarkFrame.TFrame'
        )
        self.short_term_plots_label_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.short_term_plots_label = ttk.Label(
            self.short_term_plots_label_frame,
            text='Short term plots:',
            style='ExtraLargeLabel.TLabel'
        )
        self.short_term_plots_label.pack(side='left', padx=(10, 0), pady=(5, 5))

        self.last_24h_label = ttk.Label(
            self.SN_last_24h_plots_frame,
            style='LeftAligned.TLabel',
            text='last 24h plots:'
        )
        self.last_24h_label.grid(row=1, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.last_24h_button = ttk.Button(
            self.SN_last_24h_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SN_last_24h_plots(
                *self.controller.preprocessing_before_plotting(
                    self.controller.retrieve_active_sample()[0],
                    phases='master',
                )
            )
        )
        self.last_24h_button.grid(row=1, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        self.hot_end_temperature_label = ttk.Label(
            self.SN_last_24h_plots_frame,
            style='LeftAligned.TLabel',
            text='core temperature:')
        self.hot_end_temperature_label.grid(row=2, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.hot_end_temperature_button = ttk.Button(
            self.SN_last_24h_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SN_hot_end_temperature(
                *self.controller.preprocessing_before_plotting(
                    self.controller.retrieve_active_sample()[0],
                    phases='master',
                )
            )
        )
        self.hot_end_temperature_button.grid(row=2, column=1, sticky='w', padx=(20, 5), pady=(10, 0))


class SmallTestPlotControl(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style='Standard.TFrame')
        self.parent = parent
        self.controller = controller

        # Small test section subframes:
        self.SS_master_controller_frame = ttk.Frame(self, style='Standard.TFrame')
        self.SS_master_controller_frame.pack(side='top', fill='x', pady=(20, 0))
        self.SS_master_controller_frame.grid_columnconfigure(1, weight=1)
        self.SS_regular_animated_plots_frame = ttk.Frame(self, style='Standard.TFrame')
        self.SS_regular_animated_plots_frame.pack(side='top', fill='x', pady=(20, 0))
        self.SS_regular_plots_frame = ttk.Frame(self.SS_regular_animated_plots_frame, style='Standard.TFrame')
        self.SS_regular_plots_frame.pack(side='left', fill='y')
        self.SS_regular_plots_frame.grid_columnconfigure(1, weight=1)
        self.SS_animated_plots_frame = ttk.Frame(self.SS_regular_animated_plots_frame, style='Standard.TFrame')
        self.SS_animated_plots_frame.pack(side='left', fill='both', expand=True, padx=(10, 0))
        self.SS_animated_plots_frame.grid_columnconfigure(1, weight=1)

        # Master control section widgets:
        self.master_controller_label_frame = ttk.Frame(self.SS_master_controller_frame, style='DarkFrame.TFrame')
        self.master_controller_label_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.master_control_label = ttk.Label(
            self.master_controller_label_frame,
            text='Master control:',
            style='ExtraLargeLabel.TLabel'
        )
        self.master_control_label.pack(side='left', padx=(10, 0), pady=(5, 5))

        self.plot_all_active_sample_label = ttk.Label(
            self.SS_master_controller_frame,
            style='LeftAligned.TLabel',
            text='plot all (active sample):'
        )
        self.plot_all_active_sample_label.grid(row=1, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.plot_all_active_sample_button = ttk.Button(
            self.SS_master_controller_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SS_plot_all_active_sample(
                self.controller.retrieve_active_sample(),
                phases='phases',
            )
        )
        self.plot_all_active_sample_button.grid(row=1, column=1, sticky='w', padx=(20, 0), pady=(10, 0))

        self.plot_all_active_test_label = ttk.Label(
            self.SS_master_controller_frame,
            style='LeftAligned.TLabel',
            text='plot all (active test):'
        )
        self.plot_all_active_test_label.grid(row=2, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.plot_all_active_test_button = ttk.Button(
            self.SS_master_controller_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=controller.app_SS_plot_all_active_test
        )
        self.plot_all_active_test_button.grid(row=2, column=1, sticky='w', padx=(20, 0), pady=(10, 0))

        self.plot_all_both_tests_label = ttk.Label(
            self.SS_master_controller_frame,
            style='LeftAligned.TLabel',
            text='plot all (both tests):'
        )
        self.plot_all_both_tests_label.grid(row=3, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.plot_all_both_test_button = ttk.Button(
            self.SS_master_controller_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=controller.app_SN_SS_plot_all_both_tests
        )
        self.plot_all_both_test_button.grid(row=3, column=1, sticky='w', padx=(20, 0), pady=(10, 0))

        # Regular plots control section widgets:
        self.regular_plots_label_frame = ttk.Frame(self.SS_regular_plots_frame, style='DarkFrame.TFrame')
        self.regular_plots_label_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.regular_plots_label = ttk.Label(
            self.regular_plots_label_frame,
            text='Regular plots control:',
            style='ExtraLargeLabel.TLabel'
        )
        self.regular_plots_label.pack(side='left', padx=(10, 0), pady=(5, 5))

        self.plot_temperature_series_label = ttk.Label(
            self.SS_regular_plots_frame,
            style='LeftAligned.TLabel',
            text='temperature series:')
        self.plot_temperature_series_label.grid(row=1, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.plot_temperature_series_button = ttk.Button(
            self.SS_regular_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SS_temperature_series(
                *self.controller.preprocessing_before_plotting(
                    self.controller.retrieve_active_sample()[0],
                    phases='master'
                )
            )
        )
        self.plot_temperature_series_button.grid(row=1, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        self.plot_temperature_gradient_label = ttk.Label(
            self.SS_regular_plots_frame,
            style='LeftAligned.TLabel',
            text='temperature gradient:'
        )
        self.plot_temperature_gradient_label.grid(row=2, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.plot_temperature_gradient_button = ttk.Button(
            self.SS_regular_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=lambda: controller.app_SS_temperature_gradient(
                *self.controller.preprocessing_before_plotting(
                    self.controller.retrieve_active_sample()[0],
                    phases='master',
                )
            )
        )
        self.plot_temperature_gradient_button.grid(row=2, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        # Animated plots control section widgets:
        self.animated_plots_label_frame = ttk.Frame(self.SS_animated_plots_frame, style='DarkFrame.TFrame')
        self.animated_plots_label_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.animated_plots_label = ttk.Label(
            self.animated_plots_label_frame,
            text='Animated plots control:',
            style='ExtraLargeLabel.TLabel'
        )
        self.animated_plots_label.pack(side='left', padx=(10, 0), pady=(5, 5))

        self.plot_animated_temperature_series_label = ttk.Label(
            self.SS_animated_plots_frame,
            style='LeftAligned.TLabel',
            text='temperature series:'
        )
        self.plot_animated_temperature_series_label.grid(row=1, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.plot_animated_temperature_series_button = ttk.Button(
            self.SS_animated_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=controller.SS_animated_temperature_series
        )
        self.plot_animated_temperature_series_button.grid(row=1, column=1, sticky='w', padx=(20, 5), pady=(10, 0))

        self.plot_animated_temperature_gradient_label = ttk.Label(
            self.SS_animated_plots_frame,
            style='LeftAligned.TLabel',
            text='temperature gradient:'
        )
        self.plot_animated_temperature_gradient_label.grid(row=2, column=0, sticky='w', padx=(20, 0), pady=(10, 0))
        self.plot_animated_temperature_gradient_button = ttk.Button(
            self.SS_animated_plots_frame,
            style='Standard.TButton',
            text='plot',
            width=6,
            takefocus=False,
            command=controller.SS_animated_temperature_gradient
        )
        self.plot_animated_temperature_gradient_button.grid(row=2, column=1, sticky='w', padx=(20, 5), pady=(10, 0))


class HydraulicConductivityPlotControl(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)  # add style='Standard.TFrame'
        self.parent = parent
        self.controller = controller


class WaterRetentionPlotControl(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)  # add style='Standard.TFrame'
        self.parent = parent
        self.controller = controller


class ThermalConductivityPlotControl(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)  # add style='Standard.TFrame'
        self.parent = parent
        self.controller = controller


class WaterDrainagePlotControl(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)  # add style='Standard.TFrame'
        self.parent = parent
        self.controller = controller


class ParticleGradationPlotControl(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)  # add style='Standard.TFrame'
        self.parent = parent
        self.controller = controller


def main():
    root = MainApp()
    style = ttk.Style()
    StyleConfiguration(style)
    root.mainloop()


main()
