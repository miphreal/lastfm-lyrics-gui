#!/usr/bin/env python

"""
requirements.txt / python3.5

pylast==1.6.0
PyLyrics==1.1.0
"""

import tkinter as tk
import pylast
from PyLyrics import *


LASTFM_API_KEY = ''
LASTFM_API_SECRET = ''
LASTFM_API_USERNAME = ''
LASTFM_SYNC_TIME = 15000


class Application(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack()
        self._create_widgets()
        self._lastfm_api = self._init_lastfm_api()
        self._lastfm_user = self._lastfm_api.get_user(LASTFM_API_USERNAME)
        self._current_track = self._prev_track = None
        self._update_now_playing()

    def _init_lastfm_api(self):
        return pylast.LastFMNetwork(api_key=LASTFM_API_KEY, api_secret=LASTFM_API_SECRET, username=LASTFM_API_USERNAME)

    def _create_widgets(self):
        self.track_name = tk.Label(self.master, text='')
        self.track_lyric = tk.Text(self.master, height=100, borderwidth=0, highlightthickness=0)
        self.track_lyric.tag_configure('tag-center', justify='center')
        self.track_name.pack(fill=tk.X, ipady=5)
        self.track_lyric.pack(fill=tk.BOTH)

    def _retrieve_current_track(self):
        track = self._lastfm_user.get_now_playing()
        return track

    def _retrieve_current_lyric(self, track):
        try:
            return PyLyrics.getLyrics(str(track.artist), track.title)
        except ValueError as e:
            print(e)
        return 'No Lyric'

    def _set_now_playing(self, track):
        if track:
            self.track_name.config(text='{t.artist} - {t.title}'.format(t=track))
        else:
            self.track_name.config(text='----')

    def _set_current_lyric(self, lyric):
        self.track_lyric.delete('1.0', tk.END)
        self.track_lyric.insert(tk.END, lyric, 'tag-center')

    def _update_now_playing(self):
        self._current_track = self._retrieve_current_track()
        print(self._current_track)

        if self._current_track != self._prev_track:
            self._set_now_playing(self._current_track)

            if self._current_track:
                lyric = self._retrieve_current_lyric(self._current_track)
                self._set_current_lyric(lyric)

        self._prev_track = self._current_track
        self.master.after(LASTFM_SYNC_TIME, self._update_now_playing)


app = Application()
app.master.maxsize(height=600, width=400)
app.mainloop()
