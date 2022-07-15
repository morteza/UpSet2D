import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def _clean_label(label: str):
    if '_-' in label:
        label = label.split('_-')[0]
    else:
        label = label.replace('_', ' ')

    return label


def plot_hypergraph(adj, show=True):

    nodes_idx, edges_idx = np.where(adj == 1.0)

    nodes = adj.index.unique()  # Y-axis
    edges = adj.columns.unique()  # X-axis

    n_nodes = len(nodes)
    n_edges = len(edges)

    grid = np.mgrid.__getitem__([slice(0, n_edges, 1), slice(0, n_nodes, 1)])
    grid = grid.reshape(2, -1).T
    grid_df = pd.DataFrame(grid, columns=['edge', 'node'])

    # TODO use a more flexible way to compute figure size
    _, ax = plt.subplots(figsize=(n_edges / 1.5, n_nodes / 3))

    # background dots
    ax.scatter(grid_df['edge'], grid_df['node'], s=70, color='lightgray', zorder=1)

    # background lines
    for xi in range(n_edges):
        ax.plot([xi, xi], [0, n_nodes - 1], color='lightgray', lw=3, zorder=2)

    # black dots
    ax.scatter(edges_idx, nodes_idx, color='black', s=120, zorder=3)

    # black lines
    for _edge in range(n_edges):
        idx = np.where(edges_idx == _edge)
        _node = nodes_idx[idx]
        ax.plot([_edge, _edge],
                [_node.min(), _node.max()],
                lw=3, color='black', zorder=4)

    # shading
    for i in range(0, n_nodes, 2):
        rect = plt.Rectangle((-.5, i - .45), n_edges, .9,
                             facecolor='#eeeeee', lw=0, zorder=0)
        ax.add_patch(rect)

    # reorder axes and clean the frame
    ax.xaxis.tick_top()
    ax.invert_yaxis()
    ax.set_frame_on(False)
    ax.tick_params(axis='both', which='both', length=0)

    # ticks
    plt.xticks(range(n_edges))
    plt.yticks(range(n_nodes))

    # tick label properties
    [t.set_y(.955) for t in ax.xaxis.get_ticklabels()]
    [t.set_x(0.04) for t in ax.yaxis.get_ticklabels()]

    # tick labels
    ax.set_xticklabels([_clean_label(lbl) for lbl in edges], fontsize=24)
    ax.set_yticklabels([_clean_label(lbl) for lbl in nodes], fontsize=20)

    # rotate x-tick labels
    plt.xticks(rotation=45, ha='left', rotation_mode='anchor')

    if show:
        plt.show()
