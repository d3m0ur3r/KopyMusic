import sys
import argparse

banner = r"""
 _   __                     ___  ___             _       
| | / /                     |  \/  |            (_)      
| |/ /   ___   _ __   _   _ | .  . | _   _  ___  _   ___ 
|    \  / _ \ | '_ \ | | | || |\/| || | | |/ __|| | / __|
| |\  \| (_) || |_) || |_| || |  | || |_| |\__ \| || (__ 
\_| \_/ \___/ | .__/  \__, |\_|  |_/ \__,_||___/|_| \___|
              | |      __/ |                             
              |_|     |___/                              
"""

banner = f"\x1b[1;32m{banner}\x1b[0m"  # Adds color


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
                        metavar='Remote',
                        type=str,
                        required=True,
                        help=r'Remote path e.g. Hostname\Users\MyUser\Music')

    parser.add_argument('-l', '--local',
                        action='store',
                        metavar='Local',
                        type=str,
                        required=True,
                        help=r'Local folder e.g. C:\Users\MyUser\Music.')

    parser.add_argument('-u', '--username',
                        action='store',
                        metavar='Username',
                        help='Username is only for network transfers.')

    parser.add_argument('-p', '--password',
                        action='store',
                        metavar='Password',
                        help='sftp password (ssh)')

    parser.add_argument('-k', '--key',
                        action='store',
                        metavar='Private key',
                        help='Specify key path, common path: "~/.ssh/id_rsa"')

    parser.add_argument('--reverse',
                        action='store_true',
                        help='Reverses the copy direction from "remote >> local" to "local >> remote"')

    parser.add_argument('-m', '--mirror',
                        action='store_true',
                        help='Mirrors path')

    parser.add_argument('-t', '--transfer',
                        action='store_true',
                        help='Signals the program to copy the Music')

    parser.add_argument('--ext',
                        action='store',
                        metavar='File type',
                        nargs="+",
                        help='Specify file type extension e.g. .mp3 mp4 etc.')

    parser.add_argument('-P', '--port',
                        action='store',
                        metavar='Port',
                        type=int,
                        default=22,
                        help='Specify port number. Defaults to 22')

    parser.add_argument('--debug',
                        action='store_true',
                        help=argparse.SUPPRESS)

    parser.add_argument('-v', action='version',
                        version=f'{banner}'
                                f'\nKopy '
                                f'\nMusic '
                                f'\nv0.2 by \x1b[1;3;32md3m0ur3r\x1b[0m ',
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
