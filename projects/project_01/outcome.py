from enum import Enum

class Outcome(Enum):
    VICTORY = 1
    DEFEAT = 2
    TIE = 3

def inverse(outcome: Outcome):
    if outcome == Outcome.VICTORY:
        return Outcome.DEFEAT
    elif outcome == Outcome.DEFEAT:
        return Outcome.VICTORY
    else:
        return Outcome.TIE
