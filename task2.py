import os, sys, shutil, hashlib, json

directory_path = sys.argv[1]
outer_dict = {}
count=0

def make_json():
    for root, directories, files in os.walk(directory_path):
        for filename in files:
            
            file_path = os.path.join(root, filename)
            file_size = os.path.getsize(file_path)
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as file:
                    chunk = file.read(4096)  # Read 4096 bytes at a time
                    while chunk:
                        hash_md5.update(chunk)
                        chunk = file.read(4096)
                        md5_hash = hash_md5.hexdigest()


            inner_dict = {"filename": filename, "filepath": file_path, "filesize" : file_size, "md5_hash" : md5_hash}
            count+=1
            outer_dict["fileNo.{}".format(count)] = inner_dict  # Insert inner_dict into outer_dict

    with open("my_data.json", "w") as file:
        json.dump(outer_dict, file,  indent=4)
        
make_json()        

#bonus solution : 
def copy_directory():
    for root, directories, files in os.walk(directory_path):
        for filename in files:
            
            file_path = os.path.join(root, filename)
            with open(file_path, "r") as file:  # Open the file in read mode
                contents = file.read()  # Read the entire contents into a string
            file_path2 = os.path.join(root+"_copied",os.path.splitext(filename)[0]+ "_copied"+os.path.splitext(filename)[1])
            os.makedirs(os.path.dirname(file_path2), exist_ok=True)
            with open(file_path2, "w") as file:
                file.write(contents)
        root =  root+"_copied"        
     
# copy_directory()            
            

def copy_files_and_update_json(source_dir, destination_dir, json_file_path):
    """
    Copies all files from the specified directory to a new directory, keeping the same file structure.
    Updates the JSON file with the new file paths in the copied directory.
    """

    shutil.copytree(source_dir, destination_dir, copy_function=shutil.copy2)  # Preserve metadata

    with open(json_file_path, 'r') as f:
        data = json.load(f)

    for file_info in data.values():  # Iterate over nested file information dictionaries
        if isinstance(file_info.get('filepath'), str) and os.path.isfile(file_info['filepath']):  # Check for file path
            old_path = os.path.join(source_dir, file_info['filepath'])
            new_path = os.path.join(destination_dir, file_info['filepath'])
            file_info['filepath'] = os.path.relpath(new_path, os.path.dirname(json_file_path))  # Update nested path

    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)            
copy_files_and_update_json(directory_path, directory_path+"_copied2","my_data.json")