
def printMat(mat):
    #imprime una matriz hecha con listas que SI tiene los bordes
    for each in mat:
        print(each)

def createDirected_G_Mat_with_edges(vertices, aristas):
    #crea la matriz de adyacencia pero CON los bordes (Grafo Dirijido)
    #agrego los bordes
    #crea la matriz de adyacencia pero SIN los bordes
    vertices.sort()
    n = len(vertices)
    # crear matriz de adyacencia inicializada con ceros
    matriz = [[0] * n for x in range(n)]
    # llenar matriz con unos donde haya aristas
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