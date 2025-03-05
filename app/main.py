import sys
import os
import shlex

# TODO: Refactor to use match-case instead of elifs
# Can even make functions as well
#  Current task: GQ9 The cd builtin: Relative paths

def write_output(output, filepath_location):
    if filepath_location:
        with open(filepath_location, 'w') as f:
            f.write(output)
    else:
        sys.stdout.write(output)
            

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
        command = user_input.strip()


        words = user_input.split(" ")
        cmd_tail = " ".join(words[1:])
        # notice the difference between words and args, that will probably be the cause of some errors
        # note args[0] and words[0] will be equal unless the input begins with a quote (which will just be an unknown command)
        args = shlex.split(command, posix=True)
        cmd = args[0]
        
        # file redirecting
        # vulnerability if someone just writes a "> " anywhere
        filepath_location = None
        if "> " in user_input:
            for i, arg in enumerate(args):
                if ">" in arg:
                    filepath_location = args[i+1]
                    # remove the redirect from the tail and args
                    args = args[:i]
                    cmd_tail = " ".join(words[1:i])
                    break
        


        try:

            


            if cmd == "exit":
                sys.exit(int(cmd_tail))

            elif cmd == "echo":
                output = f"{" ".join(args[1:])}\n"
                write_output(output, filepath_location)

            elif cmd == "type":
                current_path = None
                for path in paths:
                    if os.path.isfile(f"{path}/{cmd_tail}"):
                        current_path = f"{path}/{cmd_tail}"
                        break
                if cmd_tail in builtIns:
                    output = f"{cmd_tail} is a shell builtin\n"
                    write_output(output, filepath_location)
                elif current_path:
                    output = f"{cmd_tail} is {current_path}\n"
                    write_output(output, filepath_location)
                else:
                     output = f"{cmd_tail}: not found\n"
                     write_output(output, filepath_location)
            elif cmd == "pwd":
                output = f"{os.getcwd()}\n"
                write_output(output, filepath_location)
            elif cmd == "cd":
                try:
                    os.chdir(cmd_tail)
                except OSError as err:
                    if cmd_tail == "~":
                        os.chdir(HOME)
                    else:
                        output = f"cd: {cmd_tail}: No such file or directory\n"
                        write_output(output, filepath_location)

            else:

                # Execute executable or skip
                current_path = None
                for path in paths:
                    if os.path.isfile(f"{path}/{cmd}"):
                        os.system(user_input)
                        break
                else:
                    output = f"{user_input}: command not found\n"
                    write_output(output, filepath_location)

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
