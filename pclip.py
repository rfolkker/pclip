#!/ussr/bin/env python3

# %% Imports
import math
import argparse

# %% Alignment function definitions

# Get the difference between the current text and the expected length
# Assumed length is longer than text length
def get_diff(text, length):
    return length-len(text)

def get_center(text, length):
    full_spacer = get_diff(text, length)
    left_side = 0
    right_side = 0
    if full_spacer > 0: # We have something to work with
        left_side = math.ceil(full_spacer/2) # Centered ~+1
        right_side = math.floor(full_spacer/2) # Centered ~-1

    return f"{' '*left_side}{text}{' '*right_side}"

def get_left(text, length):
    return f"{text}{' '*get_diff(text, length)}"

def get_right(text, length):
    return f"{' '*get_diff(text, length)}{text}"

# %% Alignment lookup table

text_align = {
    0        : get_center,
    "Center" : get_center,
    "center" : get_center,
    1        : get_left,
    "Left"   : get_left,
    "left"   : get_left,
    2        : get_right,
    "Right"  : get_right,
    "right"  : get_right
}

# %% Perform clipification

# converting a file to a list, then clipify
def clipify_file(filename, align):
    file_lines = []
    with open(filename, 'r') as f:
        file_lines = [line.replace("\n", "") for line in f.readlines()]
        
    return clipify_list(file_lines, align)

# converting a string into a list, then clipify
def clipify_text(text, align):
    # From commandline, \n characters come in as text, convert then split
    lines = text.replace("\\n", "\n").split("\n")
    return clipify_list(lines, align)

def clipify_list(lines, align):
    max_length = 20 # Default is the min length for the chat bubble size
    clipped_text = ""
    # Reset max length to the longest single line
    for line in lines:
        if len(line) > max_length:
            max_length = len(line)

    clipped_text += f"  {'_'*(max_length-2)}  \n"
    clipped_text += f" /{' '*max_length}\\\n"
    for line in lines:
        clipped_text += f"| {text_align.get(align, get_center)(line, max_length)} |\n"

    clipped_text += f" \\{'_'*max_length}/\n"
    clipped_text += "   ____   |   /         \n"
    clipped_text += "  /    \\  |  /          \n"
    clipped_text += " /      \\ | /           \n"
    clipped_text += "|        ||/            \n"
    clipped_text += "| |(o)(o)|              \n"
    clipped_text += "| |      |              \n"
    clipped_text += "| | | |  |              \n"
    clipped_text += "\\ \\ \\_/  /              \n"
    clipped_text += " \\ \\____/ /             \n"
    clipped_text += "  \\______/              \n"
    clipped_text += "\n"
    
    return clipped_text
def init_cmdline():
    parser = argparse.ArgumentParser(
        prog="pclip",
        description="Have a paperclip say what you mean."
    )
    parser.add_argument("-c", "--center", action="store_true", help="Center the text")
    parser.add_argument("-l", "--left", action="store_true", help="Center the text")
    parser.add_argument("-r", "--right", action="store_true", help="Center the text")
    parser.add_argument("-f", "--file", nargs="?", default="", help="File to load text from, use this or text, never both")
    parser.add_argument("-t","--text", nargs="?", default="", help="Text to display, use this or file, never both")
    return parser.parse_args()

def main():
    args = init_cmdline()
    
    align = (1*args.left) | (2*args.right)
    
    if args.text != "":
        print(clipify_text(args.text, align))
    elif args.file !="":
        print(clipify_file(args.file, align))
    
if __name__ == '__main__':
    main()