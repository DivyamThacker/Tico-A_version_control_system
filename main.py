import ticolib, sys
def welcome():
    print("Tico - A Version Control System.")
    print("tico init - Initialize a new Tico repository")
    print("tico add <file> - Add a file to the index")
    print("tico commit -m <message> - Commit changes with a message")
    print("tico rmadd <file> - remove a file from the index")
    print("tico rmcommit - remove last commit")
    print("tico log - Display commit log")
    print("tico checkout <commit> - Checkout a specific commit")
    print("tico help - to see this usage help")
    print("tico status - to see status")
    print("tico user show - to see present user")
    print("tico user set <username> - to change user")
    print("tico push <path> - to push your file to another folder")
    print("Created by - Divyam Thacker")

if len(sys.argv) < 2:
    welcome()
else:    
    ticolib.main()