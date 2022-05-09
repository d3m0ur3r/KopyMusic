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
        self.file_type: str = self.args.file_type
        self.reverse: bool = self.args.reverse
        self.mirror: bool = self.args.mirror
        self.transfer_files: bool = self.args.transfer
        self.debug: bool = self.args.debug

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

    def debugger(self):
        """Debugger menu"""
        debugger_list = [f"Remote Path:    {self.remote_path}",
                         f"Local Path:     {self.local_path}",
                         f"Username:       {self.username}",
                         f"Password:       {self.password}",
                         f"Reverse:        {self.reverse}",
                         f"Mirror:         {self.mirror}",
                         f"Transfer Files: {self.transfer_files}"]
        max_length = max([len(x) for x in debugger_list])
        padding = 4
        spacer = " " * padding
        padding_calculation = max_length + (padding * 2)
        debugger_list = [f"║{spacer}{x.ljust(max_length)}{spacer}║" for x in debugger_list]

        debug_top = f"╔{'═' * padding_calculation}╗"
        debug_top_msg = f"║{'DEBUGGER'.center(padding_calculation)}║"
        debug_top_bar = f"{'╠' + ('═' * padding_calculation) + '╣'}"
        debug_bottom = f"╚{'═' * padding_calculation}╝"

        debugger_list.insert(0, debug_top)
        debugger_list.insert(1, debug_top_msg)
        debugger_list.insert(2, debug_top_bar)
        debugger_list.append(debug_bottom)

        _ = *map(print, debugger_list),


    @staticmethod
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

        if self.ping(self.host, self.username) != self.username:  # Validates remote path via ssh connection
            print("Host not up. Exiting.")
            raise SystemExit(0)

    @staticmethod
    def validate_path(path: str) -> bool:
        """Validate path"""
        return os.path.exists(path)

    def list_local_folder(self, local_path: str) -> list:
        """Lists a local folder using powershell"""
        file_types = f"*.{self.file_type}" if self.file_type else ""
        windows_cmdline = f"powershell -c \"(ls {local_path} {file_types}).Name\""
        command = subprocess.Popen(windows_cmdline, shell=True, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = command.communicate()
        windows_output: list = [x for x in output.split("\n") if x]
        return windows_output

    def echo_transport_direction(self, remote: str, local: str, reverse: bool = False) -> None:
        """Prints a transport direction"""
        if reverse:
            local, remote = remote, local

        print(
            f"{self.co('╔[', 'red')}Transport direction{self.co(']', 'red')}\n"
            f"{self.co('╚[', 'red')}{self.co(local, 'green')}{self.co(']', 'red')}"
            f"{self.co('═[>>>]═', 'red')}"
            f"{self.co('[', 'red')}{self.co(remote, 'blue')}{self.co(']', 'red')}")

    @staticmethod
    def ping(host: str, username: str) -> str:
        response_code, response_txt = subprocess.getstatusoutput(f'ssh {username}@{host} "whoami"')
        return response_txt  # Username

    def path_handler(self):
        """Replaces slashes based on OS"""
        if '/' in self.remote_path:
            """Linux System parsing of folder path"""
            self.host, path = self.remote_path.split("/", maxsplit=1)
            self.path = f"./{path}"
            self.operating_system = "Linux"

        elif '\\' in self.remote_path:
            """Windows System parsing of folder path"""
            self.host, path = self.remote_path.split("\\", maxsplit=1)
            self.path = fr".\{path}"
            self.operating_system = "Windows"

    def filetransfer(self, private_key: str = "~/.ssh/id_rsa") -> None:
        """Uses sftp to check remote folder and compare it to a local folder.
        The difference between those folders are copied to the local folder
        If no username is present, a local to local copy direction is used instead"""

        source_path: str = ""
        target_path: str = ""

        if not self.username:
            self.local_to_local()

            self.remote_files: list = self.list_local_folder(self.remote_path)
            self.local_files: list = self.list_local_folder(self.local_path)

            if not self.reverse:
                self.username = os.environ['USERNAME']
                self.host = os.environ['COMPUTERNAME']
                difference = set(self.remote_files).difference(set(self.local_files))  # Checks difference
                self.echo_transport_direction(self.local_path, self.remote_path)
            else:
                self.username = os.environ['USERNAME']
                self.host = os.environ['COMPUTERNAME']
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
                        self.co('+', 'green'),
                        self.co(self.username,
                                'green'),
                        self.co(self.host, 'green'),
                        self.co(self.path, 'green'),
                        self.co(d, 'green'))
                    print(output_format)

                    if self.transfer_files:
                        with open(source_path, 'rb') as rf:
                            file = rf.read()

                        with open(target_path, 'wb') as wf:
                            wf.write(file)
        else:
            self.remote_to_local()

            with pysftp.Connection(host=self.host, username=self.username, password=self.password,
                                   private_key=private_key) as sftp:
                self.remote_files: list = sorted(sftp.listdir(self.path))  # Music folder on my raspberry pi
                self.local_files: list = sorted(self.list_local_folder(self.local_path))

                if self.file_type:
                    self.remote_files = [x for x in self.remote_files if x.split('.')[-1] == self.file_type]
                    self.local_files = [x for x in self.local_files if x.split('.')[-1] == self.file_type]

                if not self.reverse:
                    loader = sftp.get
                    difference = set(self.remote_files).difference(set(self.local_files))  # Checks difference
                    self.echo_transport_direction(self.local_path, self.remote_path)
                else:
                    self.username = os.environ['USERNAME']
                    self.host = os.environ['COMPUTERNAME']
                    path = self.local_path
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
                            self.co('+', 'green'),
                            self.co(self.username,
                                    'green'),
                            self.co(self.host, 'green'),
                            self.co(self.path, 'green'),
                            self.co(d, 'green'))
                        print(output_format)

                        if self.transfer_files:
                            loader(remotepath=f"{self.path}/{d}", localpath=target_path)  # Does the heavy lifting

                else:
                    print("\x1b[1;31m[-]\x1b[0m Nothing to copy.")


def main() -> int:
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
