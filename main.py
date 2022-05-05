"""Copies new music files on to my main pc."""
import subprocess
import pysftp
import os
from km_argparser import arg_parser


def co(text, color: str) -> str:
    """Colors the text"""

    match color.lower():
        case 'red':
            color = 31
        case 'green':
            color = 32
        case 'yellow':
            color = 33
        case 'blue':
            color = 34

    return f"\x1b[1;{color}m{text}\x1b[0m"


def validate_path(path: str) -> bool:
    """Validate path"""
    return os.path.exists(path)


def list_local_folder(local_path: str) -> list:
    """Lists a local folder using powershell"""
    windows_cmdline = f"powershell -c \"(ls {local_path}).Name\""
    command = subprocess.Popen(windows_cmdline, shell=True, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = command.communicate()
    windows_output: list = [x for x in output.split("\n") if x]
    return windows_output


def echo_transport_direction(remote, local, reverse: bool = False):
    """Prints a transport direction"""
    if reverse:
        local, remote = remote, local

    print(
        f"{co('╔[', 'red')}Transport direction{co(']', 'red')}\n"
        f"{co('╚[', 'red')}{co(local, 'green')}{co(']', 'red')}"
        f"{co('═[>>>]═', 'red')}"
        f"{co('[', 'red')}{co(remote, 'blue')}{co(']', 'red')}")


def ping(host, username):
    response_code, response_txt = subprocess.getstatusoutput(f'ssh {username}@{host} "whoami"')
    return response_txt  # Username


def filetransfer(local_path: str, remote_path: str, username: str, password: str = None,
                 transfer_files: bool = False, reverse: bool = False, private_key: str = "~/.ssh/id_rsa") -> None:
    """Uses sftp to check remote folder and compare it to a local folder.
    The difference between those folders are copied to the local folder"""

    host: str = "Host"
    path: str = "Path"
    operating_system: str = "OS"

    if '/' in remote_path:
        """Linux System parsing of folder path"""
        host, path = remote_path.split("/", maxsplit=1)
        path = f"./{path}"
        operating_system = "Linux"

    elif '\\' in remote_path:
        """Windows System parsing of folder path"""
        host, path = remote_path.split("\\", maxsplit=1)
        path = fr".\{path}"
        operating_system = "Windows"

    if not validate_path(local_path):  # Validates local path
        print("Local path not valid.")
        raise SystemExit(0)

    if ping(host, username) != username:  # Validates remote path via ssh connection
        print("Host not up. Exiting.")
        raise SystemExit(0)

    with pysftp.Connection(host=host, username=username, password=password, private_key=private_key) as sftp:
        remote_files = sftp.listdir(path)  # Music folder on my raspberry pi
        local_files = list_local_folder(local_path)
        # print(local_files) Debug

        if not reverse:
            loader = sftp.get
            difference = set(remote_files).difference(set(local_files))  # Checks difference
            echo_transport_direction(local_path, remote_path)
        else:
            username = os.environ['USERNAME']
            host = os.environ['COMPUTERNAME']
            path = local_path
            loader = sftp.put
            difference = set(local_files).difference(set(remote_files))  # Checks difference
            echo_transport_direction(local_path, remote_path, reverse)

        if difference:
            for d in difference:

                if operating_system == "Windows":
                    target_path = os.path.join(local_path, d)
                elif operating_system == "Linux":
                    target_path = os.path.join(local_path, d).replace("\\", "/")

                output_format = "[{0}]━━[USER:{1}]━[HOST:{2}]━[FOLDER:{3}]━[TRACK:{4}]".format(co('+', 'green'),
                                                                                               co(username,
                                                                                                  'green'),
                                                                                               co(host, 'green'),
                                                                                               co(path, 'green'),
                                                                                               co(d, 'green'))
                print(output_format)
                if transfer_files:
                    loader(remotepath=f"{path}/{d}", localpath=target_path)  # Does the heavy lifting

        else:
            print("\x1b[1;31m[-]\x1b[0m Nothing to copy.")


def main() -> int:
    args = arg_parser()

    filetransfer(local_path=args.local,
                 remote_path=args.remote,
                 username=args.username,
                 reverse=args.reverse,
                 private_key=args.key,
                 transfer_files=args.t)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
