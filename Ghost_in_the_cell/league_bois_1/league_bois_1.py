from __future__ import print_function
import sys
import uuid
import copy
import traceback


################################################################################################
# LIBRARIES
# ###############################################################################################
class Graph:
    def __init__(self):
        self.nodes = dict()
        self.edges = dict()
        self.origins = dict()

    def __str__(self):
        output_str = 'Nodes: ' + str(self.nodes) + '\n'
        output_str += 'Edges: ' + str(self.get_edges()) + '\n'
        return output_str

    def get_node_value(self, i_node_id):
        self.check_node_exists(i_node_id, 'get_node_value')
        return self.nodes[i_node_id]

    def set_node_value(self, i_node_id, i_value):
        self.nodes[i_node_id] = i_value

    def delete_node(self, i_node_id):
        self.check_node_exists(i_node_id, 'delete_node')
        del self.nodes[i_node_id]

    def check_node_exists(self, i_node_id, i_fun_name):
        try:
            self.nodes[i_node_id]
        except KeyError:
            log("Graph." + i_fun_name + ": ERROR: node_id " + str(i_node_id) + " doesn't exist.")
            traceback.print_stack()
            raise KeyError

    def add_directed_edge(self, i_node1_id, i_node2_id, i_weight=0):
        """ adds a directed adge between 2 nodes, and creates an empty value for the node if not existing"""
        if i_node1_id not in self.nodes.keys():
            self.set_node_value(i_node1_id, 0)
        if i_node2_id not in self.nodes.keys():
            self.set_node_value(i_node2_id, 0)
        if i_node1_id not in self.edges.keys():
            self.edges[i_node1_id] = dict()
        if i_node2_id not in self.origins.keys():
            self.origins[i_node2_id] = dict()
        self.edges[i_node1_id][i_node2_id] = i_weight
        self.origins[i_node2_id][i_node1_id] = i_weight

    def add_undirected_edge(self, i_node1_id, i_node2_id, i_weight=0):
        self.add_directed_edge(i_node1_id, i_node2_id, i_weight)
        self.add_directed_edge(i_node2_id, i_node1_id, i_weight)

    def check_edge_exists(self, i_node1_id, i_node2_id, i_fun_name):
        try:
            self.edges[i_node1_id]
        except KeyError:
            log("Graph." + i_fun_name + ": ERROR: node_id " + repr(i_node1_id) + " doesn't exist.")
            traceback.print_stack()
            raise KeyError
        try:
            self.edges[i_node1_id][i_node2_id]
        except KeyError:
            log("Graph." + i_fun_name + ": ERROR: node_id " + repr(i_node2_id) + " doesn't exist.")
            traceback.print_stack()
            raise KeyError

    def delete_directed_edge(self, i_node1_id, i_node2_id):
        self.check_edge_exists(i_node1_id, i_node2_id, "delete_directed_edge")
        del self.edges[i_node1_id][i_node2_id]
        del self.origins[i_node2_id][i_node1_id]
        if not self.edges[i_node1_id]:
            del self.edges[i_node1_id]
        if not self.origins[i_node2_id]:
            del self.origins[i_node2_id]

    def delete_undirected_edge(self, i_node1_id, i_node2_id):
        self.check_edge_exists(i_node1_id, i_node2_id, "delete_undirected_edge")
        self.check_edge_exists(i_node2_id, i_node1_id, "delete_undirected_edge")
        self.delete_directed_edge(i_node1_id, i_node2_id)
        self.delete_directed_edge(i_node2_id, i_node1_id)

    def get_edge_weight(self, i_node1_id, i_node2_id):
        self.check_edge_exists(i_node1_id, i_node2_id, "get_edge_weight")
        return self.edges[i_node1_id][i_node2_id]

    def set_edge_weight(self, i_node1_id, i_node2_id, i_weight):
        self.check_edge_exists(i_node1_id, i_node2_id, "get_edge_weight")
        self.edges[i_node1_id][i_node2_id] = i_weight

    def get_nodes(self):
        """ returns a copy of the list of nodes ids of the graph"""
        return list(self.nodes.keys())

    def get_edges(self):
        """ returns the dictionary of edges + values of the graph"""
        return self.edges

    def get_children_nodes(self, i_node_id):
        """ returns the list of nodes ids after outgoing edges of given node"""
        if i_node_id not in self.edges.keys():
            return list()
        return list(self.edges[i_node_id].keys())

    def get_parent_nodes(self, i_node_id):
        """ returns the list of nodes ids of nodes incoming into given node"""
        return list(self.origins[i_node_id].keys())

    def get_min_path(self, i_start_node, i_end_node, i_previous_nodes):
        # check if path exists
        path = []
        if i_end_node in i_previous_nodes or i_start_node == i_end_node:
            current_node = i_end_node
            path.append(current_node)
            while current_node in i_previous_nodes:
                current_node = i_previous_nodes[current_node]
                path.append(current_node)
            path.reverse()
        return path


