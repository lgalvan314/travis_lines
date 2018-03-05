from Tkinter import *
from math import sqrt
import tkFileDialog
import csv
import arcpy


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


def makecsv():
    res = orderedlist
    #res[point].insert(whereInpointtoinsert, res[point + 1(keep)][Where to copy out of from point])
    for i in range(len(res) - 1):
        res[i].insert(2, res[i + 1][1])
        res[i].insert(4, res[i + 1][2])
        res[i].insert(6, res[i + 1][3])
    res[0] = ['PointNum', 'Easting1', 'Easting2', 'Northing1', 'Northing2', 'Elevation1', 'Elevation2', 'OrdNum']
    res.pop()

    #CSV location
    root.filename = tkFileDialog.asksaveasfilename(initialdir="/", title="Select new CSV output location:",
        filetypes=(("CSV", "*.csv*"), ("Shapefile", "*.shp")))
    print root.filename
    with open(root.filename + '.csv', "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(res)
    return root.filename

def xytoline(make):
    root.filename = tkFileDialog.asksaveasfilename(initialdir="/", title="Ouput Feature Class:", filetypes=(("Shapefile", "*.shp*"), ("all", "*.*")))
    arcpy.XYToLine_management(make, root.filename, "Easting1", "Northing1", "Easting2", "Northing2", "0", "", "PROJCS['NAD_1983_2011_StatePlane_Illinois_West_FIPS_1202_Ft_US',GEOGCS['GCS_NAD_1983_2011',DATUM['D_NAD_1983_2011',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',2296583.333333333],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-90.16666666666667],PARAMETER['Scale_Factor',0.9999411764705882],PARAMETER['Latitude_Of_Origin',36.66666666666666],UNIT['Foot_US',0.3048006096012192]];-16150900 -46131100 3048.00609601219;-100000 10000;-100000 10000;3.28083333333333E-03;0.001;0.001;IsHighPrecision")

    #Add fields (elev 1 and 2)
    arcpy.AddField_management(root.filename + '.shp', "Elevation1", "FLOAT", "", "2", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(root.filename + '.shp', "Elevation2", "FLOAT", "", "2", "", "", "NULLABLE", "NON_REQUIRED", "")

def makeLine():
    arcpy.env.workspace = "C:/data"
    inFeatures = 'Ordered_List.shp'
    outFeature = 'C:/output/output.gdb/out_line'
    lineField = 'Ord'



coordList = []
orderedlist = [['PointNum', 'Easting', 'Northing', 'Elevation', 'OrdNum']]
root = Tk()


def main():
    #Find their file
    root.filename = tkFileDialog.askopenfilename(initialdir="/", title="Select pipeline listing", filetypes=(
        ("all files", "*.*"), ("Excel Files", "*.xlsx")))

    #Turn columns into lists. found by names, not column locations
    with open(root.filename, "r") as gpstrack:
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

    make = makecsv() + '.csv'
    xytoline(make)




if __name__ == '__main__':
    main()

