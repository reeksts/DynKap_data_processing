import pandas as pd
import os
from tkinter import ttk
from modules.SensorCorrection import SensorCorrection
from modules.PlotMeasurementFigures import PlotMeasurementFigures
from modules.PlotCalibrationFigures import PlotCalibrationFigures
from modules.DataProcessor import DataProcessor
from modules.SampleData import SampleData
from modules.FigureFormatting import FigureFormatting


# Sample selection
sample_data = SampleData()
sample = sample_data.SN2
path = sample['dir']
timestamps = sample['timestamps']
fignames = sample_data.fignames

# Folder path
measurement_data = '02_measurement_data\\'
comsol_data = '03_comsol_model\\'
calib_data = '04_calib_data\\'
figures_save = '06_figures\\'
folders = {'01_combined_plots': '01_combined_plots\\',
           '02_time_series_temperature': '02_time_series_temperature\\',
           '03_time_series_moisture': '03_time_series_moisture\\',
           '04_gradient_temperature': '04_gradient_temperature\\',
           '05_gradient_moisture': '05_gradient_moisture\\',
           '06_last_24_hours': '06_last_24_hours\\'}
save_path = path + figures_save
comsol_path = path + comsol_data
data_path = path + measurement_data

# Calibration fit figures (optional):
calibration_figures = PlotCalibrationFigures(data_path, sample)
#calibration_figures.plot_calibration_figure()


# Plot formatter
formatter = FigureFormatting()

# Column names:
temperature_columns_main = ['U1', 'U2', 'U3', 'U4', 'U5', 'U6',
                            'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
                            'D1', 'D2', 'D3', 'D4', 'D5', 'D6']
temperature_columns_moist = ['U1', 'U2', 'U3', 'U4',
                            'R1', 'R2', 'R3', 'R4',
                            'D1', 'D2', 'D3', 'D4']
temperature_columns_ext = ['X1', 'X2', 'X3', 'K1', 'K2', 'K3']
temperature_columns = temperature_columns_main + temperature_columns_ext
moisture_columns = ['MS1', 'MS2', 'MS3', 'MS4', 'MS5', 'MS6', 'MS7', 'MS8', 'MS9', 'MS10', 'MS11', 'MS12']
power_column = ['power']
columns = temperature_columns + moisture_columns + power_column

# Setting file path:
df = pd.DataFrame(columns=columns)
for file in os.listdir(path + measurement_data):
    if file.endswith('csv'):
        df_loc = pd.read_csv(path + measurement_data + file, index_col=0, names=columns)
        df = pd.concat([df, df_loc])
    else:
        pass

# Measurement corrections:
def corrector_func():
    corrector = SensorCorrection(path + calib_data)
    for name in temperature_columns:
        df[name] = df[name].apply(lambda mes_val: corrector.tempertaure_sensor_correction(name, mes_val))
    for temp_name, moist_name in zip(temperature_columns_moist, moisture_columns):
        df[moist_name] = df.apply(lambda line: corrector.moisture_sensor_correction(temp_name,
                                                                                    moist_name,
                                                                                    line[temp_name],
                                                                                    line[moist_name]), axis=1)
#corrector_func()

# Plot figures
"""
Options to select from:
- plot_all_measurements()   -> plots a 4 row, 3 column figure
- plot_temperature_series()   -> plots temperature series separately
- plot_moisture_series()   -> plots separately moisture figures series
- plot_temperature_gradient()   -> plots temperature gradient separately
- plot_moisture_gradient()   -> plots separately moisture figure gradient
"""

df.index = pd.to_datetime(df.index)

# Execute data deletion (this deletes flawed data)
data_processor = DataProcessor(sample)
data_processor.delete_flawed_data(df)


