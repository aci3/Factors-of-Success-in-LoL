import pickle
import random
import time
import cassiopeia as cass
import csv
import sys

# Command Line Arguments
# 1) filename of matchFile to be read (cannot already exist)
# 2) filename of the CSV file to store the data without the ".csv" portion (cannot already exist)
# 3) The Maximum number of matches to save to matchFile

#Globals
if(len(sys.argv) != 4):
    sys.exit("ERROR: Invalid Amount of Command Line Arguements. Exiting...")
matchFileName = sys.argv[1]
csvfilename = sys.argv[2] + ".csv"
maxMatchCount = int(sys.argv[3]);
sleepTime = 1.2

#Setting up cass
cass.set_riot_api_key("RGAPI-a846da11-2c86-44e4-8336-00281da07e37")  # This overrides the value set in your configuration/settings.
cass.set_default_region("NA")

# Check if csvfilename already exists, if so, error out
try:
    f = open(csvfilename)
except:
    print("CSV File named \"" + str(csvfilename) + "\" will be created")
else:
    sys.exit("ERROR: CSV File named \"" + str(csvfilename) + "\" already existed. Exiting...")

# Loading Match History File
matchFile = open(matchFileName, 'rb')
matches = pickle.load(matchFile)
print("Matches File named \"" + str(matchFileName) + "\" loaded")
print("Number of Matches in file: " + str(len(matches)))
print("Max Number of Matches to be logged to CSV File: " + str(maxMatchCount))

matchNum = 0
for match in matches:
    # Manage Iteration of Match Number
    if(matchNum==maxMatchCount):
        exit()
    print("Processing Match " + str(matchNum))
        
    with open(csvfilename, 'a+', newline='') as file:
        #Properly Format Bans
        bans = {"b0": match.blue_team.bans[0], "b1": match.blue_team.bans[1], "b2": match.blue_team.bans[2], "b3": match.blue_team.bans[3], "b4": match.blue_team.bans[4],"r0": match.red_team.bans[0], "r1": match.red_team.bans[1], "r2": match.red_team.bans[2], "r3": match.red_team.bans[3], "r4": match.red_team.bans[4]}
        for ban in bans.keys():
            if bans[ban] == None:
                bans[ban] = "NONE"
            else:
                bans[ban] = bans[ban].name

        #Append the CSV with new rows
        writer = csv.writer(file)
        if(matchNum==0):
            writer.writerow(["id","version","side","win","ban1","ban2","ban3","ban4","ban5","champion1","champion2","champion3","champion4","champion5","tower_kills","inhibitor_kills ","dragon_kills","rift_herald_kills","baron_kills","first_tower","first_inhibitor","first_dragon","first_rift_herald","first_baron"])
        writer.writerow([str(match.id),str(match.version),str(match.blue_team.side),str(match.blue_team.win),str(bans["b0"]),str(bans["b1"]),str(bans["b2"]),str(bans["b3"]),str(bans["b4"]),str(match.blue_team.participants[0].champion.name),str(match.blue_team.participants[1].champion.name),str(match.blue_team.participants[2].champion.name),str(match.blue_team.participants[3].champion.name),str(match.blue_team.participants[4].champion.name),str(match.blue_team.tower_kills),str(match.blue_team.inhibitor_kills),str(match.blue_team.dragon_kills),str(match.blue_team.rift_herald_kills),str(match.blue_team.baron_kills),str(match.blue_team.first_tower),str(match.blue_team.first_inhibitor),str(match.blue_team.first_dragon),str(match.blue_team.first_rift_herald),str(match.blue_team.first_baron)])
        writer.writerow([str(match.id),str(match.version),str(match.red_team.side),str(match.red_team.win),str(bans["r0"]),str(bans["r1"]),str(bans["r2"]),str(bans["r3"]),str(bans["r4"]),str(match.red_team.participants[0].champion.name),str(match.red_team.participants[1].champion.name),str(match.red_team.participants[2].champion.name),str(match.red_team.participants[3].champion.name),str(match.red_team.participants[4].champion.name),str(match.red_team.tower_kills),str(match.red_team.inhibitor_kills),str(match.red_team.dragon_kills),str(match.red_team.rift_herald_kills),str(match.red_team.baron_kills),str(match.red_team.first_tower),str(match.red_team.first_inhibitor),str(match.red_team.first_dragon),str(match.red_team.first_rift_herald),str(match.red_team.first_baron)])

    # Increment Match Number for Iteration
    matchNum += 1
