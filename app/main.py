import sys


def main():

    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")

        # Wait for user input
        user_input = input()
        words = user_input.split(" ")
        cmd = words[0]
        cmd_tail = " ".join(words[1:])

        builtins = ["exit", "echo", "type"]

        try:

            if cmd == "exit":
                sys.exit(cmd_tail)
            elif cmd == "echo":
                print(cmd_tail)
            elif cmd == "type":
                if cmd_tail in builtins:
                    print(f"{cmd_tail} is a shell builtin")
                else:
                    print(f"{cmd_tail}: not found")
            else:
                print(f"{user_input}: command not found")

        except OSError as err:
            print("OS error:", err)
        except ValueError:
            print("Could not convert data to an integer.")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise


if __name__ == "__main__":
    main()
