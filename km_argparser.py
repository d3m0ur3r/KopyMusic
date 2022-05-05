import sys
import argparse

banner = """\x1b[1;32m
 _   __                     ___  ___             _       
| | / /                     |  \/  |            (_)      
| |/ /   ___   _ __   _   _ | .  . | _   _  ___  _   ___ 
|    \  / _ \ | '_ \ | | | || |\/| || | | |/ __|| | / __|
| |\  \| (_) || |_) || |_| || |  | || |_| |\__ \| || (__ 
\_| \_/ \___/ | .__/  \__, |\_|  |_/ \__,_||___/|_| \___|
              | |      __/ |                             
              |_|     |___/                              
\x1b[0m"""


def arg_parser() -> argparse.Namespace:
    # ArgParser - Define Usage
    prog_name = sys.argv[0]
    parser = argparse.ArgumentParser(prog=prog_name,
                                     epilog=r"""
 *   KopyMusic does 'no-clobber' by default.
 **  KopyMusic uses sftp to connect to remote path.
╔══════════════════════════════════════[ Examples ]═════════════════════════════════════╗                                         
║  -u jack -r 192.168.1.110/Music -l C:\Users\Jack\Music -t    #Linux to Windows        ║
║  -u jack -r 192.168.1.110/Music -l ~/Music/ -t               #Linux to Linux          ║
║  -u jack -r 192.168.1.110/Music -l ~/Music/ --reverse -t #Reverses the copy direction ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
""",
                                     usage=f"{prog_name} [options] -u [user] -r [remote path] -l [local path]",
                                     prefix_chars="-",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-r', '--remote',
                        action='store',
                        metavar='\tRemote',
                        type=str,
                        required=True,
                        help=r'Remote path e.g. Hostname\Users\MyUser\Music')

    parser.add_argument('-l', '--local',
                        action='store',
                        metavar='\tLocal',
                        type=str,
                        required=True,
                        help=r'Local folder e.g. C:\Users\MyUser\Music.')

    parser.add_argument('-u', '--username',
                        action='store',
                        metavar='Username',
                        help='Username is required, if remote path is over the network.')

    parser.add_argument('-k', '--key',
                        action='store',
                        metavar='Private key',
                        help='Specify key path, common path: "~/.ssh/id_rsa"')

    parser.add_argument('--reverse',
                        action='store_true',
                        help='Reverses the copy direction from "remote >> local" to "local >> remote"')

    parser.add_argument('-t',
                        action='store_true',
                        help='Signals the program to copy the Music')

    parser.add_argument('--debug',
                        action='store_true',
                        help=argparse.SUPPRESS)

    parser.add_argument('-v', action='version',
                        version=f'{banner}'
                                f'\nKopy '
                                f'\nMusic '
                                f'\nv0.1 by \x1b[1;32md3m0ur3r\x1b[0m ',
                        help=f'Prints the version of {prog_name}')

    args = parser.parse_args()  # Engages ArgParser

    # ═══════════════════════════════════════════════[ ARGS ]════════════════════════════════════════════════════ #

    # ═══════════════════════════════════════════════════════════════════════════════════════════════════════════ #

    return args


def main() -> int:
    print(arg_parser())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
