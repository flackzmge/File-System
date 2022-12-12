# File-System

This is a Python object-oriented program that creates a virtual file system. It contains a PlainFile, Directory, and FileSystem class.

# Usage

To use this program, create an instance of the FileSystem class and use the available methods to manipulate the virtual file system.

# Classes

PlainFile
This class represents a plain file in the file system. It has the following methods:

chown(user: str, group: str): Changes the owner and group of the file
chmod(permissions: str): Changes the permissions of the file
Directory
This class represents a directory in the file system. It has the following methods:

ls(): Lists the files and directories inside the current directory
mkdir(name: str): Creates a new directory inside the current directory
cd(name: str): Changes the current directory to the specified directory
cd_up(): Changes the current directory to the parent directory
FileSystem
This is the main class that represents the file system. It has the following methods:

pwd(): Prints the current working directory
create_file(name: str, content: str): Creates a new plain file with the given name and content inside the current directory
rm(name: str): Deletes the file or directory with the given name inside the current directory
find(name: str): Searches for a file or directory with the given name inside the current directory and all of its subdirectories



Additionally, the FileSystem class has the following attributes:

root: This is the root directory of the file system. It is the starting point for all file system operations.
cwd: This is the current working directory. It represents the directory that the user is currently in.
Examples

Here are some examples of how to use the FileSystem class:


# Create a new instance of the FileSystem class
fs = FileSystem()

# Print the current working directory
fs.pwd()  # Output: /

# Create a new file inside the current directory
fs.create_file("hello.txt", "Hello, world!")

# Change the current directory to a subdirectory
fs.cd("documents")

# Create a new directory inside the current directory
fs.mkdir("new_folder")

# Change the current directory to the new_folder directory
fs.cd("new_folder")

# Create a new file inside the new_folder directory
fs.create_file("hello.txt", "Hello from the new folder!")

# Print the current working directory
fs.pwd()  # Output: /documents/new_folder

# Print the current working directory
fs.pwd()  # Output: /documents

# Search for a file with the name "hello.txt"
fs.find("hello.txt")  # Output: /documents/new_folder/hello.txt

# Delete the file with the name "hello.txt" inside the new_folder directory
fs.rm("hello.txt")

# List the files and directories inside the current directory
fs.ls()  # Output: ["new_folder"]

# Delete the new_folder directory
fs.rm("new_folder")

# List the files and directories inside the current directory
fs.ls()  # Output: []
