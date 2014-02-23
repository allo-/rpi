#!/usr/bin/python

from evdev import InputDevice
from select import select

import sys
import os
import subprocess
import json

# cheap usb remote: 073a:2330 Chaplet Systems, Inc.
DEVICE = '/dev/input/by-id/'\
    'usb-www.tigerfly.net_www.tigerfly.net_www.tigerfly.net-event-mouse'

COMMANDS_FILENAME = '/etc/commands.json'


get_codes_mode = len(sys.argv) >= 2 and "--show-codes" in sys.argv
set_codes_mode = len(sys.argv) >= 2 and "--set-codes" in sys.argv

commands_timestamp = 0
commands = {}
dev = InputDevice(DEVICE)


def load_commands():
    if os.path.exists(COMMANDS_FILENAME):
        with open(COMMANDS_FILENAME, 'r') as cmd_file:
            commands = json.load(cmd_file)
            return commands
    return {}

if not get_codes_mode:
    if not os.path.exists(COMMANDS_FILENAME):
        print 'warning: no commands file'
    if set_codes_mode:
        commands = load_commands()
        print "Existing Commands:"
        for code in commands:
            print "{0:d}: {1:s}".format(int(code), commands[code])


try:
    while True:
        r, w, x = select([dev], [], [])
        for event in dev.read():
            if event.type == 1 and event.value == 1:
                code = str(event.code)
                if get_codes_mode:
                    print code
                elif set_codes_mode:
                    print "code: ", code
                    sys.stdout.write('Command: ')
                    command = raw_input()
                    commands[code] = command
                    with open(COMMANDS_FILENAME, 'w') as cmd_file:
                        json.dump(commands, cmd_file, indent=2)
                else:
                    mtime = os.stat(COMMANDS_FILENAME).st_mtime
                    if mtime != commands_timestamp:
                        commands = load_commands()
                    if code in commands:
                        print commands[code]
                        subprocess.call([commands[code]], shell=True)
except KeyboardInterrupt:
    print
    print "Exiting"
