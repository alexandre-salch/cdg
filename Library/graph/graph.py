from __future__ import print_function # compatiba
import sys
import traceback
import datetime

# TODO:
# Get node degree

# GLOBALS
OUTPUT = sys.stderr

# FUNCTIONS
def log(i_text):
    print(i_text, file=OUTPUT)

# CLASSES
class CycleException(Exception):
    pass

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

    def depth_first_search(self, i_node_start_id):
        # check
        self.check_node_exists(i_node_start_id, 'depth_first_search')
        # initialize memoization structure
        visited = dict()
        for node_id in self.get_nodes():
            visited[node_id] = 'not_visited'
        visited[i_node_start_id] = 'being_visited'
        # initialize father structure
        father = dict()
        father[i_node_start_id] = None
        # Initialize nodes_stack
        nodes_stack = [i_node_start_id]
        # Init stack max length
        nodes_stack_max_length = 0
        # Exploration loop
        while nodes_stack:
            nodes_stack_max_length = max(nodes_stack_max_length,len(nodes_stack))
            current_node = nodes_stack[-1] #LIFO
            #log("current_node: "+str(current_node))
            unvisited_neighbours = [it_neigbour_node_id for it_neigbour_node_id in self.get_children_nodes(current_node) if visited[it_neigbour_node_id] == 'not_visited']
            if unvisited_neighbours:
                # take first unvisited
                #log("there are unvisited neighbours.")
                next_node_to_visit = unvisited_neighbours[0]
                #log("next_node_to_visit: "+str(next_node_to_visit))
                visited[next_node_to_visit] = 'being_visited'
                #log("visited: "+str(visited))
                father[next_node_to_visit] = current_node
                #log("father: "+str(father))
                nodes_stack.append(next_node_to_visit)
                #log("nodes_stack: "+str(nodes_stack))
            else:
                #log("there are NO unvisited neighbours.")
                # close the branch and mark it
                nodes_stack.pop()
                #log("nodes_stack: "+str(nodes_stack))
                visited[current_node] = 'visited'
                #log("visited: "+str(visited))
        return (father, nodes_stack_max_length)

    def dijkstra(self, i_node_start_id):
        # init vars
        min_distances = dict()
        previous_nodes = dict()
        for it_node_id in self.get_nodes():
            min_distances[it_node_id] = sys.maxsize
        min_distances[i_node_start_id] = 0
        nodes = self.get_nodes()
        while nodes:
            min_distance = sys.maxsize
            next_node = nodes[0]
            for it_node in nodes:
                if min_distances[it_node] < min_distance:
                    min_distance = min_distances[it_node]
                    next_node = it_node
            nodes.remove(next_node)
            for it_neighbor in self.get_children_nodes(next_node):
                if it_neighbor in nodes:
                    new_distance = min_distances[next_node] + self.get_edge_weight(next_node, it_neighbor)
                    if min_distances[it_neighbor] > new_distance:
                        min_distances[it_neighbor] = new_distance
                        previous_nodes[it_neighbor] = next_node
        return min_distances, previous_nodes

    def bellman_v1(self, i_node_start_id):
        distances_previous = {}
        distances_current = {}
        # initialize all previous distances to infinity, except start node
        for node in self.nodes:
            distances_previous[node] = sys.maxsize
        distances_previous[i_node_start_id] = 0
        # loop over the number of arcs to reach the node
        previous_nodes = {}
        for k in range(1, len(self.nodes), 1):
            #log("k="+str(k))
            for node in self.nodes:
                #log("node="+node)
                distances_current[node] = distances_previous[node]
                #log("parent nodes:"+str(self.get_parent_nodes(node)))
                for source_node in self.get_parent_nodes(node):
                    #log("source_node="+source_node)
                    new_distance = distances_previous[source_node] + self.get_edge_weight(source_node, node)
                    #log("new distance="+str(new_distance))
                    if new_distance < distances_current[node]:
                        distances_current[node] = new_distance
                        previous_nodes[node] = source_node
            distances_previous = distances_current
            distances_current = {}
        return distances_previous, previous_nodes

    def bellman_v2(self, i_node_start_id):
        distances = {}
        previous_nodes = {}
        for node in self.nodes:
            distances[node] = sys.maxsize
        distances[i_node_start_id] = 0
        for k in range(1, len(self.nodes), 1):
            #log("k="+str(k))
            for node in self.edges.keys():
                #log("node="+node)
                dist_from_node = [(adj_node, (self.get_edge_weight(node,adj_node) + distances[adj_node])) for adj_node in self.get_children_nodes(node)]
                #log("dist_from_node="+str(dist_from_node))
                (min_node, min_value) = min(dist_from_node, key = lambda t: t[1])
                #log("min_node="+str(min_node))
                #log("min_value="+str(min_value))
                previous_nodes[min_node] = node
                distances[node] = min(distances[node], min_value)
                #log("distances["+node+"]="+str(distances[node]))
        return distances, previous_nodes

    def topological_order(self):
        """ Purpose of this function is to extract a topological order in a graph
            ie a list of the nodes ordered with starting nodes first and then 
            new starting nodes when you cut edges from starting node
        """
        res = []
        removed_edges = set()

        # initializing set of vertices without predecessors
        vertices_with_no_incoming_edges = set(self.nodes)
        vertices_with_no_incoming_edges.difference_update(set(self.origins.keys()))

        # main loop
        while vertices_with_no_incoming_edges:
            current_node = vertices_with_no_incoming_edges.pop()
            res.append(current_node)
            # for each destination node of an edge starting from one of this vertices (with no predecessor)
            if current_node not in self.edges:
                continue
            for it_end_node in self.edges[current_node]:
                # remove edge
                removed_edges.add((current_node, it_end_node))
                it_end_node_still_has_incoming_edges = False
                # for each edge origin node of our graph
                for it_start_node in self.origins[it_end_node]:
                    # if our end_node is part of destinations and the corresponding edge is not removed yet
                    if (it_start_node, it_end_node) not in removed_edges:
                        # mark it in it_end_node_still_has_incoming_edges
                        it_end_node_still_has_incoming_edges = True
                        break
                # if node has no more edges reaching it, add it to vertices_with_no_incoming_edges
                if not it_end_node_still_has_incoming_edges:
                    vertices_with_no_incoming_edges.add(it_end_node)

        for it_start_node in self.edges:
            for it_end_node in self.edges[it_start_node]:
                if (it_start_node, it_end_node) not in removed_edges:
                    raise CycleException("Graph contains a cycle, thus no topological order possible")
                    traceback.print_stack()

        return res

    def longest_path_topological_order(self):
        distances = {}
        previous_nodes = {}
        
        #time_start = datetime.datetime.utcnow()
        topo_order = self.topological_order()
        #log("topo order: "+str(topo_order))
        # Going through all nodes in topological order
        for it_node in topo_order:
            best_distance = None
            best_node = None
            #log("checking node: " + str(it_node))
            if it_node in self.origins:
                for it_previous_node in self.origins[it_node]:
                    if it_previous_node in distances:
                        current_distance = distances[it_previous_node] + self.get_edge_weight(it_previous_node, it_node)
                        if best_distance is None or current_distance > best_distance:
                            # log("found better predecessor: " + str(it_previous_node))
                            # log("cost: " + str(current_distance))
                            best_distance = current_distance
                            best_node = it_previous_node
            # it it_node is still not in distances, it means that it_node has no predecessors
            if best_distance is None:
                distances[it_node] = 0
            else:
                distances[it_node] = best_distance
                previous_nodes[it_node] = best_node
            # log("distances: " + str(distances))
            # log("previous_nodes: " + str(previous_nodes))
        #time_after_shortest_path = datetime.datetime.utcnow()
        #log((time_after_shortest_path-time_start).total_seconds())
        return distances, previous_nodes


    def longest_path_topological_order_nodes(self):
        distances = {}
        previous_nodes = {}
        topo_order = self.topological_order()
        #log("topo order: "+str(topo_order))
        for it_node in topo_order:
            best_distance = None
            best_node = None
            #log("checking node: " + str(it_node))
            for it_previous_node in distances:
                if it_node in self.edges[it_previous_node]:
                    current_distance = distances[it_previous_node] + self.get_node_value(it_node)
                    if best_distance is None or current_distance > best_distance:
                        # log("found better predecessor: " + str(it_previous_node))
                        # log("cost: " + str(current_distance))
                        best_distance = current_distance
                        best_node = it_previous_node
            # it it_node is still not in distances, it means that it_node has no predecessors
            if best_distance is None:
                distances[it_node] = self.get_node_value(it_node)
            else:
                distances[it_node] = best_distance
                previous_nodes[it_node] = best_node
            # log("distances: " + str(distances))
            # log("previous_nodes: " + str(previous_nodes))
        return distances, previous_nodes

    def a_star(self, i_node_start_id, i_node_end_id, i_func):
        # init vars
        min_distances = dict()
        previous_nodes = dict()
        target_distance = dict()
        for it_node_id in self.get_nodes():
            min_distances[it_node_id] = sys.maxsize
            target_distance[it_node_id] = i_func(it_node_id,i_node_end_id)
        log(str(target_distance))
        min_distances[i_node_start_id] = 0
        nodes = [i_node_start_id]
        while nodes:
            min_heuristic = sys.maxsize
            next_node = nodes[0]
            for it_node in nodes:
                if min_distances[it_node]+target_distance[it_node] < min_heuristic:
                    min_heuristic = min_distances[it_node]+target_distance[it_node]
                    next_node = it_node
            nodes.remove(next_node)
            if next_node==i_node_end_id:
                return min_distances, previous_nodes
            #log("Chosen node: "+next_node + "; min_heuristic: "+str(min_heuristic))
            for it_neighbor in self.get_children_nodes(next_node):
                #log("Analyzing neighbor: "+it_neighbor)
                if it_neighbor not in nodes:
                    if min_distances[it_neighbor]==sys.maxsize: # not ideal
                        nodes.append(it_neighbor)
                        #log("Node appended to queue (1): " + it_neighbor + "; Queue: " + str(nodes))
                new_distance = min_distances[next_node] + self.get_edge_weight(next_node, it_neighbor)
                #log("New distance: "+str(new_distance))
                if min_distances[it_neighbor] > new_distance:
                    #log("shorter distance found.")
                    min_distances[it_neighbor] = new_distance
                    previous_nodes[it_neighbor] = next_node
                    if it_neighbor not in nodes:
                        nodes.append(it_neighbor)
                        #log("Node appended to queue (2): " + it_neighbor + "; Queue: " + str(nodes))
        return min_distances, previous_nodes

if __name__ == '__main__':
    log("Test")
    g = Graph()
    g.set_node_value('0',0.0)
    g.set_node_value('a',5.0)
    g.set_node_value(1,"text")
    log(g)
