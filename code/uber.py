from utilities import *
import sys
import pickle as pk


def create_map(file):
    #Function to open the map and store the content in it
    with open(file,"r") as Map: #name the file and close 
        #check if the txt is readble
        if Map.readable() is False:
            return "map not readable"
        
        #vertexs
        aux=(Map.readlines(1))
        aux=aux[0][2:]#cut the string
        verts=eval(aux)#convert string to list

        #edges
        aux=(Map.readlines(2))
        aux=aux[0][2:]#cut the string and replace the <>
        aux=aux.replace('>',')')
        aux=aux.replace('<','(')
        edges=eval(aux)#convert string to list

    #create the map
    return createDirected_G_Mat_with_edges(verts,edges)

#crate a list with the args
Largs=sys.argv


"""CreateMAP"""

try:
    if Largs[1]=="-create_map": #create the map using matrix representation
        #store path
        file=" ".join(Largs[2:])
        Map=create_map(file)
        #Serialize the map matrix and store it in a file using pickle
        with open("serialized_matrix.pickle","wb") as Matfile:
            pk.dump(Map,Matfile)

        #Calculate the distances so we don't do it later
        Distances=Map #the table

        #Using dynamic programming we calculate the shortest distance for every set of vertex

        Distances=Initial_Mat_for_FloydW(Distances)
        #preparo la matriz de recorridos
        RouteM=Null_Mat(len(Distances)) # mat numv X numv
        RouteM=Init_PATHMAT_FloydW(RouteM,Distances)
        
        #paso final aplicando floyd_warshall en O(V^3) y recibiendo tanto los camninos mas cortos como los recorridos
        Distances,RouteM=floyd_warshall(Distances,RouteM)

        #printMat(Distances)
        #printMat(RouteM)
        
        #position1,position2=vertexToPosition(15,3)
        #Rebuild_Path(RouteM ,position1 ,position2)

        #bloque de guardado en memoria dichas matrices
        with open("serialized_Distances.pickle","wb") as Dfile:
            pk.dump(Distances,Dfile)

        with open("serialized_PATHS.pickle","wb") as Pfile:
            pk.dump(RouteM,Pfile)

        print("map created successfully")
        
except:
    print("something is wrong in -create_map :( , try again")

"""CreateELEMENTS"""

try:
    if Largs[1]=="-load_fix_element":
        validateAdress(Largs[3])
        try: 
            with open("FE.pickle","rb") as FE_file:
               F_elements=pk.load(FE_file)
        except:
            F_elements={} #if the file is empty it will create a dictionary
        #Convert character to uppercase for better management and eliminate '' of parameter
        try:
            element=Largs[2]
            element=element.strip("''")
            element=element.upper()
        except:
            print("element not valid")
            raise
        #convert direction to a list
        direction=convertAdress(Largs[3])
        #verify if it already exits
        if element in F_elements:
            print("The element is already loaded")
            print("Do you want to change it? 1-Yes 0-No")
            choice=input()
            if choice=="1":
                F_elements[element]= direction
            elif choice=="0":
                print("oki doki")
            else:
                print("Not valid")
                raise # error
        else:
            #append new element to dictionary
            F_elements[element] = direction
        with open("FE.pickle","wb") as FE_file:
            pk.dump(F_elements,FE_file) #Save the changes in the file
            print("element created successfully")
            print(F_elements)

    elif Largs[1]=="-load_movil_element":
        #Verify if money is a number
        try:
            float(Largs[4])
        except:
            print("The third parameter is money, it has to be a number")
            raise
        validateAdress(Largs[3])
        #Convert character to uppercase for better management and eliminate '' of parameter
        try:
            element=Largs[2]
            element=element.strip("''")
            element=element.upper()
        except:
            print("element not valid")
            raise
        if element[0]=="P": #People
            try:
                with open("people.pickle","rb") as peopleFile:
                    people=pk.load(peopleFile)
            except:
                people={} #if the file is empty it will create a dictionary

            #convert direction to a list
            direction=convertAdress(Largs[3])
            #Verify if it already exists
            if element in people:
                print("The element is already loaded")
                print("Do you want to change it? 1-Yes 0-No")
                choice=input()
                if choice=="1":
                    people[element]= direction,Largs[4]
                elif choice=="0":
                    print("oki doki")
                else:
                    print("Not valid")
                    raise # error
            else:
                #append new person to dictionary
                people[element] = direction,Largs[4]
            with open("people.pickle","wb") as peopleFile:
                
                pk.dump(people,peopleFile) #save the changes in the file
                print("person placed successfully")
                print(people)

        if element[0]=="C": #Cars
            try:
                with open("cars.pickle","rb") as carsFile:
                    cars=pk.load(carsFile)
            except:
                cars={} #if the file is empty it will create a dictionary
            #convert direction to a list
            direction=convertAdress(Largs[3])
            #Verify if it already exists
            if element in cars:
                print("The element is already loaded")
                print("Do you want to change it? 1-Yes 0-No")
                choice=input()
                if choice=="1":
                    cars[element]= direction,Largs[4]
                elif choice=="0":
                    print("oki doki")
                else:
                    print("Not valid")
                    raise # error
            else:
                #append new car to dictionary
                cars[element] = direction,Largs[4]
            with open("cars.pickle","wb") as carsFile:
                pk.dump(cars,carsFile) #Save the changes in the file
                print("car created successfully")
                print(cars)
