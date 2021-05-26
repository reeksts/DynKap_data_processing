
# Frame colors
STANDARD_FRAME_BACKGROUND = '#404040'
DARK_FRAME_BACKGROUND = '#262626'

# Button colors
STANDARD_BUTTON_BACKGROUND = '#404040'
STANDARD_BUTTON_PRESSED_BACKGROUND = '#b2b2b2'
STANDARD_BUTTON_ACTIVE_BACKGROUND = '#808080'

# Label colors
STANDARD_LABEL_BACKGROUND = '#404040'
DARK_LABEL_BACKGROUND = '#262626'
STANDARD_LABEL_FOREGROUND = '#e5e5e5'

# Radiobutton colors
STANDARD_RADIOBUTTON_BACKGROUND = '#404040'
STANDARD_RADIOBUTTON_BACKGROUND_ACTIVE = '#808080'

# Checkbutton
STANDARD_CHECKBOX_UPPERBORDERCOLOR = '#262626'
STANDARD_CHECKBOX_LOWERBORDERCOLOR = '#262626'
STANDARD_CHECKBOX_BACKGROUND = '#404040'
STANDARD_CHECKBOX_ACTIVE_BACKGROUND = '#b2b2b2'
STANDARD_CHECKBOX_ACTIVE_INDICATORBACKGROUND = '#b2b2b2'
STANDARD_CHECKBOX_INDICATORBACKGROUND = '#808080'
STANDARD_CHECKBOX_INDICATORFOREGROUND = '#e5e5e5'

# Combobox colors
STANDARD_COMBOBOX_BORDER = '#b2b2b2'
STANDARD_COMBOBOX_DARKCOLOR = '#404040'
STANDARD_COMBOBOX_LIGHTCOLOR = '#404040'
STANDARD_COMBOBOX_ARROW_COLOR = '#404040'
STANDARD_COMBOBOX_FIELD_BACKGROUND_FOCUS = '#404040'
STANDARD_COMBOBOX_FIELD_BACKGROUND_NOT_FOCUS = '#404040'
STANDARD_COMBOBOX_SELECT_FOREGROUND_FOCUS = '#e5e5e5'
STANDARD_COMBOBOX_SELECT_FOREGROUND_NOT_FOCUS = '#e5e5e5'
STANDARD_COMBOBOX_SELECT_BACKGROUND_FOCUS = '#404040'
STANDARD_COMBOBOX_SELECT_BACKGROUND_NOT_FOCUS = '#404040'
STANDARD_COMBOBOX_ARROW_BACKGROUND = '#b2b2b2'
STANDARD_COMBOBOX_ARROW_BACKGROUND_ACTIVE = '#f2f2f2'
STANDARD_COMBOBOX_FOREGROUND = '#e5e5e5'


class StyleConfiguration:
    def __init__(self, style):
        style.theme_use('clam')

        # Standard Frame configuration
        style.configure('Standard.TFrame',
                        background=STANDARD_FRAME_BACKGROUND)

        # Dark frame configuration
        style.configure('DarkFrame.TFrame',
                        background=DARK_FRAME_BACKGROUND)

        # Standard Button configuration
        style.configure('Standard.TButton',
                        font=('Calibri', 10),
                        padding=1,
                        background=STANDARD_BUTTON_BACKGROUND,
                        foreground=STANDARD_LABEL_FOREGROUND, )
        style.map('Standard.TButton',
                  background=[('pressed', '!disabled', STANDARD_BUTTON_PRESSED_BACKGROUND),
                              ('active', STANDARD_BUTTON_ACTIVE_BACKGROUND)])

        # Left aligned Label configuration
        style.configure('LeftAligned.TLabel',
                        font=('Calibri', 10),
                        background=STANDARD_LABEL_BACKGROUND,
                        foreground=STANDARD_LABEL_FOREGROUND,
                        justify='left',
                        anchor='w')

        # Extra large Label configuration:
        style.configure('ExtraLargeLabel.TLabel',
                        font=('Calibri', 13, 'bold'),
                        background=DARK_LABEL_BACKGROUND,
                        foreground=STANDARD_LABEL_FOREGROUND)

        # Standard Radiobutton configuration
        style.configure('Standard.TRadiobutton',
                        padding=0,
                        background=STANDARD_RADIOBUTTON_BACKGROUND)
        style.map('Standard.TRadiobutton',
                  background=[('active', STANDARD_RADIOBUTTON_BACKGROUND_ACTIVE)])

        # Standard Checkbutton configuration
        style.configure('Standard.TCheckbutton',
                        focusthickness=0,
                        indicatorsize=12,
                        indicatormargin=3,
                        upperbordercolor=STANDARD_CHECKBOX_UPPERBORDERCOLOR,
                        lowerbordercolor=STANDARD_CHECKBOX_LOWERBORDERCOLOR,
                        indicatorbackground=STANDARD_CHECKBOX_INDICATORBACKGROUND,
                        indicatorforeground=STANDARD_CHECKBOX_INDICATORFOREGROUND,
                        background=STANDARD_CHECKBOX_BACKGROUND)
        style.map('Standard.TCheckbutton',
                  background=[('active', STANDARD_CHECKBOX_ACTIVE_BACKGROUND)],
                  indicatorbackground=[('active', STANDARD_CHECKBOX_ACTIVE_INDICATORBACKGROUND)])

        # Standard Combobox configuration
        style.configure('Standard.TCombobox',
                        arrowsize=15,
                        background=STANDARD_COMBOBOX_ARROW_BACKGROUND,
                        bordercolor=STANDARD_COMBOBOX_BORDER,
                        darkcolor=STANDARD_COMBOBOX_DARKCOLOR,
                        lightcolor=STANDARD_COMBOBOX_LIGHTCOLOR,
                        arrowcolor=STANDARD_COMBOBOX_ARROW_COLOR)
        style.map('Standard.TCombobox',
                  fieldbackground=[('focus', STANDARD_COMBOBOX_FIELD_BACKGROUND_FOCUS),
                                   ('!focus', STANDARD_COMBOBOX_FIELD_BACKGROUND_NOT_FOCUS)],
                  selectforeground=[('focus', STANDARD_COMBOBOX_SELECT_FOREGROUND_FOCUS),
                                    ('!focus', STANDARD_COMBOBOX_SELECT_FOREGROUND_NOT_FOCUS)],
                  selectbackground=[('focus', STANDARD_COMBOBOX_SELECT_BACKGROUND_FOCUS),
                                    ('!focus', STANDARD_COMBOBOX_SELECT_BACKGROUND_NOT_FOCUS)],
                  foreground=[('!focus', STANDARD_COMBOBOX_FOREGROUND)],
                  background=[('active', STANDARD_COMBOBOX_ARROW_BACKGROUND_ACTIVE)])