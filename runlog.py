import subprocess

def run_program(command, log_list):
    """Run a command, print and capture its output in real-time."""
    try:
        # Start the subprocess and capture stdout and stderr in real-time
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Read stdout and stderr line-by-line
        for stdout_line in iter(process.stdout.readline, ''):
            print(stdout_line, end='')  # Print stdout line in real-time
            log_list.append(stdout_line)
        
        for stderr_line in iter(process.stderr.readline, ''):
            print(stderr_line, end='')  # Print stderr line in real-time
            log_list.append(stderr_line)
        
        process.stdout.close()
        process.stderr.close()
        process.wait()

        if process.returncode != 0:
            log_list.append(f"Command failed with return code {process.returncode}")
            
    except Exception as e:
        log_list.append(f"Exception occurred: {str(e)}")

def write_log(log_list, log_file):
    """Write the log list to a file."""
    with open(log_file, 'w') as file:
        for entry in log_list:
            file.write(entry)
        file.write("="*40 + "\n")

def main():
    # Define a list to store the log
    

    f = open('linux-scripts/build-sdk.sh')
    for i in f.readlines():
        log_list = []
    #command = 'sh linux-scripts/install-frameworks.sh 14'  # Replace this with your command
    # Run the command and capture the output
        run_program(i, log_list)
        tok =  i.split(' ')
        log_file = 'build-gcc'+tok[2]+'.log'
    # Write the log list to the file
        write_log(log_list, log_file)
    # Define the command to run
    

    # Define the log file name
    

if __name__ == "__main__":
    main()
