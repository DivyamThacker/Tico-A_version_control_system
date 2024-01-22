import argparse, os , sys ,datetime, hashlib ,json

argparser = argparse.ArgumentParser(description="This is the Main program that tracks your files :)")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case "init": cmd_init(args)
        case "add" : cmd_add(args)
        case "status" : cmd_status(args)
        case _ : print("Bad Command")

argsp = argsubparsers.add_parser("init", help="Initialize a new, empty repository.")

argsp.add_argument("path",
                   metavar="directory",
                   nargs="?",
                   default=".",
                   help="Where to create the repository.")

argsp = argsubparsers.add_parser("add", help="Track all the files in the current directories and sub directories")    

argsp.add_argument("path",
                   metavar="directory",
                   nargs="?",
                   default=".",
                   help="from where to add all the new files to tracking")

def cmd_init(args):
    username = input("Set the username as .. ")
    paths = [".tico",".tico/branches",".tico/objects", ".tico/branches/main"]
    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)
    file_paths = ["added.json", "index.json", "users.txt"]
    for file_path in file_paths:
        file_path = os.path.join(".tico/branches/main", file_path)
        if os.path.exists(file_path):
            print("File already exists!")
        else:
            with open(file_path, "a") as file:
                if (os.path.basename(file_path)=="users.txt"):
                    now = datetime.datetime.now()
                    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")  # Output: 2024-01-23 14:25:30
                    timestamp = now.timestamp()  # Output (example): 1690546730.0
                    file.write(f"{formatted_datetime} {timestamp} {username}" + os.linesep) 
                else : pass
def add_file_to_tracking(filename, valid_json_files):
    try:
        with open(filename, "rb") as file:
            content = file.read()
            hash_object = hashlib.md5(content)
            md5_hash = hash_object.hexdigest()

        for json_file in valid_json_files:
            try:
                with open(json_file, "r") as f:
                    data = json.load(f)

                if filename not in data:
                    # Update the dictionary with the new key-value pair
                    data.update({filename: md5_hash})

                with open(json_file, "w") as file:
                    json.dump(data, file, indent=4)
                    print(f"Successfully added '{filename}' and hash to '{json_file}'")

            except Exception as e:
                print(f"Error writing to '{json_file}': {e}")

    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
    

def cmd_add(args):
    valid_json_files = [".tico/branches/main/index.json", ".tico/branches/main/added.json"]
    data = None
    if os.path.isdir(args.path):
        for root, _, files in os.walk(args.path):
            for filename in files:
                filepath = os.path.join(root, filename)
                add_file_to_tracking(filepath, valid_json_files)
    else:
        add_file_to_tracking(args.path, valid_json_files)

argsp = argsubparsers.add_parser("status", help="Check the status of all the files in your directory")    

argsp.add_argument("path",
                   metavar="directory",
                   nargs="?",
                   default=".",
                   help="for which directory do you want to check the status of files")
        
def cmd_status(args):
    untracked_files = []
    directory_path = args.path
    with open(".tico/branches/main/index.json", "r") as file:
        content = json.load(file)
    for root, _, files in os.walk(directory_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                if filepath not in content.values():
                    untracked_files.append(filepath)
    print(untracked_files)
    return untracked_files        

