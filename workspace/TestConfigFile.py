import json
from IHL import *
""" Test the loading of the configuration file and the File I/O of the UniqueUser Files"""
jsonfile= json.load(open('ihlconfig.json'))
print(jsonfile)
## Load Server name and IP Address for the etlrs
etlr_server=jsonfile['etlr']['server']
etlr_ip=jsonfile['etlr']['ip']

## Load the IHLs' details and set up test variables
nus= IHL("NUS",jsonfile['nus']['ip'], jsonfile['nus']['server'])
ntu= IHL("NTU",jsonfile['ntu']['ip'], jsonfile['ntu']['server'])
smu= IHL("SMU",jsonfile['smu']['ip'], jsonfile['smu']['server'])
astar= IHL("ASTAR",jsonfile['astar']['ip'], jsonfile['astar']['server'])
nie= IHL("NIE",jsonfile['nie']['ip'], jsonfile['nie']['server'])
ihlList=[nus,ntu,smu,astar,nie]
month='05'
year_2numbers='15'

## Check the domains with the reference notes, see whether correct or not
print("euro top-level domain: {} , euro accesspoint:{}".format(etlr_server,etlr_ip))
print("nus server: {} , nus accesspoint:{}".format(nus.server,nus.ipAddress))
print("ntu server: {} , ntu accesspoint:{}".format(ntu.server,ntu.ipAddress))
print("smu server: {} , smu accesspoint:{}".format(smu.server,smu.ipAddress))
print("astar server: {} , astar accesspoint:{}".format(astar.server,astar.ipAddress))
print("nie server: {} , nie accesspoint:{}".format(nie.server,nie.ipAddress))    

## Test reading and writing of uniqueUserFiles
for i in ihlList:
    i.readUniqueUserFiles(month, year_2numbers)
    print("Read 4 {} UniqueUserFiles".format(i.name))
    i.writeUniqueUserFiles(month,year_2numbers)
    print("Write 4 {} UniqueUserFiles".format(i.name))
