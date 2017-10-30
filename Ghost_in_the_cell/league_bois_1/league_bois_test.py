from __future__ import print_function
import sys
import unittest
from league_bois_1 import Entity, Factory, Troop, Bomb, State, Graph, Order, GameController
from league_bois_1 import launch_bomb, arrival_scheme, production_and_arrival_scheme, needed_cyborgs, cost_to_increase_prod
import ast

OUTPUT = sys.stdout

# Global function log
def log(i_text):
    print(i_text, file=OUTPUT)

edges_network_2 = "{0: {1: 7, 2: 7, 3: 2, 4: 2, 5: 4, 6: 4}, 1: {0: 7, 2: 15, 3: 3, 4: 10, 5: 2, 6: 12}, 2: {0: 7, 1: 15, 3: 10, 4: 3, 5: 12, 6: 2}, 3: {0: 2, 1: 3, 2: 10, 4: 5, 5: 1, 6: 7}, 4: {0: 2, 1: 10, 2: 3, 3: 5, 5: 7, 6: 1}, 5: {0: 4, 1: 2, 2: 12, 3: 1, 4: 7, 6: 9}, 6: {0: 4, 1: 12, 2: 2, 3: 7, 4: 1, 5: 9}}"

edges_network_32_54 = "{0: {1: 7, 2: 7, 3: 6, 4: 6, 5: 2, 6: 2, 7: 1, 8: 1, 9: 4, 10: 4, 11: 6, 12: 6}, 1: {0: 7, 2: 15, 3: 1, 4: 14, 5: 8, 6: 7, 7: 4, 8: 9, 9: 6, 10: 10, 11: 3, 12: 14}, 2: {0: 7, 1: 15, 3: 14, 4: 1, 5: 7, 6: 8, 7: 9, 8: 4, 9: 10, 10: 6, 11: 14, 12: 3}, 3: {0: 6, 1: 1, 2: 14, 4: 13, 5: 6, 6: 7, 7: 3, 8: 9, 9: 4, 10: 10, 11: 1, 12: 14}, 4: {0: 6, 1: 14, 2: 1, 3: 13, 5: 7, 6: 6, 7: 9, 8: 3, 9: 10, 10: 4, 11: 14, 12: 1}, 5: {0: 2, 1: 8, 2: 7, 3: 6, 4: 7, 6: 6, 7: 4, 8: 3, 9: 1, 10: 7, 11: 5, 12: 9}, 6: {0: 2, 1: 7, 2: 8, 3: 7, 4: 6, 5: 6, 7: 3, 8: 4, 9: 7, 10: 1, 11: 9, 12: 5}, 7: {0: 1, 1: 4, 2: 9, 3: 3, 4: 9, 5: 4, 6: 3, 8: 4, 9: 4, 10: 5, 11: 5, 12: 9}, 8: {0: 1, 1: 9, 2: 4, 3: 9, 4: 3, 5: 3, 6: 4, 7: 4, 9: 5, 10: 4, 11: 9, 12: 5}, 9: {0: 4, 1: 6, 2: 10, 3: 4, 4: 10, 5: 1, 6: 7, 7: 4, 8: 5, 10: 9, 11: 3, 12: 11}, 10: {0: 4, 1: 10, 2: 6, 3: 10, 4: 4, 5: 7, 6: 1, 7: 5, 8: 4, 9: 9, 11: 11, 12: 3}, 11: {0: 6, 1: 3, 2: 14, 3: 1, 4: 14, 5: 5, 6: 9, 7: 5, 8: 9, 9: 3, 10: 11, 12: 14}, 12: {0: 6, 1: 14, 2: 3, 3: 14, 4: 1, 5: 9, 6: 5, 7: 9, 8: 5, 9: 11, 10: 3, 11: 14}}"

