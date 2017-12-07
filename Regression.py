import sqlite3
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

connection = sqlite3.connect('ComicChron.db')
cursor = connection.cursor()


def main():
   # keyword = input('Enter a keyword or character name: \n')
    keyword = 'batman'
    data_set = read_db(keyword)
    print(data_set)
    cursor.close()


def read_db(keyword):
    statement = "SELECT rank, units FROM comicTable WHERE title LIKE '%" + keyword + "%' ORDER BY units DESC"
    print(statement)
    cursor.execute(statement)
    df = DataFrame(cursor.fetchall())
    array = np.array(df.values)
    return array

main()
