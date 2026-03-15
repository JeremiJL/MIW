import logger
import copy
from gesture import Gesture
from logger import LogLevel
from outcome import Outcome, inverse
import random
import matplotlib.pyplot as plt

static_transition_matrix: dict[Gesture, dict[Gesture, float]] = {
    Gesture.PAPER: {Gesture.PAPER: 2 / 3, Gesture.ROCK: 1 / 3, Gesture.SCISSORS: 0 / 3},
    Gesture.ROCK: {Gesture.PAPER: 0 / 3, Gesture.ROCK: 2 / 3, Gesture.SCISSORS: 1 / 3},
    Gesture.SCISSORS: {Gesture.PAPER: 2 / 3, Gesture.ROCK: 0 / 3, Gesture.SCISSORS: 1 / 3}
}

learning_transition_matrix = copy.deepcopy(static_transition_matrix)

# metrics
games_played: int = 0
max_games: int = 100
static_player_game_outcomes: list[Outcome] = []
learning_player_games_outcomes: list[Outcome] = []

# params
learning_rate: float = 0.02

# game state
last_move_of_static_player: Gesture = Gesture.PAPER
last_move_of_learning_player: Gesture = Gesture.PAPER


def main():
    for i in range(1, max_games +1):
        play_game()

    visualize()


def visualize():
    num_of_wins_by_learning_player: int = len([win for win in learning_player_games_outcomes if win == Outcome.VICTORY])
    num_of_wins_by_static_player: int = len([win for win in static_player_game_outcomes if win == Outcome.VICTORY])

    name_of_chart_file: str = "results.png"

    fig, ax = plt.subplots()

    total_wins_history_for_learning_player = compute_gradual_win_history(learning_player_games_outcomes)
    total_wins_history_for_static_player = compute_gradual_win_history(static_player_game_outcomes)

    ax.plot(range(0,max_games), total_wins_history_for_learning_player,
            label = "learning player #victories", color = "green"
    )
    ax.plot(range(0,max_games), total_wins_history_for_static_player,
            label = "static player #victories", color = "red"
    )

    ax.set_title("Head-to-head record between static and learning player")
    ax.set_ylabel("Total number of victories")
    ax.set_xlabel("Game number")
    ax.grid(True)
    ax.legend()

    fig.savefig(name_of_chart_file)

    logger.log(
        f'Games played: {games_played}, '
        f'Games won by learning player: {num_of_wins_by_learning_player},'
        f' Games won by static player: {num_of_wins_by_static_player},'
        f' Learning rate applied: {learning_rate}.\n\n'
        f'Overall learning player {"wins" if num_of_wins_by_learning_player > num_of_wins_by_static_player else "loses"},'
        f' by the margin of {abs(num_of_wins_by_learning_player - num_of_wins_by_static_player)}.\n\n'
        f'Final transition matrix of learning player: {learning_transition_matrix}.\n'
        f'Transition matrix of static player: {static_transition_matrix}.\n\n'
        f'Check {name_of_chart_file} for more details.'
        , level=LogLevel.INFO)


def play_game():
    global games_played, last_move_of_static_player, last_move_of_learning_player, static_player_game_outcomes, static_player_game_outcomes

    logger.log(f'Game number:{games_played}')
    static_player_move = pick_move(static_transition_matrix[last_move_of_learning_player])
    learning_player_move = pick_move(learning_transition_matrix[last_move_of_static_player])
    logger.log(f'Static player plays:{static_player_move} | Learning player plays:{learning_player_move}')

    outcome_for_learning_player = clash(your_move=learning_player_move, opponent_move=static_player_move)
    outcome_for_static_player = inverse(outcome_for_learning_player)
    logger.log(
        f'Game outcomes | Learning player:{outcome_for_learning_player}, Static player: {outcome_for_static_player}')

    update_distribution(myGesture=learning_player_move, opponent_gesture=static_player_move,
                        outcome=outcome_for_learning_player)
    logger.log(f'Updated moves transition matrix for leaning player: {learning_transition_matrix}')

    last_move_of_learning_player = learning_player_move
    last_move_of_static_player = static_player_move

    games_played += 1
    static_player_game_outcomes.append(outcome_for_static_player)
    learning_player_games_outcomes.append(outcome_for_learning_player)


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

def compute_gradual_win_history(game_outcomes: list[Outcome]) -> list[int]:
    current_total = 0
    total_gradual_wins_history = []
    for outcome in game_outcomes:
        if outcome == Outcome.VICTORY:
            current_total += 1
        total_gradual_wins_history.append(current_total)
    return total_gradual_wins_history


main()