# ###############################################################################################
# OBJECTS
# ###############################################################################################

class Entity(object):
    def __init__(self, i_id, i_player):
        self.id = i_id
        self.player = i_player

    @staticmethod
    def parse(i_str, turn):
        splitted_str = [field.split(": ")[1] for field in i_str.split("; ")]
        if i_str.startswith("Factory"):
            return Factory.parse(splitted_str, turn)
        elif i_str.startswith("Troop"):
            return Troop.parse(splitted_str, turn)
        elif i_str.startswith("Bomb"):
            return Bomb.parse(splitted_str, turn)
        return None


class Factory(Entity):
    def __init__(self, i_id, i_player, i_nb_cyborgs, i_production):
        Entity.__init__(self, i_id, i_player)
        self.nb_cyborgs = i_nb_cyborgs
        self.production = i_production
        self.can_produce_after_turn = -1
        self.probable_bomb_target = None

    def __str__(self):
        return "Factory id: " + str(self.id) + "; player: " + str(self.player) + "; nb_cyborgs: " + str(
            self.nb_cyborgs) + "; production: " + str(self.production)

    @staticmethod
    def parse(i_str, i_turn):
        return Factory(i_str[0], int(i_str[1]), int(i_str[2]), int(i_str[3]))

    def __eq__(self, other):
        if not isinstance(other, Factory):
            return False
        return self.player == other.player and self.nb_cyborgs == other.nb_cyborgs \
            and self.production == other.production

    def __ne__(self, other):
        return not self.__eq__(other)

    def closest_opponent_factory(self, i_network, i_state):

        opponent = - self.player
        closest_distance = None
        closest_id = None
        for it_factory in i_network.edges[self.id]:
            if i_state.factories[it_factory].player == opponent:
                distance = i_network.get_edge_weight(self.id, it_factory)
                if closest_distance is None or closest_distance > distance:
                    closest_distance = distance
                    closest_id = it_factory
        return closest_id


class Troop(Entity):
    def __init__(self, i_id, i_player, i_origin, i_destination, i_nb_cyborgs, i_nb_turns, i_turn_created):
        Entity.__init__(self, i_id, i_player)
        self.origin = i_origin
        self.destination = i_destination
        self.nb_cyborgs = i_nb_cyborgs
        self.nb_turns = i_nb_turns
        self.turn_created = i_turn_created

    def __str__(self):
        return "Troop id: " + str(self.id) + "; player: " + str(self.player) + "; origin: " + str(
            self.origin) + "; destination: " + str(self.destination) + "; nb_cyborgs: " + str(
            self.nb_cyborgs) + "; nb_turns: " + str(self.nb_turns)

    @staticmethod
    def parse(i_str, turn):
        return Troop(i_str[0], int(i_str[1]), i_str[2], i_str[3], int(i_str[4]), int(i_str[5]), turn)

    def __eq__(self, other):
        if not isinstance(other, Troop):
            return False
        return self.player == other.player and self.origin == other.origin and self.destination == other.destination \
               and self.nb_cyborgs == other.nb_cyborgs and self.nb_turns == other.nb_turns

    def __ne__(self, other):
        return not self.__eq__(other)


class Bomb(Entity):
    def __init__(self, i_id, i_player, i_origin, i_destination, i_nb_turns, i_turn_created):
        Entity.__init__(self, i_id, i_player)
        self.origin = i_origin
        self.destination = i_destination
        self.nb_turns = i_nb_turns
        self.exploded = False
        self.turn_created = i_turn_created

    def __str__(self):
        return "Bomb id: " + str(self.id) + "; player: " + str(self.player) + "; origin: " + str(
            self.origin) + "; destination: " + str(self.destination) + "; nb_turns: " + str(self.nb_turns)

    @staticmethod
    def parse(i_str, turn):
        return Bomb(i_str[0], int(i_str[1]), i_str[2], i_str[3], int(i_str[4]), turn)

    def __eq__(self, other):
        """
        Destination and nb_turns shouldn't be taken into account, since we don't have this information for the other
        player.
        """
        if not isinstance(other, Bomb):
            return False
        return self.origin == other.origin

    def __ne__(self, other):
        return not self.__eq__(other)


