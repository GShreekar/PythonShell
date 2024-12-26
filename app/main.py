import sys
import os

def handleUserInput(command):
    if not command.strip():
        return
    
    command = command.strip().split()
    
    PATH = os.environ.get("PATH")
    PATH = PATH.split(":")
    
    match command[0]:
        case "exit":
            if len(command) == 2 and command[1] == "0":
                sys.exit(0)
            else:
                print("invalid exit status")
        case "echo":
            print(" ".join(command[1:]))
        case "type":
            commands = {"exit", "echo", "type", "pwd"}
            cmdPath = None
            for path in PATH:
                if os.path.isfile(f"{path}/{command[1]}"):
                    cmdPath = f"{path}/{command[1]}"
                    break
            if command[1] in commands:
                print(f"{command[1]} is a shell builtin")
            elif cmdPath:
                print(f"{command[1]} is {cmdPath}")
            else:
                print(f"{command[1]}: not found")
        case "pwd":
            print(os.getcwd())
        case "cd":
            if command[1] == "~":
                path = os.path.expanduser("~")
            else:
                path = os.path.expanduser(command[1])
            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: {command[1]}: No such file or directory")
        case _:
            cmdPath = None
            for path in PATH:
                if os.path.isfile(f"{path}/{command[0]}"):
                    cmdPath = f"{path}/{command[0]}"
                    break
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
