import argparse
import pathlib
import psutil
import subprocess
import threading
import time
import sys
import shlex

def poll(process, f, time_step):
    while process.poll() is None:
        cpu = psutil.cpu_percent()
        mem_perc = psutil.virtual_memory().percent
        mem_used = psutil.virtual_memory().used
        mem_active = psutil.virtual_memory().active
        print(time.time(), cpu, mem_perc, mem_used, mem_active, file=f)
        time.sleep(time_step)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot CPU and memory consumption of binary program.")

    parser.add_argument("-c", "--cmd", type=str, help="Command to execute")

    parser.add_argument("-o", "--output", type=pathlib.Path, help="Output text file")

    parser.add_argument("-t", "--time_step", type=int, help="Time step of polling in ms", default=100)

    args = parser.parse_args()

    cmd = args.cmd

    time_step = float(args.time_step) / 1000

    output_exists = False
    try:
        with open(args.output, "r") as f:
            output_exists = True
    except:
        pass

    while output_exists:
        print("File " + str(args.output) + " already exists. Do you want to overwrite it?")
        inpt = input("[Y] / [N] (default)\n")
        if inpt == "" or inpt.lower() == "n":
            sys.exit("Not overwriting output file. Exiting program.")
        if inpt.lower() == "y":
            print("Overriding " + str(args.output))
            break

    print("Running process: " + cmd)
    cmd = shlex.split(cmd)
    with open(args.output, "w") as f:
        print(r"time %cpu %mem mem_used mem_active", file=f)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        thread = threading.Thread(target=poll, args=(process,f, time_step))
        thread.start()
        thread.join()

        stdout, stderr = process.communicate()
        if process.returncode == 0:
            print(f"Command exited successfully. Output:\n {stdout.decode()}")
        else:
            print(f"Command failed!\n {stderr.decode()}")
