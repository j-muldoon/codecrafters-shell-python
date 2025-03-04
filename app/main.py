import sys


def main():

    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()
        words = command.split(" ")

        try:

            if words[0] == "exit":
                sys.exit(int(words[1]))
            elif words[0] == "echo":
                print(" ".join(words[1:]))
                continue
            else:
                print(f"{command}: command not found")

        except OSError as err:
            print("OS error:", err)
        except ValueError:
            print("Could not convert data to an integer.")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise


if __name__ == "__main__":
    main()
