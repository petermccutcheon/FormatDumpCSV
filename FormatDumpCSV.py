# -*- coding: utf-8 -*-
#************************************************************************************************************************************************
#***** Author:		Peter McCutcheon
#***** Created:		8/10/2017
#***** Modified:    8/14/2017   Make more Pythonic by eliminating separate counter and using enumerate.
#*****
#------------------------------------------------------------------------------------------------------------------------------------------------
#***** Description:
#*****
#*****		This script reads an inputed CSV file and displays the file field by field in a verticle
#*****      format.  The CSV file must have the first row (or record) as a list of fields separated
#*****      by commas.  This will be used to generate the field labels.  The user enters the CSV
#*****      file name and a file name for the output file.  The file is read sequentially with one
#*****      record displayed at a time.  The user has the option to enter a row number to jump to
#*****      for display.  The entered row must be greater than the current row otherwise the next
#*****      row is displayed.  As each row is displayed the program waits for input from the user
#*****      If the user wants the next row displayed then they just press carraige return.  The
#*****      displayed data is also written to the entered out put file.  To stop processing the
#*****      file and exit the user enters 'Q' at the row prompt.  The user can also enter 'C' to
#*****      have the program read to the end of the file without displaying any records.  This will
#*****      give and accurate record count for the csv file.
#*****
#*************************************************************************************************************************************************

#=====================================================================================================
#==		Import all packages here.
#=====================================================================================================

import csv
import sys

#=====================================================================================================
#==	Define all functions here.
#=====================================================================================================

def getRowNum(cnt):
    msg = input("Enter Row # or <cr> for next: ")
    if msg == "Q":
        return -1
        
    if msg == "C":
        return -2

    if msg != "":
        rNum = int(msg)
        if rNum <= cnt:
            print("Sorry, can back up in a sequential file, reading next row.")
            rNum = cnt + 1
    else:
        rNum = 0
            
    return rNum
    
#=====================================================================================================
#==	Initialize variables and open necessary files.
#=====================================================================================================

csvFile = input("CSV File: ")
outFile = input("Output File: ")

outcnt = 0
continueOn = False

fout = open(outFile, 'w')

#=====================================================================================================
#==	Main processing.
#=====================================================================================================

with open(csvFile, 'r') as fin:
    data = csv.reader(fin)
    for counter, row in enumerate(data):
        if continueOn:
            continue
        if counter == 0:
            columns = []
            for colCount, col in enumerate(row):
                oneCol = col + "[" + str(colCount) + "]"
                oneCol = oneCol.rjust(30)
                columns.append(oneCol)
                numOfColumns = len(columns)
                colCount += 1
            rowNum = getRowNum(counter)
            if rowNum == -1:
                break
            if rowNum == -2:
                continueOn = True
        else:
            numOfColumnsData = len(row)
            if numOfColumnsData != numOfColumns:
                dashes = "--------------------------------------------------------------------"
                txt = "Number of Labels: " + str(numOfColumns) + " Number of Data Columns: " + str(numOfColumnsData) + " For Row: " + str(counter)
                print("")
                fout.write("\n")
                print(dashes)
                fout.write(dashes + "\n")
                print(txt)
                fout.write(txt + "\n")
                print(dashes)
                fout.write(dashes + "\n")
                print("")
                fout.write("" + "\n")
                
            if ((counter == rowNum) or rowNum == 0):
                outcnt += 1
                txt = "Row Number: " + str(counter)
                txt = txt.center(60,"=")
                print(txt)
                fout.write(txt + "\n")
                for colCount, col in enumerate(row):
                    if (numOfColumnsData != numOfColumns) and (colCount >= numOfColumns):
                        oneCol = "Dummy Field"
                        oneCol = oneCol.rjust(30)
                    else:
                        oneCol = columns[colCount]
                    oneData = row[colCount]
                    toPrint = oneCol + ":\t" + oneData
                    print(toPrint)
                    fout.write(toPrint + "\n")
                    colCount += 1
                rowNum = getRowNum(counter)
                if rowNum == -1:
                    break
                if rowNum == -2:
                    continueOn = True
                
#=====================================================================================================
#==	Close files, cleanup, exit program.
#=====================================================================================================        
        
fout.close()

print("")
print("Input record count: " + str(counter))
print("")
print("One record for column names and " + str(counter-1) + " data records.")
print("")
print("Output record count: " + str(outcnt))
print