class Order(object):
    def __init__(self, i_origin=None, i_destination=None):
        self.origin = i_origin
        self.destination = i_destination

    @staticmethod
    def parse(i_str):
        splited_str = i_str.split(" ")[1:]
        if i_str.startswith("WAIT"):
            return OrderWait.parse(splited_str)
        elif i_str.startswith("MOVE"):
            return OrderTroops.parse(splited_str)
        elif i_str.startswith("BOMB"):
            return OrderBomb.parse(splited_str)
        elif i_str.startswith("INC"):
            return OrderIncrease.parse(splited_str)
        return None


class OrderWait(Order):
    def __init__(self):
        Order.__init__(self)

    def __str__(self):
        return "WAIT"

    @staticmethod
    def parse(i_str):
        return OrderWait()


class OrderTroops(Order):
    def __init__(self, i_origin, i_destination, i_nb_troop):
        Order.__init__(self, i_origin, i_destination)
        self.nb_troops = i_nb_troop

    def __str__(self):
        return " ".join(["MOVE", str(self.origin), str(self.destination), str(self.nb_troops)])

    @staticmethod
    def parse(i_str):
        return OrderTroops(i_str[0], i_str[1], int(i_str[2]))


class OrderBomb(Order):
    def __init__(self, i_origin, i_destination):
        Order.__init__(self, i_origin, i_destination)

    def __str__(self):
        return " ".join(["BOMB", str(self.origin), str(self.destination)])

    @staticmethod
    def parse(i_str):
        return OrderBomb(i_str[0], i_str[1])


class OrderIncrease(Order):
    def __init__(self, i_origin):
        Order.__init__(self, i_origin)

    def __str__(self):
        return " ".join(["INC", str(self.origin)])

    @staticmethod
    def parse(i_str):
        return OrderIncrease(i_str[0])


class ActionPlan(object):
    def __init__(self, i_order_set):
        self.order_set = i_order_set

    def __str__(self):
        return ";".join([str(it_order) for it_order in self.order_set])


