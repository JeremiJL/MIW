import logger
from gesture import Gesture
from outcome import Outcome, inverse
import random
# Markov chain simulation for rock paper and scissors


static_transition_matrix: dict[Gesture, dict[Gesture, float]] = {
    Gesture.PAPER: {Gesture.PAPER: 2/3, Gesture.ROCK: 1/3, Gesture.SCISSORS: 0/3},
    Gesture.ROCK: {Gesture.PAPER: 0/3, Gesture.ROCK: 2/3, Gesture.SCISSORS: 1/3},
    Gesture.SCISSORS: {Gesture.PAPER: 2/3, Gesture.ROCK: 0/3, Gesture.SCISSORS: 1/3}
}

learning_transition_matrix = static_transition_matrix.copy()

# metrics
games_played: int = 0
static_player_score: int  = 0
learning_player_score: int = 0

# params
learning_rate: float = 0.1

# game state
last_move_of_static_player: Gesture = Gesture.PAPER
last_move_of_learning_player: Gesture = Gesture.PAPER

def main():
    for i in range(0,100):
        play_game()

    visualize()

    logger.log(message=f'learning transition matrix before update {learning_transition_matrix}')
    update_distribution(opponent_gesture=Gesture.PAPER, myGesture=Gesture.PAPER,win=True)
    logger.log(f'learning transition matrix before update {learning_transition_matrix}')


def visualize():
    pass

def play_game():
    logger.log(f'Game number:{games_played}')
    static_player_move = pick_move(static_transition_matrix[last_move_of_learning_player])
    learning_player_move = pick_move(learning_transition_matrix[last_move_of_static_player])
    logger.log(f'Static player plays:{static_player_move} | Learning player plays:{learning_player_move}')

    outcome_for_learning_player = clash(your_move=learning_player_move, opponent_move=static_player_move)
    outcome_for_static_player = inverse(outcome_for_learning_player)
    logger.log(f'Game outcomes | Learning player:{outcome_for_learning_player}, Static player: {outcome_for_static_player}')

    update_distribution(myGesture=learning_player_move, opponent_gesture=static_player_move, outcome=outcome_for_learning_player)
    logger.log(f'Updated moves transition matrix for leaning player: {learning_transition_matrix}')





def update_distribution(opponent_gesture: Gesture, myGesture: Gesture, outcome: Outcome):

    outdated_transition_matrix = learning_transition_matrix[opponent_gesture]

    for gesture in outdated_transition_matrix.keys():
        if outcome == Outcome.VICTORY:
            if gesture == myGesture:
                outdated_transition_matrix[gesture] += learning_rate
        elif outcome == Outcome.DEFEAT:
            if gesture != myGesture:
                outdated_transition_matrix[gesture] += learning_rate / 2

    # normalize to range (0,1)
    total: float = sum(outdated_transition_matrix.values())
    for gesture in outdated_transition_matrix.keys():
        outdated_transition_matrix[gesture] /= total

    assert sum(learning_transition_matrix[opponent_gesture].values()), "Total probability has to sum up to 1."

def pick_move(moves: dict[Gesture, float]):
    random_f: float = random.random()
    picked_move: Gesture

    if random_f < moves[Gesture.PAPER]:
        picked_move = Gesture.PAPER
    else:
        if random_f < moves[Gesture.PAPER] + moves[Gesture.ROCK]:
            picked_move = Gesture.ROCK
        else:
            picked_move = Gesture.SCISSORS

    return picked_move

def clash(your_move: Gesture, opponent_move: Gesture) -> Outcome:

    clash_outcomes: dict[Gesture, dict[Gesture, Outcome]] = {
        Gesture.PAPER: {Gesture.PAPER: Outcome.TIE, Gesture.ROCK: Outcome.VICTORY, Gesture.SCISSORS: Outcome.DEFEAT},
        Gesture.SCISSORS: {Gesture.PAPER: Outcome.VICTORY, Gesture.ROCK: Outcome.DEFEAT, Gesture.SCISSORS: Outcome.TIE},
        Gesture.ROCK: {Gesture.PAPER: Outcome.DEFEAT, Gesture.ROCK: Outcome.TIE, Gesture.SCISSORS: Outcome.VICTORY},
    }

    return clash_outcomes[your_move][opponent_move]

main()