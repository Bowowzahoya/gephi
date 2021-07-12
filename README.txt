Package for creating Gephi nodes and edges .csv/.xlsx files from scientific publication/patent data.

----------------
----------------
BACKGROUND
Gephi can create force-directed graphs of nodes and edges. When using keywords, scientific journals or patent categories, this can be used to distill clusters of keywords that define an area of research/R&D. 

Clusters can be identified by eye, or with the use of the Leiden algorithm available in Gephi.

See the example/ folder for an example of such a graph.

----------------
----------------
USAGE
Main function is get_nodes_edges(), or the separate versions get_nodes(), get_edges()

Use a dictionary or Series 'limited_node_sizes' for supplying the size of a node when there is a limit in export size (Scopus: 20,000 papers, Lens: 50,000 patents/papers)

There is also the flag 'includes_internal_similarity' to calculate the internal similarity within a node, though this will take a bit longer. 

nodes = get_nodes(fnames, limited_node_sizes = sr, includes_internal_similarity=True)

To use Scopus export files set database="scopus" (default)
To use Lens export files (either patent or scholarly, both works), set database="lens"

nodes = get_nodes(fnames, limited_node_sizes = sr, includes_internal_similarity=True, database="lens")

