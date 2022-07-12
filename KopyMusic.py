import platform
import os
import subprocess
import pysftp
from km_argparser import arg_parser


class KopyMusic:
    def __init__(self):
        super(KopyMusic, self).__init__()

        self.args = arg_parser()

        self.remote_path: str = self.args.remote
        self.local_path: str = self.args.local
        self.username: str = self.args.username
        self.password: str = self.args.password
        self.extension: list = self.args.ext
        self.reverse: bool = self.args.reverse  # Switch
        self.mirror: bool = self.args.mirror  # Switch
        self.transfer_files: bool = self.args.transfer  # Switch
        self.debug: bool = self.args.debug  # Switch
        self.port: int = self.args.port
        self.host: str = "Host"
        self.path: str = "Path"
        self.operating_system: str = "OS"

        self.remote_files: list = []
        self.local_files: list = []

        if self.debug:
            self.debugger()
        else:
            self.path_handler()

            if not self.mirror:
                self.filetransfer()
            else:
                self.filetransfer()
                self.reverse = True
                self.filetransfer()

    def determine_os(self) -> tuple:
        """Determines the OS"""

        self.operating_system = platform.system()

        if self.operating_system == 'Windows':
            username = os.environ['USERNAME']
            host = os.environ['COMPUTERNAME']
        else:
            username = os.environ['USER']
            host = os.uname().nodename

        return username, host

    def debugger(self):
        """Debugger menu"""
        debugger_list = [f"Remote Path:    {self.remote_path}",
                         f"Local Path:     {self.local_path}",
                         f"Username:       {self.username}",
                         f"Password:       {self.password}",
                         f"Reverse:        {self.reverse}",
                         f"Mirror:         {self.mirror}",
                         f"Extension:      {self.extension}",
                         f"Port:           {self.port}",
                         f"Transfer Files: {self.transfer_files}"]

        max_length = max([len(x) for x in debugger_list])
        padding = 3
        spacer = " " * padding
        padding_calculation = max_length + (padding * 2)
        debugger_list = [f"║{spacer}{x.ljust(max_length)}{spacer}║" for x in debugger_list]

        debug_top = f"╔{'═' * padding_calculation}╗"
        debug_top_msg = f"║{'DEBUGGER'.center(padding_calculation)}║"
        debug_top_bar = f"{'╠' + ('═' * padding_calculation) + '╣'}"
        debug_bottom = f"╚{'═' * padding_calculation}╝"

        for index, d in enumerate(debugger_list):
            d = list(d)
            for i, x in enumerate(d):
                if x not in ['║']:
                    d[i] = f"\x1b[1m{x}\x1b[0m"
            debugger_list[index] = "".join(d)

        debugger_list.insert(0, debug_top)
        debugger_list.insert(1, debug_top_msg)
        debugger_list.insert(2, debug_top_bar)
        debugger_list.append(debug_bottom)

        _ = *map(print, debugger_list),

    @staticmethod
    def color(text, color: str) -> str:
        """Colors the text"""

        color = color.lower()
        if color == 'red':
            color = 31
        elif color == 'green':
            color = 32
        elif color == 'yellow':
            color = 33
        elif color == 'blue':
            color = 34

        return f"\x1b[1;{color}m{text}\x1b[0m"

    def local_to_local(self):
        """local path filetransfer"""
        if not self.validate_path(self.local_path):
            print("Local path not valid.")
            raise SystemExit(0)

        if not self.validate_path(self.remote_path):
            print("Remote path not valid.")
            raise SystemExit(0)

    def remote_to_local(self):
        """Uses sftp to connect to remote path"""
        if not self.validate_path(self.local_path):
            print("Local path not valid.")
            raise SystemExit(0)

        if self.remote_host_check(self.host,
                                  self.username) != self.username:  # Validates remote path via ssh connection
            print("Host not up. Exiting.")
            raise SystemExit(0)

    @staticmethod
    def validate_path(path: str) -> bool:
        """Validate path"""
        return os.path.exists(path)

    def list_local_folder(self, local_path: str) -> list:
        """Lists a local folder using powershell"""
        self.operating_system = platform.system()

        if self.operating_system == 'Windows':
            cmdline = f"powershell -c \"(Get-ChildItem {local_path}).Name\""
        else:  # Unix
            cmdline = f"ls {local_path}"

        command = subprocess.Popen(cmdline, shell=True, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = command.communicate()
        list_output: list = [x for x in output.split("\n") if x]
        return list_output

    def echo_transport_direction(self, remote: str, local: str, reverse: bool = False) -> None:
        """Prints a transport direction"""
        if reverse:
            local, remote = remote, local

        print(
            f"{self.color('╔[', 'red')}Transport direction{self.color(']', 'red')}\n"
            f"{self.color('╚[', 'red')}{self.color(local, 'green')}{self.color(']', 'red')}"
            f"{self.color('═[>>>]═', 'red')}"
            f"{self.color('[', 'red')}{self.color(remote, 'blue')}{self.color(']', 'red')}")

    def remote_host_check(self, host: str, username: str) -> str:
        response_code, response_txt = subprocess.getstatusoutput(f'ssh -p {self.port} -l {username} {host} "whoami"')
        return response_txt

    def path_handler(self):
        """Replaces slashes based on OS"""
        if '/' in self.remote_path:
            """Linux System parsing of folder path"""
            self.host, path = self.remote_path.split("/", maxsplit=1)
            self.path = f"./{path}"
            # self.operating_system = "Linux"

        elif '\\' in self.remote_path:
            """Windows System parsing of folder path"""
            self.host, path = self.remote_path.split("\\", maxsplit=1)
            self.path = fr".\{path}"
            # self.operating_system = "Windows"

    def file_extension(self, files: list) -> list:
        """Checks file extension"""
        return [x for x in files if x.split('.')[-1] in self.extension]

    def filetransfer(self, private_key: str = "~/.ssh/id_rsa") -> None:
        """Uses sftp to check remote folder and compare it to a local folder.
        The difference between those folders are copied to the local folder
        If no username is present, a local to local copy direction is used instead.
        """

        source_path: str = ""
        target_path: str = ""
        username, host = self.determine_os()

        if not self.username:  # Local to local transfer
            # print(self.username) # Debug
            self.local_to_local()  # Checks if paths are valid

            self.remote_files: list = self.list_local_folder(self.remote_path)
            self.local_files: list = self.list_local_folder(self.local_path)

            if self.extension:  # --ext
                self.remote_files: list = self.file_extension(self.remote_files)
                self.local_files: list = self.file_extension(self.local_files)

            if not self.reverse:
                self.path = self.remote_path
                difference = set(self.remote_files).difference(set(self.local_files))  # Checks difference
                self.echo_transport_direction(self.local_path, self.remote_path)
            else:
                self.path = self.local_path
                difference = set(self.local_files).difference(set(self.remote_files))  # Checks difference
                self.echo_transport_direction(self.local_path, self.remote_path, self.reverse)

            if difference:

                for d in difference:

                    if self.operating_system == "Windows":
                        source_path = os.path.join(self.remote_path, d)
                        target_path = os.path.join(self.local_path, d)
                    elif self.operating_system == "Linux":
                        source_path = os.path.join(self.remote_path, d).replace("\\", "/")
                        target_path = os.path.join(self.local_path, d).replace("\\", "/")

                    if self.reverse:
                        source_path, target_path = target_path, source_path

                    output_format = "[{0}]━━[USER:{1}]━[HOST:{2}]━[FOLDER:{3}]━[TRACK:{4}]".format(
                        self.color('+', 'green'),
                        self.color(username,
                                   'green'),
                        self.color(host, 'green'),
                        self.color(self.path, 'green'),
                        self.color(d, 'green'))
                    print(output_format)

                    if self.transfer_files:
                        with open(source_path, 'rb') as rf:
                            file = rf.read()

                        with open(target_path, 'wb') as wf:
                            wf.write(file)
            else:
                print("\x1b[1;31m[-]\x1b[0m Nothing to copy.")

        else:
            self.remote_to_local()  # Checks if paths are valid and remote host is up

            with pysftp.Connection(host=self.host, username=self.username, password=self.password,
                                   private_key=private_key, port=self.port) as sftp:

                self.remote_files: list = sftp.listdir(self.path)  # Music folder on my raspberry pi
                self.local_files: list = self.list_local_folder(self.local_path)

                if self.extension:
                    self.remote_files: list = self.file_extension(self.remote_files)
                    self.local_files: list = self.file_extension(self.local_files)

                if not self.reverse:
                    username = self.username
                    host = self.host
                    loader = sftp.get
                    difference = set(self.remote_files).difference(set(self.local_files))  # Checks difference
                    self.echo_transport_direction(self.local_path, self.remote_path)
                else:

                    loader = sftp.put
                    difference = set(self.local_files).difference(set(self.remote_files))  # Checks difference
                    self.echo_transport_direction(self.local_path, self.remote_path, self.reverse)

                if difference:
                    for d in difference:

                        if self.operating_system == "Windows":
                            target_path = os.path.join(self.local_path, d)
                        elif self.operating_system == "Linux":
                            target_path = os.path.join(self.local_path, d).replace("\\", "/")

                        output_format = "[{0}]━━[USER:{1}]━[HOST:{2}]━[FOLDER:{3}]━[TRACK:{4}]".format(
                            self.color('+', 'green'),
                            self.color(username,
                                       'green'),
                            self.color(host, 'green'),
                            self.color(self.path, 'green'),
                            self.color(d, 'green'))
                        print(output_format)

                        if self.transfer_files:
                            loader(remotepath=f"{self.path}/{d}", localpath=target_path)  # Does the heavy lifting

                else:
                    print("\x1b[1;31m[-]\x1b[0m Nothing to copy.")


def main() -> int:
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
