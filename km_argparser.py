import sys
import argparse

banner = r"""
 _____  _    _  _____ 
/  ___|| |  | |/  ___|
\ `--. | |  | |\ `--. 
 `--. \| |/\| | `--. \
/\__/ /\  /\  //\__/ /
\____/  \/  \/ \____/ 
"""


def arg_parser() -> argparse.Namespace:
    # ArgParser - Define Usage
    prog_name = sys.argv[0]
    parser = argparse.ArgumentParser(prog=prog_name,
                                     epilog=f"""
╔══════════════════════════════════════[ Examples ]═════════════════════════════════════╗                                         
║  -c                                                                                   ║
║  -i <APP_ID> -fac -s <SEARCH_STRING>                                                  ║
║  -i <APP_ID> -fc --most-subs -s <SEARCH_STRING> -r <RANGE>                            ║
║  -i <APP_ID> -fac --most-subs -s <SEARCH_STRING> -r <RANGE>                           ║
║  -i <APP_ID> -u <USER_ID>                                                             ║
║  -i <APP_ID> -u <USER_ID> -s <SEARCH_STRING>                                          ║
║  -i <APP_ID> -r <RANGE> --filter-author <AUTHOR_NAME>                                 ║ 
╠═══════════════════════════════════════════════════════════════════════════════════════╣
║  SWS is a script designed to scrape steam workshop for mods.                          ║
║  It does so by looking through a range of pages and then scrape all the urls.         ║
║  Should be used in conjunction with https://steamworkshopdownloader.io/               ║
║  For more information, see https://github.com/d3m0ur3r/sws                            ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
""",
                                     usage=f"{prog_name} [options] -i <appid>",
                                     prefix_chars="-",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-r', '--range',
                        action='store',
                        metavar='\tRange',
                        default='1',
                        type=str,
                        help=f'[lownum-highnum] example: 1-40 or 1 for page 1 etc.')

    parser.add_argument('-u', '--user',
                        action='store',
                        metavar='\tUser',
                        type=str,
                        help='Searches for mods at a user with app id')

    parser.add_argument('-e', '--echo',
                        action='store_true',
                        help='Echoes output to terminal')

    parser.add_argument('--clear-cache',
                        action='store_true',
                        help='Clears cache for given AppID')

    parser.add_argument('--rich-table',
                        action='store_true',
                        help='Uses rich tables to display output')

    parser.add_argument('--debug',
                        action='store_true',
                        help=argparse.SUPPRESS)

    parser.add_argument('-c', '--color',
                        action='store_true',
                        help="Colors the output")

    parser.add_argument('-f', '--fast',
                        action='store_true',
                        help='Improves performance')

    parser.add_argument('-a', '--all',
                        action='store_true',
                        help='Gets all output')

    parser.add_argument('--most-subs',
                        action='store_true',
                        help='Sorts by most subscribed of all time')

    parser.add_argument('--filter-author',
                        action='store',
                        metavar='\tFilter Author',
                        nargs='+',
                        help='Filters chosen author')

    parser.add_argument('--sort-by',
                        action='store',
                        metavar='Sort',
                        type=str,
                        help='Sorts by chosen input [ID, STARS, AUTHOR, USERID, TITLE]')

    parser.add_argument('-s', '--search',
                        action='store',
                        metavar='Search',
                        type=str,
                        nargs='+',
                        help="Searches for a particular mod")

    parser.add_argument('-i', '--id',
                        action='store',
                        metavar='AppId',
                        type=int,
                        default=107410,
                        required=False,
                        help=f'Steam AppId number example: 920210')

    parser.add_argument('-o', '--outfile',
                        action='store',
                        metavar='Outfile',
                        type=str,
                        help='Saves output to a file')

    parser.add_argument('-v', action='version',
                        version=f'{banner}'
                                f'\nSteam '
                                f'\nWorkshop '
                                f'\nScraper v1.5.1 by \x1b[1;32md3m0ur3r\x1b[0m ',
                        help=f'Prints the version of {prog_name}')

    args = parser.parse_args()  # Engages ArgParser

    # ═══════════════════════════════════════════════[ ARGS ]════════════════════════════════════════════════════ #
    sws_range = "1" if not args.range else args.range  # flag -r, --range,     defaults to page 1
    sws_app_id = 107410 if not args.id else args.id  # flag -i, --id,        defaults to 107410
    sws_all = args.all  # flag -a, --all
    sws_output = args.outfile  # flag -o, --output
    sws_echo = True if not sws_output else args.echo  # flag -e, --echo       True if not -o
    sws_search = args.search  # flag -s, --search
    sws_fast = args.fast  # flag -f, --fast
    sws_rich = args.rich_table  # flag     --rich-table
    sws_color = args.color  # flag -c, --color
    sws_most_subs = args.most_subs  # flag     --most-subs
    sws_filter_author = args.filter_author  # flag     --filter-author
    sws_sort_by = args.sort_by  # flag    --sort-by
    sws_user_id = args.user  # flag -u, --user
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════════════ #

    return args


def main() -> int:
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
