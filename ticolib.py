import argparse, os , sys ,datetime, hashlib ,json, base64, shutil

argparser = argparse.ArgumentParser(description="This is the Main program that tracks your files :)")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case "init": cmd_init(args)
        case "add" : cmd_add(args)
        case "status" : cmd_status(args)
        case "commit" : cmd_commit(args)
        case "rmcommit":  cmd_rmcommit(args)
        case "rmadd" : cmd_rmadd(args)
        case "push" : cmd_push(args)
        case "create_user": cmd_create_user(args)
        case "set_user": cmd_set_user(args)
        case "show_user" : cmd_show_user(args)
        case "checkout" : cmd_checkout(args)
        case "log" : cmd_log(args)
        case "revert": cmd_revert(args)
        case "help": welcome()
        case _ : print("Bad Command")
        
argsp = argsubparsers.add_parser("help", help="Get to know about all the commands")        
def welcome():
    print("tico help - to get help of the available commands")
    print("tico init - Initialize a new Tico repository")
    print("tico add <file> - Add a file to the index")
    print("tico status - to see status")
    print("tico commit -m <message> - Commit changes with a message")
    print("tico rmcommit - remove last commit")
    print("tico rmadd <file> - remove a file from the index")
    print("tico log - Display commit log")
    print("tico checkout <commit> - Checkout a specific commit")
    print("tico show_user  - to see present user")
    print("tico create_user  - to create new user")
    print("tico set_user <username> - to change user")
    print("tico push <path> - to push your file to another folder")
    print("tico revert- to revert the changes done in the previous commit")

argsp = argsubparsers.add_parser("init", help="Initialize a new, empty repository.")

argsp.add_argument("path",
                   metavar="directory",
                   nargs="?",
                   default=".",
                   help="Specify where to create the repository.")

argsp = argsubparsers.add_parser("add", help="Track all the files in the current directories and sub directories")    

argsp.add_argument("path",
                   metavar="directory",
                   nargs="?",
                   default=".",
                   help="from where to add all the new files to tracking")

def cmd_init(args):
    directory_path = args.path
    paths = [".tico",".tico/branches", ".tico/branches/main"] #  put this if needed ,".tico/objects"
    for path in paths:
        # if directory_path != ".":
        path = os.path.join(directory_path,path)
        if not os.path.exists(path):
            os.mkdir(path)
    if os.path.exists(".tico/branches/main/commits.json"):
        print("Root Commit Already Exists!")
        return        
    file_paths = ["added.json", "index.json", "users.txt"]
    for file_path in file_paths:
        file_path = os.path.join(directory_path,".tico/branches/main", file_path)
        if os.path.exists(file_path):
            print("File already exists!")
        else:
            with open(file_path, "w") as file:
                if not os.path.basename(file_path) =="users.txt":
                    file.write("{}")
    if not os.path.exists(".tico/branches/main/commits.json"):                
        create_user(directory_path) 
        create_root_commit()
            
argsp = argsubparsers.add_parser("set_user", help="set the current user")
argsp.add_argument("username", help="Username of the current user")                
                
def cmd_set_user(args):
    file_path = ".tico/branches/main/users.txt"
    if not os.path.exists(file_path):
        print("You need to initialize tico with 'tico init' command before performing this action")
        return 
    username = args.username
    with open(file_path, "r") as file:  
        lines = file.readlines()
        
    for line in lines:
        words = line.split()  # Split the line into words
        if  words and words[-1] == username:  # Check if the last word is equal to username
            lines.pop()
            lines.append(f"Current User: {username}")
            print(f"Successfully set the Current User to {username}")
            with open(file_path, "w") as file:  # Open the file in write mode ("w")
                file.writelines(lines)  # Write all lines from the list
            return  # Exit the loop once the name is found
    print("No Such Users Exist, you first need to create the user using 'tico create_user' command")
        
        
        
                
def create_user(directory_path=".", username=None):
    file_path = ".tico/branches/main/users.txt"
    file_path=os.path.join(directory_path, file_path)
    if username==None:
        username = input("Set the username as .. ")
    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")  # Output: 2024-01-23 14:25:30
    timestamp = now.timestamp()  # Output (example): 1690546730.0
    with open(file_path, "r") as file:  
        lines = file.readlines()
    if len(lines) > 1:
        lines.pop()
        
    lines.append(f"{formatted_datetime} {timestamp} {username}")   
    lines.append(f"\nCurrent User: {username}")   
    with open(file_path, "w") as file:  # Open in append mode ("a")
        for line in lines:
            file.write(line)
        
        
