from sys import maxsize as inf

class Minimax(object):

    def __init__(self, i_max_depth):
        self.max_depth = i_max_depth

    def evaluate(self, i_game_state):
        if i_game_state.is_gameover() and i_game_state.get_winning_player() == 1:
            evaluation = inf
        else:
            if i_game_state.is_gameover() and i_game_state.get_winning_player() == -1:
                evaluation = -inf
            else:
                evaluation = 0
        #log("evaluate: " + str(evaluation))
        return evaluation

    def min_play(self, i_game_state, i_max_depth):
        if i_game_state.is_gameover() or i_max_depth == 0:
            #log("min_play: depth = " + str(i_max_depth) + '\n' + str(i_game_state) + "eval = " + str(evaluate(i_game_state)))
            return(self.evaluate(i_game_state))
        min_score = min(map(lambda move: self.max_play(i_game_state.next_state(move), i_max_depth - 1), i_game_state.get_available_moves()))
        #log("min_play: depth = " + str(i_max_depth) + '\n' + str(i_game_state) + "min_score = " + str(min_score))
        return min_score

    def max_play(self, i_game_state, i_max_depth):
        if i_game_state.is_gameover() or i_max_depth == 0:
            #log("max_play: depth = " + str(i_max_depth) + '\n' + str(i_game_state) + "eval = " + str(evaluate(i_game_state)))
            return(self.evaluate(i_game_state))
        max_score = max(map(lambda move: self.min_play(i_game_state.next_state(move), i_max_depth - 1), i_game_state.get_available_moves()))
        #log("max_play: depth = " + str(i_max_depth) + '\n' + str(i_game_state) + "max_score = " + str(max_score))
        return max_score

    def get_best_move(self, i_game_state):
        possible_moves = map(lambda move: (move, self.min_play(i_game_state.next_state(move), self.max_depth)), i_game_state.get_available_moves())
        #log("possible_moves: " + str(possible_moves))
        return max(possible_moves, key = lambda x: x[1])[0]

class MinimaxSimult(object):
    """
        Needed functions on GameState class:
        get_available_moves must have one argument: player_id, and return the list of possible moves for this player, indepently from what the other player can plan.
        next_state must have two arguments: move_player_1 and move_player_minus_1
    """
    def __init__(self, i_max_depth, i_neutral_move):
        self.max_depth = i_max_depth
        self.neutral_move = i_neutral_move

    def evaluate(self, i_game_state):
        pass

    def min_play(self, i_game_state, i_max_depth):
        """
        We suppose here that the player 1 (us) has played the neutral move.
        We determine the best action for player -1 by taking the min of scores, that is lower for positions advantageous for the opponent
        """
        if i_game_state.is_gameover() or i_max_depth == 0:
            #log("min_play: depth = " + str(i_max_depth) + '\n' + str(i_game_state) + "eval = " + str(evaluate(i_game_state)))
            return(self.evaluate(i_game_state))

        possible_moves = map(lambda move: self.max_play(i_game_state.next_state(move_player_1 = self.neutral_move, move_player_minus_1 = move), i_max_depth - 1), i_game_state.get_available_moves(player_id = -1))
        min_score_move = min(possible_moves, key= lambda x:x[1])[0]
        min_score = min(possible_moves)
        log("min_play: depth = " + str(i_max_depth) + "\nmin_score_move = " + str(min_score_move) + "\nmin_score = " + str(min_score))
        return (min_score, min_score_move)

    def max_play(self, i_game_state, i_max_depth):
        """
        We suppose here that the player -1 (the opponent) has played the his most advantageous move.
        We determine the best action for player 1 by taking the max of scores, that is higher for positions advantageous for us

        PROBLEM: HOW DO WE GET THE BEST MOVE FROM PLAYER -1 ????
        --> RETURN BEST MOVE FOR PLAYER -1 IN RESULT OF MIN_PLAY
        --> GET IT IN MAX_PLAY 
        --> IMPLEMENT PLAYER_ID AS PARAMETER OF MIN, MAX and GET_BEST: DONE
        
        """
        if i_game_state.is_gameover() or i_max_depth == 0:
            #log("max_play: depth = " + str(i_max_depth) + '\n' + str(i_game_state) + "eval = " + str(evaluate(i_game_state)))
            return(self.evaluate(i_game_state))
        max_score = max(map(lambda move: self.min_play(i_game_state.next_state(move_player_1 = move, move_player_minus_1 = best_move_for_player_minus_1), i_max_depth - 1), i_game_state.get_available_moves(player_id = 1)))
        #log("max_play: depth = " + str(i_max_depth) + '\n' + str(i_game_state) + "max_score = " + str(max_score))
        return max_score

    def get_best_move(self, i_game_state):
        possible_moves = map(lambda move: (move, self.min_play(i_game_state.next_state(move), self.max_depth)), i_game_state.get_available_moves(1))
        #log("possible_moves: " + str(possible_moves))
        return max(possible_moves, key = lambda x: x[1])[0]