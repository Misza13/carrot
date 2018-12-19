from argparse import ArgumentParser

from carrot.carrot import Carrot


def main():
    commands = [
        StatusCommand(),
        ListCommand(),
        InstallCommand(),
        InitCommand()
    ]

    ap = ArgumentParser(prog='carrot')

    subparsers = ap.add_subparsers()

    for cmd in commands:
        cmd.register_help(subparsers)

    args = ap.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        ap.print_help()


class Command(object):
    carrot = Carrot()

    def register_help(self, subparsers):
        raise NotImplementedError()

    def handle_args(self, args):
        raise NotImplementedError()


class StatusCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'status',
            help='Display a summary of current mod directory')

        parser.set_defaults(func=self.handle_args)

    def handle_args(self, args):
        if self.carrot.initialized():
            print('Mod repo status: OK')
        else:
            print('Mod repo status: INVALID')
            print('This directory does not appear to be a valid mod repo.')



class ListCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'list',
            help='List mods installed in current directory')

        parser.set_defaults(func=self.handle_args)


class InitCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'init',
            help='Initialize a mod repo in current directory.'
        )

        parser.add_argument(
            '--name',
            help='Name of this repo/modpack'
        )
        parser.add_argument(
            '--mc_version',
            help='Minecraft version',
            required=True
        )
        parser.add_argument(
            '--channel',
            help='Mod release channel',
            choices=['Alpha', 'Beta', 'Release'],
            default='Beta'
        )

        parser.set_defaults(func=self.handle_args)

    def handle_args(self, args):
        if self.carrot.initialized():
            print('ERROR! This directory is already a mod repo.')
        else:
            self.carrot.initialize(vars(args))
            print('Repo initialized.')


class InstallCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'install',
            help='Install a mod and its dependencies')

        parser.add_argument(
            'mod_key',
            help='"Key" id of a mod *exactly* as used in e.g. CurseForge URLs. '
                 'If no mod matches exactly, a list of possible matches will be displayed.')

        parser.set_defaults(func=self.handle_args)


if __name__ == '__main__':
    main()