argsp = argsubparsers.add_parser("create_user", help="create a new user")
argsp.add_argument("username", help="Username of the current user")

def cmd_create_user(args):
    username = args.username
    file_path = ".tico/branches/main/users.txt"
    # file_path=os.path.join(directory_path, file_path)
    if not os.path.exists(file_path):
        print("You need to initialize tico with 'tico init' command before performing this action")
        return
    with open(file_path, "r") as file:  
        lines = file.readlines()
        
    for line in lines:
        words = line.split()  # Split the line into words
        if words and words[-1] == username:  # Check if the last word is equal to username
            print("This user aldready exists.")
            return  # Exit the function if the name is found
    create_user(".", username)
    
    
    
                    
def add_file_to_tracking(filepath, valid_json_files):
    try:
        with open(filepath, "rb") as file:
            content = file.read()
            hash_object = hashlib.md5(content)
            md5_hash = hash_object.hexdigest()

        for json_file in valid_json_files:
            try:
                with open(json_file, "r") as f:
                    data = json.load(f)

                # Update the dictionary with the new key-value pair
                data.update({filepath: md5_hash})

                with open(json_file, "w") as file:
                    json.dump(data, file, indent=4)
                    if (json_file==".tico/branches/main/index.json"):
                        print(f"Successfully added '{filepath}'")

            except Exception as e:
                print(f"Error writing to '{json_file}': {e}")

    except Exception as e:
        print(f"Error reading file '{filepath}': {e}")
    

def cmd_add(args):
    valid_json_files = [".tico/branches/main/index.json", ".tico/branches/main/added.json"]
    data = None
    if os.path.isdir(args.path):
        for root, _, files in os.walk(args.path):
            for filename in files:
                filepath = os.path.join(root, filename)
                if (len(filepath)>6 and filepath[:6] == ".tico"):
                    print(f"Adding {filepath} to tracking files Failed because it is inside '.tico' directory")
                    continue
                add_file_to_tracking(filepath, valid_json_files)
    else:
        filepath = args.path
        if (len(filepath)>6 and filepath[:6] == ".tico"):
            print(f"Cannot add files inside '.tico' directory to tracking!")
            return
        add_file_to_tracking(filepath, valid_json_files)

argsp = argsubparsers.add_parser("status", help="Check the status of all the files in your directory")    

argsp.add_argument("path",
                   metavar="directory",
                   nargs="?",
                   default=".",
                   help="for which directory do you want to check the status of files")

