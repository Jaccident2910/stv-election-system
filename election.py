import pandas
from math import floor

# --- SETTINGS ---
ron_keyword = 'RON'


# ----------------

def process_vote(vote):
    #converts vote string into a python list

    #print(vote)
    #ignore the poor choice of var name
    length = len(vote)
    i = 0
    voteList = []
    currentItem = ""
    while (i < length):
        #loop invariant left as exercise to reader
        if vote[i] == ";":
            voteList.append(currentItem)
            currentItem = ""
        else:
            currentItem += vote[i]
        #don't forget to increment i
        i += 1
    return(voteList)


def get_candidate(vList, failedCandidates):
    i = 0
    #loop until a candidate who hasn't been knocked out is found
    while(vList[i] in failedCandidates):
        i += 1
    return(vList[i])
    
def showVote(name, stage, vDict):
    print("Votes for " + name + " in Stage " + str(stage) + ":")
    for cand in vDict:
        print(cand + ": " + str(vDict[cand]))

def tiebreak(cand1, cand2):
    #ties are extremely unlikely but still possible.
    # TODO: ask Danny (Secretary) how tiebreaks should be resolved.
    print("tie broken in favour of " + cand2)
    return(cand1) # placeholder decision


def run_election(name, series):
    #print(name + ":")
    votes = []
    for index, vote in series.items():
        voteAsList = process_vote(vote)
        votes.append(voteAsList)
    #now we have a list of all the votes: time to STV
    votesDict = {}
    #get names of candidates
    for name2 in votes[0]:
        if name2 != ron_keyword:
            votesDict[name2] = 0
    votesDict[ron_keyword] = 0
    failedCandidates = []
    i = 0
    while (i < len(votes[0])-2):
        #reset count
        for name2 in votes[0]:
            if name2 != ron_keyword:
                votesDict[name2] = 0
        votesDict[ron_keyword] = 0
        #count votes
        for vote in votes:
            theVote = get_candidate(vote, failedCandidates)
            votesDict[theVote] += 1
        showVote(name, i, votesDict)
        lowest = None
        for cand in votesDict:
            if lowest == None:
                lowest = cand
            else:
                if (votesDict[cand] < votesDict[lowest] and cand != ron_keyword and (not (cand in failedCandidates))):
                    lowest = cand              
                elif (cand != ron_keyword and votesDict[cand] == votesDict[lowest] and (not (cand in failedCandidates))):
                    lowest = tiebreak(lowest, cand)
        failedCandidates.append(lowest)
        print(lowest + " was eliminated!")
        i += 1
    #time to find the winner
    winner = None
    winnerCheck = 0
    for cand in votesDict:
        if cand != ron_keyword and not (cand in failedCandidates):
            winner = cand
            winnerCheck += 1
    if (winnerCheck == 1):
        if len(votesDict) < 3:
            #gotta have the logic for just 1 person running
            for vote in votes:
                theVote = get_candidate(vote, failedCandidates)
                votesDict[theVote] += 1
            showVote(name, 0, votesDict)
        if votesDict[winner] >= votesDict[ron_keyword]:
            print(winner + " is the winner of the election for " + name + "!!!\n")
        else:
            print("RON has won the election. Time to reopen nominations.")
    else: 
        print("This election has more than one winner, or no winners at all. Get Jack.")
    #showVote(name, i, votesDict)    
    #print(data)

def get_multiseat_candidate(vList, failedCandidates, winningCandidates):
    i = 0
    #loop until a candidate who hasn't been knocked out or beat the quota is found
    while(vList[i][0] in failedCandidates or vList[i][0] in winningCandidates):
        i += 1
    return(vList[i:])
    
def redistribute_votes(votesDict, winningCandidates, failedCandidates, quota):
    #Assume both winning and failed does not have RON in it
    assert(not (ron_keyword in winningCandidates or ron_keyword in failedCandidates))
    for winner in winningCandidates:
        winnerMargin = len(votesDict[winner]) - quota
        winMultiplier = winnerMargin/votesDict[winner]
        for voter , vMultiplier in votesDict[winner]:
            newVotes = get_multiseat_candidate(voter, winningCandidates, failedCandidates)
            votesDict[newVotes[0]].append((newVotes, vMultiplier * winMultiplier))
        votesDict.pop(winner)
    return(votesDict)



def run_multirole_election(name, series, num_cands):
    votes = []
    for index, vote in series.items():
        voteAsList = process_vote(vote)
        votes.append(voteAsList)
    num_votes = len(votes)
    quota = floor(num_votes / (num_cands + 1)) + 1
    votesDict = {}
    #get names of candidates
    for name2 in votes[0]:
        if name2 != ron_keyword:
            votesDict[name2] = []
    votesDict[ron_keyword] = []
    failedCandidates = []
    winningCandidates = []
   # Step 1: Count all the votes, store each vote in the "dict" as the vote list and a multiplier
   # Step 2: For each candidate over the quota, do multiplier *= (numVotes - quota)/numVotes for each voter
   # Step 3: Calculate new winners??
   # Step 4: Repeat until all winners are figured out.
   # Step 5: If there is a RON winner, stop so new election can be called for remaining seats.
   # Good god this is complicated.

   #get all vote counts:
    for vote in votes:
        #store each vote as a pair, with the list of votes in [0] and multiplier in [1]
        voteItem = (vote, 1)
        votesDict[vote[0]].append(voteItem)
    #set up loop
    while(len(winningCandidates) < quota and (not ron_keyword in winningCandidates)):
        assert(len(votesDict) > 1)
        #check for winners
        for cand in votesDict:
            #this is wrong
            #if len(votesDict[cand]) >= quota:
            #    winningCandidates.append(cand)
            #this is right
            #get sum of all votes
            voteSum = 0
            for vList, multiplier in votesDict[cand]:
                assert vList[0] == cand
                voteSum += multiplier
            if voteSum >= quota:
                winningCandidates.append(cand)
        votesDict = redistribute_votes(votesDict, winningCandidates, failedCandidates)

    
    




