import os
import re
import platform


class SSHConfig:
    def __init__(self, operating_system):
        super(SSHConfig, self).__init__()

        self.operating_system = operating_system
        self.home = KMOperatingSystem().determine_os()[-1]
        self.ssh_config_path = self.config_path()

    def config_path(self):
        if self.operating_system == 'Windows':
            return f"{self.home}\\.ssh\\config"
        else:
            return f"{self.home}/.ssh/config"

    def find_user_ssh_config(self, username: str) -> dict.values:
        """Finds local .ssh/config if present and returns HostName and User"""

        host = ''
        users: dict = {'Host': {}}

        if os.path.exists(self.ssh_config_path):
            with open(self.ssh_config_path, 'r') as f:
                lines: list = f.readlines()

        for line in lines:
            host_pattern = re.compile(r'^(\w+)\s(.+)')
            host_search = re.search(host_pattern, line)

            if host_search:
                host = host_search.group().split(' ')[-1].lower()
                users['Host'].update({host: {}})

            config_pattern = re.compile(r'^\s+.+')
            config_search = re.search(config_pattern, line)

            if config_search:
                key, val = config_search.group().strip().split(' ')

                users['Host'][host].update({key: val})

        result: dict = users['Host'].get(username.lower())
        if result:
            return result.values()


class KMOperatingSystem:
    def __init__(self):
        super(KMOperatingSystem, self).__init__()

        self.operating_system: str = 'OS'
        self.username: str = 'Username'
        self.host: str = 'Host'
        self.home_path: str = 'HomePath'

    def determine_os(self) -> tuple[str, str, str]:
        """Determines the OS"""

        self.operating_system = platform.system()

        if self.operating_system == 'Windows':
            self.username = os.environ['USERNAME']
            self.host = os.environ['COMPUTERNAME']
            self.home_path = os.environ['HOMEPATH']
        else:  # Linux
            self.username = os.environ['USER']
            self.host = os.uname().nodename
            self.home_path = os.environ['HOME']

        return self.username, self.host, self.home_path


def main() -> int:
    print(SSHConfig('Windows').find_user_ssh_config('pialps'))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
