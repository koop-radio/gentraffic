import os
import datetime

def list_recent_kdrive_files(num_files=10):
    directory = "k:/DAD/Files/PLAYLIST"
    # Get a list of files in the directory
    try:
        files = os.listdir(directory)
    except:
        return f"directory {directory} not found"

    # Create a list of tuples containing the file path and modification time
    file_info = [(os.path.join(directory, file), os.path.getmtime(os.path.join(directory, file))) for file in files]

    # Sort the list based on the modification time in descending order
    file_info.sort(key=lambda x: x[1], reverse=True)

    # Get the specified number of most recent files
    recent_files = file_info[:num_files]
    #print("recent_files is ",recent_files)

    # Print the most recent files
    recent_files_info = f"\n{num_files} most recent files in the directory:\n\n"
    for file, mtime in recent_files:
        timestamp = datetime.datetime.fromtimestamp(mtime)
        recent_files_info += f"    {file} (Modified: {timestamp})\n"
    return recent_files_info

def main():
    # Specify the directory path using Windows-style notation

    # Call the function to list the 10 most recent files
    print(list_recent_kdrive_files())

if __name__ == "__main__":
    main()
