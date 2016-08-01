from setuptools import setup
import os
del os.link

_version = os.getenv('BUILD_COUNTER', '1')

setup(
    name='lastfm lyrics gui',
    scripts=['lasfm_lyrics_gui.py'],
    author='miphreal',
    author_email='miphreal@gmail.com',
    url='https://github.com/miphreal/lastfm-lyrics-gui',
    version=_version
)