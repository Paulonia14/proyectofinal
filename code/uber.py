from utilities import *
import sys
import pickle as pk


def create_map():
    #Function to open the map and store the content in it
    with open("map.txt","r") as Map: #name the file and close 
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

try:
    with open("FE.pickle","rb") as FE_file:
       F_elements=pk.load(FE_file)
except:
    F_elements={}



try:
    if Largs[1]=="-create_map": #create the map using matrix representation
        Map=create_map()
        #printMat(Map)
        #Serialize the map matrix and store it in a file using pickle
        with open("serialized_matrix.pickle","wb") as Matfile:
            pk.dump(Map,Matfile)
        print("map created successfully")
    elif Largs[1]=="-load_fix_element":
        with open("FE.pickle","wb") as FE_file:
            #verify alredy exits
            if Largs[2] in F_elements:
                print("El elemento ya se encuentra cargado")
                print("desea cambiarlo? 1-Si 0-No")
                Desc=input()
                if Desc=="1":
                    F_elements[Largs[2]]==Largs[2]
                elif Desc=="0":
                    print("oki doki")
                else:
                    print("Not valid")
                    raise # error
            else:
                #convert to a list-tuple
                aux=Largs[3]
                aux="["+ aux + "]"
                aux=aux.replace('e','')
                aux=eval(aux)
                #append to diccionary
                F_elements[Largs[2]] = aux
                pk.dump(F_elements,FE_file)#save the structure
                print("element created successfully")
                print(F_elements)


    elif Largs[1]=="-load_movil_element":
        print("Work in progress")
    elif Largs[1]=="-create_trip":
        try:
            with open("serialized_matrix.pickle","rb") as Matfile:
                mapMatrix=pk.load(Matfile)
                printMat(mapMatrix)
        except:
            print("Map not defined")
    elif Largs[1]=="-close":
        print("have a nice day :)")
    else:
        print("you typed it wrong, try again")
except:
    print("something is wrong, try again") 
        
