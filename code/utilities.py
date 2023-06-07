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

def Rebuild_Path(RouteM ,start ,end): #Como parámetro hay que pasarle las posc de los vertices
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


def CalculatePrice(path_cost, carPrice): return ((path_cost+carPrice)/4)
    #calcula el monto a pagar por la persona que pide el auto


def Short_Car_Path(DMAT,addressC,personDirection,mapMatrix):
    #calcula la distancia mas corta para un auto
    
    """estan en la misma arista -->>"""

    tuplecar=(addressC[0],addressC[2]) #tomo los valores que interesan para la verif
    tupleperson=(personDirection[0],personDirection[2])


    if (tuplecar[0] in tupleperson) and (tuplecar[1] in tupleperson) : #evaluo si estan tambien el la dir de la persona
        #misma arista/calle
        #Nota: nos interesa mucho mas si la calle es de un sentido concreto ya que si es doble mano 
        #la ubicacion de la persona y el auto no hace muchos problemas

        #determino el sentido de dicha calle/arista ->
        car2dir,theway=thisIsTheWay(mapMatrix,tuplecar)

        initialvertex=theway[0] #unas referencias para evaluar posiciones intermedias

        for i in range(0,len(personDirection)):
            if i==0 or i==2:
                if initialvertex==personDirection[i]:
                    distPers_to_Ivertx=personDirection[i+1]
                if initialvertex==addressC[i]:
                    distCar_to_Ivertx=addressC[i+1]

        #calculo para

        if car2dir==True: #calle dos manos #!!!!!!!!!!!!!!!!
            #calculo de el recorte de los costados
            separateDist=distPers_to_Ivertx-distCar_to_Ivertx
            return abs(separateDist)

        if distPers_to_Ivertx < distCar_to_Ivertx: #el auto NO llega a la persona en la misma arista
            pos1,pos2=vertexToPosition(theway[0],theway[1])
            Distfinal=DMAT[pos2][pos1]
            if Distfinal==INF: #no hay camino posible
                return None
            #calculo para los "pedacitos"
            separateDist=distCar_to_Ivertx-distPers_to_Ivertx
            Distfinal=Distfinal+((mapMatrix[pos1+1][pos2+1])-separateDist)
            return Distfinal
        else:
            pos1,pos2=vertexToPosition(theway[0],theway[1]) #el auto SI llega a la persona en la misma arista

            #calculo para los "pedacitos"
            if distPers_to_Ivertx==distCar_to_Ivertx: #autos en la misma posc
                return 0
            else:
                separateDist=distPers_to_Ivertx-distCar_to_Ivertx
                return separateDist


    """NO estan en la misma arista/calle -->>"""

    car2dir,thewayC=thisIsTheWay(mapMatrix,tuplecar)
    per2dir,thewayP=thisIsTheWay(mapMatrix,tupleperson)
    

    if per2dir==True and car2dir==True: #caso 1 ambas Doble mano
        Ld=[]
        for i in range(0,len(addressC)):
            if i==0 or i==2:
                aux=addressC[i+1]
                for j in range(0,len(personDirection)):
                    result=0
                    if j==0 or j==2:
                        pos1,pos2=vertexToPosition(addressC[i],personDirection[j])
                        D=DMAT[pos1][pos2]
                        if D == INF:
                            Ld.append(INF)
                        else:
                            result=aux+D+personDirection[j+1]
                            Ld.append(result)
        Ld.sort()
        if Ld[0]==INF: #no hay camino posible ya que el menor es inf
            return None
        else:
            return Ld[0]

    if per2dir==True and car2dir==False: #caso 2 solo la persona dos manos
        Ld=[]
        for i in range(0,len(addressC)):
            if (i==0 or i==2) and thewayC[1]==addressC[i]:
                aux=addressC[i+1]
                for j in range(0,len(personDirection)):
                    result=0
                    if j==0 or j==2:
                        pos1,pos2=vertexToPosition(addressC[i],personDirection[j])
                        D=DMAT[pos1][pos2]
                        if D == INF:
                            Ld.append(INF)
                        else:
                            result=aux+D+personDirection[j+1]
                            Ld.append(result)
        Ld.sort()
        if Ld[0]==INF: #no hay camino posible ya que el menor es inf
            return None
        else:
            return Ld[0]

    if per2dir==False and car2dir==True: #caso 3 solo el auto dos manos
        Ld=[]
        for i in range(0,len(addressC)):
            if (i==0 or i==2):
                aux=addressC[i+1]
                for j in range(0,len(personDirection)):
                    result=0
                    if (j==0 or j==2) and thewayP[0]==personDirection[j]:
                        pos1,pos2=vertexToPosition(addressC[i],personDirection[j])
                        D=DMAT[pos1][pos2]
                        if D == INF:
                            Ld.append(INF)
                        else:
                            result=aux+D+personDirection[j+1]
                            Ld.append(result)
        Ld.sort()
        if Ld[0]==INF: #no hay camino posible ya que el menor es inf
            return None
        else:
            return Ld[0]

    if per2dir==False and car2dir==False: #caso 4 ambas una soloa mano
        Ld=[]
        for i in range(0,len(addressC)):
            if (i==0 or i==2) and thewayC[1]==addressC[i]:
                aux=addressC[i+1]
                for j in range(0,len(personDirection)):
                    result=0
                    if (j==0 or j==2) and thewayP[0]==personDirection[j]:
                        pos1,pos2=vertexToPosition(addressC[i],personDirection[j])
                        D=DMAT[pos1][pos2]
                        if D == INF:
                            Ld.append(INF)
                        else:
                            result=aux+D+personDirection[j+1]
                            Ld.append(result)
        Ld.sort()
        if Ld[0]==INF: #no hay camino posible ya que el menor es inf
            return None
        else:
            return Ld[0]



