import sys
import math

# ###############################################################################################
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
            node = self.nodes[i_node_id]
        except KeyError as exception:
            log("Graph." + i_fun_name + ": ERROR: node_id "+str(i_node_id)+" doesn't exist.")
            traceback.print_stack()
            raise KeyError

    def add_directed_edge(self, i_node1_id, i_node2_id, i_weight = 0):
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

    def add_undirected_edge(self, i_node1_id, i_node2_id, i_weight = 0):
        self.add_directed_edge(i_node1_id, i_node2_id, i_weight)
        self.add_directed_edge(i_node2_id, i_node1_id, i_weight)

    def check_edge_exists(self, i_node1_id, i_node2_id, i_fun_name):
        try:
            a_node_1 = self.edges[i_node1_id]
        except KeyError as exception:
            log("Graph." + i_fun_name + ": ERROR: node_id "+str(i_node1_id)+" doesn't exist.")
            traceback.print_stack()
            raise KeyError
        try:
            a_weight = self.edges[i_node1_id][i_node2_id]
        except KeyError as exception:
            log("Graph." + i_fun_name + ": ERROR: node_id "+str(i_node2_id)+" doesn't exist.")
            traceback.print_stack()
            raise KeyError

    def delete_directed_edge(self, i_node1_id, i_node2_id):
        self.check_edge_exists(i_node1_id,i_node2_id,"delete_directed_edge")
        del self.edges[i_node1_id][i_node2_id]
        del self.origins[i_node2_id][i_node1_id]
        if not self.edges[i_node1_id]:
            del self.edges[i_node1_id]
        if not self.origins[i_node2_id]:
            del self.origins[i_node2_id]

    def delete_undirected_edge(self, i_node1_id, i_node2_id):
        self.check_edge_exists(i_node1_id,i_node2_id,"delete_undirected_edge")
        self.check_edge_exists(i_node2_id,i_node1_id,"delete_undirected_edge")
        self.delete_directed_edge(i_node1_id, i_node2_id)
        self.delete_directed_edge(i_node2_id, i_node1_id)

    def get_edge_weight(self, i_node1_id, i_node2_id):
        self.check_edge_exists(i_node1_id,i_node2_id,"get_edge_weight")
        return self.edges[i_node1_id][i_node2_id]

    def set_edge_weight(self, i_node1_id, i_node2_id, i_weight):
        self.check_edge_exists(i_node1_id,i_node2_id,"get_edge_weight")
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
class Factory(object):

    def __init__(self, i_id, i_player, i_nb_cyborgs, i_production):
        self.id = i_id
        self.player = i_player
        self.nb_cyborgs = i_nb_cyborgs
        self.production = i_production

    def __str__(self):
        return "Factory id: " + str(self.id) + "; player: " + str(self.player) + "; nb_cyborgs: " + str(self.nb_cyborgs) + "; production: " + str(self.production)

class Troop(object):

    def __init__(self, i_id, i_player, i_origin, i_destination, i_nb_cyborgs, i_nb_turns):
        self.id = i_id
        self.player = i_player
        self.origin = i_origin
        self.destination = i_destination
        self.nb_cyborgs = i_nb_cyborgs
        self.nb_turns = i_nb_turns

    def __str__(self):
        return "Troop id: " + str(self.id) + "; player: " + str(self.player) + "; origin: " + str(self.origin) +"; destination: " + str(self.destination) +"; nb_cyborgs: " + str(self.nb_cyborgs) + "; nb_turns: " + str(self.nb_turns)

class Bomb(object):

    def __init__(self, i_id, i_player, i_origin, i_destination, i_nb_turns):
        self.id = i_id
        self.player = i_player
        self.origin = i_origin
        self.destination = i_destination
        self.nb_turns = i_nb_turns

    def __str__(self):
        return "Bomb id: " + str(self.id) + "; player: " + str(self.player) + "; origin: " + str(self.origin) +"; destination: " + str(self.destination) + "; nb_turns: " + str(self.nb_turns)

# ###############################################################################################
# FUNCTIONS
# ###############################################################################################
def log(i_text):
    print(str(i_text), file=sys.stderr)

def score_factory(i_source_factory_id, i_target_factory_id):
    target_factory = network.get_node_value(i_target_factory_id)
    target_nb_cyborgs = target_factory.nb_cyborgs
    target_production = - target_factory.production * target_factory.player
    distance = network.get_edge_weight(i_source_factory_id, i_target_factory_id)
    source_factory = network.get_node_value(i_source_factory_id)
    source_nb_cyborgs = source_factory.nb_cyborgs
    source_production = source_factory.production

    diff_troops_at_arrival = source_nb_cyborgs - target_nb_cyborgs - target_production * distance

    return  target_factory.production + diff_troops_at_arrival - distance

def select_target():
    global network
    res = []
    for node_1 in network.get_nodes():
        factory_1 = network.get_node_value(node_1)
        if factory_1.player == 1:
            for node_2 in network.get_nodes():
                factory_2 = network.get_node_value(node_2)
                if factory_2.player != 1:
                    res.append((factory_1.id, factory_2.id, score_factory(factory_1.id, factory_2.id)))
    log(res)
    if res:
        res = max(res, key = lambda x: x[2])
        log(res)
        return res
    return None


# ###############################################################################################
# MAIN CODE
# ###############################################################################################
network = Graph()

# input parsing
nb_factories = int(input())  # the number of factories
nb_links = int(input())  # the number of links between factories
for i in range(nb_links):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    network.add_undirected_edge(factory_1, factory_2, distance)

# log
log(network)


# game loop
while True:
    # input parsing
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
            network.set_node_value(entity_id, Factory(entity_id, arg_1, arg_2, arg_3))
        elif entity_type == "TROOP":
            troops[entity_id] = Troop(entity_id, arg_1, arg_2, arg_3, arg_4, arg_5)
        else:
            bombs[entity_id] = Bomb(entity_id, arg_1, arg_2, arg_3, arg_4)

    # log
    [log(network.get_node_value(it_node)) for it_node in network.get_nodes()]
    [log(troops[it_troop]) for it_troop in troops]
    [log(bombs[it_bomb]) for it_bomb in bombs]

    # Any valid action, such as "WAIT" or "MOVE source destination cyborgs"
    target = select_target()
    if target is None:
        answer = "WAIT"
    else:
        answer = "MOVE " + str(target[0]) + " " + str(target[1]) + " " + str(network.get_node_value(target[0]).nb_cyborgs)
    print(answer)
