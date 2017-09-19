from __future__ import print_function
import sys
import unittest
import graph

OUTPUT = sys.stdout

# Global function log
def log(i_text):
    print(i_text, file=OUTPUT)

class GraphNodesTests(unittest.TestCase):

    def setUp(self):
        self.g = graph.Graph()
        self.g.set_node_value('0',0.0)
        self.g.set_node_value('a',5.0)
        self.g.set_node_value(1,"text")

    def test_node_set_and_get(self):
        #log(self.g)
        self.assertEqual(self.g.get_node_value('0'), 0.0)
        self.assertEqual(self.g.get_node_value('a'), 5.0)
        self.assertEqual(self.g.get_node_value(1), "text")
        with self.assertRaises(KeyError):
            self.g.get_node_value(2)

    def test_node_delete(self):
        #log(self.g)
        self.g.delete_node('a')
        with self.assertRaises(KeyError):
            self.g.get_node_value('a')

class GraphEdgesTests(unittest.TestCase):

    def setUp(self):
        self.g = graph.Graph()

    def test_add_directed_edge(self):
        self.g.add_directed_edge('0', 'a', 1)
        self.g.add_directed_edge('a', 1, 1)
        self.g.add_directed_edge('a', 'b', -1)
        log(self.g)
        self.assertEqual(self.g.get_node_value('0'), 0)
        self.assertEqual(self.g.get_node_value('a'), 0)
        self.assertEqual(self.g.get_node_value('b'), 0)
        self.assertEqual(set(self.g.get_children_nodes('0')), {'a'})
        self.assertEqual(set(self.g.get_children_nodes('a')), {1,'b'})
        self.assertEqual(self.g.get_children_nodes(1), list())
        self.assertEqual(self.g.get_children_nodes('b'), list())
        self.assertEqual(self.g.origins['a'], {'0':1})
        self.assertEqual(self.g.origins[1], {'a':1})

    def test_delete_directed_edge(self):
        self.g.add_directed_edge('0', 'a', 1)
        self.g.add_directed_edge('a', 1, 1)
        self.g.add_directed_edge('a', 'b', -1)
        #log(self.g)
        self.g.delete_directed_edge('a',1)
        self.assertEqual(set(self.g.get_children_nodes('0')), {'a'})
        self.assertEqual(set(self.g.get_children_nodes('a')), {'b'})
        with self.assertRaises(KeyError):
            self.g.get_edge_weight('a',1)


    def test_add_undirected_edge(self):
        self.g.add_undirected_edge('0', 'a', 1)
        self.g.add_undirected_edge('a', 1, 1)
        self.g.add_undirected_edge('a', 'b', -1)
        #log(self.g)
        self.assertEqual(self.g.get_node_value('0'), 0)
        self.assertEqual(self.g.get_node_value('a'), 0)
        self.assertEqual(self.g.get_node_value('b'), 0)
        self.assertEqual(set(self.g.get_children_nodes('0')), {'a'})
        self.assertEqual(set(self.g.get_children_nodes('a')), {'0','b',1})
        self.assertEqual(set(self.g.get_children_nodes(1)), {'a'})
        self.assertEqual(set(self.g.get_children_nodes('b')), {'a'})

    def test_delete_undirected_edge(self):
        self.g.add_undirected_edge('0', 'a', 1)
        self.g.add_undirected_edge('a', 1, 1)
        self.g.add_undirected_edge('a', 'b', -1)
        #log(self.g)
        self.g.delete_directed_edge('a',1)
        self.assertEqual(set(self.g.get_children_nodes('0')), {'a'})
        self.assertEqual(set(self.g.get_children_nodes('a')), {'0','b'})
        self.assertEqual(set(self.g.get_children_nodes(1)), {'a'})
        self.assertEqual(set(self.g.get_children_nodes('b')), {'a'})
        self.g.delete_undirected_edge('a','b')
        self.assertEqual(set(self.g.get_children_nodes('a')), {'0'})
        self.assertEqual(set(self.g.get_children_nodes(1)), {'a'})
        self.assertEqual(self.g.get_children_nodes('b'), list())
        with self.assertRaises(KeyError):
            self.g.get_edge_weight('a',1)

    def test_get_edge_weight(self):
        self.g.add_directed_edge('0', 'a', 1)
        self.g.add_undirected_edge('a', 2, -1)
        #log(self.g)
        self.assertEqual(self.g.get_edge_weight('0','a'), 1)
        with self.assertRaises(KeyError):
            self.g.get_edge_weight('a','0')
        self.assertEqual(self.g.get_edge_weight('a',2), -1)
        self.assertEqual(self.g.get_edge_weight(2,'a'), -1)

    def test_set_edge_weight(self):
        self.g.add_directed_edge('0', 'a', 1)
        self.g.add_undirected_edge('a', 2, -1)
        #log(self.g)
        self.g.set_edge_weight('0','a',42)
        self.assertEqual(self.g.get_edge_weight('0','a'), 42)
        with self.assertRaises(KeyError):
            self.g.set_edge_weight('a','0',-42)
        self.g.set_edge_weight('a',2,21)
        self.assertEqual(self.g.get_edge_weight('a',2), 21)
        self.assertEqual(self.g.get_edge_weight(2,'a'), -1)

    def test_get_parent_nodes(self):
        self.g.add_undirected_edge('0', 'a', 1)
        self.g.add_undirected_edge('a', 1, 1)
        self.g.add_undirected_edge('a', 'b', -1)
        #log(self.g)
        self.assertEqual(set(self.g.get_parent_nodes('0')), {'a'})
        self.assertEqual(set(self.g.get_parent_nodes('a')), {'0','b',1})

