import subprocess

name = input("Command: ")
subprocess.call(name, shell=True)