#### turn 2
# Nodes: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
# Edges: {0: {1: 7, 2: 7, 3: 2, 4: 2, 5: 4, 6: 4}, 1: {0: 7, 2: 15, 3: 3, 4: 10, 5: 2, 6: 12}, 2: {0: 7, 1: 15, 3: 10, 4: 3, 5: 12, 6: 2}, 3: {0: 2, 1: 3, 2: 10, 4: 5, 5: 1, 6: 7}, 4: {0: 2, 1: 10, 2: 3, 3: 5, 5: 7, 6: 1}, 5: {0: 4, 1: 2, 2: 12, 3: 1, 4: 7, 6: 9}, 6: {0: 4, 1: 12, 2: 2, 3: 7, 4: 1, 5: 9}}

turn_2 = """nb turns: 2
Factory id: 0; player: 0; nb_cyborgs: 0; production: 0
Factory id: 1; player: 1; nb_cyborgs: 26; production: 1
Factory id: 2; player: -1; nb_cyborgs: 26; production: 1
Factory id: 3; player: 0; nb_cyborgs: 4; production: 3
Factory id: 4; player: 0; nb_cyborgs: 4; production: 3
Factory id: 5; player: 0; nb_cyborgs: 0; production: 0
Factory id: 6; player: 0; nb_cyborgs: 0; production: 0"""

turn_2_player_1 = "MOVE 1 5 26"

turn_2_player_minus_1 = "MOVE 2 4 5;INC 2;BOMB 2 1"

turn_4 = """nb turns: 3
Factory id: 0; player: 0; nb_cyborgs: 0; production: 0
Factory id: 1; player: 1; nb_cyborgs: 1; production: 1
Factory id: 2; player: -1; nb_cyborgs: 13; production: 2
Factory id: 3; player: 0; nb_cyborgs: 4; production: 3
Factory id: 4; player: 0; nb_cyborgs: 4; production: 3
Factory id: 5; player: 0; nb_cyborgs: 0; production: 0
Factory id: 6; player: 0; nb_cyborgs: 0; production: 0
Troop id: 7; player: 1; origin: 1; destination: 5; nb_cyborgs: 26; nb_turns: 2
Bomb id: 8; player: -1; origin: 2; destination: -1; nb_turns: -1
Troop id: 9; player: -1; origin: 2; destination: 4; nb_cyborgs: 5; nb_turns: 3"""

turn_54 = """nb turns: 54
Factory id: 0; player: -1; nb_cyborgs: 0; production: 0
Factory id: 1; player: -1; nb_cyborgs: 3; production: 1
Factory id: 2; player: -1; nb_cyborgs: 3; production: 1
Factory id: 3; player: 0; nb_cyborgs: 10; production: 2
Factory id: 4; player: 0; nb_cyborgs: 10; production: 2
Factory id: 5; player: -1; nb_cyborgs: 1; production: 1
Factory id: 6; player: -1; nb_cyborgs: 0; production: 0
Factory id: 7; player: -1; nb_cyborgs: 8; production: 0
Factory id: 8; player: -1; nb_cyborgs: 0; production: 0
Factory id: 9; player: -1; nb_cyborgs: 14; production: 2
Factory id: 10; player: -1; nb_cyborgs: 6; production: 2
Factory id: 11; player: -1; nb_cyborgs: 9; production: 3
Factory id: 12; player: -1; nb_cyborgs: 9; production: 3
Troop id: 109; player: -1; origin: 12; destination: 5; nb_cyborgs: 3; nb_turns: 1
Troop id: 118; player: -1; origin: 12; destination: 9; nb_cyborgs: 3; nb_turns: 4
Troop id: 119; player: -1; origin: 10; destination: 9; nb_cyborgs: 2; nb_turns: 2
Troop id: 125; player: -1; origin: 2; destination: 0; nb_cyborgs: 2; nb_turns: 1
Troop id: 131; player: -1; origin: 12; destination: 7; nb_cyborgs: 3; nb_turns: 4
Troop id: 133; player: 1; origin: 11; destination: 5; nb_cyborgs: 3; nb_turns: 1
Troop id: 134; player: -1; origin: 7; destination: 11; nb_cyborgs: 7; nb_turns: 1
Troop id: 136; player: -1; origin: 12; destination: 11; nb_cyborgs: 3; nb_turns: 10
Troop id: 138; player: -1; origin: 2; destination: 11; nb_cyborgs: 2; nb_turns: 10
Troop id: 139; player: -1; origin: 10; destination: 11; nb_cyborgs: 2; nb_turns: 7
Troop id: 141; player: -1; origin: 7; destination: 11; nb_cyborgs: 2; nb_turns: 2
Troop id: 143; player: -1; origin: 12; destination: 11; nb_cyborgs: 3; nb_turns: 11
Troop id: 144; player: -1; origin: 10; destination: 11; nb_cyborgs: 2; nb_turns: 8
Troop id: 146; player: -1; origin: 9; destination: 11; nb_cyborgs: 2; nb_turns: 1
Troop id: 147; player: -1; origin: 12; destination: 11; nb_cyborgs: 3; nb_turns: 12
Troop id: 148; player: -1; origin: 1; destination: 11; nb_cyborgs: 2; nb_turns: 1
Troop id: 149; player: -1; origin: 2; destination: 11; nb_cyborgs: 2; nb_turns: 12
Troop id: 150; player: -1; origin: 10; destination: 11; nb_cyborgs: 2; nb_turns: 9"""

