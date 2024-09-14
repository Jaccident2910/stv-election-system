import pandas
# --- SETTINGS ---
college_prefix = "jesu"


# ----------------


def deletePrompt(email, name):
    prompt = "\n Do you want to delete voter " + name + ", email "  + email + "? (y/n)\n"
    prompt = prompt + "\n Sometimes JCR members just have non-college emails so do double check.\n"
    return(prompt)

def nameCheck(frame):
    newFrame = frame.copy()
    for index, row in newFrame.iterrows():
        voterEmail = row['Email']
        if not (college_prefix in voterEmail):
            deleteQ = input(deletePrompt(voterEmail, row['Name']))
            while(not (deleteQ == 'y' or deleteQ == 'n')):
                deleteQ = input(deletePrompt(voterEmail))
            if deleteQ == 'y':
                newFrame = newFrame.drop(index)
                print("Voter deleted.")
            else:
                print("Voter not deleted.")
    return(newFrame)

