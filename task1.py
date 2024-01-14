import os, sys, shutil

path = input("Enter the directory path that you want to organize :  ")

#Getting input using command line
# path = sys.argv[1]

path = os.path.abspath(path)

directories_created = set()  # Set to track created directories
existing_directories = set(os.listdir(path))  # Store existing directories at the start

for root, directories, files in os.walk(path, topdown=False):  # Reverse order for efficient checks
    for file in files:
        file_path = os.path.join(root, file)

        extension_without_dot = os.path.splitext(file_path)[1][1:]
        dir_path = os.path.join(root, f"{extension_without_dot} files")

        if dir_path not in directories_created:  # Create directory if not already created
            os.mkdir(dir_path)
            directories_created.add(dir_path)

        try:
            shutil.move(file_path, dir_path)
            print("File moved successfully!")
        except shutil.Error as error:
            print("Error moving file:", error)

    directories[:] = [d for d in directories if d in existing_directories]  # Filter newly created directories


