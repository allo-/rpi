#!/usr/bin/python

from mpd import MPDClient, ConnectionError
import os
from flask import *
import re
import hashlib
import time

HOSTNAME = 'localhost'
PORT = 6600
THEME = "dark"  # dark / light


app = Flask(__name__)


def name2color(name):
    md5 = hashlib.md5(name).hexdigest()
    color = "#"
    for i in range(3):
        if THEME == "dark":
            deccolor = int(int(md5[i:i+2], 16)/3.0 + 0)  # dark
        else:
            deccolor = int(int(md5[i:i+2], 16)/3.0 + 100)  # light
        hexcolor = hex(deccolor)[2:]
        if len(hexcolor) == 1:
            hexcolor = "0"+hexcolor
        color += hexcolor
    return color


def title_from_filename(filename):
    matched_name = re.match('.*/(.*)\.[a-z0-9]*$', filename).group(1)
    return matched_name if matched_name else filename


@app.route('/')
def main():
    while True:
        try:
            c.ping()
            break
        except ConnectionError:
            try:
                c.connect(HOSTNAME, PORT)
                break
            except socket.error:
                pass
        except IOError:
            pass
        time.sleep(1)

    data = c.currentsong()
    data.update(c.status())
    data['theme'] = THEME
    data['next_song'] = c.playlistid(data['nextsongid'])[0]
    if data['state'] == 'play':
        data['refresh'] = 2
    else:
        data['refresh'] = 60

    if not 'title' in data:
        data['title'] = title_from_filename(data['file'])
    if not 'title' in data['next_song']:
        data['next_song']['title'] = \
            title_from_filename(data['next_song']['file'])

    if 'artist' in data:
        data['song_color'] = name2color(data['artist'])
    else:
        if THEME == "dark":
            data['song_color'] = "#000000"
        else:
            data['song_color'] = "#ffffff"
    if 'artist' in data['next_song']:
        data['nextsong_color'] = name2color(data['next_song']['artist'])
    else:
        if THEME == "dark":
            data['nextsong_color'] = "#000000"
        else:
            data['nextsong_color'] = "#ffffff"

    time = map(lambda x: int(x), data['time'].split(':'))
    if len(time) != 2:
        if len(time) == 0:
            time = [None, None]
        else:
            time.insert(0, None)

    data['song_played_time'] = \
        '{0:02d}:{1:02d}'.format(*divmod(time[0], 60)) if time[0] else None
    data['song_length'] = '{0:02d}:{1:02d}'.format(*divmod(time[1], 60))
    data['percent'] = \
        100 * time[0] / float(time[1]) if time[0] and time[1] else 0
    return render_template("mpdstatus.html", **data)


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


c = MPDClient()
app.debug = True
app.run(host='0.0.0.0')
