from argparse import ArgumentParser, SUPPRESS

from carrot_mc.carrot import CarrotService


def main():
    commands = [
        StatusCommand(),
        #ListCommand(),
        InstallCommand(),
        InitCommand(),
        UpdateCommand()
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
    carrot_service = CarrotService()

    def register_help(self, subparsers):
        raise NotImplementedError()

    def handle_args(self, args):
        raise NotImplementedError()


class StatusCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'status',
            help='Display a summary of current mod directory'
        )

        parser.set_defaults(func=self.handle_args)

    def handle_args(self, args):
        if self.carrot_service.initialized():
            print('Mod repo status: OK')
            self.carrot_service.status(args)
        else:
            print('Mod repo status: INVALID')
            print('This directory does not appear to be a valid mod repo.')


class ListCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'list',
            help='List mods installed in current directory'
        )

        parser.set_defaults(func=self.handle_args)

        # TODO: Implement


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
        if self.carrot_service.initialized():
            print('ERROR! This directory is already a mod repo.')
        else:
            self.carrot_service.initialize(vars(args))
            print('Repo initialized.')


class InstallCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'install',
            help='Install a mod and its dependencies'
        )

        parser.add_argument(
            'mod_key',
            help='"Key" id of a mod *exactly* as used in e.g. CurseForge URLs. '
                 'If no mod matches exactly, a list of possible matches will be displayed.',
            nargs='+'
        )

        parser.add_argument(
            '--channel',
            help='Specify channel (Alpha/Beta/Release) to use when installing. '
                 'Overrides settings from mods.json.',
            choices=['Alpha', 'Beta', 'Release'],
            default=None
        )

        parser.add_argument(
            '--upgrade',
            help='Specify that upgrading mods to newer versions is allowed. '
                 'By default when a mod or dependency is already installed and a new version is found '
                 'during installation, it will be skipped for safety reasons.',
            nargs='?',
            const=True
        )

        parser.add_argument(
            '--downgrade',
            help='Specify that a downgrade to an older version is allowed. '
                 'This can happen e.g. if you explicitly request a Release channel but '
                 'already have a newer Beta file installed.',
            nargs='?',
            const=True
        )

        parser.set_defaults(func=self.handle_args)
    
    def handle_args(self, args):
        self.carrot_service.install(args)


class UpdateCommand(Command):
    def register_help(self, subparsers):
        parser = subparsers.add_parser(
            'update',
            help='Update a currently-installed mod (and its dependencies) or all mods to newer/older version and/or different channel.'
        )

        parser.add_argument(
            'mod_key',
            help='"Key" id of a mod to update (along with its dependencies).',
            nargs='?',
            default=None
        )

        parser.add_argument(
            '--channel',
            help='Specify target channel (Alpha/Beta/Release) to use when updating. '
                 'Overrides settings from mods.json.',
            choices=['Alpha', 'Beta', 'Release'],
            default=None
        )

        # Hidden "option" for compatibility in the installer logic
        parser.add_argument(
            '--upgrade',
            help=SUPPRESS,
            nargs='?',
            default=True
        )

        parser.add_argument(
            '--downgrade',
            help='Specify that downgrades to an older version are allowed. '
                 'This can happen e.g. if you explicitly request a Release channel but '
                 'already have newer versions of mods from the Beta channel installed.',
            nargs='?',
            const=True
        )

        parser.set_defaults(func=self.handle_args)

    def handle_args(self, args):
        self.carrot_service.update(args)


if __name__ == '__main__':
    main()