import datetime
import json
import csv
import re
import os
import sys
from IHL import *

def logExtract(logData,IHL_Array,etlr_server,etlr_ip):
    """ Defines the logic in extracting the information from the log file"""
    daily_AcceptRecords= set()
    daily_RejectRecords= set()
    ihlNameList=list(IHL_Array.keys())
    print(ihlNameList)
    for line in logData:
        ## check if user access is accepted or rejected, re.I ignores cases, re.M goes from start of string to end of string(multiline)
        matchAccept = re.search(r'Access-Accept for user',line,re.M|re.I)
        matchReject = re.search(r'Access-Reject for user',line,re.M|re.I)
        tokens=line.split(" ")
        date=tokens[0].strip() + " " + tokens[1].strip() + " " + tokens[2].strip() + " " +tokens[3].strip().rstrip(':')
        time=tokens[2].strip()
        ## Extracts specific information from the logfile, coming_from denotes the identity provider, going_to denotes the access point.
        for x in range(len(tokens)):
            if tokens[x].strip() == 'user':
                user = tokens[x+1].strip()
            if tokens[x].strip() == 'from':
                coming_from = tokens[x+1].strip()
            if tokens[x].strip() == 'to':
                going_to = tokens[x+1].strip()
        if matchReject:
            ## Access is rejected for the user
            if user not in daily_RejectRecords and user !='':
                daily_RejectRecords.add(user)
                #visitors TRAFFIC FOR ALL IHL
                #Overseas users using their accounts in IHL
                if coming_from in etlr_server:
                    for ihl in IHL_Array:
                        if going_to in IHL_Array[ihl].ipAddress:
                            IHL_Array[ihl].reject_visitors+=1
                            IHL_Array[ihl].rejectRecordsMonth.add(user)
                            IHL_Array[ihl].rejectRecordsYear.add(user)
                #Handle all the local IHLs
                else:
                    for ihl in IHL_Array:
                    #Coming from any IHL and going to etlr1 or etlr2
                        if coming_from in IHL_Array[ihl].server:
                            if not(going_to in IHL_Array[ihl].ipAddress):
                                IHL_Array[ihl].reject_localUsers+=1
                                IHL_Array[ihl].rejectRecordsMonth.add(user)
                                IHL_Array[ihl].rejectRecordsYear.add(user)

        if matchAccept:
            ## Access is accepted for the user
            if user not in daily_AcceptRecords and user!='':
                daily_AcceptRecords.add(user)
                #visitors TRAFFIC FOR ALL IHL
                #Overseas users using their accounts in IHL
                if coming_from in etlr_server:
                    for ihl in IHL_Array:
                        if going_to in IHL_Array[ihl].ipAddress:
                            IHL_Array[ihl].visitors+=1
                            IHL_Array[ihl].userRecordsMonth.add(user)
                            IHL_Array[ihl].userRecordsYear.add(user)
                #Handle all the local IHLs
                else:
                    for ihl in IHL_Array:
                        if coming_from in IHL_Array[ihl].server:
                            if not(going_to in IHL_Array[ihl].ipAddress):
                                IHL_Array[ihl].userRecordsMonth.add(user)
                                IHL_Array[ihl].userRecordsYear.add(user)
                                if going_to in etlr_ip:
                                    IHL_Array[ihl].localUsersCount['etlr']+=1
                                else:
                                    print("IHL!!!!!")
                                    for i in ihlNameList:
                                        if going_to in IHL_Array[i].ipAddress:
                                            print("{}".format(i))
                                            IHL_Array[ihl].localUsersCount[i]+=1
                                            IHL_Array[i].localvisitors+=1
    # Get total count of local users and visitors for each ihl
    for ihl in IHL_Array:
        IHL_Array[ihl].localUsers= sum(IHL_Array[ihl].localUsersCount.values())
        #IHL_Array[ihl].visitors= IHL_Array[ihl].visitors+ IHL_Array[ihl].localvisitors
        print("{}: {}".format(IHL_Array[ihl].name,IHL_Array[ihl].localUsersCount))
        print ("LocalUsers from {}: {}".format(ihl,IHL_Array[ihl].localUsers))
        print("Local Visitors from {}: {}".format(ihl,IHL_Array[ihl].localvisitors))
    
