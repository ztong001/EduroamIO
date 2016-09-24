Final package:
- convert.py : Offline processing of log file and save to csv. Requires IHL.py and ihlconfig.json.
- IHL.py: Consist of the class IHL which contains the IHL-specific methods for uniqueUserFiles I/O and specific variables for keeping track of usage statistics.
- CreateHTML.py : Writing of html files for each IHL with data from csv.
- CreateHTML_singaren.py : Writing of html files for singaren webpage to check eduroam server.
- ihlconfig.json : Configuration file containing IHL's server names and IP addresses. Includes Euro Top-level servers too.
- Daily/Monthly/Yearly CSV files in csv folder(12mths,3years,1)
- HTML files in html folder(where CreateHTML.py dumps the files in)
- Stats_results folder contains results text files for the month of May 2015.
- Full Documentation: Contains detailed description of the modules in the program.



WARNING: Check the filepath of the python program before running!