import tkinter as tk
from tkinter import ttk
from modules.MainControl import PlottingOptions
from app.StyleConfiguration import StyleConfiguration


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Plot figures')

        # Adding main frame:
        self.main_frame = ttk.Frame(self, style='Standard.TFrame', padding=10)
        self.main_frame.pack(side='top', fill='both', expand=True)

        # Adding section frames:
        self.test_setup_plot_options_frame = ttk.Frame(self.main_frame, style='Standard.TFrame')
        self.test_setup_plot_options_frame.pack(side='top')
        self.test_setup_frame = ttk.Frame(self.test_setup_plot_options_frame, style='Standard.TFrame')
        self.test_setup_frame.pack(side='left')
        self.plot_options_frame = ttk.Frame(self.test_setup_plot_options_frame, style='Standard.TFrame')
        self.plot_options_frame.pack(side='left')

        self.samples_frame = ttk.Frame(self.main_frame, style='Standard.TFrame')
        self.samples_frame.pack(side='top')
        self.master_controller_frame = ttk.Frame(self.main_frame, style='Standard.TFrame')
        self.master_controller_frame.pack(side='top')
        self.combined_separate_plots_frame = ttk.Frame(self.main_frame, style='Standard.TFrame')
        self.combined_separate_plots_frame.pack(side='top')
        self.combined_plots_frame = ttk.Frame(self.combined_separate_plots_frame, style='Standard.TFrame')
        self.combined_plots_frame.pack(side='left')
        self.seperate_plots_frame = ttk.Frame(self.combined_separate_plots_frame, style='Standard.TFrame')
        self.seperate_plots_frame.pack(side='left')
        self.last_24h_plots_frame = ttk.Frame(self.main_frame, style='Standard.TFrame')
        self.last_24h_plots_frame.pack(side='top')

        # Test setup section widgets:
        self.test_setup_label = ttk.Label(self.test_setup_frame,
                                          text='Test setup:',
                                          style='ExtraLargeLabel.TLabel')
        self.test_setup_label.grid(row=0, column=0, columnspan=2)

        # Plot options section widgets:
        self.plot_options_label = ttk.Label(self.plot_options_frame,
                                          text='Plot options:',
                                          style='ExtraLargeLabel.TLabel')
        self.plot_options_label.grid(row=0, column=0, columnspan=3)

        # Samples section widgets:
        self.samples_label = ttk.Label(self.samples_frame,
                                            text='Samples:',
                                            style='ExtraLargeLabel.TLabel')
        self.samples_label.grid(row=0, column=0, columnspan=3)

        # Master control section widgets:
        self.master_control_label = ttk.Label(self.master_controller_frame,
                                       text='Master control:',
                                       style='ExtraLargeLabel.TLabel')
        self.master_control_label.grid(row=0, column=0, columnspan=3)

        # Combined plots section widgets:
        self.combined_plot_label = ttk.Label(self.combined_plots_frame,
                                              text='Combined plots:',
                                              style='ExtraLargeLabel.TLabel')
        self.combined_plot_label.grid(row=0, column=0, columnspan=3)

        # Separate plots:
        self.separate_plot_label = ttk.Label(self.seperate_plots_frame,
                                             text='Separate plots:',
                                             style='ExtraLargeLabel.TLabel')
        self.separate_plot_label.grid(row=0, column=0, columnspan=3)

        # Last 24h our plots
        self.last_24h_plot_label = ttk.Label(self.last_24h_plots_frame,
                                             text='Last 24h plots:',
                                             style='ExtraLargeLabel.TLabel')
        self.last_24h_plot_label.grid(row=0, column=0, columnspan=3)


def main():
    root = MainApp()
    style = ttk.Style()
    StyleConfiguration(style)
    root.mainloop()

main()