def results(IHL_Array,filename):                            
    """ Keep the results in a daily log file with date attached to it. """
    result = open(filename,"w")
    print("Writing to Results.txt")
    ## ihlNameList: List of the names of ihls in the stats
    ihlNameList=list(IHL_Array.keys())
    for ihl in IHL_Array:
        result.write("Total number of localUsers from %s who are abroad : %d \n" %(IHL_Array[ihl].name,IHL_Array[ihl].localUsersCount['etlr']))
        for i in ihlNameList:
            if i != ihl:
                result.write("Total number of localUsers from %s in %s : %d \n" %(IHL_Array[ihl].name,i.upper(),IHL_Array[ihl].localUsersCount[i]))
        result.write("Total number of localUsers from %s in total: %d \n \n" %(IHL_Array[ihl].name,IHL_Array[ihl].localUsers))
        result.write("Total number of visitors to %s : %d \n \n" %(IHL_Array[ihl].name,IHL_Array[ihl].visitors))

    for ihl in IHL_Array:
        result.write("Total number of unique users this month to %s : %d \n" %(IHL_Array[ihl].name,IHL_Array[ihl].getUniqueCountMonth()))
        result.write("Total number of rejectUnique users this month to %s : %d \n" %(IHL_Array[ihl].name,IHL_Array[ihl].getRejectUniqueCountMonth()))
        result.write("Total number of unique users this year to %s : %d \n" %(IHL_Array[ihl].name,IHL_Array[ihl].getUniqueCountYear()))
        result.write("Total number of rejectUnique users this year to %s : %d \n\n" %(IHL_Array[ihl].name,IHL_Array[ihl].getRejectUniqueCountYear()))
    
    for ihl in IHL_Array:
        result.write("Total number of rejected from %s for the day: %d \n" %(IHL_Array[ihl].name,IHL_Array[ihl].getRejectCount()))
    result.close()
    print('Results.txt closed')

