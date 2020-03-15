import pickle
import time
import cassiopeia as cass
import sys

# Command Line Arguments
# 1) filename of matchFile to be generated (cannot already exist)
# 2) The Starting Match ID to iterate from
# 3) The Maximum number of matches to save to matchFile

#Globals
if(len(sys.argv) != 4):
    sys.exit("ERROR: Invalid Amount of Command Line Arguements. Exiting...")
matchFileName = sys.argv[1]
starting_match_id = int(sys.argv[2])
maxMatchCount = int(sys.argv[3])
sleepTime = 1.5

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

#Load Matches into a file denoted by matchFileName. that can be loaded later on
matchCount = 0;
curr_match_id = starting_match_id;
while matchCount < maxMatchCount:
    time.sleep(sleepTime)
    match = cass.get_match(curr_match_id)
    #If a match exists
    if match.exists:
        #If the match is a 5x5 soloque ranked mode game, add the match to the list
        if match.mode == cass.data.GameMode.classic and match.queue == cass.data.Queue.ranked_solo_fives:
            print("(" + str(matchCount+1) + " Matches saved) Match id#"+str(match.id)+" being added...")
            #Load Existing Matches List from matchFile
            try:
                matchFile = open(matchFileName, 'rb')
                matches = pickle.load(matchFile)
                matchFile.close()
            except:
                matchFile = open(matchFileName, 'wb')
                matchFile.close()
                matches = []
            #Add the match to the matchList, and save the matchFile
            matches.append(match)
            matchFile = open(matchFileName, 'wb')
            pickle.dump(matches, matchFile)
            matchFile.close()
            matchCount += 1
        else:
            #Ignore this match and continue
            print("Match id#"+str(match.id)+" is not solo ranked 5x5, igorning...")
    else:
        #Ignore this match and continue
        print("Match id#"+str(match.id)+" does not exist, ignoring...")
    curr_match_id -= 1
