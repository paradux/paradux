import paradux.utils

def run() :
    cmds = paradux.utils.findSubmodules(paradux.commands)
    print('List of known sub-commands:')
    for cmd in sorted(cmds) :
        print( '    ' + cmd )
