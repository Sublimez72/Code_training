import os
import subprocess
import concurrent.futures


# port_not_set = bool
# while port_not_set:
#     try:
#         webserver_port = int(input("Enter webserver port: "))
#         port_not_set = False
#     except ValueError:
#         print("Port number only has integers ")


ip = input("Enter IP address of target: ")
try:
    os.mkdir(ip)
except FileExistsError:
    pass
os.chdir(ip)



# Define the shell commands to run
commands = [
    f"nmap {ip} -A -T4 -p-",
    f"nmap {ip} -sU -T4",
    f"nikto -h {ip}",
    f"smbclient -L \\\\{ip}\\",
]

# Define a function to run a single command
def run_command(command):
    return subprocess.run(command, shell=True, capture_output=True)

# Create a ThreadPoolExecutor with a maximum of 20 worker threads
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    # Submit the commands to the executor and store the Future objects in a list
    futures = [executor.submit(run_command, command) for command in commands]

    # Wait for all the commands to complete and get their results
    results = [future.result() for future in futures]

# Save the output of each command
for count, result in enumerate(results):
    with open(f"file_{count}.txt", "w") as f:
        if result.stdout:
            f.write(result.stdout.decode())
        elif result.stderr:
            f.write(result.stderr.decode())
