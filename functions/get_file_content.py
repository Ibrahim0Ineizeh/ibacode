import os

from config import MAX_READ_CHAR

from openai.types.chat.chat_completion_tool_union_param import ChatCompletionToolUnionParam

schema_get_file_content: ChatCompletionToolUnionParam = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Get the file content in a specified directory relative to the working directory, the function will only take up to 10_000 characters if the file is too large.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path to get the contents from, relative to the working directory (default is the working directory itself)",
                },
            },
            "required": ["file_path"],
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        file_dir_path: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(file_dir_path, file_path))
        valid_target_dir: bool = os.path.commonpath([file_dir_path, target_dir]) == file_dir_path

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(target_dir, "r") as f:
                file_content_string: str = f.read(MAX_READ_CHAR)
                if f.read(1):
                    file_content_string += f'[...File "{file_path}" truncated at {MAX_READ_CHAR} characters]'
                return file_content_string
    except Exception as e:
        return f"Error: {e}"
