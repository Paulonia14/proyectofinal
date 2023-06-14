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
    adress=adress.replace('<','')
    adress=adress.replace('>','')
    adress=adress.replace(' ',',')
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
    #Prepare the table for Floyd-Warshall algorithm
    #Remove borders (Directed Graph)
    matriz.pop(0)
    for each in matriz:
        each.pop(0)
    #fill with infinite and zeros
    for i in range(0,len(matriz)):
        for j in range(0,len(matriz)):
            if matriz[i][j]==0 and i!=j:
                matriz[i][j]=INF
    
    return matriz


def Init_PATHMAT_FloydW(RouteM,Mat):
    #Initialize path matrix for FW
    NumV=len(RouteM)
    for i in range(NumV):
        for j in range(NumV):
            if Mat[i][j] != INF and i != j: #Don't take neither the ones that don't have a path(inf) nor the diagonal
                RouteM[i][j] = i  # Initialize path matrix with middle vertex
            if i==j:
                RouteM[i][j]=None
    return RouteM


def floyd_warshall(Mat,RouteM): #O(V^3) #mat(previously prepared) #RouteM(previously prepared)
    #We implement the Floyd-Warshall algorithm to get the shortest path between every vertex pair
    NumV=len(Mat) #rows
    for k in range(NumV): #be a new n X n matrix
        for i in range(NumV):
            for j in range(NumV):
                if Mat[i][j] > Mat[i][k] + Mat[k][j]: #Recurrence equation O(1)
                    Mat[i][j] = Mat[i][k] + Mat[k][j] 
                    RouteM[i][j] = RouteM[k][j]  #Update middle vertex in the shortest path in path matrix  
    # MAT : new matrix with shortest paths (inifite means that there's no path)
    # RouteM : new route matrix used later for rebuilding the shortest path (None if there's no path)
    return Mat, RouteM

def Rebuild_Path(RouteM ,start ,end): #Use as parameter the positions of vertices
    #Rebuild the shortest path using two vertices and route matrix (previuously calculated)

    if RouteM[start][end] is None: #Check if there is no path between them and return None
        return None
    
    path = [end]
    while start != end:
        end = RouteM[start][end] #Check the middle vertex like start != end meaning that there is a vertex in the way
        path.append(end)
    
    path=path[::-1] #Invert the list for it to start from the beginning to the end
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
    #Calculate the amount to pay for the person if they choose a car


def Short_Car_Path(DMAT,addressC,personDirection,mapMatrix):
    #Calculate the shortest distance for a car (car->person)
    
    """They are in the same edge/street -->>"""

    tuplecar=(addressC[0],addressC[2]) #take values that are useful for verification
    tupleperson=(personDirection[0],personDirection[2])


    if (tuplecar[0] in tupleperson) and (tuplecar[1] in tupleperson) : #Evaluate if they are also in the person direction
        #Same edge/street
        #Note: We are more interested if the street is in a specific direction because if it is a double handed street 
        # the ubication of the person and the car won't make much trouble

        #Determine the direction of said edge/street ->
        car2dir,theway=thisIsTheWay(mapMatrix,tuplecar)

        initialvertex=theway[0] #Some references for evaluating middle positions 

        for i in range(0,len(personDirection)):
            if i==0 or i==2:
                if initialvertex==personDirection[i]:
                    distPers_to_Ivertx=personDirection[i+1]
                if initialvertex==addressC[i]:
                    distCar_to_Ivertx=addressC[i+1]


        if car2dir==True: #calle dos manos #!!!!!!!!!!!!!!!! #Double hand street
            #Calculate the trimming of the sides
            separateDist=distPers_to_Ivertx-distCar_to_Ivertx
            return abs(separateDist)

        if distPers_to_Ivertx < distCar_to_Ivertx: #The car CAN'T go to the person in the same edge (has to go through other streets)
            pos1,pos2=vertexToPosition(theway[0],theway[1])
            Distfinal=DMAT[pos2][pos1]
            if Distfinal==INF: #imposible to reach person
                return None
            #Calculate the "parts" of the street
            separateDist=distCar_to_Ivertx-distPers_to_Ivertx
            Distfinal=Distfinal+((mapMatrix[pos1+1][pos2+1])-separateDist)
            return Distfinal
        else:
            pos1,pos2=vertexToPosition(theway[0],theway[1]) #Car CAN go to the person in the same edge (can go directly in that street)

            #Calculate the "parts" of the street
            if distPers_to_Ivertx==distCar_to_Ivertx: #Car in the same position as the person
                return 0
            else:
                separateDist=distPers_to_Ivertx-distCar_to_Ivertx
                return separateDist


    """They are NOT in the same edge/street -->>""" 

    car2dir,thewayC=thisIsTheWay(mapMatrix,tuplecar)
    per2dir,thewayP=thisIsTheWay(mapMatrix,tupleperson)
    

    if per2dir==True and car2dir==True: #First Case: The two are double handed streets
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
        if Ld[0]==INF: #No posible path because infinite is the smallest
            return None
        else:
            return Ld[0]

    if per2dir==True and car2dir==False: #Second Case: Only person's street is double handed
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
        if Ld[0]==INF: #No posible path because infinite is the smallest
            return None
        else:
            return Ld[0]

    if per2dir==False and car2dir==True: #Third Case: Only car's street is double handed
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
        if Ld[0]==INF: #No posible path because infinite is the smallest
            return None
        else:
            return Ld[0]

    if per2dir==False and car2dir==False: #Fourth Case: Both streets are single handed
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
        if Ld[0]==INF: #No posible path because infinite is the smallest
            return None
        else:
            return Ld[0]