class DepthFirstSearchTests(unittest.TestCase):

    def setUp(self):
        self.g = graph.Graph()


    def test_depth_first_search_1(self):
        self.g.add_undirected_edge('a','b')
        self.g.add_undirected_edge('a','c')
        self.g.add_undirected_edge('b','d')
        self.g.add_undirected_edge('b','e')
        self.g.add_undirected_edge('c','d')
        self.g.add_undirected_edge('d','e')
        self.g.add_undirected_edge('e','f')
        self.g.add_undirected_edge('e','g')
        self.g.add_undirected_edge('f','g')
        self.g.add_undirected_edge('g','h')
        #log(self.g)
        self.assertEqual(self.g.depth_first_search('a'),({'a': None, 'b': 'a', 'd': 'b', 'c': 'd', 'e': 'd', 'f': 'e', 'g': 'f', 'h': 'g'},7))

    def test_depth_first_search_2(self):
        self.g.add_undirected_edge('r','a')
        self.g.add_undirected_edge('r','b')
        self.g.add_undirected_edge('r','c')
        self.g.add_undirected_edge('a','d')
        self.g.add_undirected_edge('a','e')
        self.g.add_undirected_edge('b','f')
        self.g.add_undirected_edge('b','g')
        self.g.add_undirected_edge('b','h')
        self.g.add_undirected_edge('c','i')
        self.g.add_undirected_edge('e','j')
        self.g.add_undirected_edge('e','k')
        self.g.add_undirected_edge('i','l')
        #log(self.g)
        log(self.g.depth_first_search('r'))
        self.assertEqual(self.g.depth_first_search('r'),({'r': None, 'a': 'r', 'd': 'a', 'e': 'a', 'j': 'e', 'k': 'e', 'b': 'r', 'f': 'b', 'g': 'b', 'h': 'b', 'c': 'r', 'i': 'c', 'l': 'i'},4))

class DijkstraTests(unittest.TestCase):

    def setUp(self):
        self.g = graph.Graph()


    def test_dijkstra(self):
        self.g.add_undirected_edge('a','b',85)
        self.g.add_undirected_edge('a','c',217)
        self.g.add_undirected_edge('a','e',173)
        self.g.add_undirected_edge('b','f',80)
        self.g.add_undirected_edge('c','g',186)
        self.g.add_undirected_edge('c','h',103)
        self.g.add_undirected_edge('d','h',183)
        self.g.add_undirected_edge('e','j',502)
        self.g.add_undirected_edge('f','i',250)
        self.g.add_undirected_edge('i','j',84)
        self.g.add_undirected_edge('h','j',167)
        #log(self.g)
        self.dj = self.g.dijkstra('a')
        self.assertEqual(self.dj[0]['j'],487)
        self.assertEqual(self.dj[1]['j'],'h')
        self.assertEqual(self.dj[1]['h'],'c')
        self.assertEqual(self.dj[1]['c'],'a')

class BellmanTests(unittest.TestCase):

    def setUp(self):
        self.g = graph.Graph()


    def test_bellman_v2(self):
        self.g.add_directed_edge('a','b',-4)
        self.g.add_directed_edge('a','t',-3)
        self.g.add_directed_edge('b','e',-2)
        self.g.add_directed_edge('b','d',-1)
        self.g.add_directed_edge('c','b',8)
        self.g.add_directed_edge('c','t',3)
        self.g.add_directed_edge('d','t',4)
        self.g.add_directed_edge('d','a',6)
        self.g.add_directed_edge('e','t',2)
        self.g.add_directed_edge('e','c',-3)
        #log(self.g)
        self.bm = self.g.bellman_v2('t')
        #log(self.bm)
        self.assertEqual(self.bm, ({'a': -6, 'b': -2, 't': 0, 'e': 0, 'd': 0, 'c': 3},{'b':'a', 'e':'b', 't':'c', 'a':'d', 'c':'e'}))

