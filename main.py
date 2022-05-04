"""Copies new music files on to my main pc."""
import subprocess
import pysftp
import os


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


def list_local_folder(local_path: str) -> list:
    """Lists a local folder using powershell"""
    windows_cmdline = f"powershell -c \"(ls {local_path}).Name\""
    command = subprocess.Popen(windows_cmdline, shell=True, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = command.communicate()
    windows_output: list = [x for x in output.split("\n") if x]
    return windows_output


def filetransfer(host: str, username: str, password: str = None, transfer_files: bool = False) -> None:
    """Uses sftp to check remote folder and compare it to a local folder.
    The difference between those folders are copied to the local folder"""

    local_path = os.path.join(os.environ['HOMEPATH'], "Music")  # Music folder on my main PC
    with pysftp.Connection(host=host, username=username, password=password) as sftp:
        remote_files = sftp.listdir("./Music")  # Music folder on my raspberry pi
        local_files = list_local_folder(local_path)
        # print(local_files) Debug
        difference = set(remote_files).difference(set(local_files))  # Checks difference
        # difference = set(local_files).difference(set(remote_files))  # Checks difference

        if difference:
            for d in difference:
                target_path = os.path.join(local_path, d)
                print("[{0}]━[{1}]".format(co('+', 'green'), co(d, 'blue')))
                if transfer_files:
                    sftp.get(remotepath=f"./Music/{d}", localpath=target_path)  # Does the heavy lifting
        else:
            print("\x1b[1;31m[-]\x1b[0m Nothing to copy.")


def main() -> int:
    filetransfer(host='192.168.1.224', username='pi')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
