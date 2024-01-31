import ticolib, sys

if len(sys.argv) < 2:
    print("Tico - A Version Control System.\n")
    ticolib.welcome()
else:    
    ticolib.main()