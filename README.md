# Run Remote
Run executables remotely through ssh
## Requirements
`sshserver` open the remote pc

`ssh`, `scp`, `sshpass` on the local pc
## Installation
```
python -m pip install runremote
```
## Quickstart
```
usage: python -m runremote [-h] --host HOST --user USER [--pass PASS] file

positional arguments:
  file         Executable to launch

options:
  -h, --help   show this help message and exit
  --host HOST  host[:port]
  --user USER  Remote user
  --pass PASS  Remote password
```