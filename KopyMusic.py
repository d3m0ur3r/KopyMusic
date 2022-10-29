import platform
import os
from km_argparser import arg_parser
import re
from rich.table import Table
from rich.live import Live
from km_utils import SSHConfig
from km_pseudoshell import PseudoShell


class KopyMusic:
    def __init__(self):
        super(KopyMusic, self).__init__()

        self.args = arg_parser()  # Argparse engage
        # ═══════════════════════════════════════════════[ Args String ]══════════════════════════════════════════════ #
        self.remote_path: str = self.args.remote  # String
        self.local_path: str = self.args.local  # String
        self.username: str = self.args.username  # String
        self.password: str = self.args.password  # String
        self.search: str = self.args.search  # String
        # ═══════════════════════════════════════════════[ Args Bools ]═══════════════════════════════════════════════ #
        self.reverse: bool = self.args.reverse  # Switch
        self.mirror: bool = self.args.mirror  # Switch
        self.transfer_files: bool = self.args.transfer  # Switch
        self.clobber: bool = self.args.clobber  # Switch
        self.debug: bool = self.args.debug  # Switch
        self.shell: bool = self.args.shell  # Switch
        # ═══════════════════════════════════════════════[ Args Lists ]═══════════════════════════════════════════════ #
        self.extension: list = self.args.ext  # List
        # ════════════════════════════════════════════════[ Args Ints ]═══════════════════════════════════════════════ #
        self.port: int = self.args.port  # Int
        # ════════════════════════════════════════════════════════════════════════════════════════════════════════════ #

        self.title: str = ''
        self.host: str = 'Host'
        self.path: str = 'Path'
        self.remote_operation_system: str = 'OS'
        self.local_operating_system: str = 'OS'

        self.remote_files: list = []
        self.local_files: list = []

        # ═══════════════════════════════════════════════[ Runs Script ]═════════════════════════════════════════════ #
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
        # ═══════════════════════════════════════════════════════════════════════════════════════════════════════════ #

    def debugger(self) -> None:
        """Debugger menu"""

        table = Table()
        table.add_column('[yellow]Arg', justify='left')
        table.add_column('[green]Value', justify='left')

        with Live(table, refresh_per_second=10):
            for k, v in self.args.__dict__.items():
                table.add_row(f'[yellow]{k.title()}', f'[green]{v}')

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
        # No use as of v0.2
        if not self.validate_path(self.local_path):
            print("Local path not valid.")
            raise SystemExit(0)

    @staticmethod
    def validate_path(path: str) -> bool:
        """Validate path"""
        return os.path.exists(path)

    def list_local_folder(self, path: str) -> list:
        """Lists a local folder using powershell"""
        self.local_operating_system = platform.system()

        list_output: list = os.listdir(path)
        return list_output

    def path_handler(self):
        """Replaces slashes based on OS"""

        if self.local_operating_system == 'Windows':
            slash = '\\'
        else:
            slash = '/'

        # ════════════════════════════════════════════[ Ssh Config Handle ]══════════════════════════════════════════ #

        try:
            r_host, r_path = self.remote_path.split(slash, maxsplit=1)
        except ValueError:
            r_host = self.remote_path
            r_path = "Music"

        check_ssh_config: dict.values = SSHConfig(self.local_operating_system).find_user_ssh_config(
            r_host)  # Finds .ssh/config and uses hostname and user

        if check_ssh_config:
            r_host, self.username = check_ssh_config
            self.remote_path = os.path.join(r_host, r_path)

        self.host = r_host
        self.path = r_path

        # ════════════════════════════════════════════[ Local Path Handle ]══════════════════════════════════════════ #

        if self.local_path[2:] == os.environ.get('HOMEPATH'):

            try:
                l_host, l_path = self.local_path.split(slash, maxsplit=1)
            except ValueError:
                l_host = self.local_path
                l_path = "Music"
            self.local_path = os.path.join(l_host, l_path)

        # ═══════════════════════════════════════════════════════════════════════════════════════════════════════════ #

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
        if '*' in self.extension:
            return files
        else:
            return [x for x in files if x.split('.')[-1] in self.extension]

    def source_dest_handler(self, files, mode='local') -> tuple[list, list] or list:
        """Handles transfer paths. Returns two list with source and destination paths.
        If mode is set to 'remote', then only destination path are returned.
        """

        source_path: list = []
        dest_path: list = []

        if self.local_operating_system == "Windows":
            source_path = [os.path.join(self.remote_path, d) for d in files]  # From path
            dest_path = [os.path.join(self.local_path, d) for d in files]  # To path
            # copy_mode = "robocopy" # Possible future upgrade
        elif self.local_operating_system == "Linux":
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

        # print(self.local_path)
        # print(self.remote_path)
        if not self.reverse:
            self.title = self.remote_path.replace('\\', ' | ').replace('/', ' | ')
        else:
            self.title = self.local_path.replace('\\', ' | ').replace('/', ' | ')

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
                table.title = self.title
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
                # file_names = []
                # dir_names = []
                # un_name = []
                # sftp.walktree(self.path, lambda x: file_names.append(x), lambda y: dir_names.append(y),
                #               lambda z: un_name.append(z), recurse=True)
                # print(len(file_names))
                # print(len(dir_names))
                # print(un_name)

                if 'home' in sftp.pwd:
                    self.remote_operation_system = 'Linux'
                    self.remote_path.replace('\\', '/')
                else:
                    self.remote_operation_system = 'Windows'
                    self.remote_path.replace('/', '\\')

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

                # ═════════════════════════════════════════[ Work In Progress ]═══════════════════════════════════════ #
                if self.shell:
                    PseudoShell().run_shell(self.remote_path, self.remote_files)
                # ════════════════════════════════════════════════════════════════════════════════════════════════════ #

                if files:
                    files = sorted(files)
                    table = Table()
                    table.title = self.title
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