class GameController(object):
    """
    Check that the all the actions in the action plan are valid.
    Moves to the next state.
    """

    def __init__(self, i_network):
        self.network = i_network

    def move_existing_entities(self, i_new_state):
        # the game controller should know everything about the game to be able to play a turn.

        for it_troop in i_new_state.troops:
            i_new_state.troops[it_troop].nb_turns -= 1
        for it_bomb in i_new_state.bombs:
            i_new_state.bombs[it_bomb].nb_turns -= 1

    def execute_player_orders(self, i_new_state, i_player_id, i_action_plan):

        for it_order in i_action_plan:
            if isinstance(it_order, OrderTroops):
                factory = i_new_state.factories[it_order.origin]
                if factory.player == i_player_id and it_order.nb_troops > 0:
                    current_troops = it_order.nb_troops if it_order.nb_troops < factory.nb_cyborgs else factory.nb_cyborgs
                    distance = self.network.get_edge_weight(it_order.origin, it_order.destination)
                    new_id = str(uuid.uuid4())
                    i_new_state.troops[new_id] = Troop(new_id, i_player_id, it_order.origin, it_order.destination,
                                                       current_troops, distance, i_new_state.nb_turns)
                    factory.nb_cyborgs -= current_troops
            elif isinstance(it_order, OrderBomb):
                factory = i_new_state.factories[it_order.origin]
                if factory.player == i_player_id and i_new_state.nb_bombs_launched()[i_player_id] < 2:
                    distance = self.network.get_edge_weight(it_order.origin, it_order.destination)
                    new_id = str(uuid.uuid4())
                    i_new_state.bombs[new_id] = Bomb(new_id, i_player_id, it_order.origin, it_order.destination,
                                                     distance, i_new_state.nb_turns)
            elif isinstance(it_order, OrderIncrease):
                factory = i_new_state.factories[it_order.origin]
                if factory.player == i_player_id and factory.production < 3 and factory.nb_cyborgs >= 10:
                    factory.production += 1
                    factory.nb_cyborgs -= 10

    def generate_troops(self, i_new_state):

        for it_factory in i_new_state.factories:
            factory = i_new_state.factories[it_factory]
            if factory.player != 0 and factory.can_produce_after_turn <= i_new_state.nb_turns:
                factory.nb_cyborgs += factory.production

    def play_fights(self, i_new_state):

        arriving, arriving_ids = i_new_state.get_troops_arriving()
        for it_destination in arriving:
            min_troops = min(arriving[it_destination][1], arriving[it_destination][-1])
            arriving[it_destination][1] -= min_troops
            arriving[it_destination][-1] -= min_troops
            arriving_winner = 1 if arriving[it_destination][1] > 0 else -1
            factory = i_new_state.factories[it_destination]
            if arriving_winner == factory.player:
                factory.nb_cyborgs += arriving[it_destination][arriving_winner]
            else:
                factory.nb_cyborgs -= arriving[it_destination][arriving_winner]
                if factory.nb_cyborgs < 0:
                    factory.nb_cyborgs *= -1
                    factory.player = arriving_winner

        for it_arriving_ids in arriving_ids:
            del i_new_state.troops[it_arriving_ids]

    def explode_bombs(self, i_new_state):
        arriving = i_new_state.get_arriving_bombs()
        for it_arriving in arriving:
            factory = i_new_state.factories[i_new_state.bombs[it_arriving].destination]
            nb_casualties = factory.nb_cyborgs / 2
            if nb_casualties < 10:
                nb_casualties = min(10, factory.nb_cyborgs)
            factory.nb_cyborgs -= nb_casualties
            factory.can_produce_after_turn = i_new_state.nb_turns + 5
            factory.probable_bomb_target = None
            for it_factory in i_new_state.factories:
                if i_new_state.factories[it_factory].probable_bomb_target is not None and \
                                i_new_state.factories[it_factory].probable_bomb_target[0] == it_arriving:
                    i_new_state.factories[it_factory].probable_bomb_target = None
            i_new_state.bombs[it_arriving].exploded = True

    def is_end_of_game(self, i_new_state):

        if i_new_state.nb_turns == 50:
            return True
        nb_entities = i_new_state.count_player_entities()
        return nb_entities[1] == 0 or nb_entities[-1] == 0

    def simulate_next_state(self, i_current_state, i_action_plan_player_1, i_action_plan_player_minus_1):
        """
        Return new instance of state object.
        """
        new_state = copy.deepcopy(i_current_state)
        self.move_existing_entities(new_state)
        new_state.nb_turns += 1
        self.execute_player_orders(new_state, 1, i_action_plan_player_1)
        self.execute_player_orders(new_state, -1, i_action_plan_player_minus_1)
        self.generate_troops(new_state)
        self.play_fights(new_state)
        self.explode_bombs(new_state)
        return self.is_end_of_game(new_state), new_state


