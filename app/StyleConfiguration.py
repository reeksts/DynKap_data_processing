
# Frame colors
STANDARD_FRAME_BACKGROUND = '#404040'
DARK_FRAME_BACKGROUND = '#262626'

# Label colors
STANDARD_LABEL_BACKGROUND = '#404040'
DARK_LABEL_BACKGROUND = '#262626'
STANDARD_LABEL_FOREGROUND = '#e5e5e5'


class StyleConfiguration:
    def __init__(self, style):
        style.theme_use('clam')

        # Standard Frame configuration
        style.configure('Standard.TFrame',
                        background=STANDARD_FRAME_BACKGROUND)

        # Dark frame configuration
        style.configure('DarkFrame.TFrame',
                        background=DARK_FRAME_BACKGROUND)

        # Extra large Label configuration:
        style.configure('ExtraLargeLabel.TLabel',
                        font=('Calibri', 13, 'bold'),
                        background=DARK_LABEL_BACKGROUND,
                        foreground=STANDARD_LABEL_FOREGROUND)