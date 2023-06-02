import argparse
import getpass
import subprocess
from subprocess import PIPE
import sys
import os as oslib

def run(host, user, password, cmd, get_result=False):
    command = ["sshpass", "-p", password, "ssh", "-t", "-q", "-o", "StrictHostKeyChecking=no", f"{user}@{host}"] + cmd.split()
    if get_result:
        p = subprocess.Popen(command, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        p.wait()
        return p.communicate()[0]
    else:
        p = subprocess.Popen(command, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin)
        return p.wait()

def main():
    parser = argparse.ArgumentParser("runremote")
    parser.add_argument("--host", required=True, type=str, help="host[:port]")
    parser.add_argument("--user", required=True, type=str, help="Remote user")
    parser.add_argument("--pass", required=False, type=str, help="Remote password")
    parser.add_argument("file", type=str, help="Executable to launch")
    args = parser.parse_args()
    host : str = args.host
    user : str = args.user
    password : str | None = getattr(args, "pass")
    file : str = args.file

    if password is None:
        password = getpass.getpass()

    os_raw = run(host, user, password, "echo %OS%", True)
    if os_raw == b'Windows_NT\r\n':
        os = "windows"
    elif os_raw == b'%OS%\n':
        os = "linux"
    else:
        print("Unable to recognize os:", os_raw)
        exit(1)
    
    scp = oslib.system(f'sshpass -p "{password}" scp -o StrictHostKeyChecking=no "{file}" "{user}@{host}:_a.exe"')
    if scp:
        print("Copying failed")
        exit(1)
    if os == "windows":
        exit(run(host, user, password, "_a.exe"))
    elif os == "linux":
        exit(run(host, user, password, "./_a.exe"))

if __name__ == "__main__": main()