class State(object):
    """
    Must be immutable.
    Attributes are dictionaries.
    """

    def __init__(self, i_factories=None, i_troops=None, i_bombs=None, i_nb_turns=0):
        if i_bombs is None:
            i_bombs = {}
        if i_troops is None:
            i_troops = {}
        if i_factories is None:
            i_factories = {}
        self.factories = i_factories
        self.troops = i_troops
        self.bombs = i_bombs
        self.nb_turns = i_nb_turns

    def __str__(self):

        entities = {}
        entities.update(self.factories)
        entities.update(self.troops)
        entities.update(self.bombs)
        entities_str = "\n".join([str(entities[entity_id]) for entity_id in sorted(entities.keys())])
        return "\n".join(["nb turns: " + str(self.nb_turns), entities_str])

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        if other is self:
            return True

        self_active_bombs = copy.deepcopy(self.bombs)
        for it_bomb in self.bombs:
            if self_active_bombs[it_bomb].exploded:
                del self_active_bombs[it_bomb]
        other_active_bombs = copy.deepcopy(other.bombs)
        for it_bomb in other.bombs:
            if other_active_bombs[it_bomb].exploded:
                del other_active_bombs[it_bomb]

        dictionaries = [(self.factories, other.factories), (self.troops, other.troops),
                        (self_active_bombs, other_active_bombs)]

        for it_dictionaries in range(len(dictionaries)):
            dico = dictionaries[it_dictionaries]

            if len(dico[0]) != len(dico[1]):
                print("Different dico size: {0}".format(it_dictionaries))
                print("self.dico: \n{0}".format("\n".join([str(dico[0][key]) for key in sorted(dico[0].keys())])))
                print("other.dico: \n{0}".format("\n".join([str(dico[1][key]) for key in sorted(dico[1].keys())])))
                return False

            self_keys = list(dico[0].keys())  # compatibility for python 3.+
            other_keys = list(dico[1].keys())
            for entity_self_id in dico[0]:
                if entity_self_id in dico[1]:
                    if dico[0][entity_self_id] != dico[1][entity_self_id]:
                        print("Same id, different entities: " + entity_self_id)
                        print("self :  " + str(dico[0][entity_self_id]))
                        print("other: " + str(dico[1][entity_self_id]))
                        return False
                    else:
                        self_keys.remove(entity_self_id)
                        other_keys.remove(entity_self_id)

            for self_key in self_keys:
                found_match = False
                for other_key in other_keys:
                    if dico[0][self_key] == dico[1][other_key]:
                        found_match = True
                        break
                if not found_match:
                    print("No match found for self id: " + self_key)
                    return False

                    # check remaining elements

        return self.nb_turns == other.nb_turns

    def nb_bombs_launched(self):
        nb_bombs = {1: 0, -1: 0}
        for it_bomb in self.bombs:
            nb_bombs[self.bombs[it_bomb].player] += 1
        return nb_bombs

    def get_troops_arriving(self):
        arriving = {}
        arriving_ids = []
        for it_troops in self.troops:
            troop = self.troops[it_troops]
            if troop.nb_turns == 0:
                if troop.destination not in arriving:
                    arriving[troop.destination] = {1: 0, -1: 0}
                arriving[troop.destination][troop.player] += troop.nb_cyborgs
                arriving_ids.append(it_troops)
        return arriving, arriving_ids

    def get_arriving_bombs(self):
        arriving = {}
        for it_bombs in self.bombs:
            bomb = self.bombs[it_bombs]
            if bomb.nb_turns == 0:
                arriving[it_bombs] = bomb
        return arriving

    def count_player_entities(self):
        nb_entities = {1: 0, -1: 0, 0: 0}
        for it_factory in self.factories:
            nb_entities[self.factories[it_factory].player] += 1
        for it_troops in self.troops:
            nb_entities[self.troops[it_troops].player] += 1
        return nb_entities

    def project_troops(self):

        projected_factories = {}
        for it_factory in self.factories:
            factory = self.factories[it_factory]
            projected_factories[it_factory] = {1: 0, -1: 0}
            projected_factories[it_factory][factory.player] = factory.nb_cyborgs
        for it_troop in self.troops:
            troop = self.troops[it_troop]
            projected_factories[troop.destination][troop.player] += troop.nb_cyborgs
        return projected_factories


class AI(object):
    def __init__(self):
        pass

    def compute_score(self, i_state):
        """
        Return a dictionnary with key = player id and value = score.
        """
        pass

    def decide_action_plan(self, i_game_controler):
        """
        Return object ActionPlan
        """
        pass

    def generate_actions(self, i_state):
        """
        Should generate the subset of actions that make sense for the AI.
        May not be all possible actions.
        Takes into account both palyers, or only one?
        """
        pass


# ###############################################################################################
# FUNCTIONS
# ###############################################################################################
def log(i_text):
    print(str(i_text), file=sys.stderr)


def score_factory(network, state, i_source_factory_id, i_target_factory_id, i_TroopBombBoolean):
    target_factory = state.factories[i_target_factory_id]
    target_nb_cyborgs = target_factory.nb_cyborgs
    target_production = - target_factory.production * target_factory.player
    distance = network.get_edge_weight(i_source_factory_id, i_target_factory_id)
    source_factory = state.factories[i_source_factory_id]
    source_nb_cyborgs = source_factory.nb_cyborgs

    diff_troops_at_arrival = source_nb_cyborgs - target_nb_cyborgs - target_production * distance

    if i_TroopBombBoolean:
        return target_factory.production + diff_troops_at_arrival - distance
    else:
        return target_production * distance


def select_actions(network, state):
    res = []
    if state.nb_bombs_launched()[1] > 1:
        for node_1 in network.get_nodes():
            factory_1 = state.factories[node_1]
            if factory_1.player == 1:
                actions_factory_1 = []
                for node_2 in network.get_nodes():
                    factory_2 = state.factories[node_2]
                    if factory_2.player != 1:
                        actions_factory_1.append((factory_1.id, factory_2.id,
                                                  score_factory(network, state, factory_1.id, factory_2.id, True)))
                best_action_factory_1 = max(actions_factory_1, key=lambda x: x[2])
                res.append(OrderTroops(best_action_factory_1[0], best_action_factory_1[1],
                                       state.factories[best_action_factory_1[0]].nb_cyborgs))
    else:
        actions_factory_0 = []
        for node_1 in network.get_nodes():
            factory_1 = state.factories[node_1]
            if factory_1.player == 1:
                actions_factory_1 = []
                for node_2 in network.get_nodes():
                    factory_2 = state.factories[node_2]
                    if factory_2.player != 1:
                        actions_factory_1.append((factory_1.id, factory_2.id,
                                                  score_factory(network, state, factory_1.id, factory_2.id, True)))
                        actions_factory_0.append((factory_1.id, factory_2.id,
                                                  score_factory(network, state, factory_1.id, factory_2.id, False)))
                if actions_factory_1:
                    best_action_factory_1 = max(actions_factory_1, key=lambda x: x[2])
                    res.append(OrderTroops(best_action_factory_1[0], best_action_factory_1[1],
                                           state.factories[best_action_factory_1[0]].nb_cyborgs))
        if actions_factory_0:
            best_action_factory_0 = max(actions_factory_0, key=lambda x: x[2])
            if best_action_factory_0[2] > 16:
                res.append(OrderBomb(best_action_factory_0[0], best_action_factory_0[1]))

    if not res:
        res.append(OrderWait())
    # log(res)
    return res