turn_54_player_1 = "WAIT"

turn_54_player_minus_1 = "INC 9"

turn_32 = """nb turns: 32
Factory id: 0; player: -1; nb_cyborgs: 5; production: 0
Factory id: 1; player: 1; nb_cyborgs: 1; production: 1
Factory id: 2; player: -1; nb_cyborgs: 2; production: 1
Factory id: 3; player: 0; nb_cyborgs: 10; production: 2
Factory id: 4; player: 0; nb_cyborgs: 10; production: 2
Factory id: 5; player: 1; nb_cyborgs: 0; production: 0
Factory id: 6; player: -1; nb_cyborgs: 0; production: 0
Factory id: 7; player: -1; nb_cyborgs: 0; production: 0
Factory id: 8; player: -1; nb_cyborgs: 7; production: 0
Factory id: 9; player: 1; nb_cyborgs: 14; production: 2
Factory id: 10; player: -1; nb_cyborgs: 2; production: 2
Factory id: 11; player: 1; nb_cyborgs: 1; production: 3
Factory id: 12; player: -1; nb_cyborgs: 3; production: 3
Bomb id: 14; player: -1; origin: 2; destination: 1; nb_turns: 1
Troop id: 23; player: -1; origin: 2; destination: 1; nb_cyborgs: 2; nb_turns: 4
Troop id: 25; player: -1; origin: 12; destination: 1; nb_cyborgs: 1; nb_turns: 4
Troop id: 29; player: -1; origin: 2; destination: 1; nb_cyborgs: 2; nb_turns: 6
Troop id: 32; player: -1; origin: 12; destination: 7; nb_cyborgs: 3; nb_turns: 1
Troop id: 37; player: -1; origin: 12; destination: 7; nb_cyborgs: 3; nb_turns: 2
Troop id: 38; player: -1; origin: 2; destination: 7; nb_cyborgs: 2; nb_turns: 2
Troop id: 49; player: -1; origin: 12; destination: 0; nb_cyborgs: 3; nb_turns: 1
Troop id: 50; player: -1; origin: 2; destination: 0; nb_cyborgs: 2; nb_turns: 2
Troop id: 55; player: -1; origin: 12; destination: 8; nb_cyborgs: 3; nb_turns: 1
Troop id: 62; player: -1; origin: 12; destination: 6; nb_cyborgs: 3; nb_turns: 2
Troop id: 63; player: -1; origin: 2; destination: 8; nb_cyborgs: 2; nb_turns: 1
Troop id: 66; player: 1; origin: 1; destination: 11; nb_cyborgs: 1; nb_turns: 1
Troop id: 70; player: -1; origin: 12; destination: 6; nb_cyborgs: 3; nb_turns: 3
Troop id: 71; player: 1; origin: 1; destination: 11; nb_cyborgs: 1; nb_turns: 2
Troop id: 75; player: -1; origin: 7; destination: 1; nb_cyborgs: 1; nb_turns: 3
Troop id: 76; player: -1; origin: 6; destination: 8; nb_cyborgs: 1; nb_turns: 3
Troop id: 77; player: -1; origin: 12; destination: 8; nb_cyborgs: 3; nb_turns: 4
Troop id: 78; player: -1; origin: 2; destination: 8; nb_cyborgs: 2; nb_turns: 3
Troop id: 79; player: -1; origin: 10; destination: 8; nb_cyborgs: 2; nb_turns: 3
Troop id: 80; player: 1; origin: 1; destination: 11; nb_cyborgs: 1; nb_turns: 3
Troop id: 81; player: 1; origin: 5; destination: 11; nb_cyborgs: 1; nb_turns: 5
Troop id: 83; player: -1; origin: 0; destination: 8; nb_cyborgs: 7; nb_turns: 1
Troop id: 84; player: -1; origin: 12; destination: 8; nb_cyborgs: 3; nb_turns: 5
Troop id: 85; player: -1; origin: 10; destination: 8; nb_cyborgs: 2; nb_turns: 4"""

