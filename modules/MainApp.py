import tkinter as tk
from tkinter import ttk


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Plot figures')

        # Adding main frame
        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(side='top', fill='both', expand=True)

        self.load_title = tk.Label(self.main_frame, text='Select files to merge')
        self.load_title.grid(row=0, column=0, sticky='w')
        self.load_button = tk.Button(self.main_frame, text='Load', command=self.load_files)
        self.load_button.grid(row=0, column=1, sticky='w')

        self.main_title = tk.Label(self.main_frame, text='Figure control option', font='16')
        self.main_title.grid(row=1, column=0, sticky='w', pady=(15, 0))

        # Adding time series control
        self.time_series_label = tk.Label(self.main_frame, text='Time series control', font='14')
        self.time_series_label.grid(row=2, column=0, sticky='w', pady=(10, 0))

        self.time_temperature_series_label = tk.Label(self.main_frame, text='Set start and end for temperature series')
        self.time_temperature_series_label.grid(row=4, column=0, columnspan=2, sticky='w')

        self.time_series_common_frame = tk.Frame(self.main_frame)
        self.time_series_common_frame.grid(row=5, column=0, columnspan=2, sticky='ew')
        self.time_series_common_label = tk.Label(self.time_series_common_frame, text='Common with moisture:')
        self.time_series_common_label.pack(side='left')
        self.common_moisture = tk.IntVar()
        self.common_moisture.set(0)
        self.time_series_common_checkbutton = tk.Checkbutton(self.time_series_common_frame,
                                                             variable=self.common_moisture)
        self.time_series_common_checkbutton.pack(side='left')

        self.time_temperatures_series_start_label = tk.Label(self.main_frame, text='Start:')
        self.time_temperatures_series_start_label.grid(row=6, column=0, sticky='w')
        self.temp_series_start = tk.StringVar()
        self.time_temperatures_series_start_button = tk.Entry(self.main_frame,
                                                              width=30,
                                                              textvariable=self.temp_series_start)
        self.time_temperatures_series_start_button.grid(row=6, column=1)
        self.time_temperatures_series_end_label = tk.Label(self.main_frame, text='End:')
        self.time_temperatures_series_end_label.grid(row=7, column=0, sticky='w')
        self.temp_series_end = tk.StringVar()
        self.time_temperatures_series_end_button = tk.Entry(self.main_frame,
                                                            width=30,
                                                            textvariable=self.temp_series_end)
        self.time_temperatures_series_end_button.grid(row=7, column=1, sticky='w')

        self.set_time_temperature_series_button = tk.Button(self.main_frame,
                                                            text='Set',
                                                            command=self.set_temperature_series_time)
        self.set_time_temperature_series_button.grid(row=8, column=1, sticky='e')

        # Adding time series control
        self.time_moisture_series_label = tk.Label(self.main_frame, text='Set start and end for moisture series')
        self.time_moisture_series_label.grid(row=9, column=0, columnspan=2, sticky='w')

        self.time_moisture_series_start_label = tk.Label(self.main_frame, text='Start:')
        self.time_moisture_series_start_label.grid(row=10, column=0, sticky='w')
        self.moist_series_start = tk.StringVar()
        self.time_moisture_series_start_entry = tk.Entry(self.main_frame,
                                                         width=30,
                                                         textvariable=self.moist_series_start)
        self.time_moisture_series_start_entry.grid(row=10, column=1)
        self.time_moisture_series_end_label = tk.Label(self.main_frame, text='End:')
        self.time_moisture_series_end_label.grid(row=11, column=0, sticky='w')
        self.moist_series_end = tk.StringVar()
        self.time_moisture_series_end_button = tk.Entry(self.main_frame,
                                                        width=30,
                                                        textvariable=self.moist_series_end)
        self.time_moisture_series_end_button.grid(row=11, column=1, sticky='w')
        self.set_time_moisture_series_button = tk.Button(self.main_frame,
                                                         text='Set',
                                                         command=self.set_moisture_series_time)
        self.set_time_moisture_series_button.grid(row=12, column=1, sticky='e')

        # Adding temperature gradient control
        self.gradient_control_label = tk.Label(self.main_frame, text='Gradient control', font='14')
        self.gradient_control_label.grid(row=13, column=0, sticky='w', pady=(10, 0))

        self.gradient_temperature_label = tk.Label(self.main_frame,
                                                   text='Add start and duration for temperature gradient:')
        self.gradient_temperature_label.grid(row=14, column=0, columnspan=2, sticky='w')

        self.gradient_temperature_start_label = tk.Label(self.main_frame, text='Start')
        self.gradient_temperature_start_label.grid(row=15, column=0, sticky='w')
        self.gradient_temperature_entry = tk.Entry(self.main_frame, width=30)
        self.gradient_temperature_entry.grid(row=15, column=1, sticky='w')
        self.gradient_temperature_duration_label = tk.Label(self.main_frame, text='Duration')
        self.gradient_temperature_duration_label.grid(row=16, column=0, sticky='w')
        self.gradient_temperature_duration_entry = tk.Entry(self.main_frame, width=30)
        self.gradient_temperature_duration_entry.grid(row=16, column=1, sticky='w')
        self.set_gradient_temperature_button = tk.Button(self.main_frame,
                                                         text='Set',
                                                         command=self.set_gradient_temperature)
        self.set_gradient_temperature_button.grid(row=17, column=1, sticky='e')

        # Adding moisture gradient control
        self.gradient_moisture_label = tk.Label(self.main_frame,
                                                   text='Add start and duration for moisture gradient:')
        self.gradient_moisture_label.grid(row=18, column=0, columnspan=2, sticky='w')

        self.gradient_moisture_start_label = tk.Label(self.main_frame, text='Start')
        self.gradient_moisture_start_label.grid(row=19, column=0, sticky='w')
        self.gradient_moisture_entry = tk.Entry(self.main_frame, width=30)
        self.gradient_moisture_entry.grid(row=19, column=1, sticky='w')
        self.gradient_moisture_duration_label = tk.Label(self.main_frame, text='Duration')
        self.gradient_moisture_duration_label.grid(row=20, column=0, sticky='w')
        self.gradient_moisture_duration_entry = tk.Entry(self.main_frame, width=30)
        self.gradient_moisture_duration_entry.grid(row=20, column=1, sticky='w')
        self.set_gradient_moisture_button = tk.Button(self.main_frame,
                                                         text='Set',
                                                         command=self.set_gradient_temperature)
        self.set_gradient_moisture_button.grid(row=21, column=1, sticky='e')



    def load_files(self):
        pass

    def set_temperature_series_time(self):
        pass

    def set_moisture_series_time(self):
        pass

    def set_gradient_temperature(self):
        pass


def main():
    root = MainApp()
    style = ttk.Style()
    root.mainloop()


if __name__ == '__main__':
    main()