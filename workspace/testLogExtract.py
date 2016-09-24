from IHL import *
from convert_test import logExtract
from collections import OrderedDict
import re
import json
"""Testing logExtract module to check if it works correctly
Refer to Eduroam test stats excel file to check for correctness
Test data is: radsecproxy.log_200515 or radsecproxy.log_210515(not in radlog) 
"""    
log_file = open("radlog/radsecproxy.log_310515","r")
print ("Opening radsecproxy.log_310515")

jsonfile= json.load(open('ihlconfig.json'))
print(jsonfile)
## Load Server name and IP Address for the etlrs
etlr_server=jsonfile['etlr']['server']
etlr_ip=jsonfile['etlr']['ip']
## Load the IHLs' details
nus= IHL("NUS",jsonfile['nus']['ip'], jsonfile['nus']['server'],filepath="Production/uniqueUsersFiles/")
ntu= IHL("NTU",jsonfile['ntu']['ip'], jsonfile['ntu']['server'],filepath="Production/uniqueUsersFiles/")
smu= IHL("SMU",jsonfile['smu']['ip'], jsonfile['smu']['server'],filepath="Production/uniqueUsersFiles/")
astar= IHL("ASTAR",jsonfile['astar']['ip'], jsonfile['astar']['server'],filepath="Production/uniqueUsersFiles/")
nie= IHL("NIE",jsonfile['nie']['ip'], jsonfile['nie']['server'],filepath="Production/uniqueUsersFiles/")
# Initialise array of IHL objects and test variables 'month' and 'year_2numbers'
IHL_Array=OrderedDict([('nus',nus),('ntu',ntu),('smu',smu),('astar',astar),('nie',nie)])
month='05'
year_2numbers='15'
## Reading of uniqueUserFiles to initialise the userRecordsMonth/Year for each IHL
for i in IHL_Array:
    IHL_Array[i].readUniqueUserFiles(month, year_2numbers)
    print("Read 4 {} UniqueUserFiles".format(IHL_Array[i].name))

# Initialise localUsers from ihl at other places and logExtract variables
for ihl in IHL_Array:
    IHL_Array[ihl].localUsers_abroad= 0
    IHL_Array[ihl].localUsers_astar= 0
    IHL_Array[ihl].localUsers_nie= 0
    IHL_Array[ihl].localUsers_ntu=0
    IHL_Array[ihl].localUsers_nus= 0
    IHL_Array[ihl].localUsers_smu=0

# Check if all the lines in the file is read in the variable 
print (type(log_file))
print (log_file)

logExtract(log_file,IHL_Array,etlr_server,etlr_ip)
# Check if logExtract values printed are the same as the ones in Eduroam test stats
for ihl in IHL_Array:
    IHL_Array[ihl].localUsers= IHL_Array[ihl].localUsers_abroad+ IHL_Array[ihl].localUsers_astar+ \
    IHL_Array[ihl].localUsers_nie+ IHL_Array[ihl].localUsers_ntu+ IHL_Array[ihl].localUsers_nus+ IHL_Array[ihl].localUsers_smu
    print("Number of localUsers from abroad in {}: {}".format(IHL_Array[ihl].name,IHL_Array[ihl].localUsers_abroad))
    print("Number of localUsers from NUS in {}: {}".format(IHL_Array[ihl].name,IHL_Array[ihl].localUsers_nus))
    print("Number of localUsers from NTU in {}: {}".format(IHL_Array[ihl].name,IHL_Array[ihl].localUsers_ntu))
    print("Number of localUsers from SMU in {}: {}".format(IHL_Array[ihl].name,IHL_Array[ihl].localUsers_smu))
    print("Number of localUsers from ASTAR in {}: {}".format(IHL_Array[ihl].name,IHL_Array[ihl].localUsers_astar))
    print("Number of localUsers from NIE in {}: {}".format(IHL_Array[ihl].name,IHL_Array[ihl].localUsers_nie))
    print("Number of local Users in {} : {}".format(IHL_Array[ihl].name,IHL_Array[ihl].localUsers))
    print("Number of visitors in {} : {}".format(IHL_Array[ihl].name, IHL_Array[ihl].visitors))
    print("Number of rejected Users in {}: {}".format(IHL_Array[ihl].name, IHL_Array[ihl].getRejectCount()))
    print("Number of accepted Unique Users in {} for the month: {}".format(IHL_Array[ihl].name,IHL_Array[ihl].getUniqueCountMonth()))
    print("Number of rejected Unique Users in {} for the month: {}".format(IHL_Array[ihl].name,IHL_Array[ihl].getRejectUniqueCountMonth()))
    print("Number of accepted Unique Users in {} for the year: {}".format(IHL_Array[ihl].name,IHL_Array[ihl].getUniqueCountYear()))
    print("Number of rejected Unique Users in {} for the year: {}".format(IHL_Array[ihl].name,IHL_Array[ihl].getRejectUniqueCountYear()))
