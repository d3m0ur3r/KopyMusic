import sys
import argparse
import os
from km_utils import KMOperatingSystem

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

_, _, home_path = KMOperatingSystem().determine_os()


def arg_parser() -> argparse.Namespace:
    # ArgParser - Define Usage
    prog_name = sys.argv[0]
    parser = argparse.ArgumentParser(prog=prog_name,
                                     epilog=r"""
 *    KopyMusic does 'no-clobber' by default.
 **   KopyMusic uses sftp to connect to remote path.
 ***  KopyMusic defaults to the users Music path if no path is specified.
 **** KopyMusic tries to use '.ssh/config' if host is found in given config.
╔══════════════════════════════════════[ Examples ]═════════════════════════════════════╗
║  -u jack -p 12345678 -r 192.168.1.110 -l $HOME -t                                     ║
║  -u jack -r 192.168.1.110/Music -l ~/Music/ -t                                        ║
║  -u jack -r 192.168.1.110/Music -l ~/Music/ --reverse -t #Reverses the copy direction ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
""",
                                     usage=f"KopyMusic [options] -r [remote path] -l [local path]",
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
                        default=os.path.join(home_path, 'Music'),
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

    parser.add_argument('-R', '--reverse',
                        action='store_true',
                        help='Reverses the copy direction from "remote >> local" to "local >> remote"')

    parser.add_argument('-m', '--mirror',
                        action='store_true',
                        help='Mirror paths')

    parser.add_argument('-t', '--transfer',
                        action='store_true',
                        help='Signals the program to copy the files')

    parser.add_argument('-E', '--ext',
                        action='store',
                        metavar='File type',
                        nargs="+",
                        default='mp3 mp4',
                        help='Specify file type. Default is mp3 mp4')

    parser.add_argument('-P', '--port',
                        action='store',
                        metavar='Port',
                        type=int,
                        default=22,
                        help='Specify port number. Defaults to 22')

    parser.add_argument('-c', '--clobber',
                        action='store_true',
                        help='Overwrites any existing files')

    parser.add_argument('-s', '--search',
                        action='store',
                        metavar='Search',
                        nargs='+',
                        help='Search for a filename(s)')

    parser.add_argument('-S', '--shell',
                        action='store_true',
                        help='Creates a pseudo-shell for ease of use [Needs works].')

    parser.add_argument('--debug',
                        action='store_true',
                        help=argparse.SUPPRESS)

    parser.add_argument('-v', action='version',
                        version=f'{banner}'
                                f'\nKopy '
                                f'\nMusic '
                                f'\nv0.3 by \x1b[1;3;32md3m0ur3r\x1b[0m ',
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
