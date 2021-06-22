#!/usr/bin/env python3

import argparse
import os.path
import sys
import sqlite3
from pathlib import Path
from sqlite3 import Error
from shutil import which


def check_requirements():
    """ check if sqlite3 is installed """
    if which("sqlite3") is None:
        print("SQLite not available")
        sys.exit()


def check_dir(db_dir):
    """ create database directory """
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)


def create_connection(db_file):
    """ create a connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_tracks(conn, track):
    """ insert or update current song into the database """
    sql = """ INSERT INTO tracks(title, artist_name, album_name, plays) VALUES(?,?,?,?) ON CONFLICT(title) DO UPDATE SET plays=plays+1"""
    cur = conn.cursor()
    cur.execute(sql, track)
    conn.commit()
    return cur.lastrowid


def create_albums(conn, album):
    """ insert or update current album into the database """
    sql = """ INSERT INTO albums(title, artist_name, plays) VALUES(?,?,?) ON CONFLICT(title) DO UPDATE SET plays=plays+1"""
    cur = conn.cursor()
    cur.execute(sql, album)
    conn.commit()
    return cur.lastrowid


def create_artists(conn, artist):
    """ insert or update current artist into the database """
    sql = """ INSERT INTO artists(name, plays) VALUES(?,?) ON CONFLICT(name) DO UPDATE SET plays=plays+1"""
    cur = conn.cursor()
    cur.execute(sql, artist)
    conn.commit()
    return cur.lastrowid


def main():
    parser = argparse.ArgumentParser(prog='cmusicbox.py',
                                     usage='%(prog)s -a [artist] -l [album] '
                                           ' -t [song title]')
    parser.add_argument('--artist', '-a', type=str, required=True,
                        help='artist name')
    parser.add_argument('--album', '-l', type=str, required=True,
                        help='album title')
    parser.add_argument('--title', '-t', type=str, required=True,
                        help='song title')
    args = parser.parse_args()

    db_dir = str(Path.home())+r'/.config/cmusicbox'
    db_file = db_dir+r'/database.db'

    sql_create_tracks_table = """ CREATE TABLE IF NOT EXISTS tracks (
                                      title text PRIMARY KEY,
                                      artist_name text,
                                      album_name text,
                                      plays integer,
                                      FOREIGN KEY (artist_name) REFERENCES artists(name),
                                      FOREIGN KEY (album_name) REFERENCES albums(name)
                                  );"""

    sql_create_albums_table = """ CREATE TABLE IF NOT EXISTS albums (
                                      title text PRIMARY KEY,
                                      artist_name text,
                                      plays integer,
                                      FOREIGN KEY (artist_name) REFERENCES artists(name)
                                  );"""

    sql_create_artists_table = """ CREATE TABLE IF NOT EXISTS artists (
                                       name text PRIMARY KEY,
                                       plays integer
                                   );"""

    check_requirements()
    check_dir(db_dir)
    conn = create_connection(db_file)

    if conn is not None:
        create_table(conn, sql_create_tracks_table)
        create_table(conn, sql_create_albums_table)
        create_table(conn, sql_create_artists_table)

        create_artists(conn, (args.artist, '1'))
        create_albums(conn, (args.album, args.artist, '1'))
        create_tracks(conn, (args.title, args.artist, args.album, '1'))

    else:
        print("Cannot create the database connection.")


if __name__ == "__main__":
    main()
