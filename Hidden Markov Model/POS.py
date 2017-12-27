# Part Of Speech Tagger
# Viterbi Algorithm (Dynamic Programming)
# Hidden Markov Model
#
# Given the probability of transition between states and output given states
# predict the sequence of states with least tolerance
#

# Internal States
start = -1; VB = 0; INF = 1; NN = 2; PPSS = 3; stateCount = 4
stateNames = [ "Verb", "Infinitive", "Noun", "Pronoun" ]

# Outputs
I = 0; WANT = 1; TO = 2; RACE = 3

# State transition probability
trans = {}
trans[(start, VB)]   = .19
trans[(start, INF)]  = .0043
trans[(start, NN)]   = .041
trans[(start, PPSS)] = .067

trans[(VB, VB)]   = .0038
trans[(VB, INF)]  = .035
trans[(VB, NN)]   = .047
trans[(VB, PPSS)] = .0070

trans[(INF, VB)]   = .83
trans[(INF, INF)]  = 0
trans[(INF, NN)]   = .00047
trans[(INF, PPSS)] = 0

trans[(NN, VB)]   = .0040
trans[(NN, INF)]  = .016
trans[(NN, NN)]   = .087
trans[(NN, PPSS)] = .0045

trans[(PPSS, VB)]   = .23
trans[(PPSS, INF)]  = .00079
trans[(PPSS, NN)]   = .0012
trans[(PPSS, PPSS)] = .00014

# State Outputs
output = {}
output[(VB, I)]    = 0
output[(VB, WANT)] = .0093
output[(VB, TO)]   = 0
output[(VB, RACE)] = .00012

output[(INF, I)]    = 0
output[(INF, WANT)] = 0
output[(INF, TO)]   = .99
output[(INF, RACE)] = 0

output[(NN, I)]    = 0
output[(NN, WANT)] = .000054
output[(NN, TO)]   = 0
output[(NN, RACE)] = .00057

output[(PPSS, I)]    = .37
output[(PPSS, WANT)] = 0
output[(PPSS, TO)]   = 0
output[(PPSS, RACE)] = 0

# Word Count
wordCount = 4

# Output Sentence
sentence = [ I, WANT, TO, RACE ]
words = [ "I", "WANT", "TO", "RACE" ]

# Manage cell values and back pointers
cells  = {}
trace = {}

# Returns maximum previous state
def computeMaxPrev(t, sNext):
    maxValue = 0
    maxState = 0

    for s in range(stateCount):
        value = cells[(t, s)] * trans[(s, sNext)]
        if (s == 0 or value > maxValue):
            maxValue = value
            maxState = s

    return (maxValue, maxState)

def viterbi(trans, output, sentence):
    # Special handling for initial state
    for s in range(stateCount):
        cells[(0, s)] = trans[(start, s)] * output[(s, sentence[0])]

    # Handling rest cases
    for t in range(1, wordCount):
        for s in range(stateCount):
            maxValue, maxState = computeMaxPrev(t - 1, s)
            trace[(t, s)] = maxState
            cells[(t, s)] = maxValue * output[(s, sentence[t])]

    # Backtrack path traced
    path = []

    for tt in range(wordCount):
        t = wordCount - tt - 1
        maxValue = 0
        maxState = 0

        for s in range(stateCount):
            value = cells[(t, s)]
            if (s == 0 or value > maxValue):
                maxValue = value
                maxState = s

        path.insert(0, maxState)

    return path

# Invoke algorithm on given problem
path = viterbi(trans, output, sentence)

# Deliver state transitions
print("Tagged by Part Of Speech:")
for tt in range(wordCount):
    state = path[tt]
    print(words[tt], stateNames[state], sep="\t")
