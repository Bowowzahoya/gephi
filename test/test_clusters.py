import pandas as pd
import unittest
import os

from context import gephi
from gephi import clusters as cl

THIS_FOLDER = os.path.dirname(__file__)
FOLD = THIS_FOLDER+"/res/gephi_files/"

@unittest.skip
class TestClusters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TEST_NODES = pd.read_csv(FOLD+"Nodes_clustered.csv", index_col=0)
        cls.TEST_EDGES = pd.read_excel(FOLD+"edges.xlsx", index_col=0)
        
    def test_get_cluster(self):
        clusters = cl.get_cluster_info(self.TEST_NODES, self.TEST_EDGES)
        clusters.to_excel(THIS_FOLDER+"/out/clusters.xlsx")
        assert clusters.loc[0, "Maximum Size of Cluster"] == 319401
        
    def test_get_overlap_from_weights(self):
        overlap = cl._get_overlap_from_weights(self.TEST_EDGES, self.TEST_NODES["size"])
        assert overlap.iloc[2] == 26
        
    def test_get_weighted_mean_weight(self):
        one_node_edges = self.TEST_EDGES.loc[self.TEST_EDGES["Source"] == "4-Nitrophenol"]
        weighted_mean_weight = cl._get_weighted_mean_weight(one_node_edges, self.TEST_NODES["size"])
        assert round(weighted_mean_weight, 3) == 0.018
        
    def test_get_weighted_mean_weights(self):
        nodes = ["High surface area", "Mesoporous-carbon", "Mesoporous-material", "Mesoporous-silica", "Microporous-material", "Nanofoam", "src_Journal of Porous Materials", "src_Microporous and Mesoporous Materials"]
        weighted_mean_weights = cl._get_weighted_mean_weights(self.TEST_NODES.loc[nodes],
                                                            self.TEST_EDGES, self.TEST_NODES["size"])
        assert round(weighted_mean_weights.loc["High surface area"], 3) == 0.020


class TestClustersNodes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TEST_NODES = pd.read_csv(FOLD+"Nodes_clustered.csv", index_col=0)
        cls.TEST_EDGES = pd.read_excel(FOLD+"edges.xlsx", index_col=0)
        
    def test_get_cluster_info_nodes(self):
        nodes = cl.get_cluster_info_nodes(self.TEST_NODES, self.TEST_EDGES)
        nodes.to_excel(THIS_FOLDER+"/out/nodes_with_info.xlsx")
        assert round(nodes.loc["Conduction band", "Mean Weight of Edges Inside Cluster"],5) == 0.00874


if __name__ == '__main__':
    unittest.main()