def is_non_zero_file(fpath):  
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False
def saveCSV(IHL_Array,filename,interval,previous_date):
        """Save the extracted data into daily, monthly and yearly CSV files for data visualisation"""
        csv_list=[]
        day= previous_date.strftime('%d')
        month_words= previous_date.strftime('%b')
        year= previous_date.strftime('%Y')
        year_2numbers= previous_date.strftime('%y')
        print(filename)
        if(is_non_zero_file(filename+'.csv')):
        #Open the file first and get csv_list
            with open(filename+'.csv','r') as csvfile:
                reader = csv.reader(csvfile)
                print("Reading the "+filename+".csv file")
                for row in reader:
                    csv_list.append(row)
        else:
            with open(filename+'.csv','w') as csvfile:
                print("Creating new "+filename+".csv file")
            csv_row=[]
            if interval=='Day':
                csv_row=["Date","IHL","UniqueUsers","Category"]
            if interval=='Month':
                csv_row=["Month","IHL","UniqueUsers","Category"]
            if interval=='Year':
                csv_row=["Year","IHL","UniqueUsers","Category"]
            csv_list.append(csv_row)
        print(csv_list)
        csv_row=csv_list[0]
        last_checked=csv_list[-1:][0]
        print(last_checked)
        if interval=='Day':
            date=day+month_words+year_2numbers
            #Check for duplicate daily entry and delete
            if not(date != last_checked and last_checked=='Date'):
                print(csv_row[0])
                #Filter away the entries where the first element is the current month
                csv_list=[row for row in csv_list if date not in row and row!=[]]
                #print(row)
                print("Filtered!")
            for ihl in IHL_Array:
                csv_list.append([date,IHL_Array[ihl].name,IHL_Array[ihl].localUsers,"LocalUsers"])
                csv_list.append([date,IHL_Array[ihl].name,IHL_Array[ihl].visitors,"Visitors"])
                csv_list.append([date,IHL_Array[ihl].name,IHL_Array[ihl].getRejectCount(),"Rejected"])
                print("Appended {}".format(IHL_Array[ihl].name))
        if interval=='Month':
            #Check for duplicate month entry and delete
            if not(month_words!= last_checked and last_checked=='Month'):
                print(csv_row[0])
                #Filter away the entries where the first element is the current month
                csv_list=[row for row in csv_list if month_words not in row and row!=[]]
                print("Filtered!")
            for ihl in IHL_Array:
                csv_list.append([month_words,IHL_Array[ihl].name,IHL_Array[ihl].getUniqueCountMonth(),"Accepted"])
                csv_list.append([month_words,IHL_Array[ihl].name,IHL_Array[ihl].getRejectUniqueCountMonth(),"Rejected"])
        if interval=='Year':
            #Check for duplicate year entry and delete
            if not(year != last_checked and last_checked=='Year'):
                print(csv_row[0])
                #Filter away the entries where the first element is the current year
                csv_list=[row for row in csv_list if year not in row and row!=[]]
                print("Filtered!")
            for ihl in IHL_Array:
                csv_list.append([year,IHL_Array[ihl].name,IHL_Array[ihl].getUniqueCountYear(),"Accepted"])
                csv_list.append([year,IHL_Array[ihl].name,IHL_Array[ihl].getRejectUniqueCountYear(),"Rejected"])
        #Then write back to csv file
        csv_list=[row for row in csv_list if row!=[]]
        with open(filename+'.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(csv_list)

def main():                
    """ Testing full program. Check and set the day for specific date"""
    ## Since datetime is a built-in module, can just use its properties to get previous day's date.
    #Comment below when you use batchfile sys.argv
    previous_date= datetime.date(day=21, month=5, year=2015)
    #previous_date= datetime.date.today()- datetime.timedelta(1)
    
    ####uncomment below for use with batchfile only. Example arg: 021215 ### 
    # log_file = open("radsecproxy.log_"+str(sys.argv[1]),"r")
    # print ("radsecproxy.log_"+str(sys.argv[1]))
    # datestring=str(sys.argv[1])
    # previous_date= datetime.date(day=int(datestring[0:2]),month=int(datestring[2:4]),year=(2000+int(datestring[4:6])))
    
    day= previous_date.strftime('%d')
    month= previous_date.strftime('%m')
    month_words= previous_date.strftime('%b')
    year= previous_date.strftime('%Y')
    year_2numbers= previous_date.strftime('%y')
    ## Comment below when using batchfile, check the filepath before running- IMPORTANT!
    log_file = open("radsecproxy.log_"+day+month+year_2numbers,"r")
    print("Opening radsecproxy.log_"+day+month+year_2numbers)

    #Save all info from log file into a list of lines named logData(for LogExtract)
    logData = log_file.readlines()
    log_file.close()
    ## Load config file from ihlconfig.json which contains details of the IHLs.
    config= json.load(open('ihlconfig.json'))
    ## Load Server name and IP Address for the etlrs
    etlr_server=config['etlr']['server']
    etlr_ip=config['etlr']['ip']
    print(etlr_server)
    print(etlr_ip)

    ## 1. Load the IHLs' details, their Unique Users file into unique Records
    IHL_Array= dict()
    for ihl in config:
        if ihl != 'etlr':
            IHL_Array[ihl]= IHL(ihl.upper(),config[ihl]['ip'],config[ihl]['server'])
    # Read UniqueUsers Files for all the IHLs
    for ihl in IHL_Array:
        IHL_Array[ihl].readUniqueUserFiles(month,year_2numbers)
    print("Finished adding users from each uniqueUser file for each IHL")
    # Initialise localUsers from ihl at other places and logExtract variables
    # localUsersCount: contains localUsers of a ihl currently at each ihl and overseas
    for ihl in IHL_Array:
        # 1 element for each ihl in the stats for the ihl's localUsersCount
        for ihlname in config:
            IHL_Array[ihl].localUsersCount[ihlname]= 0
        print("{}: {}".format(IHL_Array[ihl].name,IHL_Array[ihl].localUsersCount))
    ## 2.Do Log Extract - Code logic at Line 7
    print("Doing LogExtract")
    logExtract(logData,IHL_Array,etlr_server,etlr_ip)
    ## 3. Writing back to uniqueUserFiles
    for ihl in IHL_Array:
        IHL_Array[ihl].writeUniqueUserFiles(month,year_2numbers)
    print("Finished writing to each uniqueUser file for all the IHLs")
    
    ## 4. Write to results file - Code logic at line 79
    #results(IHL_Array,"Stats_results/results.log_"+day+month+year_2numbers)
    results(IHL_Array,"testresults"+day+month+year_2numbers+".txt")

    ## 5. Save to CSV files(Daily, Monthly, Yearly) - saveCSV(FileInterval) Code logic at line 149
    saveCSV(IHL_Array,'csv/testDaily'+month_words+year,'Day',previous_date)
    saveCSV(IHL_Array,'csv/testMonthly'+year,'Month',previous_date)
    saveCSV(IHL_Array,'csv/testYearly','Year',previous_date)
    print("Saved to CSV!")

""" Allows execution of main convert function if run as a script"""    
if __name__== '__main__':
    main()