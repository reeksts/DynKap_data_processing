import tkinter as tk
from tkinter import ttk
from modules.MainControl import PlottingOptions

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Plot figures')
        self.plotter = PlottingOptions()


        # Adding main frame
        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(side='top', fill='both', expand=True)

        self.main_title = tk.Label(self.main_frame, text='Plotting options', font=('Arial', 14))
        self.main_title.grid(row=0, column=0, columnspan=2, sticky='w', pady=(15, 0))

        # Master plot control section
        self.master_control_label = tk.Label(self.main_frame, text='Master Control', font=('Arial', 12))
        self.master_control_label.grid(row=1, column=0, columnspan=2, sticky='w', pady=(15, 0))

        self.plot_all_label = tk.Label(self.main_frame, text='Plot all:', font=('Arial', 10))
        self.plot_all_label.grid(row=2, column=0, sticky='w', pady=(15, 0))
        self.plot_all_button = tk.Button(self.main_frame, text='Plot', command=self.plotter.plot_everything)
        self.plot_all_button.grid(row=2, column=1)

        # Main combined plot section
        self.combined_plot_section_label = tk.Label(self.main_frame, text='Main combined plots', font=('Arial', 12))
        self.combined_plot_section_label.grid(row=3, column=0, columnspan=2, sticky='w', pady=(15, 0))

        self.plot_all_combined_label = tk.Label(self.main_frame, text='Combined plot:', font=('Arial', 10))
        self.plot_all_combined_label.grid(row=4, column=0, sticky='w', padx=(15, 0), pady=(15, 0))
        self.plot_all_combined_button = tk.Button(self.main_frame, text='Plot', command=self.plotter.all_combined_plot)
        self.plot_all_combined_button.grid(row=4, column=1, sticky='w', pady=(15, 0))

        self.plot_temperature_series_combined_label = tk.Label(self.main_frame,
                                                              text='Temperature series combined',
                                                              font=('Arial', 10))
        self.plot_temperature_series_combined_label.grid(row=5, column=0, sticky='w', padx=(15, 0), pady=(15, 0))
        self.plot_temperature_series_combined_button = tk.Button(self.main_frame,
                                                                 text='Plot',
                                                                 command=self.plotter.temperature_series_combined)
        self.plot_temperature_series_combined_button.grid(row=5, column=1, sticky='w', pady=(15, 0))

        self.plot_temperature_gradient_combined_label = tk.Label(self.main_frame,
                                                               text='Temperature gradient combined',
                                                               font=('Arial', 10))
        self.plot_temperature_gradient_combined_label.grid(row=6, column=0, sticky='w', padx=(15, 0), pady=(15, 0))
        self.plot_temperature_gradient_combined_button = tk.Button(self.main_frame,
                                                                 text='Plot',
                                                                 command=self.plotter.temperature_gradient_combined)
        self.plot_temperature_gradient_combined_button.grid(row=6, column=1, sticky='w', pady=(15, 0))

        self.plot_moisture_series_combined_label = tk.Label(self.main_frame,
                                                               text='Moisture series combined',
                                                               font=('Arial', 10))
        self.plot_moisture_series_combined_label.grid(row=7, column=0, sticky='w', padx=(15, 0), pady=(15, 0))
        self.plot_moisture_series_combined_button = tk.Button(self.main_frame,
                                                                 text='Plot',
                                                                 command=self.plotter.moisture_series_combined)
        self.plot_moisture_series_combined_button.grid(row=7, column=1, sticky='w', pady=(15, 0))

        self.plot_moisture_gradient_combined_label = tk.Label(self.main_frame,
                                                                 text='Moisture gradient combined',
                                                                 font=('Arial', 10))
        self.plot_moisture_gradient_combined_label.grid(row=8, column=0, sticky='w', padx=(15, 0), pady=(15, 0))
        self.plot_moisture_gradient_combined_button = tk.Button(self.main_frame,
                                                                   text='Plot',
                                                                   command=self.plotter.moisture_gradient_combined)
        self.plot_moisture_gradient_combined_button.grid(row=8, column=1, sticky='w', pady=(15, 0))

        # Separate direction plot section
        self.combined_plot_section_label = tk.Label(self.main_frame,
                                                    text='Separate direction plots',
                                                    font=('Arial', 12))
        self.combined_plot_section_label.grid(row=9, column=0, columnspan=2, sticky='w', pady=(15, 0))

        self.plot_temperature_series_separate_label = tk.Label(self.main_frame,
                                                                text='Temperature series separate',
                                                                font=('Ariel', 10))
        self.plot_temperature_series_separate_label.grid(row=10, column=0, sticky='w', padx=(15, 0), pady=(15, 0))
        self.plot_temperature_series_separate_button = tk.Button(self.main_frame,
                                                                  text='Plot',
                                                                  command=self.plotter.temperature_series_separate)
        self.plot_temperature_series_separate_button.grid(row=10, column=1, sticky='w', pady=(15, 0))

        self.plot_temperature_gradient_separate_label = tk.Label(self.main_frame,
                                                                text='Temperature gradient separate',
                                                               font=('Ariel', 10))
        self.plot_temperature_gradient_separate_label.grid(row=11, column=0, sticky='w', padx=(15, 0), pady=(15, 0))
        self.plot_temperature_gradient_separate_button = tk.Button(self.main_frame,
                                                                  text='Plot',
                                                                  command=self.plotter.temperature_gradient_separate)
        self.plot_temperature_gradient_separate_button.grid(row=11, column=1, sticky='w', pady=(15, 0))

        self.plot_moisture_series_separate_label = tk.Label(self.main_frame,
                                                               text='Moisture series separate',
                                                               font=('Ariel', 10))
        self.plot_moisture_series_separate_label.grid(row=12, column=0, sticky='w', padx=(15, 0), pady=(15, 0))
        self.plot_moisture_series_separate_button = tk.Button(self.main_frame,
                                                                 text='Plot',
                                                                 command=self.plotter.moisture_series_separate)
        self.plot_moisture_series_separate_button.grid(row=12, column=1, sticky='w', pady=(15, 0))

        self.plot_moisture_gradient_separate_label = tk.Label(self.main_frame,
                                                                 text='Moisture gradient separate',
                                                                 font=('Ariel', 10))
        self.plot_moisture_gradient_separate_label.grid(row=13, column=0, sticky='w', padx=(15, 0), pady=(15, 0))
        self.plot_moisture_gradient_separate_button = tk.Button(self.main_frame,
                                                                   text='Plot',
                                                                   command=self.plotter.moisture_gradient_separate)
        self.plot_moisture_gradient_separate_button.grid(row=13, column=1, sticky='w', pady=(15, 0))

        # Last day plot section
        self.last_day_plot_section_label = tk.Label(self.main_frame,
                                                    text='Last 24h plots',
                                                    font=('Arial', 12))
        self.last_day_plot_section_label.grid(row=14, column=0, columnspan=2, sticky='w', pady=(15, 0))

        self.plot_all_last_24h_plots_label = tk.Label(self.main_frame,
                                                               text='All last 24h plots',
                                                               font=('Ariel', 10))
        self.plot_all_last_24h_plots_label.grid(row=15, column=0, sticky='w', padx=(15, 0), pady=(15, 0))
        self.plot_all_last_24h_plots_button = tk.Button(self.main_frame,
                                                                 text='Plot',
                                                                 command=self.plotter.last_24h_plots)
        self.plot_all_last_24h_plots_button.grid(row=15, column=1, sticky='w', pady=(15, 0))

def main():
    root = MainApp()
    #style = ttk.Style()
    root.mainloop()


if __name__ == '__main__':
    main()