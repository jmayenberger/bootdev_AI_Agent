import subprocess
from functions.get_files_info import check_create_abs_paths


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
    

