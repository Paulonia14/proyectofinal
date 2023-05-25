import pickle as pk 

def printMat(mat):
    #print matrix created with lists that has borders (each vertex in the borders)
    for each in mat:
        print(each)

def createDirected_G_Mat_with_edges(vertices, aristas):
    # Create an adjacency matrix but WITH borders (Directed Graph)
    # I add the borders
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


def validateAdress(adress):
    #Validate adress of the element
    adress=adress.strip("''")
    adress=adress.replace('e','')
    adress=adress.split(",")
    vertex1= adress[0].strip()[1:]
    vertex2= adress[2].strip()[1:]
    try:
        with open("serialized_matrix.pickle","rb") as Matfile:
            mapMatrix=pk.load(Matfile)
    except:
        print("Map not defined, you have to create the map first to do this")
        raise

    if int(vertex1) and int(vertex2) not in mapMatrix[0]:
        #Check if element adress is in map
        print("Adress not in map")
        raise
    #Get the index in the first list of the matrix of the two vertex
    index1=mapMatrix[0].index(int(vertex1))
    index2=mapMatrix[0].index(int(vertex2))
    #Check if adress is an edge by searching the two vertex in the matrix
    if mapMatrix[index1][index2]!=0:
        distanceEdge=mapMatrix[index1][index2]
    elif mapMatrix[index2][index1]!=0:
        distanceEdge=mapMatrix[index2][index1]
    else:
        print("Adress is not a street")
        raise
    #add the distances and compare with the distance of the edge
    if (int(adress[1].strip()[0])) + (int(adress[3].strip()[0]))!= distanceEdge:
        print("The Distance you provided is not equivalent to the distance of the street")
        raise

#pseudo infinite XD
global INF
INF=9999999999



def Initial_Mat_for_FloydW(matriz):
    #Prepara la Tabla para el algoritmo de FW
    #quito los bordes (Grafo Dirijido)
    matriz.pop(0)
    for each in matriz:
        each.pop(0)
    #relleno con infinito y los 0 correspondientes
    for i in range(0,len(matriz)):
        for j in range(0,len(matriz)):
            if matriz[i][j]==0 and i!=j:
                matriz[i][j]=INF
    
    return matriz


def floyd_warshall(Mat): #O(V^3) #mat(previamente preparada)
    #implemento el algoritmo de FW para ver el camino mas corto entre cualquier par de vertices 
    NumV=len(Mat) #rows
    for k in range(NumV): #be a new n X n matrix
        for i in range(NumV):
            for j in range(NumV):
                Mat[i][j] = min(Mat[i][j], Mat[i][k] + Mat[k][j]) #ecuacion de recurrencia O(1)
    return Mat #nueva matriz con los caminos mas cortos (infinito significa que no hay camino)