turn_32_player_1 = "MOVE 1 7 1;MOVE 5 7 0;MOVE 9 7 14;MOVE 11 7 1"

turn_32_player_minus_1 = "MOVE 8 5 7;MOVE 0 5 5;MOVE 12 5 3;MOVE 2 5 2;MOVE 10 5 2"

turn_34 = """nb turns: 33
Factory id: 0; player: -1; nb_cyborgs: 3; production: 0
Factory id: 1; player: 1; nb_cyborgs: 0; production: 1
Factory id: 2; player: -1; nb_cyborgs: 1; production: 1
Factory id: 3; player: 0; nb_cyborgs: 10; production: 2
Factory id: 4; player: 0; nb_cyborgs: 10; production: 2
Factory id: 5; player: 1; nb_cyborgs: 0; production: 0
Factory id: 6; player: -1; nb_cyborgs: 0; production: 0
Factory id: 7; player: -1; nb_cyborgs: 3; production: 0
Factory id: 8; player: -1; nb_cyborgs: 12; production: 0
Factory id: 9; player: 1; nb_cyborgs: 2; production: 2
Factory id: 10; player: -1; nb_cyborgs: 2; production: 2
Factory id: 11; player: 1; nb_cyborgs: 4; production: 3
Factory id: 12; player: -1; nb_cyborgs: 3; production: 3
Troop id: 23; player: -1; origin: 2; destination: 1; nb_cyborgs: 2; nb_turns: 3
Troop id: 25; player: -1; origin: 12; destination: 1; nb_cyborgs: 1; nb_turns: 3
Troop id: 29; player: -1; origin: 2; destination: 1; nb_cyborgs: 2; nb_turns: 5
Troop id: 37; player: -1; origin: 12; destination: 7; nb_cyborgs: 3; nb_turns: 1
Troop id: 38; player: -1; origin: 2; destination: 7; nb_cyborgs: 2; nb_turns: 1
Troop id: 50; player: -1; origin: 2; destination: 0; nb_cyborgs: 2; nb_turns: 1
Troop id: 62; player: -1; origin: 12; destination: 6; nb_cyborgs: 3; nb_turns: 1
Troop id: 70; player: -1; origin: 12; destination: 6; nb_cyborgs: 3; nb_turns: 2
Troop id: 71; player: 1; origin: 1; destination: 11; nb_cyborgs: 1; nb_turns: 1
Troop id: 75; player: -1; origin: 7; destination: 1; nb_cyborgs: 1; nb_turns: 2
Troop id: 76; player: -1; origin: 6; destination: 8; nb_cyborgs: 1; nb_turns: 2
Troop id: 77; player: -1; origin: 12; destination: 8; nb_cyborgs: 3; nb_turns: 3
Troop id: 78; player: -1; origin: 2; destination: 8; nb_cyborgs: 2; nb_turns: 2
Troop id: 79; player: -1; origin: 10; destination: 8; nb_cyborgs: 2; nb_turns: 2
Troop id: 80; player: 1; origin: 1; destination: 11; nb_cyborgs: 1; nb_turns: 2
Troop id: 81; player: 1; origin: 5; destination: 11; nb_cyborgs: 1; nb_turns: 4
Troop id: 84; player: -1; origin: 12; destination: 8; nb_cyborgs: 3; nb_turns: 4
Troop id: 85; player: -1; origin: 10; destination: 8; nb_cyborgs: 2; nb_turns: 3
Troop id: 86; player: 1; origin: 1; destination: 7; nb_cyborgs: 1; nb_turns: 4
Troop id: 88; player: 1; origin: 9; destination: 7; nb_cyborgs: 14; nb_turns: 4
Troop id: 89; player: 1; origin: 11; destination: 7; nb_cyborgs: 1; nb_turns: 5
Troop id: 90; player: -1; origin: 8; destination: 5; nb_cyborgs: 7; nb_turns: 3
Troop id: 91; player: -1; origin: 0; destination: 5; nb_cyborgs: 5; nb_turns: 2
Troop id: 92; player: -1; origin: 12; destination: 5; nb_cyborgs: 3; nb_turns: 9
Troop id: 93; player: -1; origin: 2; destination: 5; nb_cyborgs: 2; nb_turns: 7
Troop id: 94; player: -1; origin: 10; destination: 5; nb_cyborgs: 2; nb_turns: 7"""

