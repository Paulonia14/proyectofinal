
def printMat(mat):
    #print matrix created with lists that has borders (each vertex in the borders)
    for each in mat:
        print(each)

def createDirected_G_Mat_with_edges(vertices, aristas):
    # Create an adjacency matrix but WITH borders (Directed Graph)
    # I add the borders
    # Create the adjacency matrix but WITHOUT the borders ??
    vertices.sort()
    n = len(vertices)
    # Create adjacency matrix initialized with zeros
    matriz = [[0] * n for x in range(n)]
    # Fill matrix with "ones" when there is an edge
    for u, v,weight in aristas:
        i = vertices.index(u)
        j = vertices.index(v)
        matriz[i][j] = weight
    for i in range(0,len(matriz)):
        matriz[i].insert(0,vertices[i])
    matriz.insert(0,["V"])
    for each in vertices:
        matriz[0].append(each)
 
    return matriz