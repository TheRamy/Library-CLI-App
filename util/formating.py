
import os





def print_terminal(char_to_print):
    """Fills ONE line in the terminal with one character. For example "----------". """
    cols, rows = os.get_terminal_size()
    dashes = f'{char_to_print}' * cols
    print(dashes, end='', flush=True)


