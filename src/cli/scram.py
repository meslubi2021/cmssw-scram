#!/usr/bin/env python3
from sys import exit, argv, path
from os import environ
from os.path import dirname, abspath, join
from inspect import getmembers, isfunction

path.insert(0, dirname(dirname(abspath(argv[0]))))
import SCRAM

#Parse common arguments
def parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(add_help=False)
    parser.add_argument('-a', '--arch',
                        dest='arch',
                        type=str,
                        default=None,
                        help='Override the SCRAM_ARCH environment variable value.')
    parser.add_argument('-f', '--force',
                        dest='force',
                        action='store_true',
                        default=False,
                        help='Force changes without asking.')
    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        action='store_true',
                        default=False,
                        help='Turns on any verbose output.')
    parser.add_argument('-h', '--help',
                        dest='help',
                        action='store_true',
                        default=False,
                        help='Print help message.')
    parser.add_argument('--debug',
                        dest='debug',
                        action='store_true',
                        default=False,
                        help='Turns on any debug output.')
    opts, args = parser.parse_known_args()
    if not args: args.append('help')
    if opts.help: args[0]='help'
    if opts.arch:
        environ ['SCRAM_ARCH'] = opts.arch
        SCRAM.FORCED_ARCH = opts.arch
    return (opts, args)

def usage(commands):
    usage = "***************************************************\n"
    usage+="SCRAM HELP ------------- Recognised Commands\n"
    usage+="***************************************************\n"
    usage+="\n"
    for cmd in commands:
      usage+="\t scram %s\n" % cmd
    usage+="\n"
    usage+= "See scram manual pages for detail documentation about these commands.\n"
    return usage

#Initialize SCRAM env
def initialize_scram():
    dbpath          = SCRAM.BASEPATH
    dbpath_rw       = SCRAM.BASEPATH
    environ['SCRAM_VERSION'] = SCRAM.VERSION
    if not 'SCRAM_LOOKUPDB' in environ:
        if 'SCRAM_USERLOOKUPDB' in environ:
            dbpath = environ['SCRAM_USERLOOKUPDB']
            dbpath_rw = dbpath
        environ['SCRAM_LOOKUPDB'] = dbpath
    if not 'SCRAM_LOOKUPDB_WRITE' in environ:
       if 'SCRAM_USERLOOKUPDB' in environ:
           dbpath_rw = environ['SCRAM_USERLOOKUPDB']
       environ['SCRAM_LOOKUPDB_WRITE'] = dbpath_rw

#Run scram command
def execcommand(args):
    import SCRAM.Core.CMD as scram_commands
    commands = [ cmd[0][4:] for cmd in getmembers(scram_commands, isfunction)
                 if cmd[0].startswith('cmd_')]
    cmd = args.pop(0)
    cmds = [ c for c in commands if c==cmd ]
    if len(cmds)==0:
        cmds = [ c for c in commands if c.startswith(cmd) ]
    cmds_count = len(cmds)
    if cmds_count>1:
        print ("ERROR: %s commands matched '%s': %s" %  (cmds_count, cmd,", ".join(cmds)));
        exit(1)
    if cmds_count==0:
        print (usage(commands))
        exit(1)
    initialize_scram()
    return eval('scram_commands.cmd_%s' % cmds[0])(args)

opts, args = parse_args()
if not execcommand (args): exit(1)

