import os

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    # Background colors (optional)
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'

# Function to print colored messages
def print_colored(message, color=Colors.GREEN, bold=False):
    if os.name == 'nt': # Check if running on Windows
        print(message)
    else:
        prefix = color
        if bold:
            prefix += Colors.BOLD
        print(f"{prefix}{message}{Colors.RESET}")