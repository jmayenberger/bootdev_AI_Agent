import os
from config import MAX_CHARS

#returns contents of a file at file_path as a string. Does security checks first
def get_file_content(working_directory, file_path, max_chars=MAX_CHARS):
    try:
        working_directory_abs, file_path_abs = check_create_abs_paths(working_directory, file_path=file_path)
    except (ValueError, FileNotFoundError, PermissionError) as e:
        return e
    try:
        with open(file_path_abs, "r") as f:
            file_content_string = f.read(int(max_chars))
    except:
        return f'Error: could not read {file_path}'
    if len(file_content_string) >= max_chars:
        file_content_string += f'\nFile "{file_path}" truncated at {max_chars} characters'
    return file_content_string

#returns a list of files in directory as a string. Does security checks first
def get_files_info(working_directory, directory=""):
    try:
        working_directory_abs, directory_abs = check_create_abs_paths(working_directory, directory=directory)
    except (ValueError, FileNotFoundError, PermissionError) as e:
        return e
    
    output = []
    for file in os.listdir(directory_abs):
        file_path = os.path.join(working_directory, directory, file)
        file_path_abs = os.path.join(directory_abs, file)
        try:
            file_size = os.path.getsize(file_path_abs)
        except:
            return f'Error: could not get filesize of "{file_path}"'
        try:
            is_dir = os.path.isdir(file_path_abs)
        except:
            return f'Error: could not verify if "{file_path}" is a directory or not'
        output.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")
    if len(output) == 0:
        output.append(f'no files found in "{directory}"')
    return "\n".join(output)

#checks that destination lies inside working_directory. Raises Exception if not and returns abs paths otherwise
def check_create_abs_paths(working_directory, directory=None, file_path=None):
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
        raise Exception("missing target input in check_create_abs_paths")
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
    elif not is_dir and not os.path.isfile(target_abs):
        raise FileNotFoundError(f'Error: "{file_path}" is not a file')
    
    if not target_abs.startswith(working_directory_abs):
        raise PermissionError(f'Error: Cannot list "{target}" as it is outside the permitted working directory')
    
    return working_directory_abs, target_abs
