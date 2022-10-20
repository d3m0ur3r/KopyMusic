import os
import re


class SSHConfig:
    def __init__(self):
        super(SSHConfig, self).__init__()

        self.home = os.environ.get('HOMEPATH')
        self.ssh_config_path = f"{self.home}\\.ssh\\config"

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


def main() -> int:
    print(SSHConfig().find_user_ssh_config('pi'))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
