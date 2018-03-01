from Tkinter import *
from math import sqrt
import tkFileDialog
import csv


def calcdist(list1, list2):
    x1 = list1[1]
    x2 = list2[1]
    y1 = list1[2]
    y2 = list2[2]
    z1 = list1[3]
    z2 = list2[3]
    inner = (x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2
    distance = sqrt(inner)
    return distance


def indexofclosest(mindist, distlist):
    index = distlist.index(mindist)
    return index


def search_delete(i, first):
    for point in coordList:
        if point[0] == int(first):
            point.append(i)
            orderedlist.append(point)
            coordList.remove(point)
            return point


coordList = []
orderedlist = []


def main():
    #Find their file
    root = Tk()
    root.filename = tkFileDialog.askopenfilename(initialdir="/", title="Select pipeline listing", filetypes=(
        ("all files", "*.*"), ("Excel Files", "*.xlsx")))

    #Turn columns into lists. found by names, not column locations
    gpstrack = open(root.filename, "r")
    csvreader = csv.reader(gpstrack)
    header = csvreader.next()

    latIndex = header.index("Easting")
    longIndex = header.index("Northing")
    elevIndex = header.index("Point Elevation")
    pointIndex = header.index("Point Number")

    #Put all data into nested list
    #coordList = []

    for row in csvreader:
        lat = row[latIndex]
        long = row[longIndex]
        elev = row[elevIndex]
        pointnum = row[pointIndex]
        coordList.append([int(float(pointnum)),float(lat),float(long),float(elev)])

    #Ask for first point and start ordered list
    #orderedlist = []
    first = int(raw_input("Point number value of first point: "))
    i = 1
    first = search_delete(i, first)
    print(first)

    while len(coordList) > 0:
        distlist = []
        #calculate dist and put in list
        for item in coordList:
            distlist.append(calcdist(item, first))
        mindist = min(distlist)
        index = indexofclosest(mindist, distlist)
        first = coordList[index]
        i = i + 1
        #remove next closest
        search_delete(i, first[0])

    print (orderedlist)

if __name__ == '__main__':
    main()
