# Viterbi Algorithm (Dynamic Programming)
# Hidden Markov Model
#
# Given the probability of transition between states and output given states
# predict the sequence of states with least tolerance
#
# Here, we are using a weather forecast example. A day can be either of these
# three: Cold, Normal or Hot. Depending upon the weather a certain beverage is
# distributed: Soda, Hot Chocolate and Ice cream.

# Internal States
start = -1; cold = 0; normal = 1; hot = 2; stateCount = 3
stateNames = [ "Cold", "Normal", "Hot" ]

# Outputs
hotChoc = 0; soda = 1; iceCream = 2;

# Duration
timeSteps = 7

# State transition probability
trans = {}
trans[(start, cold)]   = .1
trans[(start, normal)] = .8
trans[(start, hot)]    = .1

trans[(cold, cold)]   = .7
trans[(cold, normal)] = .1
trans[(cold, hot)]    = .2

trans[(normal, cold)]   = .3
trans[(normal, normal)] = .4
trans[(normal, hot)]    = .3

trans[(hot, cold)]   = .2
trans[(hot, normal)] = .4
trans[(hot, hot)]    = .4

# State Outputs
output = {}
output[(cold, hotChoc)]  = .7
output[(cold, soda)]     = .3
output[(cold, iceCream)] = 0

output[(normal, hotChoc)]  = .1
output[(normal, soda)]     = .7
output[(normal, iceCream)] = .2

output[(hot, hotChoc)]  = 0
output[(hot, soda)]     = .6
output[(hot, iceCream)] = .4

# Output catalog
diary = [ soda, soda, hotChoc, iceCream, soda, soda, iceCream ]

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

def viterbi(trans, output, diary):
    # Special handling for initial state
    for s in range(stateCount):
        cells[(0, s)] = trans[(start, s)] * output[(s, diary[0])]

    # Handling rest cases
    for t in range(1, timeSteps):
        for s in range(stateCount):
            maxValue, maxState = computeMaxPrev(t - 1, s)
            trace[(t, s)] = maxState
            cells[(t, s)] = maxValue * output[(s, diary[t])]

    # Backtrack path traced
    path = []

    for tt in range(timeSteps):
        t = timeSteps - tt - 1
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
path = viterbi(trans, output, diary)

# Deliver state transitions
print("Weather by Days:")
for tt in range(timeSteps):
    state = path[tt]
    print(stateNames[state])
