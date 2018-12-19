from argparse import ArgumentParser


def main():
    commands = [
        StatusCommand(),
        ListCommand(),
        InstallCommand()
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


class ListCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'list',
            help='List mods installed in current directory')

        parser.set_defaults(func=self.handle_args)


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