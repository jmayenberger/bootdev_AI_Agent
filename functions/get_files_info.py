import os

def get_files_info(working_directory, directory=""):
    if not isinstance(working_directory, str):
        return 'Error: not a string: "{working_directory}"'
    if not isinstance(directory, str):
        return 'Error: not a string: "{directory}"'
    try:
        working_directory_abs = os.path.abspath(working_directory)
    except:
        return 'Error: could not generate absolute path for "{working_directory}"'
    try:
        directory_abs = os.path.abspath(os.path.join(working_directory, directory))
    except:
        return 'Error: could not generate absolute path for "{directory}"'
    if not os.path.isdir(directory_abs):
        return f'Error: "{directory}" is not a directory'
    if not os.path.isdir(working_directory_abs):
        return f'Error: "{working_directory}" is not a directory'
    if not directory_abs.startswith(working_directory_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    output = ""
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
            return f'Error: could not verify if "{file_path}" is a directory'
        output += f"- {file}: file_size={file_size} bytes, is_dir={is_dir}\n"
    if output == "":
        return f'no files found in "{directory}"'
    return output[:-1]