import os
import subprocess

from openai.types.chat.chat_completion_tool_union_param import ChatCompletionToolUnionParam

schema_run_python_file: ChatCompletionToolUnionParam = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run the python file or execute it in a specified directory relative to the working directory, providing arguments for the execution command is optional.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path for the python file to be run, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                  "type": "array whos items are strings",
                  "description": "a list containin all the arguments that might be passed to the run command, that will be used to run the script.",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        file_dir_path: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(file_dir_path, file_path))
        valid_target_dir: bool = os.path.commonpath([file_dir_path, target_dir]) == file_dir_path

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        else:
            command: list[str] = ["python", target_dir]

            if (args is not None) and (len(args) != 0):
                for arg in args:
                    command.extend(arg)

            command_result: subprocess.CompletedProcess = subprocess.run(
                args=command,
                cwd=working_directory,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if command_result.returncode != 0:
                return f"Process exited with code {command_result.returncode}"
            elif (command_result.stderr != "") and (command_result.stdout != ""):
                return "No output produced"
            else:
                stdout_result: str = f"STDOUT: {command_result.stdout}"
                stderr_result: str = f"STDERR: {command_result.stderr}"
                return stdout_result + "\n" + stderr_result


    except RuntimeError as e:
        return (f"Error: executing Python file: {e}")
