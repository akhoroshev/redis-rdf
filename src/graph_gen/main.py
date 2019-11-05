from src.graph_gen import generate_free_scale_graph, graph2txt

n = 500
for k in [1, 3, 5, 10]:
    g = generate_free_scale_graph(n, k, ['a', 'b', 'c', 'd'])
    g_reversed_edges = generate_free_scale_graph(n, k, ['a', 'b', 'c', 'd'], True)
    graph2txt(g, f'graphs/directed_free_scale_net_{n}_{k}.txt')
    graph2txt(g_reversed_edges, f'graphs/undirected_free_scale_net_{n}_{k}.txt')