except:
    print("something is wrong in the creation :( , try again") 

"""CreateTRIP"""  

try:
    if Largs[1]=="-create_trip":
        try:
            with open("serialized_matrix.pickle","rb") as Matfile:
                mapMatrix=pk.load(Matfile)
                #printMat(mapMatrix)
        except:
            print("Map not defined")
        #Convert person to uppercase for better management and eliminate '' of parameter
        try:
            person=Largs[2]
            person=person.strip("''")
            person=person.upper()
        except:
            print("person not valid")
            raise
        #Verify if person exists
        try:
            with open("people.pickle","rb") as peopleFile:
                people=pk.load(peopleFile)
        except:
            print("You have to create a person first")
            raise
        peopleKeys=people.keys()
        if person not in peopleKeys:
            print("Person doesn't exists")
            raise
        #Verify if Largs[3] is element or direction
        if "," in Largs[3]:
            #is direction
            validateAdress(Largs[3])
            finalDirection=convertAdress(Largs[3])
        else:
            #is element
            #Convert element to uppercase for better management and eliminate '' of parameter
            try:
                element=Largs[3]
                element=element.strip("''")
                element=element.upper()
            except:
                print("element not valid")
                raise
            try:
                with open("FE.pickle","rb") as FE_file:
                    F_elements=pk.load(FE_file)
            except:
                print("You don't have any elements")
                raise
            #Check if element exists
            FelementsKeys=F_elements.keys()
            if element not in FelementsKeys:
                print("That element is not in the map")
                raise
            finalDirection=F_elements.get(element)

        #Get direction of person
        personDirection=(people.get(person))[0]

        try:
            with open("serialized_Distances.pickle","rb") as Dfile:
                DistancesMAT=pk.load(Dfile)
        except:
            print("not load before something")

        try:
            with open("cars.pickle","rb") as carsFile:
                carsHash=pk.load(carsFile)
        except:
            print("not load before something")

        #bloque para calcular las distancias a los autos
        print(personDirection)
        for car in carsHash:
            S_dist=Short_Car_Path(DistancesMAT,(carsHash[car][0]),personDirection,mapMatrix)
            print(car,S_dist,carsHash[car][0])


except:
    print("something is wrong :( , try again") 


"""Close"""

if Largs[1]=="-close":
    print("have a nice day :)")

if Largs[1] != "-close" and Largs[1] !="-create_trip" and Largs[1] !="-load_fix_element" and Largs[1] !="-load_movil_element" and Largs[1] !="-create_map":
    print("you typed it wrong, try again")


