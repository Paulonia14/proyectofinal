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

        #calculamos de entarda las distancias para no hacerlo mas tarde
        Distances=Map #the table
        #usando programacion dinamica calculamos la dist mas corta a cada par de vertices
        Distances=Initial_Mat_for_FloydW(Distances)
        Distances=floyd_warshall(Distances)

        printMat(Distances)

        with open("serialized_Distances.pickle","wb") as Dfile:
            pk.dump(Distances,Dfile)

        print("map created successfully")
        
except:
    print("something is wrong in -create_map :( , try again")

"""CreateELEMENTS"""

try:
    if Largs[1]=="-load_fix_element":
        print(Largs[3])
        #validar!
        validateAdress(Largs[3])
        try: 
            with open("FE.pickle","rb") as FE_file:
               F_elements=pk.load(FE_file)
        except:
            F_elements={} #if the file is empty it will create a dictionary

        #convert direction to a list-tuple
        aux=Largs[3]
        aux="["+ aux + "]"
        aux=aux.replace('e','')
        aux=eval(aux)
        #verify if it already exits
        if Largs[2] in F_elements:
            print("The element is already loaded")
            print("Do you want to change it? 1-Yes 0-No")
            choice=input()
            if choice=="1":
                F_elements[Largs[2]]= aux
            elif choice=="0":
                print("oki doki")
            else:
                print("Not valid")
                raise # error
        else:
            #append new element to dictionary
            F_elements[Largs[2]] = aux
        with open("FE.pickle","wb") as FE_file:
            pk.dump(F_elements,FE_file) #Save the changes in the file
            print("element created successfully")
            print(F_elements)

    elif Largs[1]=="-load_movil_element":
        validateAdress(Largs[3])
        if Largs[2][0]=="P" or Largs[2][0]=="p": #People
            try:
                with open("people.pickle","rb") as peopleFile:
                    people=pk.load(peopleFile)
            except:
                people={} #if the file is empty it will create a dictionary

            #convert direction to a list-tuple
            aux=Largs[3]
            aux="["+ aux + "]"
            aux=aux.replace('e','')
            aux=eval(aux)
            #Verify if it already exists
            if Largs[2] in people:
                print("The element is already loaded")
                print("Do you want to change it? 1-Yes 0-No")
                choice=input()
                if choice=="1":
                    people[Largs[2]]= aux,Largs[4]
                elif choice=="0":
                    print("oki doki")
                else:
                    print("Not valid")
                    raise # error
            else:
                #append new person to dictionary
                people[Largs[2]] = aux,Largs[4]
            with open("people.pickle","wb") as peopleFile:
                
                pk.dump(people,peopleFile) #save the changes in the file
                print("person placed successfully")
                print(people)

        if Largs[2][0]=="C" or Largs[2][0]=="c": #Cars
            try:
                with open("cars.pickle","rb") as carsFile:
                    cars=pk.load(carsFile)
            except:
                cars={} #if the file is empty it will create a dictionary
            #convert direction to a list-tuple
            aux=Largs[3]
            aux="["+ aux + "]"
            aux=aux.replace('e','')
            aux=eval(aux)
            #Verify if it already exists
            if Largs[2] in cars:
                print("The element is already loaded")
                print("Do you want to change it? 1-Yes 0-No")
                choice=input()
                if choice=="1":
                    cars[Largs[2]]= aux,Largs[4]
                elif choice=="0":
                    print("oki doki")
                else:
                    print("Not valid")
                    raise # error
            else:
                #append new car to dictionary
                cars[Largs[2]] = aux,Largs[4]
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
                printMat(mapMatrix)
        except:
            print("Map not defined")
except:
    print("something is wrong :( , try again") 


"""Close"""

if Largs[1]=="-close":
    print("have a nice day :)")

if Largs[1] != "-close" and Largs[1] !="-create_trip" and Largs[1] !="-load_fix_element" and Largs[1] !="-load_movil_element" and Largs[1] !="-create_map":
    print("you typed it wrong, try again")