#!/usr/bin/env python3

import argparse
import os.path
import sys
from cmusicbox import check_requirements, create_connection
from pathlib import Path
from tabulate import tabulate


def check_db(db_file):
    """ check if database exists """
    if not os.path.exists(db_file):
        print("Database not available.")
        sys.exit()


def select_top10_artists(conn, table):
    cur = conn.cursor()
    cur.execute("SELECT artist_name, SUM(plays) FROM tracks GROUP BY \
                 artist_name ORDER BY SUM(plays) DESC LIMIT 10")

    results = cur.fetchall()

    print(tabulate(results, headers=["Top 10 artists", "Plays"],
                   tablefmt=table))


def select_top10_tracks(conn, table):
    cur = conn.cursor()
    cur.execute("SELECT title, artist_name, plays FROM tracks ORDER BY plays DESC LIMIT 10")

    results = cur.fetchall()
    print(tabulate(results, headers=["Top 10 songs", "Artist",
                                     "Plays"], tablefmt=table))


def main():
    db_dir = str(Path.home())+r'/.config/cmusicbox'
    db_file = db_dir+r'/database.db'

    parser = argparse.ArgumentParser(prog='cmusicbox-print.py',
                                     usage='%(prog)s -t [table format]')
    parser.add_argument('--table', '-t', nargs='?', type=str, default="pretty",
                        help='table format (consult tabulate documentation)')
    args = parser.parse_args()

    check_db(db_file)
    check_requirements()
    conn = create_connection(db_file)

    if conn is not None:
        table = args.table
        select_top10_tracks(conn, table)
        print()
        select_top10_artists(conn, table)
    else:
        print("Cannot create the database connection.")


if __name__ == "__main__":
    main()

