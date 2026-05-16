import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()

    def build_graph(self, distanza_minima):
        self._graph.clear()

        edges = DAO.get_edges(distanza_minima)

        for row in edges:
            id1 = row["id1"]
            id2 = row["id2"]

            self._graph.add_node(
                id1,
                iata = row["iata1"],
                airport = row["airport1"])

            self._graph.add_node(
                id2,
                iata=row["iata2"],
                airport=row["airport2"])

            self._graph.add_edge(
                id1,
                id2,
                weight = float(row["avg_distance"]))

    def get_num_nodes(self):
        return self._graph.number_of_nodes()

    def get_num_edges(self):
        return self._graph.number_of_edges()

    def get_edges(self):
        edges = list(self._graph.edges(data=True))

        edges.sort(key=lambda x: x[2]["weight"], reverse=True)

        result = []

        for id1, id2, data in edges:
            iata1 = self._graph.nodes[id1]["iata"]
            iata2 = self._graph.nodes[id2]["iata"]
            airport1 = self._graph.nodes[id1]["airport"]
            airport2 = self._graph.nodes[id2]["airport"]
            distance = data["weight"]

            result.append((iata1, airport1, iata2, airport2, distance))

        return result
