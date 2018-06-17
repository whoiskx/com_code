import os

dir_file = os.path.abspath(__file__)
dir_folder = os.path.dirname(dir_file)
dir_x = os.path.basename(dir_file)

print(dir_file, dir_folder, '\n', dir_x)

def foo(folder):
    while True:
        if os.path.isdir(folder):
            return foo()