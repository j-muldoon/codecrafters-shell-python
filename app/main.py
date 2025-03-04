import sys
import shutil
import os

def main():

    PATH = os.environ.get("PATH", "")
    paths = PATH.split(":")
    builtIns = ["exit", "echo", "type"]

    print(PATH)

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
                current_path = None
                for path in paths:
                    if os.path.isfile(f"{path}/{cmd_tail}"):
                        current_path = f"{path}/{cmd_tail}"
                if cmd_tail in builtIns:
                    sys.stdout.write(f"{cmd_tail} is a shell builtin\n")
                elif current_path:
                    print(f"{cmd_tail} is {current_path}")
                else:
                     sys.stdout.write(f"{cmd_tail}: not found\n")

            else:

                # Execute executable or skip
                current_path = None
                for path in paths:
                    if os.path.isfile(f"{path}/{cmd_tail}"):
                        os.system(f"{path}/{cmd_tail}")
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