class TopologicalTests(unittest.TestCase):

    def setUp(self):
        self.g = graph.Graph()


    def test_topological_ordering(self):
        self.g.add_directed_edge('1','2')
        self.g.add_directed_edge('1','8')
        self.g.add_directed_edge('2','3')
        self.g.add_directed_edge('8','4')
        self.g.add_directed_edge('4','3')
        self.g.add_directed_edge('4','5')
        self.g.add_directed_edge('3','6')
        self.g.add_directed_edge('5','6')
        self.g.add_directed_edge('3','5')
        #log(self.g)
        self.topo = self.g.topological_order()
        #log(self.topo)
        self.assertIn(self.topo, [['1', '2', '8', '4', '3', '5', '6'],['1', '8', '2', '4', '3', '5', '6'],['1', '8', '4', '2', '3', '5', '6']])

class LongestTopologicalPathTests(unittest.TestCase):

    def setUp(self):
        self.g = graph.Graph()


    def test_topological_ordering(self):
        self.g.add_directed_edge('1','2', 1)
        self.g.add_directed_edge('1','8', 1)
        self.g.add_directed_edge('2','3', 1)
        self.g.add_directed_edge('8','4', 1)
        self.g.add_directed_edge('4','3', 1)
        self.g.add_directed_edge('4','5', 1)
        self.g.add_directed_edge('3','6', 1)
        self.g.add_directed_edge('5','6', 1)
        self.g.add_directed_edge('3','5', 1)
        #log(self.g)
        self.longest_path = self.g.longest_path_topological_order()
        #log(self.longest_path)
        self.assertEqual(self.longest_path, ({'1': 0, '3': 3, '2': 1, '5': 4, '4': 2, '6': 5, '8': 1}, {'3': '4', '2': '1', '5': '3', '4': '8', '6': '5', '8': '1'}))

class AStarTests(unittest.TestCase):

    def setUp(self):
        self.g = graph.Graph()


    def distance_nodes(i_origin, i_destination):
        dist_dict = {'s':10, 'a':9, 'b':7, 'c':8, 'd':8, 'e':0, 'f':6, 'g':3, 'h':6, 'i':4, 'j':4, 'k':3, 'l':6}
        return dist_dict[i_origin]

    def test_A_star(self):
        self.g.add_undirected_edge('s','a',7)
        self.g.add_undirected_edge('s','b',2)
        self.g.add_undirected_edge('s','c',3)
        self.g.add_undirected_edge('a','b',3)
        self.g.add_undirected_edge('a','d',4)
        self.g.add_undirected_edge('b','d',4)
        self.g.add_undirected_edge('b','h',1)
        self.g.add_undirected_edge('c','l',2)
        self.g.add_undirected_edge('d','f',5)
        self.g.add_undirected_edge('f','h',3)
        self.g.add_undirected_edge('g','e',2)
        self.g.add_undirected_edge('g','h',2)
        self.g.add_undirected_edge('i','j',6)
        self.g.add_undirected_edge('i','k',4)
        self.g.add_undirected_edge('i','l',4)
        self.g.add_undirected_edge('j','k',4)
        self.g.add_undirected_edge('j','l',4)
        self.g.add_undirected_edge('k','e',5)
        #log(self.g)
        self.a_star = self.g.a_star('s','e', AStarTests.distance_nodes)
        self.min_path = self.g.get_min_path('s','e',self.a_star[1])
        #log(self.longest_path)
        self.assertEqual(self.a_star, ({'s': 0, 'a': 5, 'b': 2, 'c': 3, 'd': 6, 'h': 3, 'l': 9223372036854775807, 'f': 6, 'g': 5, 'e': 7, 'i': 9223372036854775807, 'j': 9223372036854775807, 'k': 9223372036854775807}, {'a': 'b', 'b': 's', 'c': 's', 'd': 'b', 'h': 'b', 'f': 'h', 'g': 'h', 'e': 'g'}))
        self.assertEqual(self.min_path, ['s', 'b', 'h', 'g', 'e'])



# to run all tests
if __name__ == "__main__":
    unittest.main()
