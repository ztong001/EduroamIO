import datetime
import csv
from convert_test import saveCSV
from convert_test import results
from IHL import *
from collections import OrderedDict
""" Testing the output of Stats results report and CSV File(since they contain the same data)"""
## Setting up the variables
# Setup Date
previous_date= datetime.date(day=2, month=1, year=1991)
day= previous_date.strftime('%d')
month= previous_date.strftime('%m')
month_words= previous_date.strftime('%b')
year= previous_date.strftime('%Y')
year_2numbers= previous_date.strftime('%y')

# Setup IHLs and IHL_Array Dictionary
nus= IHL("NUS")
ntu= IHL("NTU")
smu= IHL("SMU")
astar= IHL("ASTAR")
nie= IHL("NIE")
# Initialise array of IHL objects to be used in the other functions
IHL_Array=OrderedDict([('nus',nus),('ntu',ntu),('smu',smu),('astar',astar),('nie',nie)])
# Initialise localUsers from ihl at other places and logExtract variables
for ihl in IHL_Array:
    IHL_Array[ihl].localUsers_abroad= 1
    IHL_Array[ihl].localUsers_astar= 1
    IHL_Array[ihl].localUsers_nie= 1
    IHL_Array[ihl].localUsers_ntu=1
    IHL_Array[ihl].localUsers_nus= 1
    IHL_Array[ihl].localUsers_smu=1
    IHL_Array[ihl].visitors=1
    IHL_Array[ihl].reject_localUsers= 4
    IHL_Array[ihl].reject_visitors= 4
    IHL_Array[ihl].userRecordsMonth= set(["john"])
    IHL_Array[ihl].userRecordsYear= set(["john","bro"])
    IHL_Array[ihl].rejectRecordsMonth= set(["badjohn","bang"])
    IHL_Array[ihl].rejectRecordsYear= set(["badjohn","badbro","bang","bros"])
for ihl in IHL_Array:
    IHL_Array[ihl].localUsers= IHL_Array[ihl].localUsers_abroad+ IHL_Array[ihl].localUsers_astar+ \
    IHL_Array[ihl].localUsers_nie+ IHL_Array[ihl].localUsers_ntu+ IHL_Array[ihl].localUsers_nus+ IHL_Array[ihl].localUsers_smu

## Do the test: SaveCSV (Note:Monthly and Yearly values will correlate with values in userRecordsMonth/Year)
saveCSV(IHL_Array,'testDaily'+month_words+year,'Day',previous_date)
saveCSV(IHL_Array,'testMonthly'+year,'Month',previous_date)
saveCSV(IHL_Array,'testYearly','Year',previous_date)
print("Saved to CSV!")

## Do the test: Results
# EXPECTED RESULT will be sum of localUsers from other IHLs in *IHL*= total no of localUsers in *IHL* -1
# since localUsers frm *IHL* in *IHL* is included in the addition.(Exclusion is done in logExtract)
results(IHL_Array,"results"+day+month+year_2numbers+".txt")