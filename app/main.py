import sys
import os
import shlex

def handleUserInput(command):
    if not command.strip():
        return

    original_command = command
    command = shlex.split(command)

    PATH = os.environ.get("PATH", "").split(os.pathsep)

    match command[0]:
        case "exit":
            if len(command) == 2 and command[1] == "0":
                sys.exit(0)
            else:
                print("invalid exit status")
        case "echo":
            content = original_command[5:].strip()
            if content.startswith("'") and content.endswith("'"):
                content = content[1:-1]
                if os.path.isfile(content):
                    try:
                        with open(content, "r") as file:
                            print(file.read(), end="")
                    except Exception as e:
                        print(f"Error reading file: {e}")
                else:
                    print(content)
            else:
                print(" ".join(command[1:]))
        case "cat":
            content = original_command[4:].strip()
            files = shlex.split(content) if content.startswith(("'", '"')) else command[1:]
            for file in files:
                if os.path.isfile(file):
                    try:
                        with open(file, "r") as f:
                            print(f.read(), end="")
                    except Exception as e:
                        print(f"Error reading {file}: {e}")
                else:
                    print(f"cat: {file}: No such file or directory")
        case "type":
            if len(command) < 2:
                print("type: missing argument")
                return

            commands = {"exit", "echo", "type", "pwd", "cd"}
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
            if len(command) < 2:
                print("cd: missing argument")
                return
            path = os.path.expanduser(command[1]) if command[1] != "~" else os.path.expanduser("~")
            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: {command[1]}: No such file or directory")
            except Exception as e:
                print(f"cd: Error: {e}")
        case _:
            executable = command[0]
            cmdPath = None
            for path in PATH:
                potential_path = os.path.join(path, executable)
                if os.path.isfile(potential_path):
                    cmdPath = potential_path
                    break
            if cmdPath:
                os.system(" ".join([shlex.quote(cmdPath)] + command[1:]))
            else:
                print(f"{command[0]}: command not found")

def main():
    while True:
        try:
            sys.stdout.write("$ ")
            command = input()
            handleUserInput(command)
        except KeyboardInterrupt:
            print("\nExiting shell.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
