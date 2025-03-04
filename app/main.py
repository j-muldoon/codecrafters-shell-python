import sys
import os

# TODO: Refactor to use match-case instead of elifs
# Can even make functions as well
#  Current task: GQ9 The cd builtin: Relative paths

def main():

    
    builtIns = ["exit", "echo", "type", "pwd", "cd"]

    while True:

        PATH = os.environ.get("PATH", "")
        HOME = os.environ.get("HOME")
        paths = PATH.split(":")

        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")

        # Wait for user input
        user_input = input()
        words = user_input.split(" ")
        cmd = words[0]
        cmd_tail = " ".join(words[1:])

        try:

            if cmd == "exit":
                sys.exit(int(cmd_tail))

            elif cmd == "echo":
                sys.stdout.write(f"{cmd_tail}\n")

            elif cmd == "type":
                current_path = None
                for path in paths:
                    # Error here the path is incorrect (but only for exe files?? not always)
                    if os.path.isfile(f"{path}/{cmd_tail}"):
                        current_path = f"{path}/{cmd_tail}"
                        break
                if cmd_tail in builtIns:
                    sys.stdout.write(f"{cmd_tail} is a shell builtin\n")
                elif current_path:
                    print(f"{cmd_tail} is {current_path}")
                else:
                     sys.stdout.write(f"{cmd_tail}: not found\n")
            elif cmd == "pwd":
                sys.stdout.write(f"{os.getcwd()}\n")
            elif cmd == "cd":
                try:
                    os.chdir(cmd_tail)
                except OSError as err:
                    if cmd_tail == "~":
                        os.chdir(HOME)
                    else:
                        sys.stdout.write(f"cd: {cmd_tail}: No such file or directory\n")

            else:

                # Execute executable or skip
                current_path = None
                for path in paths:
                    if os.path.isfile(f"{path}/{cmd}"):
                        os.system(user_input)
                        break
                else:
                    sys.stdout.write(f"{user_input}: command not found\n")

        # The tester likes a certain error output
        except OSError as err:
            sys.stdout.write(f"OS error: {err}\n")
        except ValueError:
            sys.stdout.write("Could not convert data to an integer\n")
        except Exception as err:
            sys.stdout.write(f"Unexpected {err=}, {type(err)=}\n")
            raise


if __name__ == "__main__":
    main()