def launch_bomb(i_network, i_state):
    """
    Launch a bomb:
    - never launch the first turn, wait and see
    - the second turn targeting the planet of the opponent with prod >= 1 and max cyborgs
    - the next planet from the opponent with a prod >= 2
    """
    if i_state.nb_turns == 1:
        return []
    if i_state.nb_bombs_launched()[1] == 0 or i_state.nb_bombs_launched()[1] == 1:
        production_threshold = i_state.nb_bombs_launched()[1]
        projected_factories = i_state.project_troops()
        max_factory_id = ""
        max_factory_cyborgs = 0
        for it_factory in projected_factories:
            factory = i_state.factories[it_factory]
            if factory.player == -1 and factory.production > production_threshold and projected_factories[it_factory][
                -1] > max_factory_cyborgs and projected_factories[it_factory][-1] > projected_factories[it_factory][1]:
                max_factory_id = it_factory
                max_factory_cyborgs = projected_factories[it_factory][-1]
        if max_factory_id != "":
            our_closest_planet = i_state.factories[max_factory_id].closest_opponent_factory(i_network, i_state)
            if our_closest_planet is not None:
                return [OrderBomb(our_closest_planet, max_factory_id)]

    return []


def arrival_scheme(i_state):
    """
    Returns dictionary with
    - key: factory id
    - value: dictionary with
        - key: arrival turn
        - value: number of troops arriving
            - if > 0 our troops
            - if < 0 opponent troops
    """
    factories = {}
    for it_troop in i_state.troops:
        troop = i_state.troops[it_troop]
        if troop.destination not in factories:
            factories[troop.destination] = {}
        if troop.nb_turns not in factories[troop.destination]:
            factories[troop.destination][troop.nb_turns] = troop.nb_cyborgs * troop.player
        else:
            factories[troop.destination][troop.nb_turns] += troop.nb_cyborgs * troop.player

    for it_factory in factories:
        sorted_turns = sorted(factories[it_factory].keys())
        for it_turns in range(1, len(sorted_turns), 1):
            factories[it_factory][sorted_turns[it_turns]] += factories[it_factory][sorted_turns[it_turns - 1]]

    return factories


def production_and_arrival_scheme(i_state):
    """
    Returns dictionary with
    - key: factory id
    - value: dictionary with
        - key: arrival turn
        - value: number of troops present on the planet considering current troops, arrivals and production
            - if > 0 our troops
            - if < 0 opponent troops
    -> the weakest of our planet is the one with the minimum number of cyborgs
    -> the weakest of their planet is the one with the maximum number of cyborgs
    """
    arrivals = arrival_scheme(i_state)
    for it_factory in i_state.factories:
        factory_player = i_state.factories[it_factory].player
        current_cyborgs = factory_player * i_state.factories[it_factory].nb_cyborgs if factory_player != 0 else -i_state.factories[it_factory].nb_cyborgs
        if it_factory in arrivals:
            for it_turns in arrivals[it_factory]:
                arrivals[it_factory][it_turns] += current_cyborgs + \
                                                  (i_state.factories[it_factory].player *
                                                   i_state.factories[it_factory].production * it_turns)
        else:
            NB_TURNS = 10
            arrivals[it_factory] = {}
            arrivals[it_factory][NB_TURNS] = current_cyborgs + \
                                             (i_state.factories[it_factory].player *
                                              i_state.factories[it_factory].production * NB_TURNS)

    return arrivals