def thisIsTheWay(mapMatrix,tup):
    #ve el sentido de las calles
    pos1,pos2=vertexToPosition(tup[0],tup[1])

    onew=False
    otherw=False

    #este chequeo es necesario ya que las direcciones no necesaramente vienen ordenadas
    if mapMatrix[pos1+1][pos2+1]!=0: 
        theway=(tup[0],tup[1])
        onew=True
    if mapMatrix[pos2+1][pos1+1]!=0:
        theway=(tup[1],tup[0])
        otherw=True

    Tdir=False
    if onew==True and otherw==True: #calle dos manos 
        Tdir=True


    return Tdir,theway


def Short_FinalDestination_Path(DMAT,finalD,InitialD,mapMatrix):
    #retorna el par de vertices de la distancia mas corta hacia la direccion final

    """estan en la misma arista -->>"""
    tupleIn=(InitialD[0],InitialD[2]) #tomo los valores que interesan para la verif
    tupleFin=(finalD[0],finalD[2])
    if (tupleIn[0] in tupleFin) and (tupleIn[1] in tupleFin):
        per2dir,theway=thisIsTheWay(mapMatrix,tupleIn)

        initialvertex=theway[0] #unas referencias para evaluar posiciones intermedias

        for i in range(0,len(finalD)):
            if i==0 or i==2:
                if initialvertex==finalD[i]:
                    distDir_to_Ivertx=finalD[i+1]
                if initialvertex==InitialD[i]:
                    distPers_to_Ivertx=InitialD[i+1]

        #calculo para

        if per2dir==True: #calle dos manos 
            tw1,tw2=vertexToPosition(theway[0],theway[1])
            t=(tw1,tw2)
            return t

        if distPers_to_Ivertx > distDir_to_Ivertx: #la persona NO llega a la direccion en la misma arista
            tw1,tw2=vertexToPosition(theway[0],theway[1])
            t=(tw2,tw1)
            return t
        else:  #la persona Si llega a la direccion en la misma arista
            if distPers_to_Ivertx==distDir_to_Ivertx:
                return 0
            else:
                tw1,tw2=vertexToPosition(theway[0],theway[1])
                t=(tw1,tw2)
                return t

    """NO estan en la misma arista/calle -->>"""

    In2dir,thewayIn=thisIsTheWay(mapMatrix,tupleIn)
    Fin2dir,thewayFin=thisIsTheWay(mapMatrix,tupleFin)
    

    if In2dir==True and Fin2dir==True: #caso 1 ambas Doble mano
        Ld=[]
        hashtemp={}
        pp1,pp2=vertexToPosition(thewayIn[0],thewayIn[1])
        pf1,pf2=vertexToPosition(thewayFin[0],thewayFin[1])
        D1=DMAT[pp1][pf1]
        hashtemp[D1].append((pp1,pf1))
        D2=DMAT[pp1][pf2]
        hashtemp[D2].append((pp1,pf2))
        D3=DMAT[pp2][pf1]
        hashtemp[D3].append((pp2,pf1))
        D4=DMAT[pp2][pf2]
        hashtemp[D4].append((pp2,pf2))
        Ld=hashtemp.keys()
        Ld.sort()
        if Ld[0]==INF: #no hay camino posible ya que el menor es inf
            return None
        else:
            return hashtemp[Ld[0]]

    if In2dir==True and Fin2dir==False: #caso 2 solo el inicio dos manos
        pp1,pp2=vertexToPosition(thewayIn[0],thewayIn[1])
        pf1,pf2=vertexToPosition(thewayFin[0],thewayFin[1])
        D1=DMAT[pp1][pf1]
        D2=DMAT[pp2][pf1]

        if D1==INF and D2==INF:
            return None
        if D1<D2:
            t=(pp1,pf1)
            return t
        else:
            t=(pp2,pf1)
            return t

    if In2dir==False and Fin2dir==True: #caso 3 solo el destino dos manos
        pp1,pp2=vertexToPosition(thewayIn[0],thewayIn[1])
        pf1,pf2=vertexToPosition(thewayFin[0],thewayFin[1])
        D1=DMAT[pp2][pf1]
        D2=DMAT[pp2][pf2]

        if D1==INF and D2==INF:
            return None
        if D1<D2:
            t=(pp2,pf1)
            return t
        else:
            t=(pp2,pf2)
            return t

    if In2dir==False and Fin2dir==False: #caso 4 ambas una soloa mano
        pp2,pf1=vertexToPosition(thewayIn[1],thewayFin[0])
        D1=DMAT[pp2][pf1]
        
        if D1==INF:
            return None
        else:
            t=(pp2,pf1)
            return t


