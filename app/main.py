import sys
import os
import shlex
import readline

# TODO: Refactor to use match-case instead of elifs
# Can even make functions as well
#  Current task: GQ9 The cd builtin: Relative paths

def write_output(output, filepath_location, output_type):
    if filepath_location and output_type == "out":
        with open(filepath_location, 'w') as f:
            f.write(output)
    elif filepath_location and (output_type == "err" or output_type == "append_err"):
        sys.stdout.write(output)

        if output_type == "err":
            file_mode = 'w'
        else:
            file_mode = 'a'

        with open(filepath_location, file_mode) as f:
            if sys.exc_info()[0]:
                f.write(",".join([sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2] ]))
            else:
                f.write("")
    elif filepath_location and output_type == "append":
        with open(filepath_location, 'a') as f:
            if output:
                f.write(output)
            else:
                f.write("")

    else:
        sys.stdout.write(output)
    
    return

def completer(text, state):

    """Autocomplete function for built-in commands."""

    builtin = ["echo ", "exit ", "type ", "pwd ", "cd "]

    matches = [cmd for cmd in builtin if cmd.startswith(text)]

    return matches[state] if state < len(matches) else None

            

def main():

    
    builtIns = ["exit", "echo", "type", "pwd", "cd"]

    # Set up autocomplete

    readline.set_completer(completer)

    readline.parse_and_bind("tab: complete")

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
        output_type = None
        filepath_location = None
        if "> " in user_input:
            for i, arg in enumerate(args):
                if ">" in arg:
                    
                    # classify the redirect type
                    
                    if (" 1> " in user_input) or (" > " in user_input):
                        output_type = "out"
                    elif (" 1>> " in user_input) or (" >> " in user_input):
                        output_type = "append"
                    elif (" 2> " in user_input):
                        output_type= "err"
                    elif (" 2>> " in user_input):
                        output_type= "append_err"
                        

                    filepath_location = args[i+1]
                    # remove the redirect from the tail and args
                    args = args[:i]
                    cmd_tail = " ".join(words[1:i])
                    break
        
            


        if cmd == "exit":
            sys.exit(int(cmd_tail))

        elif cmd == "echo":
            insert = (" ".join(args[1:]))
            output = f"{insert}\n"
            write_output(output, filepath_location, output_type)

        elif cmd == "type":
            current_path = None
            for path in paths:
                if os.path.isfile(f"{path}/{cmd_tail}"):
                    current_path = f"{path}/{cmd_tail}"
                    break
            if cmd_tail in builtIns:
                output = f"{cmd_tail} is a shell builtin\n"
                write_output(output, filepath_location, output_type)
            elif current_path:
                output = f"{cmd_tail} is {current_path}\n"
                write_output(output, filepath_location, output_type)
            else:
                    output = f"{cmd_tail}: not found\n"
                    write_output(output, filepath_location, output_type)
        elif cmd == "pwd":
            output = f"{os.getcwd()}\n"
            write_output(output, filepath_location, output_type)
        elif cmd == "cd":
            try:
                os.chdir(cmd_tail)
            except OSError as err:
                if cmd_tail == "~":
                    os.chdir(HOME)
                else:
                    output = f"cd: {cmd_tail}: No such file or directory\n"
                    write_output(output, filepath_location, output_type)

        else:

            # Execute executable or skip
            current_path = None
            for path in paths:
                if os.path.isfile(f"{path}/{cmd}"):
                    os.system(user_input)
                    break
            else:
                output = f"{user_input}: command not found\n"
                write_output(output, filepath_location, output_type)


if __name__ == "__main__":
    main()
