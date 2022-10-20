"""KopyMusic Pseudo-shell.
WORK IN PROGRESS"""
import os


# ═════════════════════════════════════════════════[ Work In Progress ]═══════════════════════════════════════════════ #
class PseudoShell:
    def __int__(self):
        super(PseudoShell, self).__init__()

        self.usr_input = ""
        self.shell_commands = ['ls']

    @staticmethod
    def run_shell(dir_name: str, files: list):
        while True:
            usr = input(f'{dir_name}: ')

            if usr.lower() == 'ls':
                _ = *map(print, files),

            elif usr.lower() == 'exit':
                break
# ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════ #


def main() -> int:
    pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
