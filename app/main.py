import sys
import shutil
import os

def main():

    path = os.environ['PATH']
    builtIns = ["exit", "echo", "type"]

    while True:
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
                if cmd_tail in builtIns:
                    sys.stdout.write(f"{cmd_tail} is a shell builtin\n")
                elif path := shutil.which(cmd_tail):
                    print(f"{cmd_tail} is {path}")
                else:
                        sys.stdout.write(f"{cmd_tail}: not found\n")

            # os obtains path info from the environment by default, need to navigate to files directory first?
            elif os.path.isfile(cmd):
                 os.system(user_input)
            
            else:
                sys.stdout.write(f"{user_input}: command not found\n")


        except OSError as err:
            print("OS error:", err)
        except ValueError:
            print("Could not convert data to an integer.")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise


if __name__ == "__main__":
    main()
