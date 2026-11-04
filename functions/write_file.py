import os

from openai.types.chat.chat_completion_tool_union_param import ChatCompletionToolUnionParam

schema_write_file: ChatCompletionToolUnionParam = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "write new content to a file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path for the file that will be written to, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                  "type": "string",
                  "description": "the content that will be written to the file.",
                },
                "required": ["file_path", "content"],
            },
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        file_dir_path: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(file_dir_path, file_path))
        valid_target_dir: bool = os.path.commonpath([file_dir_path, target_dir]) == file_dir_path

        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        else:
            os.makedirs(os.path.dirname(target_dir), exist_ok=True)
            with open(target_dir, "w") as f:
                if f.write(content) > 0:
                    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
                else:
                    return f"Error: Failed to write to {file_path}."
    except Exception as e:
        return f"Error: {e}"
