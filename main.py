import networkx as nx
import plotly.graph_objects as go
import random

# Define the edges and vertices
edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
vertices = [1, 2, 3, 4]

# Create a graph
G = nx.Graph()
G.add_nodes_from(vertices)
G.add_edges_from(edges)

# Generate positions for the nodes
pos = nx.spring_layout(G)

edge_trace = go.Scatter(x=[], y=[], line=dict(
    width=0.5, color='#888'), hoverinfo='none', mode='lines')

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

node_trace = go.Scatter(x=[], y=[], mode='markers', hoverinfo='text', marker=dict(
    showscale=True, colorscale='YlGnBu', reversescale=True, color=[], size=10))

for node in G.nodes():
    x, y = pos[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])

# Add node colors to the node trace
for node, adjacencies in enumerate(G.adjacency()):
    node_trace['marker']['color'] += tuple([len(adjacencies[1])])

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(title='<br>Network graph',
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False,
                           showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

fig.show()