def parse_network(i_str):
    """
    Reconstruct the network with the string representation of the edges dictionnary, edge value being the distance.
    """

    edges_dict = ast.literal_eval(i_str)
    graph = Graph()
    for origin in edges_dict:
        for destination in edges_dict[origin]:
            graph.add_undirected_edge(str(origin), str(destination), edges_dict[origin][destination])
    return graph

def parse_state(i_str):

    nb_turns = 0
    factories = {}
    troops = {}
    bombs = {}

    for line in i_str.split("\n"):

        if line.startswith("nb turns:"):
            nb_turns = int(line.split(": ")[1])
            continue

        entity = Entity.parse(line, nb_turns)
        if isinstance(entity, Factory):
            factories[entity.id] = entity
        elif isinstance(entity, Troop):
            troops[entity.id] = entity
        elif isinstance(entity, Bomb):
            bombs[entity.id] = entity

    return State(factories, troops, bombs, nb_turns)

def parse_orders(i_str):

    return [Order.parse(order_str) for order_str in i_str.split(";")]


def one_turn_parse_test_function(i_network_str, i_turn_str, i_player, i_other_player, i_next_turn = None, verbose = False):

    network = parse_network(i_network_str)

    turn = parse_state(i_turn_str)

    player = parse_orders(i_player)
    other_player = parse_orders(i_other_player)

    if not i_next_turn is None:
        next_turn = parse_state(i_next_turn)
    else:
        next_turn = None

    return one_turn_test_function(network, turn, player, other_player, next_turn, verbose)

def one_turn_test_function(i_network, i_turn, i_player, i_other_player, i_next_turn = None, verbose = False):

    controller = GameController(i_network)

    is_game_finished, simulated_next_state = controller.simulate_next_state(i_turn, i_player, i_other_player)

    if verbose:
        print("is game finished: " + str(is_game_finished))
        print("simulated next state:")
        print(str(simulated_next_state))
        print("saved turn:")
        print(str(i_next_turn))

    return is_game_finished, simulated_next_state, i_next_turn