class PlottingOptions:
    def __init__(self):
        self.plot_figures = PlotMeasurementFigures(df, timestamps, fignames, save_path, comsol_path, sample)
        self.formatter = FigureFormatting()

    def all_combined_plot(self, xscale):
        self.plot_figures.plot_all_measurements(folder=folders['01_combined_plots'],
                                                formatter=formatter.std_paper_4x3_full_width,
                                                xscale=xscale)

    def temperature_series_separate(self):
        self.plot_figures.plot_temperature_series(folder=folders['02_time_series_temperature'],
                                                  formatter=formatter.std_paper_1x1_full_width)
        self.plot_figures.plot_temperature_series(folder=folders['02_time_series_temperature'],
                                                  formatter=formatter.std_paper_1x1_full_width,
                                                  xaxis_type='datetime')

    def temperature_gradient_separate(self, xscale):
        self.plot_figures.plot_temperature_gradient(folder=folders['04_gradient_temperature'],
                                                    formatter=formatter.std_paper_1x1_partial_width,
                                                    xscale=xscale)

    def moisture_series_separate(self):
        self.plot_figures.plot_moisture_series(folder=folders['03_time_series_moisture'],
                                               formatter=formatter.std_paper_1x1_full_width)
        self.plot_figures.plot_moisture_series(folder=folders['03_time_series_moisture'],
                                               formatter=formatter.std_paper_1x1_full_width,
                                               xaxis_type='datetime')

    def moisture_gradient_separate(self, xscale):
        self.plot_figures.plot_moisture_gradient(folder=folders['05_gradient_moisture'],
                                            formatter=formatter.std_paper_1x1_partial_width,
                                                 xscale=xscale)

    def temperature_series_combined(self):
        self.plot_figures.plot_all_temperature_series(folder=folders['01_combined_plots'],
                                                      formatter=formatter.std_paper_3x1_full_width)
        self.plot_figures.plot_all_temperature_series(folder=folders['01_combined_plots'],
                                                      formatter=formatter.std_paper_3x1_full_width,
                                                      xaxis_type='datetime')

    def temperature_gradient_combined(self, xscale):
        self.plot_figures.plot_all_temperature_gradients(folder=folders['01_combined_plots'],
                                                         formatter=formatter.std_paper_3x1_partial_width,
                                                         xscale=xscale)

    def moisture_series_combined(self):
        self.plot_figures.plot_all_moisture_series(folder=folders['01_combined_plots'],
                                                   formatter=formatter.std_paper_3x1_full_width)
        self.plot_figures.plot_all_moisture_series(folder=folders['01_combined_plots'],
                                                   formatter=formatter.std_paper_3x1_full_width,
                                                   xaxis_type='datetime')

    def moisture_gradient_combined(self, xscale):
        self.plot_figures.plot_all_moisture_gradients(folder=folders['01_combined_plots'],
                                                      formatter=formatter.std_paper_3x1_partial_width,
                                                      xscale=xscale)

    def last_24h_plots(self):
        self.plot_figures.plot_temperature_series(folder=folders['06_last_24_hours'],
                                                  formatter=formatter.std_paper_1x1_full_width,
                                                  xaxis_type='datetime',
                                                  last_day=True)
        self.plot_figures.plot_moisture_series(folder=folders['06_last_24_hours'],
                                               formatter=formatter.std_paper_1x1_full_width,
                                               xaxis_type='datetime',
                                               last_day=True)
        self.plot_figures.plot_all_temperature_series(folder=folders['06_last_24_hours'],
                                                      formatter=formatter.std_paper_3x1_full_width,
                                                      xaxis_type='datetime',
                                                      last_day=True)
        self.plot_figures.plot_all_moisture_series(folder=folders['06_last_24_hours'],
                                                   formatter=formatter.std_paper_3x1_full_width,
                                                   xaxis_type='datetime',
                                                   last_day=True)

    def plot_everything(self, xscale):
        self.all_combined_plot(xscale)
        self.temperature_series_separate()
        self.temperature_gradient_separate(xscale)
        self.moisture_series_separate()
        self.moisture_gradient_separate(xscale)
        self.temperature_series_combined()
        self.temperature_gradient_combined(xscale)
        self.moisture_series_combined()
        self.moisture_gradient_combined(xscale)
        self.last_24h_plots()





