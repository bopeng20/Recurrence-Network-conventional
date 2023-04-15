# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

def RN(X, epsilon=1, PLOT=True,edge_width=2,vertex_size=10,*args):
    import igraph
    import pandas as pd
    import numpy as np
    from matplotlib import pyplot as plt
    X = pd.DataFrame(X)
    L = X.shape[0]
    distL = pd.DataFrame(np.array(np.meshgrid(np.arange(L), np.arange(L))).T.reshape(-1, 2), columns=["Var1", "Var2"])
    distL = distL[distL["Var1"] <= distL["Var2"]]
    tmp = (X.values[distL["Var1"]] - X.values[distL["Var2"]]) ** 2
    distL["D"] = np.apply_along_axis(lambda x: np.sqrt(np.sum(x)), 1, tmp)
    distL = distL[distL["D"] <= epsilon]
    Res1 = pd.DataFrame({"X": distL["Var1"], "Y": distL["Var2"]})
    Res2 = pd.DataFrame({"X": distL["Var2"], "Y": distL["Var1"]})
    Res = pd.concat([Res1, Res2]).drop_duplicates().reset_index(drop=True)
    R = Res.copy()
    R["S"] = np.ones(R.shape[0])
    M = np.zeros((len(pd.unique(R["X"])), len(pd.unique(R["Y"]))))
    M[R["X"], R["Y"]] = R["S"]
    M = M.astype(int)
    np.fill_diagonal(M, 0)
    graph = igraph.Graph.Adjacency(M.tolist(), mode="undirected", diag=False)
    if PLOT:
        #igraph.plot(graph,"RN.png", edge_width=2, edge_curved=0.2, vertex_size=5, vertex_label=[])
        # Set the edge width to 2
        visual_style = {}
        visual_style["edge_width"] = edge_width
        igraph.plot(graph,"RN.png",**visual_style,vertex_size=vertex_size)
        plt.show()
    edge_list = Res.to_dict(orient="records")
    return {"Network":graph,"edge_list": edge_list, "Adjacency_Matrix": M}