def parse_log_file(i_file):

    cptr = 0
    network = None

    states = []
    state_str = ""
    order_player_1 = []
    order_player_minus_1 = []

    status_list = ["network", "state", "state_in_progress", "order_player_1", "waiting_minus_1", "order_player_minus_1"]
    status = status_list[0]


    for line in i_file:
        cptr += 1
        # print("parsing line: " + str(cptr))
        # print("status: " + str(status))
        # print("line: " + str(line))
        if status == status_list[0]:
            if not line.startswith("Edges: "):
                continue
            network = parse_network(line[7:].rstrip())
            status = status_list[1]
            continue
        if status == status_list[1]:
            if not line.startswith("nb turns:"):
                continue
            status = status_list[2]
            state_str = ""
        if status == status_list[2]:
            if not line.startswith("Sortie standard :"):
                state_str += line
                continue
            else:
                # print("state_str: " + str(state_str.rstrip()))
                states.append(parse_state(state_str.rstrip()))
                status = status_list[3]
                continue
        if status == status_list[3]:
            order_player_1.append(parse_orders(line.rstrip()))
            status = status_list[4]
            continue
        if status == status_list[4]:
            if not line.startswith("Sortie standard :"):
                continue
            else:
                status = status_list[5]
                continue
        if status == status_list[5]:
            order_player_minus_1.append(parse_orders(line.rstrip()))
            status = status_list[1]
            continue

    return network, states, order_player_1, order_player_minus_1

    # print("network: " + str(network))
    # print("state: " + "\n".join([str(state) for state in states]))
    # print("p1: " + ";".join([str(order) for orders in order_player_1 for order in orders]))
    # print("p-1: " + ";".join([str(order) for orders in order_player_minus_1 for order in orders]))

def update_entities_id(i_simulated, i_stored):
    """
    Rewrite the uuid id from the entity if it is found in the corresponding stored state.
    """

    simulated = [i_simulated.troops, i_simulated.bombs]
    stored = [i_stored.troops, i_stored.bombs]

    for it_entity in range(2):
        for it_simulated_entity in simulated[it_entity]:
            if it_simulated_entity in stored[it_entity]:
                continue
            else:
                for it_stored_entity in stored[it_entity]:
                    if simulated[it_entity][it_simulated_entity] == stored[it_entity][it_stored_entity]:
                        simulated[it_entity][it_simulated_entity].id = stored[it_entity][it_stored_entity].id
                        break


class TurnTest(unittest.TestCase):


    def test_turn_2(self):

        is_game_finished, simulated_next_state, next_turn = one_turn_parse_test_function(edges_network_2, turn_2, turn_2_player_1, turn_2_player_minus_1, turn_4)

        self.assertFalse(is_game_finished)
        self.assertEqual(simulated_next_state, next_turn)

    def test_turn_32(self):

        is_game_finished, simulated_next_state, next_turn = one_turn_parse_test_function(edges_network_32_54, turn_32, turn_32_player_1, turn_32_player_minus_1, turn_34)

        self.assertFalse(is_game_finished)
        self.assertEqual(simulated_next_state, next_turn)

    def test_turn_54(self):

        is_game_finished, simulated_next_state, next_turn = one_turn_parse_test_function(edges_network_32_54, turn_54, turn_54_player_1, turn_54_player_minus_1)

        self.assertTrue(is_game_finished)


class EndToEnd(unittest.TestCase):

    file = "game_logs.log"

    def test(self):

        with open(self.file, 'r') as f:
            network, states, order_player_1, order_player_minus_1 = parse_log_file(f)
            simulated_states = [states[0]]
            for it_state in range(len(states)-1):
                # if it_state == 9:

                is_game_finished, simulated_next_state, _ = one_turn_test_function(network, simulated_states[it_state], order_player_1[it_state], order_player_minus_1[it_state])
                update_entities_id(simulated_next_state, states[it_state+1])
                simulated_states.append(simulated_next_state)

                print("it_state: " + str(it_state))
                print("state " + str(it_state) + ": " + "\n".join([str(states[it_state])]))
                print("orders 1: " + ";".join([str(orders) for orders in order_player_1[it_state]]))
                print("orders-1: " + ";".join([str(orders) for orders in order_player_minus_1[it_state]]))
                print("state " + str(it_state + 1) + ": " + "\n".join([str(states[it_state+1])]))
                print("simulated state " + str(it_state + 1) + ": " + "\n".join([str(simulated_states[it_state+1])]))
                print("state turn: simulated: "  + str(simulated_states[it_state+1].nb_turns) + " ; saved: " + str(states[it_state+1].nb_turns))
                print("simulated can produce after turn: " + str(simulated_states[it_state+1].factories["1"].can_produce_after_turn))
                print("stored can produce after turn: " + str(states[it_state+1].factories["1"].can_produce_after_turn))

                if simulated_states[it_state+1].nb_turns == 50:
                    self.assertTrue(is_game_finished, "game should not be over {0}".format(states[it_state + 1].nb_turns))
                else:
                    self.assertFalse(is_game_finished, "game should be over {0}".format(states[it_state + 1].nb_turns))
                self.assertEqual(states[it_state+1], simulated_states[it_state+1])