def needed_cyborgs(i_state):

    """
    Returns dictionary with
    - key: factory id
    - value:
      - if > 0: number of cyborgs to be sent to this factory (to attack or to defend)
      - if < 0: number of cyborgs that can be used from this factory
    """

    arrivals = production_and_arrival_scheme(i_state)
    needed = {}
    for it_factory in arrivals:
        min_cyborgs = 100000
        min_turn = None
        for it_turn in arrivals[it_factory]:
            if arrivals[it_factory][it_turn] < min_cyborgs:
                min_cyborgs = arrivals[it_factory][it_turn]
                min_turn = it_turn
        needed[it_factory] = (1 - min_cyborgs, min_turn)

    for it_factory in i_state.factories:
        if i_state.factories[it_factory].player == 1:
            if it_factory not in arrivals or i_state.factories[it_factory].probable_bomb_target is not None:
                needed[it_factory] = (-i_state.factories[it_factory].nb_cyborgs, 1)

    return needed


def cost_to_increase_prod(i_state, i_needed_cyborgs):
    """
    Cost in number of cyborgs to increase the production on any of the planet.
    :param i_state, i_needed_cyborgs:
    :return: dictionary with
      - key = score
      - value = [(factory id, cost in nb of cyborgs, production gain)]
    """
    costs = {}
    for it_factory in i_state.factories:
        if i_state.factories[it_factory].probable_bomb_target:
            continue
        current_needed = i_needed_cyborgs[it_factory][0] if it_factory in i_needed_cyborgs else 0
        current_production = i_state.factories[it_factory].production
        if current_needed > 0:
            # for it_productivity in range(0, 4 - current_production, 1):
            needed_troops = current_needed if current_production != 0 else current_needed + 10 #+ it_productivity * 10
            target_production = current_production if current_production != 0 else 1 #+ it_productivity
            score = target_production / needed_troops
            if score not in costs:
                costs[score] = []
            costs[score].append((it_factory, needed_troops, target_production))
        else:
            if current_production < 3:
            # for it_productivity in range(1, 4 - current_production, 1):
                needed_troops = 10  # it_productivity * 10
                target_production = current_production + 1
                score = target_production / needed_troops
                if score not in costs:
                    costs[score] = []
                costs[score].append((it_factory, needed_troops, target_production))
    return costs


def count_total_available_troops(i_state, i_needed_cyborgs):

    total = 0
    available_troops = {}
    for it_factories in i_state.factories:
        if i_state.factories[it_factories].player == 1:
            if it_factories in i_needed_cyborgs and i_needed_cyborgs[it_factories][0] < 0:
                current = min(i_state.factories[it_factories].nb_cyborgs, -i_needed_cyborgs[it_factories][0])
                available_troops[it_factories] = current
                total += current
    return total, available_troops


def rank_planets_by_distance(i_network, i_planet_id, i_available_planets):
    """
    Assumption: the network is complete
    """
    planets = [it_planet for it_planet in i_available_planets if it_planet != i_planet_id]
    return sorted(planets, key=lambda x: i_network.get_edge_weight(i_planet_id, x))




def send_troops(i_network, i_state, i_needed_cyborgs):

    total_available, available = count_total_available_troops(i_state, i_needed_cyborgs)
    cyborgs_cptr, selected_actions = select_best_actions(i_state, i_needed_cyborgs, total_available)
    increase_candidate = candidate_planet_to_increase(i_state, selected_actions, available, cyborgs_cptr)

    orders = []
    for it_action in selected_actions:
        dest_factory_id = it_action[0]
        if dest_factory_id in increase_candidate:
            orders.append(OrderIncrease(dest_factory_id))
        else:
            nb_cyborgs = it_action[1]
            ranked_neighbours = rank_planets_by_distance(i_network, dest_factory_id, available.keys())
            for neighbour in ranked_neighbours:
                if nb_cyborgs == 0:
                    break
                if available[neighbour] == 0:
                    continue
                sending = min(nb_cyborgs, available[neighbour])
                available[neighbour] -= sending
                nb_cyborgs -= sending
                orders.append(OrderTroops(neighbour, dest_factory_id, sending))

    return orders


def candidate_planet_to_increase(i_state, selected_actions, available, cyborgs_cptr):
    increase_candidate = []
    if i_state.nb_turns != 1:
        for it_action in selected_actions:
            factory = i_state.factories[it_action[0]]
            if factory.player == 1 and factory.production != it_action[2] and available[it_action[0]] >= 10:
                if cyborgs_cptr >= 0 or selected_actions.index(it_action) != len(selected_actions) - 1:
                    increase_candidate.append(it_action[0])
                    available[it_action[0]] -= 10

    return increase_candidate


