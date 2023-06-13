from utilities import *
import sys
import pickle as pk


def create_map(file):
    #Function to open the map and store the content in it
    with open(file,"r") as Map: #name the file and close 
        #check if the txt is readble
        print("a")
        if Map.readable() is False:
            return "map not readable"
        
        #vertexs
        aux=(Map.readlines(1))
        aux=aux[0][2:]#cut the string
        aux=aux.replace("{","[")
        aux=aux.replace("}","]")
        aux=aux.replace("e","")
        verts=eval(aux)#convert string to list

        #edges
        aux=(Map.readlines(2))
        aux=aux[0][2:]#cut the string and replace the <>
        aux=aux.replace('>',')')
        aux=aux.replace('<','(')
        aux=aux.replace("{","[")
        aux=aux.replace("}","]")
        aux=aux.replace("e","")

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
        print (file)
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
        #Convert character to uppercase for better management and eliminate '' of parameter
        try:
            element=Largs[2]
            element=element.strip("''")
            element=element.upper()
        except:
            print("element not valid")
            raise
        #Validate element
        Laux=["H","A","T","S","E","K","I"] #All posible elements
        if element[0] not in Laux:
            print("element not valid")
            raise
        #Check if is a correct Adress
        validateAdress(Largs[3])
        try: 
            with open("FE.pickle","rb") as FE_file:
               F_elements=pk.load(FE_file)
        except:
            F_elements={} #if the file is empty it will create a dictionary

        #convert direction to a list
        direction=convertAdress(Largs[3])
        #verify if it already exits
        if element in F_elements:
            flag=False
            while flag==False:
                print("The element is already loaded")
                print("Do you want to change it? (Yes/No)")
                choice=input()
                choice=choice.upper()
                if choice=="YES" or choice=="Y" or choice=="SI":
                    F_elements[element]= direction
                    flag=True
                elif choice=="NO" or choice=="N":
                    flag=True
                    print("oki doki")
                else:
                    print("Option not valid, please try again")
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
                flag=False
                while flag==False:
                    print("The element is already loaded")
                    print("Do you want to change it? (Yes/No)")
                    choice=input()
                    choice=choice.upper()
                    if choice=="YES" or choice=="Y" or choice=="SI":
                        people[element]= direction,Largs[4]
                    elif choice=="NO" or choice=="N":
                        print("oki doki")
                    else:
                        print("Option not valid, please try again")
            else:
                #append new person to dictionary
                people[element] = direction,Largs[4]
            with open("people.pickle","wb") as peopleFile:
                
                pk.dump(people,peopleFile) #save the changes in the file
                print("person placed successfully")
                print(people)

        elif element[0]=="C": #Cars
            try:
                with open("cars.pickle","rb") as carsFile:
                    cars=pk.load(carsFile)
            except:
                cars={} #if the file is empty it will create a dictionary
            #convert direction to a list
            direction=convertAdress(Largs[3])
            #Verify if it already exists
            if element in cars:
                flag=False
                while flag==False: 
                    print("The element is already loaded")
                    print("Do you want to change it? (Yes/No)")
                    choice=input()
                    choice=choice.upper()
                    if choice=="YES" or choice=="Y" or choice=="SI":
                        cars[element]= direction,Largs[4]
                    elif choice=="NO" or choice=="N":
                        print("oki doki")
                    else:
                        print("Option not valid, please try again")
            else:
                #append new car to dictionary
                cars[element] = direction,Largs[4]
            with open("cars.pickle","wb") as carsFile:
                pk.dump(cars,carsFile) #Save the changes in the file
                print("car created successfully")
                print(cars)
        else:
            print("element not valid, it must be 'P' or 'C'")
            raise
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
        #Verify if person is a person indeed
        if person[0]!="P":
            print("You have to introduce a person to have a trip")
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
        elif Largs[3][0] in ["H","A","T","S","E","K","I"] or Largs[3][0] in ["h","a","t","s","e","k","i"]:
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
        else:
            #Not direction nor element
            print("You have to introduce a direction or a valid building")
            raise
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
        ########################################################
        #Calculate distances from every car to the person
        #print(personDirection)
        directionsList=[]
        for car in carsHash:
            S_dist=Short_Car_Path(DistancesMAT,(carsHash[car][0]),personDirection,mapMatrix)
            #print(car,S_dist,carsHash[car][0])
            if S_dist!=None:
                directionsList.append((car,S_dist)) #List with tuples (car name, distance from the car to the person)
        #print(directionsList)
        if len(directionsList)>0:
            directionsList.sort(key=lambda x:x[1]) #Sort the list based on the second element of the tuple (the distances)
            #print(directionsList)
            personMoney=float(people[person][1]) #We get the money the person has now
            #print(personMoney)
            top3=[]
            for i in range(0,len(directionsList)):
                carPrice=carsHash[directionsList[i][0]][1] #We search the price of the car in CarHash (directionsList[i][0] is the car name)
                price=CalculatePrice(directionsList[i][1], float(carPrice)) #directionsList[i][1] is the distance of the car to the person
                if price<=personMoney and len(top3)<3: 
                    top3.append((directionsList[i][0],price))
        else:
            print("There are no cars available to make the trip :(")
            print("We're truly sorry, try it again sometime please!")
            raise
        if len(top3)==0: #Empty list, user can't go anywhere (not enough money)
            print("You don't have enough money to travel, we're sorry :(")
            print("Try it again sometime! Have a nice day :D")
        else:
            ########################################################
            #calculate the shortest path to the finalDirection and print it
            #print(people)
            #print(F_elements)
            pathTup=Short_FinalDestination_Path(DistancesMAT,finalDirection,personDirection,mapMatrix)
            if pathTup==0: #same placement
                print("You and the direction are in the same place")
                raise 
            if pathTup==None: #imposible to go
                print("It is imposible to reach destination")
                raise 

            if len(pathTup)==3:
                print("The shortest path to the adress you provided is --->>>")
                print(pathTup)
            else:
                try:
                    with open("serialized_PATHS.pickle","rb") as Pfile:
                        RouteM=pk.load(Pfile)
                except:
                    print("paths not loaded")

                Path_to_destination=Rebuild_Path(RouteM ,pathTup[0] ,pathTup[1])
                print("The shortest path to the adress you provided is --->>>")
                print(Path_to_destination)

            ########################################################
            #  ---- Interactive Panel ----
            print("These are the cars that can take you to the adress you provided with their respective prices:")
            print(top3)
            flag=False
            while flag==False:
                print("Do you accept the trip? (YES/NO)")
                choice=input()
                choice=choice.upper()
                if choice=="YES" or choice=="Y" or choice=="SI":
                    flag=True
                    if len(top3)==1:
                        choice=1
                        print("There is only one car available to make the trip")
                    else:
                        secondFlag=False
                        while secondFlag==False:
                            print("Please select the car you want")
                            print(top3)
                            print("To select it you have to choice a number between 1 and ",len(top3))
                            choice=input()
                            if int(choice)>0 and int(choice)<=len(top3): #Option must be between those numbers to select a car
                                secondFlag=True
                            else:
                                print("Option not valid, please try again")
                    choice=int(choice)-1
                    personMoney=personMoney - float(top3[choice][1]) #Update person money
                    people[person]=(finalDirection,personMoney) #Move the person to the destination
                    carMoney=carsHash[top3[choice][0]][1] #Save the money of the car(WE DONT CHANGE IT) to save it with the new direction in a tuple
                    carsHash[top3[choice][0]]=(finalDirection,carMoney) #Move the car to the destination
                    #Save the changes in the files of every hash
                    with open("people.pickle","wb") as peopleFile:
                        pk.dump(people,peopleFile)
                    with open("cars.pickle","wb") as carsFile:
                        pk.dump(carsHash,carsFile)

                    print("Thank you for using Uber!")

                elif choice=="NO" or choice=="N":
                    flag=True
                    print("Understandable, is really expensive to travel nowadays, we're unpaid employees")
                    print("Have a nice day :D (Don't go to cabify or we won't eat please)")
                else:
                    print("option not valid, please try again")




except:
    print("something is wrong :( , try again") 


"""Close"""


if Largs[1]=="-close":
    print("have a nice day :)")

if Largs[1] != "-close" and Largs[1] !="-create_trip" and Largs[1] !="-load_fix_element" and Largs[1] !="-load_movil_element" and Largs[1] !="-create_map":
    print("you typed it wrong, try again")


