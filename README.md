remote.py
=========

run remote.py at boot, for example from /etc/rc.local:

    /usr/local/bin/remote.py &

set keycodes
------------

    $ remote.py --set-codes

You will see a list of the current keycode mappings.
When you press a key, you will be prompted for a shell command. Stop adding new commands with ctrl-c.
If a key is alread defined, the current command will be overwritten by the new one.


show keycodes
-------------

    $ remote.py --show-codes

you can find the config in /etc/commands.json.
After editing, the file will be reloaded automatically.
Using --set-codes works immediately, too.


rpi-infodisplay
===============
see the README in the rpi-infodisplay subfolder
