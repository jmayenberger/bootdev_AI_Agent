import os

# checks that destination lies inside working_directory. Raises Exception if not and returns abs paths otherwise
def check_create_abs_paths(working_directory, directory=None, file_path=None, write=False):
    #checks for working directory
    if not isinstance(working_directory, str):
        raise ValueError(f'Error: not a string: "{working_directory}"')
    try:
        working_directory_abs = os.path.abspath(working_directory)
    except:
        raise FileNotFoundError(f'Error: could not generate absolute path for "{working_directory}"')
    if not os.path.isdir(working_directory_abs):
        raise FileNotFoundError(f'Error: "{working_directory}" is not a directory')
    
    #checks for target
    if directory is None and file_path is None:
        raise Exception("Unexpected Error: missing target input in check_create_abs_paths")
    is_dir = directory is not None
    target = directory if is_dir else file_path
    if not isinstance(target, str):
        raise ValueError('Error: not a string: "{target}"')
    try:
        target_abs = os.path.abspath(os.path.join(working_directory, target))
    except:
        raise FileNotFoundError('Error: could not generate absolute path for "{target}"')
    if is_dir and not os.path.isdir(target_abs):
        raise FileNotFoundError(f'Error: "{directory}" is not a directory')
    elif not is_dir and not write and not os.path.isfile(target_abs):
        raise FileNotFoundError(f'Error: "{file_path}" is not a file')
    
    if not target_abs.startswith(working_directory_abs):
        raise PermissionError(f'Error: Cannot access "{target}" as it is outside the permitted working directory')

    return working_directory_abs, target_abs
