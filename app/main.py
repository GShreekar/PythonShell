import sys
import os

def handleUserInput(command):
    if not command.strip():
        return
    
    command = command.strip().split()
    
    PATH = os.environ.get("PATH")
    PATH = PATH.split(":")
    
    if command[0] == "exit":
        if len(command) == 1 or command[1] != "0":
            print("Invalid exit code")
            return
        sys.exit(0)
    elif command[0] == "echo":
        print(" ".join(command[1:]))
    elif command[0] == "type":
        commands = {"exit", "echo", "type"}
        cmdPath = None
        for path in PATH:
            if os.path.isfile(f"{path}/{command[1]}"):
                cmdPath = f"{path}/{command[1]}"
        if command[1] in commands:
            print(f"{command[1]} is a shell builtin")
        elif cmdPath:
            print(f"{command[1]} is {cmdPath}")
        else:
            print(f"{command[1]}: not found")
    else:
        cmdPath = None
        for path in PATH:
            if os.path.isfile(f"{path}/{command[0]}"):
                cmdPath = f"{path}/{command[0]}"
        if cmdPath:
            os.system(" ".join(command))
        else:
            print(f"{command[0]}: command not found")
    

def main():
    
    while True:
        sys.stdout.write("$ ")
        command = input()
        handleUserInput(command)


if __name__ == "__main__":
    main()
