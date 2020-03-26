#!/usr/bin/python3
#----------------------------------------------------------------------
# Mix.py
# A tool that helps curate DJ sets by providing suggestions for song
# transitions using key & BPM.
#
# Aviv Brook.
#----------------------------------------------------------------------

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
from lxml import html
import os

infilename = 'links'    # you can change these if you want
outfilename = '.db'     # good practice to keep this as a hidden file

# Mapping key names to numerical representation
keys = {'Ab min': '1A',
        'G# min': '1A',
        'B maj': '1B',
        'Eb min': '2A',
        'D# min': '2A',
        'F# maj': '2B',
        'Gb maj': '2B',
        'Bb min': '3A',
        'A# min': '3A',
        'Db maj': '3B',
        'C# maj': '3B',
        'F min': '4A',
        'Ab maj': '4B',
        'G# maj': '4B',
        'C min': '5A',
        'Eb maj': '5B',
        'D# maj': '5B',
        'G min': '6A',
        'Bb maj': '6B',
        'A# maj': '6B',
        'D min': '7A',
        'F maj': '7B',
        'A min': '8A',
        'C maj': '8B',
        'E min': '9A',
        'G maj': '9B',
        'B min': '10A',
        'D maj': '10B',
        'F# min': '11A',
        'Gb min': '11A',
        'A maj': '11B',
        'Db min': '12A',
        'C# min': '12A',
        'E maj': '12B'}

def sanitised_input(prompt, type_=None, min_=None, max_=None):
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt)
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print("Input type must be {0}.".format(type_.__name__))
                continue
        if max_ is not None and ui > max_:
            print("Input must be less than or equal to {0}.".format(max_))
        elif min_ is not None and ui < min_:
            print("Input must be greater than or equal to {0}.".format(min_))
        else:
            return ui

class Song:
    """
    Song data structure used for all the processing.
    """
    def __init__(self, name, mix, artists, bpm, key):
        self.name = name
        self.mix = mix
        self.artists = artists
        self.bpm = bpm
        self.key = key.replace(chr(9837), 'b').replace(chr(9839), '#')

    def __str__(self):
        return self.name + ' (' + self.mix + ') by ' + self.artists + '\n' + 'BPM: ' + str(self.bpm) + '\n' + 'Key: ' + self.key + '\n'

def get_song(url):
    """
    Return a Song object from a Beatport link.
    """
    try:
        socket = urlopen(url)
        data = socket.read()
        socket.close()
        s = str(data, 'utf-8')
        soup = BeautifulSoup(s, features="html.parser")
        title = soup.find('title').text
        print('Found: ', title)
        matchObj = re.match(r'(.+) \((.+)\) by (.+) on Beatport', title, re.M|re.I)
        name = matchObj.group(1)
        mix = matchObj.group(2)
        artists = matchObj.group(3)
        bpm = int(soup.find('li', attrs={'class': 'interior-track-bpm'}).find('span', attrs={'class': 'value'}).text)
        key = soup.find('li', attrs={'class': 'interior-track-key'}).find('span', attrs={'class': 'value'}).text
        return Song(name, mix, artists, bpm, key)
    except Exception:
        print('FAILED: ', url)
        pass

def write_songs(infile, outfile):
    """
    Write songs to a database file.
    """
    songs = [song for song in [get_song(line.rstrip()) for line in infile] if song]
    [outfile.write(str(i) + '.\n' + str(songs[i])) for i in range(len(songs))]
    return songs

def read_songs(infile):
    """
    Read songs from a database file.
    """
    lines = [line.rstrip() for line in infile]
    songs = []
    for i in range(0, len(lines), 4):
        matchObj = re.match(r'(.+) \((.+)\) by (.+)', lines[i + 1], re.M|re.I)
        name = matchObj.group(1)
        mix = matchObj.group(2)
        artists = matchObj.group(3)
        bpm = int(re.match(r'BPM\: (\d+)', lines[i + 2], re.M|re.I).group(1))
        key = re.match(r'Key\: (.+)', lines[i + 3], re.M|re.I).group(1)
        songs.append(Song(name, mix, artists, bpm, key))
    return songs

def find_keys(key):
    """
    Return a list of keys that sound good with a given key.
    """
    key_val = keys[key]
    good_keys = []
    good_keys.append(key_val)
    key_list = list(key_val)
    equiv = list(key_val)
    below = list(key_val)
    above = list(key_val)
    if (key_list[1] == 'A'): equiv[1] = 'B'
    else: equiv[1] = 'A'
    good_keys.append(''.join(equiv))
    num = int(key_list[0])
    if num == 1: below[0] = '12'
    else: below[0] = str(num - 1)
    good_keys.append(''.join(below))
    if num == 12: above[0] = '1'
    else: above[0] = str(num + 1)
    good_keys.append(''.join(above))
    return good_keys

def recommend(songs, good_keyvals):
    """
    Return a list of songs that match a list of keys.
    """
    good_keys = []
    for k in keys:
        if keys[k] in good_keyvals: good_keys.append(k)
    good_songs = []
    for song in songs:
        if song.key in good_keys: good_songs.append(song)
    return good_songs

infile = open(infilename, 'r')
songs = []
if os.path.exists(outfilename) and os.stat(infilename).st_mtime < os.stat(outfilename).st_mtime:
    outfile = open(outfilename, 'r')
    songs = read_songs(outfile)
else:
    outfile = open(outfilename, 'w')
    songs = write_songs(infile, outfile)
infile.close()
outfile.close()

[print(str(i) + '.\n' + str(songs[i])) for i in range(len(songs))]

# Main loop.
sequence = []
recommended_songs = []
not_recommended_songs = songs
while songs:
    num = sanitised_input('Pick a song from the list by entering its associated number: ', int, 0, len(songs) - 1)
    if num < len(recommended_songs): song = recommended_songs[num]
    else: song = not_recommended_songs[num - len(recommended_songs)]
    songs.remove(song)
    sequence.append(song)
    print('\nSelected:\n' + str(song))
    if songs:
        recommended_songs = sorted(recommend(songs, find_keys(song.key)), key=lambda s: abs(s.bpm - song.bpm))
        print('\nRecommended songs to transition to:\n')
        [print(str(i) + '.\n' + str(recommended_songs[i])) for i in range(len(recommended_songs))]
        not_recommended_songs = list(set(songs) - set(recommended_songs))
        print('\nRest of songs:\n')
        [print(str(i + len(recommended_songs)) + '.\n' + str(not_recommended_songs[i])) for i in range(len(not_recommended_songs))]
    else:
        print('\nDone:\n')
        [print(str(i + 1) + '.\n' + str(sequence[i])) for i in range(len(sequence))]
