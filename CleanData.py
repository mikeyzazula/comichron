import ast
import os
import sqlite3
import re


def create_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS comicTable(rank REAL, title TEXT, issue REAL, publisher TEXT, units REAL, year REAL, month REAL)')


def add_data(rank, title, issue, publisher, units, year, month):
    if issue == '':
        issue = 0
    cursor.execute("INSERT INTO comicTable(rank, title, issue, publisher, units, year, month) VALUES (?, ?, ?, ?, ?, ? , ?)",
                   (rank, title, issue, publisher, units, year, month))

def parse_to_db():
    move = True  # Our line is good to add into the SQL db
    for file in os.listdir('./Data'):
        filename = os.fsdecode('./Data/' + file)
        open_file = open(filename)
        year = filename[7:-7]
        month = filename[12:-4]
        for line in open_file:
            line = line.strip('\n')
            lit_line = ast.literal_eval(line)
            if len(lit_line) < 7: # this is an ugly way of handling the old data which did not have the "dollars" ranking category
                if 'trade paperback' in str(lit_line[1]).lower(): # we need to dodge the paperbacks in the old format, which are in the same table as the comics
                    break
                else:
                    if str(lit_line[0]).isdigit():  # dodging empty data

                        if len(lit_line) == 5:
                            add_data(int(lit_line[0]), str(lit_line[1]), 0, lit_line[3], int(lit_line[4].replace(',', '')), year, month)
                        else:
                            add_data(int(lit_line[0]), str(lit_line[1]), re.sub('[^0-9]', '', lit_line[2]), lit_line[4], int(lit_line[5].replace(',', '')), year, month)
            else:
                add_data(int(lit_line[0]), str(lit_line[2]), re.sub('[^0-9]', '', lit_line[3]), lit_line[5], int(lit_line[6].replace(',', '')), year, month)
        open_file.close()

connection = sqlite3.connect('ComicChron.db')
cursor = connection.cursor()

create_table()
parse_to_db()

connection.commit()
cursor.close()
connection.close()