def calculate_status(directory_path=".", doPrint=True, deleteFromIndex=False):
    untracked_files = []
    modified_files=[]
    added_files=[]
    deleted_files=[]
    all_files=[]
    with open(".tico/branches/main/added.json", "r") as file:
        json_content = json.load(file)
    for root, _, files in os.walk(directory_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                filepath = filepath[2:]
                if not filepath or not filepath[0].isalpha():
                    continue
                all_files.append(filepath)
                with open(filepath, "rb") as file:
                    file_content = file.read()
                    hash_object = hashlib.md5(file_content)
                    md5_hash = hash_object.hexdigest()
                if filepath not in json_content.keys():
                    untracked_files.append(filepath)
                if filepath in json_content.keys() and json_content[filepath] != md5_hash:
                    modified_files.append(filepath)
                elif filepath in json_content.keys():
                    added_files.append(filepath)     
    for filepath in json_content.keys():
        if filepath not in all_files:
            deleted_files.append(filepath)
    # delete files from index.json that are in deleted_files
    if deleteFromIndex:
        with open (".tico/branches/main/index.json", "r") as file:
            index_content = json.load(file)
        my_dict = {}
        for file in index_content.keys():
            if file not in deleted_files:
                my_dict[file]= index_content[file]    
        with open(".tico/branches/main/index.json", "w")as f:
            json.dump(my_dict, f, indent=4)    
                
    if doPrint:        
        for filepath in added_files:
            print(f"Added file:       {filepath}") 

        for filepath in modified_files:
            print(f"Modified file:    {filepath}") 

        for filepath in untracked_files:
            print(f"Untracked file:   {filepath}")
                                            
                                        
        for filepath in deleted_files:
            print(f"Deleted file:     {filepath}")
            
        # for filepath in all_files:
        #     print(f"All file:   {filepath}")
        return
    
    return  deleted_files, untracked_files, modified_files, added_files, all_files                                    
    

        
def cmd_status(args):
    directory_path = args.path
    calculate_status(directory_path=args.path)
    

argsp= argsubparsers.add_parser("commit", help="Commit the added changes.")

argsp.add_argument("-m", dest="messageFlag", action="store_true", help="specify it if you want to write message for the commit")
argsp.add_argument("message",default="",help="specify message for the commit")


def get_current_author(directory_path="."):
    file_path = os.path.join(directory_path, ".tico", "branches", "main","users.txt")
    if not os.path.exists(file_path):
        print("You first need to run 'tico init' command")
        return
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines[-1].split()[-1]    

class Commit:
    def __init__(self, message, author, parent=None, modified_files=None):
        self.message = message
        self.author = author
        self.parent = parent
        self.modified_files = modified_files
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Capture creation time
        self.files = {}  # Store a dictionary of changed files and their contents
        self.file_hash={} #store a dictionary of filename and its md5 hash
        self.add_files()

    def add_files(self, json_file_path = ".tico/branches/main/index.json"): #adds tracked files that are in index.json
        json_file_path = os.path.join(".",json_file_path)
        with open(json_file_path, "r") as f:
            all_files = json.load(f)
            all_file_keys =  list(all_files.keys())
        files = {}    
        for file in all_file_keys:
            # if self.modified_files and file in self.modified_files:
            #     continue  # Skip files already in modified_files
            self.file_hash[file] = all_files[file]
            files[file] = self.read_file(file)
        self.files = files     

    def read_file(self, file_path):
        with open(file_path, "r") as f:
            content = f.read()
            content_bytes = str(content).encode("utf-8")  # Use utf-8 for wider character support
            base64_bytes = base64.b64encode(content_bytes) 
            base64_string = base64_bytes.decode("ascii") 
        return base64_string    
        
    def get_commit_info(self):
        return f"Message: {self.message}\nAuthor: {self.author}\nTimestamp: {self.timestamp}"

    # Simplified method to simulate creating a new commit based on changes
    def create_child_commit(self, message, author):
        child = Commit(message, author, parent=self)
        return child

    def __dict__(self):
        return {"message": self.message, "author": self.author, "parent":self.parent, "timestamp":self.timestamp, "file_hash":self.file_hash,
                "files":self.files}
        
def create_root_commit():
    message="This is the root commit of main branch"
    author=get_current_author()
    file_path = ".tico/branches/main/commits.json"
    commit = Commit(message, author)
    data = commit.__dict__()
    md5_hash = hashlib.md5()
    md5_hash.update(str(commit).encode())  # Encode as bytes for hashing
    hashed_value = md5_hash.hexdigest()
    my_dict = {}
    my_dict[hashed_value] = data
    with open(file_path, 'w') as f:
        json.dump(my_dict, f, indent=4)
    

def get_last_commit():
    file_path = ".tico/branches/main/commits.json"
    if not os.path.exists(file_path):
        print("Root Commit does not exists")
        return
    with open(file_path, "r") as file:
        data = json.load(file)
        last_commit  = list(data.keys())[-1]
    return last_commit

def empty_tracked_files():
    file_paths = [".tico/branches/main/added.json", ".tico/branches/main/index.json"]
    for file_path in file_paths:
        with open(file_path, "w") as f:
            f.write("{}")
 
def cmd_commit(args):
    modified_files = calculate_status(doPrint=False)[2]
    # if len(modified_files) >0:
    #     print("There are modified files whose changes are not tracked, do 'tico add <filename>' to track it.")
    calculate_status(deleteFromIndex=True, doPrint=False)
    file_path = ".tico/branches/main/commits.json"
    if not args.messageFlag:
        message = input("Please Enter a short description of this commit... ")
    else:    
        message = args.message
    author = get_current_author()
    parent = get_last_commit()    
    commit  = Commit(message,author,parent, modified_files=modified_files)
    commit.add_files()
    data = commit.__dict__()
    md5_hash = hashlib.md5()
    md5_hash.update(str(commit).encode())  # Encode as bytes for hashing
    hashed_value = md5_hash.hexdigest()
    with open(file_path, "r") as file:
        my_dict = json.load(file)
    
    my_dict[hashed_value] = data
    with open(file_path, 'w') as f:
        json.dump(my_dict, f, indent=4)
    empty_tracked_files() # Empty the tracking files in index.json after commiting them
        
        
argsp=  argsubparsers.add_parser("rmcommit", help="remove specified or last commit")
argsp.add_argument("--hash", dest="hash",action="store",   nargs="?", help="Specify the hash of the commit that you want to delete")   

def rmcommit():
    file_path=".tico/branches/main/commits.json"
    with open (file_path, "r") as file:
        content = json.load(file)
    last_key = list(content.keys())[-1]    
    del content[last_key]
    with open (file_path, "w") as file:    
        json.dump(content,file, indent=4)

def cmd_rmcommit(args):
    file_path=".tico/branches/main/commits.json"
    flag=None
    with open (file_path, "r") as file:
        content = json.load(file)
        last_key = list(content.keys())[-1]
    if args.hash:
        hash = args.hash  #UnComment the below code if you want to update the parent of commit which has removed commit as its parent commit
        # parent_hash = content[hash]["parent"]
        # for key, value in content.items():
        #     if key==hash:
        #         flag=1
        #     if flag==1:
        #         value["parent"] = parent_hash    
        del content[hash]
        with open (file_path, "w") as file:    
            json.dump(content,file, indent=4)     
    else :    
        rmcommit()
        
argsp = argsubparsers.add_parser("rmadd", help="Remove the file or directory from tracking")
argsp.add_argument("file_path", default=".", help="specify the path of file or directory that you want to untrack")

def rmadd(filepath):
    json_file_paths =[".tico/branches/main/index.json", ".tico/branches/main/added.json"]
    for json_file_path in json_file_paths:
        with open(json_file_path, "r") as f:
            my_dict = json.load(f)
        if filepath in my_dict:    
            del my_dict[filepath]
        elif json_file_path == ".tico/branches/main/index.json": print(f"{filepath} is already an untracked file or it doesn't exists")

        with open(json_file_path, "w") as f:
            json.dump(my_dict, f, indent=4)

def cmd_rmadd(args):
    file_path=args.file_path
    if os.path.isdir(file_path):
        for root, _ , files in os.walk(file_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                filepath = filepath[2:]
                rmadd(filepath)
    else:
        rmadd(file_path)

argsp = argsubparsers.add_parser("push", help="Push all the files in the last commit into your destination folder")
argsp.add_argument("directory_path", help="Specify the destination folder of the files in the commit")

def cmd_push(args):
    directory_path = args.directory_path
    json_file_path = ".tico/branches/main/commits.json"
    with open(json_file_path, "r") as f:
        content = json.load(f)
    last_key = list(content.keys())[-1]
    last_value = content[last_key]
    for file_path, encoded_file_content in last_value["files"].items():
        file_content = base64_decode(encoded_file_content)
        path = os.path.join(directory_path, file_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(file_content) 

argsp = argsubparsers.add_parser("show_user", help="To show the details about the Current User")

def cmd_show_user(args):
    curr_author = get_current_author()
    if (curr_author):
        with open(".tico/branches/main/users.txt", "r") as f:
            lines = f.readlines()
        for line in lines:
            if line.split()[-1] == curr_author:
                print(f"Current User : {line.split()[-1]}\nCreated On   : {line.split()[0]}\nCreated At   : {line.split()[1]}")
                return
    else:
        print("Failed to get the current author")     
                   
def base64_decode(string):
    base64_bytes = string.encode("ascii")

    # Handle missing padding if necessary
    missing_padding = len(base64_bytes) % 4
    if missing_padding:
        base64_bytes += b'=' * (4 - missing_padding)

    try:
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("utf-8")  # Use utf-8 for decoding
        return sample_string
    except :
        print("Error decoding Base64 string:")
        return None  # Or handle the error differently
    
argsp = argsubparsers.add_parser("checkout", help="To check the data in a particular commit")
argsp.add_argument(dest="hash", help="specify the hash of the commit you want to checkout")
argsp.add_argument(dest="directory_path",nargs="?", default=".", help="specify the directory path where you want to checkout the commit files")
argsp.add_argument("--force",dest="delFlag", default=False, action="store_true", help="This flag removes all other files that are in the mentioned directory and only files that are mentioned in commit remains")

def checkout(hash, directory_path="."):
    json_file_path=".tico/branches/main/commits.json"
    with open(json_file_path, "r") as f:
        my_dict = json.load(f)
    files = my_dict[hash]["files"]    
    for filepath , file_encoded_content in files.items():
        file_path = os.path.join(".",directory_path, filepath) #currently works only if folder is in sub directory
        folder_path = os.path.dirname(file_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
        file_content = base64_decode(file_encoded_content)
        try:
            with open(file_path, "w") as f:
                f.write(file_content)
        except PermissionError as e:    
            print("Error writing to file:", e)
            # Handle the error appropriately, e.g., prompt for elevated privileges or suggest alternative actions

def cmd_checkout(args):
    hash = args.hash
    directory_path= args.directory_path
    json_file_path=".tico/branches/main/commits.json"
    delFlag = args.delFlag
    with open(json_file_path, "r") as f:
        my_dict = json.load(f)
    if not hash in my_dict.keys():
        print("There is no existing commit with the specified hash")
        return
    files = my_dict[hash]["files"]
    if delFlag:
        shutil.rmtree(os.path.join(".", directory_path))
    checkout(hash=hash, directory_path=directory_path)


def print_commit(key, value, number=0):
    print(f"\nCommit No. {number}")
    print(f"Commit: {key}")
    print(f"Author: {value["author"]}")
    print(f"Time_stamp: {value["timestamp"]}")
    print(f"Message: {value["message"]}")
    if "file_hash" in value.keys():
        all_files_hash  = value["file_hash"]
        if len(all_files_hash)==0:
            print("There were no files in this commit\n")
        else:
            print(f"All files with its corressponding hashes :\n")    
        for filename, filehash in all_files_hash.items():
            print(f"{filename}: {filehash}")
    all_files = list(value["files"].keys())
    if len(all_files)==0:
        print("\nThere were no files in this commit\n")
    else:
        print(f"\nAll files with its corressponding content :\n")    
        for file in all_files:
            content = base64_decode(value["files"][file])
            print(f"{file} : {content}")
    print("\n\n")        
                    
        
        

argsp = argsubparsers.add_parser("log", help="Log out the previous commits you did")

argsp.add_argument(dest="count",action="store",   nargs="?", help="Specify the count of commits you want to see the meta data of")

def cmd_log(args):
    if (args.count):
        count = int(args.count)
    else : count = None    
    file_path = ".tico/branches/main/commits.json"
    with open(file_path, "r") as f:
        my_dict = json.load(f)
        dic_length = len(my_dict)
    if dic_length==1:
        print("NO commits made yet")
        return     
    if count==None:
        #specify all commits
        cnt = dic_length-1
    else:
        if count==0:
            print("NO commits made yet")
            return
        cnt = min(dic_length-1, count)
    commit_no = dic_length-1    
    for key, value in reversed(my_dict.items()):
        if (cnt<=0): return
        else :
            print_commit(key, value, commit_no)
            commit_no=commit_no-1
            cnt=cnt-1

argsp = argsubparsers.add_parser("revert", help="This reverts the changes of the previous commit")

def cmd_revert(args):
    file_path=".tico/branches/main/commits.json"
    with open (file_path, "r") as file:
        content = json.load(file)
    last_key = list(content.keys())[-1]

    #delete files that are the part of the previous commit
    files = content[last_key]["files"].keys()
    for filepath in files:
        try:
            os.remove(filepath)
            # print(f"File {filepath} deleted successfully.")
        except OSError as error:
            print(f"Error deleting file: {error}")
            
    #add the files that are in the parent commmit 
    parent_hash = content[last_key]["parent"]
    checkout(hash=parent_hash)
    rmcommit()
    