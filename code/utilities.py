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

def convertAdress(adress):
    #Convert direction to a simplified list for better management
    adress=adress.strip("''")
    adress=adress.replace('e','')
    adress=adress.replace('(','')
    adress=adress.replace(')','')
    adress=adress.split(",")
    adressResult=[]
    for each in adress:
        adressResult.append(int(each))
    return adressResult


def validateAdress(adress):
    #Validate adress of the element
    adress=convertAdress(adress)
    vertex1= adress[0]
    vertex2= adress[2]
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
    if (int(adress[1])) + (int(adress[3]))!= distanceEdge:
        print("The Distance you provided is not equivalent to the distance of the street")
        raise

#pseudo infinite XD
global INF
INF=9999999999

def Null_Mat(NumV):
    #Create a NULL matrix 
    matriz=[]
    for i in range(0,NumV):
        matriz.append([None]*NumV) # dim V X V
    return matriz


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


def Init_PATHMAT_FloydW(RouteM,Mat):
    #inicializa la matriz de recorridos para FW
    NumV=len(RouteM)
    for i in range(NumV):
        for j in range(NumV):
            if Mat[i][j] != INF and i != j: #no tomo ni los que no tiene un camino(inf),ni la diagonal
                RouteM[i][j] = i  # Inicializar la matriz de recorridos con el vértice intermedio
            if i==j:
                RouteM[i][j]=None
    return RouteM


def floyd_warshall(Mat,RouteM): #O(V^3) #mat(previamente preparada) #RouteM(previamente preparada)
    #implemento el algoritmo de FW para ver el camino mas corto entre cualquier par de vertices 
    NumV=len(Mat) #rows
    for k in range(NumV): #be a new n X n matrix
        for i in range(NumV):
            for j in range(NumV):
                if Mat[i][j] > Mat[i][k] + Mat[k][j]: #ecuacion de recurrencia O(1)
                    Mat[i][j] = Mat[i][k] + Mat[k][j] 
                    RouteM[i][j] = RouteM[k][j]  # Act en la matriz de recorridos el vértice intermedio en el camino más corto

    # MAT : nueva matriz con los caminos mas cortos (infinito significa que no hay camino)
    # RouteM : nueva matriz de recorridos usada mas adelante para reconstruir el camino mas corto (None si no hay camnino)
    return Mat, RouteM

def Rebuild_Path(RouteM ,start ,end): #Como parámetro hay que pasarle los vertices-1
    #reconstruye el camino mas corto dado dos vertices y la matriz de recorridos (previamente calculada)

    if RouteM[start][end] is None: #chequeo si no hay camino entre ellas retorno vacio
        return None
    
    path = [end]
    while start != end:
        end = RouteM[start][end] #chequeo el vertice intermedio como start != end significa que hay un vertice en el camino
        path.append(end)
    
    path=path[::-1] #invierto la lista para que empiece desde el inicio-fin
    path2=positionsToVertex(path)
    return path2

def positionsToVertex(ListPositions): 
    #Change the list of positions to vertex names
    with open("serialized_matrix.pickle","rb") as Matfile:
        mapMatrix=pk.load(Matfile)
    ListVertex=[]
    for each in ListPositions:
        ListVertex.append(mapMatrix[0][each+1])#each+1 because first element in mapMatrix[0] is 'V' meaning null
    return ListVertex

def vertexToPosition(vertex1,vertex2):
    #change the vertex to the position of the vertex in the map
    with open("serialized_matrix.pickle","rb") as Matfile:
        mapMatrix=pk.load(Matfile)
    position1=(mapMatrix[0].index(vertex1))-1
    position2=(mapMatrix[0].index(vertex2))-1
    return position1,position2

