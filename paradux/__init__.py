import argparse
import importlib
import paradux.commands
import paradux.utils
import sys

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='The subcommand to invoke. Use "list" to show available sub-commands.')
    parser.add_argument('option', nargs=argparse.REMAINDER, help='Options for the sub-command.')
    parser.add_argument('-v', '--verbose', action="count", help='Display extra output. May be repeated for even more output.')

    args,remaining = parser.parse_known_args(sys.argv[1:])
    cmd = args.command

    cmds = paradux.utils.findSubmodules(paradux.commands)
    if(cmd in cmds):
        mod=importlib.import_module('paradux.commands.' + cmd)
        mod.run()
    else:
        print('Command not found')