def thisIsTheWay(mapMatrix,tup):
    #Gets the direction of a street
    pos1,pos2=vertexToPosition(tup[0],tup[1])

    onew=False
    otherw=False

    #This checkup is necessary because the directions that the user gives aren't necessarily ordered
    if mapMatrix[pos1+1][pos2+1]!=0: 
        theway=(tup[0],tup[1])
        onew=True
    if mapMatrix[pos2+1][pos1+1]!=0:
        theway=(tup[1],tup[0])
        otherw=True

    Tdir=False
    if onew==True and otherw==True: #Double handed street
        Tdir=True

    return Tdir,theway


def Short_FinalDestination_Path(DMAT,InitialD,finalD,mapMatrix):
    #Returns the vertex pair of the shortest distance to the final direction ((InitialVertex, FinalVertex))
    #This is to get later the path from that initial vertex to the final vertex (using Rebuild_Path() function)

    """They are in the same edge/street -->>"""

    tupleIN=(InitialD[0],InitialD[2]) #take values that are useful for verification
    tupleFIN=(finalD[0],finalD[2])


    if (tupleIN[0] in tupleFIN) and (tupleIN[1] in tupleFIN) :
        #Same edge/street
        #Determine the direction of said edge/street ->
        IN2dir,theway=thisIsTheWay(mapMatrix,tupleIN)

        initialvertex=theway[0] #Some references for evaluating middle positions 

        for i in range(0,len(finalD)):
            if i==0 or i==2:
                if initialvertex==finalD[i]:
                    distDir_to_Ivertx=finalD[i+1]
                if initialvertex==InitialD[i]:
                    distPers_to_Ivertx=InitialD[i+1]

        if IN2dir==True: #Double handed street
            tw1,tw2=vertexToPosition(theway[0],theway[1])
            t=(tw1,tw2)
            return t

        if distPers_to_Ivertx > distDir_to_Ivertx: #The person CAN'T go to the direction in the same edge (has to go through other streets)
            tw1,tw2=vertexToPosition(theway[0],theway[1])
            t=(tw2,tw1)
            return t
        else:  #Person CAN go to the direction in the same edge (can go directly in that street)
            if distPers_to_Ivertx==distDir_to_Ivertx:
                return 0
            else:
                tw1,tw2=vertexToPosition(theway[0],theway[1])
                t=(tw1,tw2)
                return t

    """They are NOT in the same edge/street -->>""" 

    IN2dir,thewayIn=thisIsTheWay(mapMatrix,tupleIN)
    FIN2dir,thewayFin=thisIsTheWay(mapMatrix,tupleFIN)
    VertsHash={}

    if FIN2dir==True and IN2dir==True: #First Case: Both double handed streets
        for i in range(0,len(InitialD)):
            if i==0 or i==2:
                aux=InitialD[i+1]
                for j in range(0,len(finalD)):
                    result=0
                    if j==0 or j==2:
                        auxT=(InitialD[i],finalD[j])
                        pos1,pos2=vertexToPosition(InitialD[i],finalD[j])
                        D=DMAT[pos1][pos2]
                        if D == INF:
                            VertsHash[auxT]=INF
                        else:
                            result=aux+D+finalD[j+1]
                            VertsHash[auxT]=result
        #sort by value
        sorted_dict = dict(sorted(VertsHash.items(), key=lambda x: x[1]))
        first_element = next(iter(sorted_dict.values()))
        if first_element==INF: #No posible path because infinite is the smallest
            return None
        else:
            LkeysT=list(sorted_dict.keys())
            VTup=LkeysT[0]

            if VTup[0]==VTup[1]:
                if thewayIn[0]==VTup[0]:
                    interm=thewayIn[0]
                else:
                    interm=thewayIn[1]

                if thewayIn[0]==interm:
                    first=thewayIn[1]
                else:
                    first=thewayIn[0]

                if thewayFin[0]==interm:
                    last=thewayFin[1]
                else:
                    last=thewayFin[0]

                return [first,interm,last]
            else:
                return VTup

    if FIN2dir==False and IN2dir==True: #Second Case: Only the Initial Street is double handed
        for i in range(0,len(InitialD)):
            if (i==0 or i==2):
                aux=InitialD[i+1]
                for j in range(0,len(finalD)):
                    result=0
                    if (j==0 or j==2) and thewayFin[0]==finalD[j]:
                        auxT=(InitialD[i],finalD[j])
                        pos1,pos2=vertexToPosition(InitialD[i],finalD[j])
                        D=DMAT[pos1][pos2]
                        if D == INF:
                            VertsHash[auxT]=INF
                        else:
                            result=aux+D+finalD[j+1]
                            VertsHash[auxT]=result
        #sort by value
        sorted_dict = dict(sorted(VertsHash.items(), key=lambda x: x[1]))
        first_element = next(iter(sorted_dict.values()))
        if first_element==INF: #No posible path because infinite is the smallest
            return None
        else:
            LkeysT=list(sorted_dict.keys())
            VTup=LkeysT[0]

            if VTup[0]==VTup[1]:
                if thewayIn[0]==thewayFin[0]:
                    return [thewayIn[1],thewayFin[0],thewayFin[1]]
                else:
                    return [thewayIn[0],thewayFin[0],thewayFin[1]]
            else:
                return VTup
    
    if FIN2dir==True and IN2dir==False: #Third Case: Only Final Street is double handed
        for i in range(0,len(InitialD)):
            if (i==0 or i==2) and thewayIn[1]==InitialD[i]:
                aux=InitialD[i+1]
                for j in range(0,len(finalD)):
                    result=0
                    if j==0 or j==2:
                        auxT=(InitialD[i],finalD[j])
                        pos1,pos2=vertexToPosition(InitialD[i],finalD[j])
                        D=DMAT[pos1][pos2]
                        if D == INF:
                            VertsHash[auxT]=INF
                        else:
                            result=aux+D+finalD[j+1]
                            VertsHash[auxT]=result
        #sort by value
        sorted_dict = dict(sorted(VertsHash.items(), key=lambda x: x[1]))
        first_element = next(iter(sorted_dict.values()))
        if first_element==INF: #No posible path because infinite is the smallest
            return None
        else:
            LkeysT=list(sorted_dict.keys())
            VTup=LkeysT[0]

            if VTup[0]==VTup[1]:
                if thewayIn[1]==thewayFin[0]:
                    return [thewayIn[0],thewayIn[1],thewayFin[1]]
                else:
                    return [thewayIn[0],thewayIn[1],thewayFin[0]]
            else:
                return VTup

    if FIN2dir==False and IN2dir==False: #Fourth Case: Both streets are single handed
        for i in range(0,len(InitialD)):
            if (i==0 or i==2) and thewayIn[1]==InitialD[i]:
                aux=InitialD[i+1]
                for j in range(0,len(finalD)):
                    result=0
                    if (j==0 or j==2) and thewayFin[0]==finalD[j]:
                        auxT=(InitialD[i],finalD[j])
                        pos1,pos2=vertexToPosition(InitialD[i],finalD[j])
                        D=DMAT[pos1][pos2]
                        if D == INF:
                            VertsHash[auxT]=INF
                        else:
                            result=aux+D+finalD[j+1]
                            VertsHash[auxT]=result
        #sort by value
        sorted_dict = dict(sorted(VertsHash.items(), key=lambda x: x[1]))
        first_element = next(iter(sorted_dict.values()))
        if first_element==INF: #No posible path because infinite is the smallest
            return None
        else:
            LkeysT=list(sorted_dict.keys())
            VTup=LkeysT[0]
            if VTup[0]==VTup[1]:
                return [thewayIn[0],thewayIn[1],thewayFin[1]]
            else:
                return VTup

