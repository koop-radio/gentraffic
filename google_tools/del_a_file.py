import subprocess

# Define the path of the file you want to delete
file_path = r'C:\path\to\your\file.txt'

# Construct the command to delete the file
command = f'del /f /q "{file_path}"'

# Execute the command
result = subprocess.run(command, shell=True, text=True, capture_output=True)

# Check if the command was successful
if result.returncode == 0:
    print("File deleted successfully.")
else:
    print(f"Error deleting file: {result.stderr}")
