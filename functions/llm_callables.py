import os
import subprocess
from config import MAX_CHARS
from functions.internal import check_create_abs_paths

# Writes input content to a file at the specified file path. Constrained to the working directory
def write_file(working_directory, file_path, content):
    try:
        working_directory_abs, file_path_abs = check_create_abs_paths(working_directory, file_path=file_path, write=True)
    except (ValueError, FileNotFoundError, PermissionError) as e:
        return e
    try:
        os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)
    except:
        return f'Error: could not generate missing directories for "{file_path}"'
    if os.path.exists(file_path_abs) and os.path.isdir(file_path_abs):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        with open(file_path_abs, "w") as f:
            written_chars = f.write(content)
    except:
        return f'Error: could not write to {file_path}'
    return f'Successfully wrote to "{file_path}" ({written_chars} characters written)'

# Reads and returns the first MAX_CHARS characters of the content from a specified file within the working directory
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

# Lists files in the specified directory along with their sizes, constrained to the working directory
def get_files_info(working_directory, directory=None):
    if not directory:
        directory = "."
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

# Executes a python file at the specified file path with the given input arguments. Returns the output from the interpreter .File path constrained to the working directory
def run_python_file(working_directory, file_path, args=[]):
    try:
        working_directory_abs, file_path_abs = check_create_abs_paths(working_directory, file_path=file_path)
    except (ValueError, FileNotFoundError, PermissionError) as e:
        return e
    
    if not file_path_abs.endswith(".py"):
        return f'Error: {file_path} is not a Python file'
    try:
        command = ["python3", file_path_abs] + args
        completed_process = subprocess.run(
            command,
            capture_output=True,
            timeout=30,
            text=True,
            cwd=working_directory_abs
            )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    out = f'Executed "python3 {file_path} {" ".join(args)}\n"'
    if completed_process.returncode != 0:
        out += f"Process exited with code {completed_process.returncode}"
    else:
        if completed_process.stdout:
            out += f"STDOUT: {completed_process.stdout}\n"
        if completed_process.stderr:
            out += f"STDERR: {completed_process.stderr}\n"
        if not completed_process.stdout and not completed_process.stderr:
            out += "No output produced.\n"
    return out
