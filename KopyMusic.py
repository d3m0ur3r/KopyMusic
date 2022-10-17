import platform
import os
from km_argparser import arg_parser
import re
from rich.table import Table
from rich.live import Live


class KopyMusic:
    def __init__(self):
        super(KopyMusic, self).__init__()

        self.args = arg_parser()

        self.remote_path: str = self.args.remote
        self.local_path: str = self.args.local
        self.username: str = self.args.username
        self.password: str = self.args.password
        self.extension: list = self.args.ext
        self.search: str = self.args.search
        self.reverse: bool = self.args.reverse  # Switch
        self.mirror: bool = self.args.mirror  # Switch
        self.transfer_files: bool = self.args.transfer  # Switch
        self.clobber: bool = self.args.clobber  # Switch
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

    def debugger(self) -> None:
        """Debugger menu"""
        debugger_list = [f"Remote Path:    {self.remote_path}",
                         f"Local Path:     {self.local_path}",
                         f"Username:       {self.username}",
                         f"Password:       {self.password}",
                         f"Reverse:        {self.reverse}",
                         f"Mirror:         {self.mirror}",
                         f"Extension:      {self.extension}",
                         f"Port:           {self.port}",
                         f"Search:         {self.search}",
                         f"Clobber:        {self.clobber}",
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

    def local_to_local(self) -> None:
        """local path filetransfer"""

        if self.remote_path == self.local_path:
            print("Paths can't be identical.")
            raise SystemExit(0)

        if not self.validate_path(self.local_path):
            print("Local path not valid.")
            raise SystemExit(0)

        if not self.validate_path(self.remote_path):
            pattern = re.compile(r'((\d){1,3}\.){3}(\d){1,3}')  # Detects ip
            try:
                string_check = re.search(pattern=pattern, string=self.remote_path).group()
                if string_check:
                    print("Missing username e.g. -u <USERNAME>")
            except AttributeError:
                print("Remote path not valid")

            raise SystemExit(0)

    def remote_to_local(self) -> None:
        """Uses sftp to connect to remote path"""
        if not self.validate_path(self.local_path):
            print("Local path not valid.")
            raise SystemExit(0)

    @staticmethod
    def validate_path(path: str) -> bool:
        """Validate path"""
        return os.path.exists(path)

    def list_local_folder(self, path: str) -> list:
        """Lists a local folder using powershell"""
        self.operating_system = platform.system()

        list_output: list = os.listdir(path)
        return list_output

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

    def search_files(self, files: list) -> list:
        """Searches for input given and returns a list"""

        search_list: list = []
        for x in files:
            for y in self.search:
                if y.lower() in x.lower():
                    search_list.append(x)

        return search_list

    def file_extension(self, files: list) -> list:
        """Checks file extension"""
        if 'all' in self.extension:
            return files
        else:
            return [x for x in files if x.split('.')[-1] in self.extension]

    def source_dest_handler(self, files, mode='local') -> tuple[list, list] or list:
        """Handles transfer paths. Returns two list with source and destination paths.
        If mode is set to 'remote', then only destination path are returned.
        """

        source_path: list = []
        dest_path: list = []

        if self.operating_system == "Windows":
            source_path = [os.path.join(self.remote_path, d) for d in files]  # From path
            dest_path = [os.path.join(self.local_path, d) for d in files]  # To path
            # copy_mode = "robocopy" # Possible future upgrade
        elif self.operating_system == "Linux":
            source_path = [os.path.join(self.remote_path, d).replace("\\", "/") for d in files]  # From path
            dest_path = [os.path.join(self.local_path, d).replace("\\", "/") for d in files]  # To path
            # copy_mode = ""

        if mode == 'local':
            return source_path, dest_path
        elif mode == 'remote':
            del source_path
            return dest_path

    def filetransfer(self, private_key: str = "~/.ssh/id_rsa") -> None:
        """Uses sftp to check remote folder and compare it to a local folder.
        The difference between those folders are copied to the local folder
        If no username is present, a local to local copy direction is used instead.
        """

        # username, host = self.determine_os()

        if not self.username:  # Local to local transfer
            # print(self.username) # Debug
            self.local_to_local()  # Checks if paths are valid

            self.remote_files: list = self.list_local_folder(self.remote_path)
            self.local_files: list = self.list_local_folder(self.local_path)

            if self.extension:  # --ext
                self.remote_files: list = self.file_extension(self.remote_files)
                self.local_files: list = self.file_extension(self.local_files)

            if self.search:
                self.remote_files: list = self.search_files(self.remote_files)
                self.local_files: list = self.search_files(self.local_files)

            if not self.reverse:
                self.path = self.remote_path
                files = set(self.remote_files).difference(set(self.local_files))  # Checks difference
            else:
                self.path = self.local_path
                files = set(self.local_files).difference(set(self.remote_files))  # Checks difference

            if files:
                files = sorted(files)
                table = Table()
                table.title = self.path
                table.add_column('[yellow]No.', justify='left')
                table.add_column('[#F5F5F5]FILENAME', justify='left')
                source_path, dest_path = self.source_dest_handler(files)
                source_path: list = source_path
                dest_path: list = dest_path

                with Live(table, refresh_per_second=10):
                    for idx, (source, dest, file) in enumerate(zip(source_path, dest_path, files), start=1):

                        if self.reverse:
                            source, dest = dest, source

                        table.add_row(f'[#9ACD32]{idx:0>3}', f'{file}')

                        try:
                            if self.transfer_files:
                                table.add_row(f'[#9ACD32]{idx:0>3}', f'{file}')
                                with open(source, 'rb') as rf:
                                    read_file = rf.read()

                                with open(dest, 'wb') as wf:
                                    wf.write(read_file)
                        except PermissionError:
                            print("Can't copy directory")
                            raise SystemExit(0)
            else:
                print("\x1b[1;31m[-]\x1b[0m Nothing to copy.")

        else:
            self.remote_to_local()  # Checks if paths are valid and remote host is up

            import pysftp
            with pysftp.Connection(host=self.host, username=self.username, password=self.password,
                                   private_key=private_key, port=self.port) as sftp:

                self.remote_files: list = sftp.listdir(self.path)
                self.local_files: list = self.list_local_folder(self.local_path)

                if self.extension:
                    self.remote_files: list = self.file_extension(self.remote_files)
                    self.local_files: list = self.file_extension(self.local_files)

                if self.search:
                    self.remote_files: list = self.search_files(self.remote_files)
                    self.local_files: list = self.search_files(self.local_files)

                if not self.reverse:
                    loader = sftp.get
                    files = set(self.remote_files).difference(set(self.local_files))  # Checks difference
                else:

                    loader = sftp.put
                    files = set(self.local_files).difference(set(self.remote_files))  # Checks difference

                if files:
                    files = sorted(files)
                    table = Table()
                    table.title = self.path
                    table.add_column('[yellow]No.', justify='left')
                    table.add_column('[#F5F5F5]FILENAME', justify='left')
                    dest_path = self.source_dest_handler(files, mode='remote')

                    with Live(table, refresh_per_second=10):

                        for idx, (dest, file) in enumerate(zip(dest_path, files), start=1):

                            if self.transfer_files:
                                table.add_row(f'[#9ACD32]{idx:0>3}', f'{file}')
                                loader(remotepath=f"{self.path}/{file}", localpath=dest)  # Does the heavy lifting
                            else:
                                table.add_row(f'[#9ACD32]{idx:0>3}', f'{file}')
                else:
                    print("[\x1b[1;31m-\x1b[0m] Nothing to copy.")


def main() -> int:
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
