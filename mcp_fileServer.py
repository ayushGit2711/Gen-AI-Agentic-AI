from mcp.server.fastmcp import FastMCP
import os
import shutil


mcp = FastMCP("PersonalFileSystem")


@mcp.tool()
def addFile(filename: str):
   """Create a new file in given directory"""
   if not os.path.exists(filename):
       with open(filename, "w") as f:
           pass
       print(f"File '{filename}' created.")
   else:
       print(f"File '{filename}' already exists.")


@mcp.tool()
def addFolder(directory_name: str):
   """Create a new Directory in given directory"""
   if not os.path.exists(directory_name):
       os.mkdir(directory_name)
       print(f"Directory '{directory_name}' created.")
   else:
       print(f"Directory '{directory_name}' already exists.")

@mcp.tool()
def deleteFile(filename: str):
    """Delete a file in the given directory"""
    if os.path.exists(filename):
        if os.path.isfile(filename):
            os.remove(filename)
            print(f"File '{filename}' deleted.")
        else:
            print(f"'{filename}' exists but is not a file.")
    else:
        print(f"File '{filename}' does not exist.")

@mcp.tool()
def deleteFolder(directory_name: str):
    """Delete a directory if it exists and is a directory.

    Args:
        directory_name (str): Path to the directory to delete.

    Returns:
        str: Status message.
    """
    try:
        if os.path.exists(directory_name):
            if os.path.isdir(directory_name):
                shutil.rmtree(directory_name)
                return f"Directory '{directory_name}' deleted."
            else:
                return f"'{directory_name}' exists but is not a directory."
        else:
            return f"Directory '{directory_name}' does not exist."
    except Exception as e:
        return f"Error deleting directory '{directory_name}': {e}"


if __name__ == "__main__":
   mcp.run(transport="stdio")