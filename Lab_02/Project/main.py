from gesture import Gesture
from outcome import Outcome
import random
# Markov chain simulation for rock paper and scissors

clash_outcomes: dict[Gesture, dict[Gesture, Outcome]] = {
    Gesture.PAPER: {Gesture.PAPER: Outcome.TIE, Gesture.ROCK: Outcome.WIN, Gesture.SCISSORS: Outcome.LOSE},
    Gesture.SCISSORS: {Gesture.PAPER: Outcome.WIN, Gesture.ROCK: Outcome.LOSE, Gesture.SCISSORS: Outcome.TIE},
    Gesture.ROCK: {Gesture.PAPER: Outcome.LOSE, Gesture.ROCK: Outcome.TIE, Gesture.SCISSORS: Outcome.WIN},
}

static_transition_matrix: dict[Gesture, dict[Gesture, float]] = {
    Gesture.PAPER: {Gesture.PAPER: 2/3, Gesture.ROCK: 1/3, Gesture.SCISSORS: 0/3},
    Gesture.ROCK: {Gesture.PAPER: 0/3, Gesture.ROCK: 2/3, Gesture.SCISSORS: 1/3},
    Gesture.SCISSORS: {Gesture.PAPER: 2/3, Gesture.ROCK: 0/3, Gesture.SCISSORS: 1/3}
}

learning_transition_matrix = static_transition_matrix.copy()

games_played = 0
static_player_score = 0
learning_player_score = 0

def pick_move(moves: dict[Gesture, float]):
    random_f: float = random.random()
    picked_move: Gesture

    if random_f < moves[Gesture.PAPER]:
        picked_move = Gesture.PAPER
    else:
        if random_f < moves[Gesture.ROCK]:
            picked_move = Gesture.ROCK
        else:
            picked_move = Gesture.SCISSORS

    return picked_move