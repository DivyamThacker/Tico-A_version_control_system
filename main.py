import ticolib, sys

if len(sys.argv) < 2:
    print("\nTico - A Version Control System.")
    print("Created by - Divyam Thacker\n")
    ticolib.welcome()
else:    
    ticolib.main()