class LaunchBombTest(unittest.TestCase):

    file = "game_logs.log"

    def test(self):

        with open(self.file, 'r') as f:
            network, states, order_player_1, order_player_minus_1 = parse_log_file(f)
            simulated_states = [states[0]]
            for it_state in range(len(states)-1):
                # if it_state == 9:

                _, simulated_next_state, _ = one_turn_test_function(network, simulated_states[it_state], order_player_1[it_state], order_player_minus_1[it_state])
                update_entities_id(simulated_next_state, states[it_state+1])
                simulated_states.append(simulated_next_state)

                print("state " + str(it_state) + ": " + "\n".join([str(states[it_state])]))
                bomb_order = launch_bomb(network, simulated_states[it_state])
                print("bomb order :" + " ; ".join([str(order) for order in bomb_order]))


class ArrivalSchemeTest(unittest.TestCase):

    file = "game_logs.log"

    def test(self):

        with open(self.file, 'r') as f:
            network, states, order_player_1, order_player_minus_1 = parse_log_file(f)
            simulated_states = [states[0]]
            for it_state in range(len(states)-1):
                # if it_state == 9:

                _, simulated_next_state, _ = one_turn_test_function(network, simulated_states[it_state], order_player_1[it_state], order_player_minus_1[it_state])
                update_entities_id(simulated_next_state, states[it_state+1])
                simulated_states.append(simulated_next_state)

                arrival_scheme(simulated_states[it_state])

                print("state " + str(it_state) + ": " + "\n".join([str(states[it_state])]))
                arrivals = arrival_scheme(simulated_states[it_state])
                print("arrivals :")
                print("\n".join(["  " + str(it_factory) + " --> " + " ; ".join([str(it_turn) + " -- " + str(arrivals[it_factory][it_turn]) for it_turn in arrivals[it_factory]]) for it_factory in arrivals]))


class ProductionAndArrivalSchemeTest(unittest.TestCase):

    file = "game_logs.log"

    def test(self):

        with open(self.file, 'r') as f:
            network, states, order_player_1, order_player_minus_1 = parse_log_file(f)
            simulated_states = [states[0]]
            for it_state in range(len(states)-1):
                # if it_state == 9:

                _, simulated_next_state, _ = one_turn_test_function(network, simulated_states[it_state], order_player_1[it_state], order_player_minus_1[it_state])
                update_entities_id(simulated_next_state, states[it_state+1])
                simulated_states.append(simulated_next_state)

                print("state " + str(it_state) + ": " + "\n".join([str(states[it_state])]))
                arrivals = production_and_arrival_scheme(simulated_states[it_state])
                needed = needed_cyborgs(simulated_states[it_state])
                cost = cost_to_increase_prod(simulated_states[it_state])
                print("production arrivals :")
                print("\n".join(["  " + str(it_factory) + " --> " + " ; ".join([str(it_turn) + " -- " + str(arrivals[it_factory][it_turn]) for it_turn in arrivals[it_factory]]) for it_factory in arrivals]))
                print("needed cyborgs :")
                print("\n".join(["  " + str(it_factory) + " --> nb cyborgs: " + str(needed[it_factory][0]) + " in " + str(needed[it_factory][1]) + " turns" for it_factory in needed]))
                print("cost to increase prod :")
                print("\n".join(["  fact: " + str(it_factory[0]) + " needed: " + str(it_factory[1]) + " prod: " + str(it_factory[2]) for it_cost in sorted(cost.keys(), reverse=True) for it_factory in cost[it_cost]]))


# to run all tests
if __name__ == "__main__":
    unittest.main()

