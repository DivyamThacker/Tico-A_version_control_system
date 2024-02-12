import ticolib, sys

if len(sys.argv) < 2:
    print("\nTico - A Version Control System.")
    print("Created by - Divyam Thacker\n")
    ticolib.welcome()
    print("\n\nThis is a terminal app, so it won't Run when you Double click the exe file, you need to first locate to tico.exe file and then run ./tico.exe to run it.\nAlso note that you need to give Administrator privileges to the terminal to run this app properly without errors.")
    input()
else:    
    ticolib.main()