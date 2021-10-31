import networkx as nx
import matplotlib.pyplot as plt
__PLOT = True

def plot(solution, facilities, customers):
    G=nx.Graph()
    
    pos = {}
    clist = []
    for c in customers:
        pos["c"+str(c.index)] = (c.location.x,c.location.y)
        clist.append("c"+str(c.index))
           
    flist = []    
    for f in facilities:
        pos["f"+str(f.index)] = (f.location.x,f.location.y)
        flist.append("f"+str(f.index))
        
    
    nx.draw_networkx_nodes(G,pos,node_size=1,nodelist=clist,node_color='b')
    nx.draw_networkx_nodes(G,pos,node_size=1,nodelist=flist,node_color='r')
    

    c=0
    edges = []
    for s in solution:
        edges.append(("c"+str(c), "f"+str(s)))
        c=c+1
    
    nx.draw_networkx_edges(G, pos, edgelist=edges)
    
    plt.show()