def select_best_actions(i_state, i_needed_cyborgs, total_available):
    cost_to_increase = cost_to_increase_prod(i_state, i_needed_cyborgs)
    selected_actions = []
    cyborgs_cptr = total_available
    for it_cost in sorted(cost_to_increase.keys(), reverse=True):
        for it_action in cost_to_increase[it_cost]:
            if cyborgs_cptr >= 0:
                selected_actions.append(it_action)
                cyborgs_cptr -= it_action[1]
            else:
                break

    return cyborgs_cptr, selected_actions


def closests_oponent_planets(i_network):
    """
    Returns a sorted list of
    :param i_network:
    :return:
    """
    pass


def increase_prod():
    """
    Increase production if:
    - planet not probable target of bomb
    - enough cyborgs to increase production and defend from attacks
    """

    pass


def attack_planet():
    """
    Attack a planet from the openent if:
    -
    """
    pass


def colonize_planet():
    """
    Colonize a neutral planet if:
    -
    """


def defend_planet(i_network, i_state, i_needed_cyborgs):
    """
    Defend a planet if:
    - not probable target of a bomb
    """

    pass


def flag_probable_bomb_planet(i_network, i_state):
    """
    Then turn a new bomb is launched, evacuate the planet with the highest number of cyborgs.
    """
    for it_bomb in i_state.bombs:
        bomb = i_state.bombs[it_bomb]
        if not bomb.exploded and bomb.player == -1 and bomb.turn_created == i_state.nb_turns:
            max_factory_cyborgs = -1
            max_factory_id = None
            for it_factory in i_state.factories:
                factory = i_state.factories[it_factory]
                if factory.player == 1 and factory.nb_cyborgs > max_factory_cyborgs:
                    max_factory_cyborgs = factory.nb_cyborgs
                    max_factory_id = it_factory
            if max_factory_id is not None:
                i_state.factories[max_factory_id].probable_bomb_target = (
                    it_bomb, i_network.get_edge_weight(bomb.origin, max_factory_id))


# ###############################################################################################
# MAIN CODE
# ###############################################################################################
def main():
    network = Graph()

    # input parsing
    nb_factories = int(input())  # the number of factories
    nb_links = int(input())  # the number of links between factories
    for i in range(nb_links):
        factory_1, factory_2, distance = input().split()
        network.add_undirected_edge(int(factory_1), int(factory_2), int(distance))

    # log
    log(network)

    nb_turns = 0
    state = State()
    # game loop
    while True:
        # input parsing
        nb_turns += 1
        factories = {}
        troops = {}
        bombs = {}
        nb_entity = int(input())  # the number of entities (e.g. factories and troops)
        for i in range(nb_entity):
            entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
            entity_id = int(entity_id)
            arg_1 = int(arg_1)
            arg_2 = int(arg_2)
            arg_3 = int(arg_3)
            arg_4 = int(arg_4)
            arg_5 = int(arg_5)
            if entity_type == "FACTORY":
                if entity_id in state.factories:
                    factories[entity_id] = copy.deepcopy(state.factories[entity_id])
                    factories[entity_id].player = arg_1
                    factories[entity_id].nb_cyborgs = arg_2
                    factories[entity_id].production = arg_3
                else:
                    factories[entity_id] = Factory(entity_id, arg_1, arg_2, arg_3)
            elif entity_type == "TROOP":
                if entity_id in state.troops:
                    troops[entity_id] = copy.deepcopy(state.troops[entity_id])
                    troops[entity_id].nb_turns = nb_turns
                else:
                    troops[entity_id] = Troop(entity_id, arg_1, arg_2, arg_3, arg_4, arg_5, nb_turns)
            else:
                if entity_id in state.bombs:
                    bombs[entity_id] = copy.deepcopy(state.bombs[entity_id])
                    bombs[entity_id].nb_turns = arg_4
                else:
                    bombs[entity_id] = Bomb(entity_id, arg_1, arg_2, arg_3, arg_4, nb_turns)

        state = State(factories, troops, bombs, nb_turns)
        log(state)

        # Any valid action, such as "WAIT" or "MOVE source destination cyborgs"
        flag_probable_bomb_planet(network, state)
        needed = needed_cyborgs(state)
        actions = send_troops(network, state, needed)
        actions.extend(launch_bomb(network, state))
        answer = ";".join([str(action) for action in actions])
        if not answer:
            answer = str(OrderWait())

        nb_turns += 1
        print(answer)


# to run all tests
if __name__ == "__main__":
    main()
