import pandas
from math import floor

# --- SETTINGS ---
ron_keyword = 'RON (Re-Open Nominations)'


# ----------------

def process_ballot(ballot_str):
    """
    Converts ballot string into a python list of votes
    
    Parameters
    - ballot_str (str): A string containing the information from one ballot in the election.

    Returns
    - vote_list (list): A list containing the ballot's votes, in descending order of preference.
    """

    #print(vote)
    #ignore the poor choice of var name
    length = len(ballot_str)
    i = 0
    vote_list = []
    curr = ""
    while i < length:
        #loop invariant left as exercise to reader
        if ballot_str[i] == ";":
            vote_list.append(curr)
            curr = ""
        else:
            curr += ballot_str[i]
        #don't forget to increment i
        i += 1
    return vote_list


def get_candidate(vote_list, failed_candidates):
    """
    Goes through a list of ordered votes in a ballot and identifies the highest-ranked non-eliminated candidate.
    
    Parameters
    - vote_list (list): an ordered list of candidate preferences for the given ballot
    - failed_candidates (list): a list of eliminated candidates from the election
    """

    i = 0
    #loop until a candidate who hasn't been knocked out is found
    while vote_list[i] in failed_candidates:
        i += 1
    return(vote_list[i])
    
def showVote(name, stage, vote_dict):
    """
    Formats and prints the votes at a given stage of the election.
    
    Parameters:
    - name (str): the role for which the election is being held
    - stage (int): the STV round of the election being held
    - vote_dict (dict): a dictionary with candidates and vote totals
    """
    print("Votes for " + name + " in Stage " + str(stage) + ":")
    for cand in vote_dict:
        print(cand + ": " + str(vote_dict[cand]))

def tiebreak(cand1, cand2):
    """
    Given two tied candidates, prints winner of tiebreaker and returns loser.
    
    Parameters
    - cand1 (str): first tied candidate
    - cand2 (str): second tied candidate

    Returns
    - lowest: the candidate who loses the tiebreak
    """
    # TODO: ask Secretary how tiebreaks should be resolved.
    print("tie broken in favour of " + cand2)
    return(cand1) # placeholder decision


def run_election(name, series):
    """
    Runs election for a given role and prints winners (or lack thereof).
    
    Parameters
    - name (str): the role for which the election is being held
    - series (Pandas.series): a Pandas series of ballots
    """
    #print(name + ":")
    votes = []
    for _, ballot in series.dropna().items():
        vote_list = process_ballot(ballot)
        votes.append(vote_list)
    #now we have a list of all the votes: time to STV
    votes_dict = {}
    #get names of candidates
    for name2 in votes[0]:
        if name2 != ron_keyword:
            votes_dict[name2] = 0
    votes_dict[ron_keyword] = 0
    failed_candidates = []
    i = 0
    while (i < len(votes[0])-2):
        #reset count
        for name2 in votes[0]:
            if name2 != ron_keyword:
                if name2 in votes_dict and name2 in failed_candidates:
                    del votes_dict[name2]
                else:
                    votes_dict[name2] = 0
        votes_dict[ron_keyword] = 0
        #count votes
        for vote in votes:
            theVote = get_candidate(vote, failed_candidates)
            votes_dict[theVote] += 1
        showVote(name, i, votes_dict)
        lowest = None
        for cand in votes_dict:
            if lowest == None:
                lowest = cand
            else:
                if (votes_dict[cand] < votes_dict[lowest] and cand != ron_keyword and (not (cand in failed_candidates))):
                    lowest = cand              
                elif (cand != ron_keyword and votes_dict[cand] == votes_dict[lowest] and (not (cand in failed_candidates))):
                    lowest = tiebreak(lowest, cand)
        failed_candidates.append(lowest)
        print(lowest + " was eliminated!")
        i += 1
    #time to find the winner
    winner = None
    winner_check = 0
    for cand in votes_dict:
        if cand != ron_keyword and not (cand in failed_candidates):
            winner = cand
            winner_check += 1
    if (winner_check == 1):
        if len(votes_dict) < 3:
            #gotta have the logic for just 1 person running
            for vote in votes:
                theVote = get_candidate(vote, failed_candidates)
                votes_dict[theVote] += 1
            showVote(name, 0, votes_dict)
        if votes_dict[winner] >= votes_dict[ron_keyword]:
            print(winner + " is the winner of the election for " + name + "!!!\n")
        else:
            print("RON has won the election. Time to reopen nominations.\n")
    else: 
        print("This election has more than one winner, or no winners at all. Get the IT officer.\n")
    #showVote(name, i, votes_dict)    
    #print(data)

def get_multiseat_candidate(vList, failed_candidates, winningCandidates):
    i = 0
    #loop until a candidate who hasn't been knocked out or beat the quota is found
    while(vList[i][0] in failed_candidates or vList[i][0] in winningCandidates):
        i += 1
    return(vList[i:])
    
def redistribute_votes(votes_dict, winningCandidates, failed_candidates, quota):
    #Assume both winning and failed does not have RON in it
    assert(not (ron_keyword in winningCandidates or ron_keyword in failed_candidates))
    for winner in winningCandidates:
        winnerMargin = len(votes_dict[winner]) - quota
        winMultiplier = winnerMargin/votes_dict[winner]
        for voter , vMultiplier in votes_dict[winner]:
            newVotes = get_multiseat_candidate(voter, winningCandidates, failed_candidates)
            votes_dict[newVotes[0]].append((newVotes, vMultiplier * winMultiplier))
        votes_dict.pop(winner)
    return(votes_dict)


# DEPRECATED as we no longer run multirole elections
def run_multirole_election(name, series, num_cands):
    votes = []
    for _, ballot in series.dropna().items():
        voteAsList = process_ballot(ballot)
        votes.append(voteAsList)
    num_votes = len(votes)
    quota = floor(num_votes / (num_cands + 1)) + 1
    votes_dict = {}
    #get names of candidates
    for name2 in votes[0]:
        if name2 != ron_keyword:
            votes_dict[name2] = []
    votes_dict[ron_keyword] = []
    failed_candidates = []
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
        votes_dict[vote[0]].append(voteItem)
    #set up loop
    while(len(winningCandidates) < quota and (not ron_keyword in winningCandidates)):
        assert(len(votes_dict) > 1)
        #check for winners
        for cand in votes_dict:
            #this is wrong
            #if len(votes_dict[cand]) >= quota:
            #    winningCandidates.append(cand)
            #this is right
            #get sum of all votes
            voteSum = 0
            for vList, multiplier in votes_dict[cand]:
                assert vList[0] == cand
                voteSum += multiplier
            if voteSum >= quota:
                winningCandidates.append(cand)
        votes_dict = redistribute_votes(votes_dict, winningCandidates, failed_candidates)

    
    




