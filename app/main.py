import sys


def main():

    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("Enter QUIT to exit\n$ ")

        # Wait for user input
        command = input()

        if command == "QUIT":
            break

        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
