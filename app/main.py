import sys
import shutil

def path_search(check_item, path_input):
    
    # Going to brute force it, but better way would be to use hash table to not go into directories that have already been covered

    directories = path_input.split(":")

    for directory in directories:
        layers = directory.split("/")
        path_as_list = []
        for layer in layers:
            path_as_list.append(layer)
            if check_item == layer:
                return True, path_as_list
    return False, None
        

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
            
            if cmd not in builtins:
                sys.stdout.write(f"{user_input}: command not found\n")
            elif cmd == "exit":
                sys.exit(int(cmd_tail))
            elif cmd == "echo":
                sys.stdout.write(f"{cmd_tail}\n")
            elif cmd == "type":
                
                if cmd_tail in builtins:
                    sys.stdout.write(f"{cmd_tail} is a shell builtin\n")
                elif path := shutil.which(cmd_tail):
                    print(f"{cmd_tail} is {path}")
                else:
                        sys.stdout.write(f"{cmd_tail}: not found\n")


        except OSError as err:
            print("OS error:", err)
        except ValueError:
            print("Could not convert data to an integer.")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise


if __name__ == "__main__":
    main()
