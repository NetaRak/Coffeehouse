import sqlite3
import os
import sys
import persistance
from persistance import repo

repo.create_repo()


def PerformAction():
    f = open("action.txt", "r")
    for line in f:
        if line[-1] == "\n":
            line = line[:-1]
        splited = line.split(',')
        products = repo.findProduct(splited[0])
        for p in products:
            q = int(p[3])
            l = int(splited[1])
            sum = l + q
            if sum > 0:
                repo.updateProduct(splited[0], sum)
                activity = persistance.Activity(splited[0], splited[1], splited[2], splited[3])
                repo.activities.insert(activity)


PerformAction()
