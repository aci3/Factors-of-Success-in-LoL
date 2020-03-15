import pickle
from random import randint
import random
import time
import cassiopeia as cass
import os
import sys

# Command Line Arguments
# 1) filename of matchFile to be generated (cannot already exist)
# 2) filename of summonerFile to be generated (cannot already exist)
# 3) The Starting Summoner Name to search from
# 4) The Maximum number of matches to save to matchFile PER SUMMONER
# 5) The Maximum number of Summoners to search through

if(len(sys.argv) != 6):
    print("Invalid Amount of Command Line Arguements. Exiting...")
    time.sleep(3)
    exit()

#Globals
matchFileName = sys.argv[1]
summonerFileName = sys.argv[2]
starting_summoner = sys.argv[3]
maxMatchCount = int(sys.argv[4]);
maxSummonerCount = int(sys.argv[5]);
sleepTime = 1.2

#Setting up cass
cass.set_riot_api_key("RGAPI-a846da11-2c86-44e4-8336-00281da07e37")  # This overrides the value set in your configuration/settings.
cass.set_default_region("NA")

# Check if matchFile already exists, if so, error out
try:
    f = open(matchFileName)
except:
    print("matchFile named \"" + str(matchFileName) + "\" will be created")
else:
    sys.exit("ERROR: matchFile named \"" + str(matchFileName) + "\" already existed. Exiting...")
# Check if summonerFile already exists, if so, error out
try:
    f = open(summonerFileName)
except:
    print("summonerFile named \"" + str(summonerFileName) + "\" will be created")
else:
    sys.exit("ERROR: summonerFile named \"" + str(summonerFileName) + "\" already existed. Exiting...")

def get_matches(summonerName, summonerCount):

    # Break Recursion
    if summonerCount == maxSummonerCount:
        return
    summonerCount += 1

    #Get Current Summoner Info
    print("~~~~~GETTING MATCHES FOR SUMMONER: " + summonerName + "~~~~~")
    summoner = cass.get_summoner(name=summonerName)
    current_history = summoner.match_history.filter(lambda match: match.queue == cass.data.Queue.ranked_solo_fives)

    #Load Existing Summoners List from summonerFile
    try:
        summonerFile = open(summonerFileName, 'rb')
        summonerDict = pickle.load(summonerFile)
        summonerFile.close()
    except:
        summonerFile = open(summonerFileName, 'wb')
        summonerFile.close()
        summonerDict = {}
    #Load Existing matches List from matchFile
    try:
        matchFile = open(matchFileName, 'rb')
        matches = pickle.load(matchFile)
        matchFile.close()
    except:
        matchFile = open(matchFileName, 'wb')
        matchFile.close()
        matches = []
    
    #Collect Matches & Summoners
    x = 0
    for match in current_history:
        # Match Iteration Management
        if(x == maxMatchCount):
            break
        print("(" + str(x+1) + " Matches saved) Match id#"+str(match.id)+" being added...")
        x += 1
        time.sleep(sleepTime)

        #Add the match to the matchlist
        matches.append(match)

        #Add the summoners to summonerList
        summonerDict[str(match.participants[0].summoner.name)] = 0
        summonerDict[str(match.participants[1].summoner.name)] = 0
        summonerDict[str(match.participants[2].summoner.name)] = 0
        summonerDict[str(match.participants[3].summoner.name)] = 0
        summonerDict[str(match.participants[4].summoner.name)] = 0
        summonerDict[str(match.participants[5].summoner.name)] = 0
        summonerDict[str(match.participants[6].summoner.name)] = 0
        summonerDict[str(match.participants[7].summoner.name)] = 0
        summonerDict[str(match.participants[8].summoner.name)] = 0
        summonerDict[str(match.participants[9].summoner.name)] = 0
    
    summonerDict[str(summoner.name)] = 1
        
    # Write matchFile
    matchFile = open(matchFileName, 'wb')
    pickle.dump(matches, matchFile)
    matchFile.close()

    # Write summonerFile
    summonerFile = open(summonerFileName, 'wb')
    pickle.dump(summonerDict, summonerFile)
    summonerFile.close()

    # Select Random Summoner
    summonerDict2 = {}

    for key in summonerDict.keys():
        if summonerDict[key] == 0:
            summonerDict2[key] = 0
    summonerList = list(summonerDict2)

    randomSummonerName = summonerList[randint(0, len(summonerList)-1)]
        
    get_matches(randomSummonerName, summonerCount)
    
get_matches(starting_summoner, 0)
