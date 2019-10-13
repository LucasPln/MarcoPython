from itertools import chain, combinations
import time
import random

#### Fonctions ####

def toutesLesRepartitions(n):
    listePossibilite = []
    nb2 = n//2
    reste = n - (2 * nb2)

    if(reste == 0):
        queDesDeux = []
        for i in range(nb2):
            queDesDeux.append(2)

        listePossibilite.append(queDesDeux)

    nb2 = nb2 - 1

    while (nb2 >= 0):
        nb3 = 1
        somme = 2*nb2 + 3*nb3

        while (somme <= n):
            if (somme == n):
                possibilite = []

                for i in range(nb3):
                    possibilite.append(3)

                for i in range(nb2):
                    possibilite.append(2)

                listePossibilite.append(possibilite)

            nb3 += 1
            somme = 2*nb2 + 3*nb3

        nb2 = nb2 - 1

    return listePossibilite
    
    

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def afficherGroupesPossibles(listePossibilite, listeEleve, notesAttribuees):
    nbRep = 0
    listeSolutionsAvecNotes = dict()

    for repartition in listePossibilite:
        solution = []
        listeSolutions = []
        uneSolution(repartition, listeEleve, solution, listeSolutions)

        for possibilite in listeSolutions:
            listeSolutionsAvecNotes[str(possibilite)] = notePossibilite(possibilite, listeEleve, notesAttribuees)


        nbRep += len(listeSolutions)
        
    for possibilite, note in listeSolutionsAvecNotes.items():
        print("{}, note de la repartition : {}".format(possibilite, note))

    print(nbRep,"possibilites")

def uneSolution(repartition, listeEleve, solution, listeSolutions):

    if(len(repartition) == 0):
        if(estDoublon(solution,listeSolutions) == False):
            listeSolutions.append(solution)    # Compte le nb de solutions trouvees

    else :
        tailleGroupe = repartition[0]
        allSet = []

        for s in list(powerset(listeEleve)):
            if(len(s) == tailleGroupe):
                allSet.append(s)

        diviseur = 0
        if(tailleGroupe == 2):
            diviseur = repartition.count(tailleGroupe)
        else :
            diviseur = 1

        for k in range(len(allSet)//diviseur):
            possibiliteSet = allSet[k]
            solutionTemp = list(solution)
            solutionTemp.append(possibiliteSet)
            listeTemp = list(listeEleve)
                
            for i in range(tailleGroupe):
                listeTemp.remove(allSet[k][i])

            newRepartition = list(repartition)
            del newRepartition[0]

            uneSolution(newRepartition, listeTemp, solutionTemp, listeSolutions)


def estDoublon(solution, listeSolutions):
	if(len(listeSolutions) == 0):
		return False

	for solutionTest in listeSolutions:

		nb = 0

		i = 0
		while(i < len(solution)):
			trouveCorres = False
			for groupeSolTest in solutionTest:
				if(solution[i] == groupeSolTest):
					nb += 1
					trouveCorres = True

			if(trouveCorres == False):
				break

			i += 1

		if(nb == len(solution)):
			#print(solution,"=",solutionTest)
			return True

	return False

def notePossibilite(possibilite, listeEleve, notesAttribuees):
    medianeGroupe = []
    for groupe in possibilite:
        notesGroupe = []
        for eleve1 in groupe:
            for eleve2 in groupe:
                note = notesAttribuees[listeEleve.index(eleve1)][listeEleve.index(eleve2)]
                if(not note == "-"):
                    notesGroupe.append(note)

        if("AR" in notesGroupe):
            medianeGroupe.append("AR")
        elif("I" in notesGroupe):
            medianeGroupe.append("I")
        elif("P" in notesGroupe):
            medianeGroupe.append("P")
        elif("AB" in notesGroupe):
            medianeGroupe.append("AB")
        elif("B" in notesGroupe):
            medianeGroupe.append("B")
        elif("TB" in notesGroupe):
            medianeGroupe.append("TB")
    
    if("AR" in medianeGroupe):
        return "AR"
    elif("I" in medianeGroupe):
        return "I"
    elif("P" in medianeGroupe):
        return "P"
    elif("AB" in medianeGroupe):
        return "AB"
    elif("B" in medianeGroupe):
        return "B"
    elif("TB" in medianeGroupe):
        return "TB"




#### Programme principale ####

start_time=time.time()

n = int(input("n : "))

repartitionPossibles = toutesLesRepartitions(n)

#for repartition in repartitionPossibles:
#    print(repartition)

listeEleve = []
for i in range(65,n+65):
    listeEleve.append(chr(i))

listeNotes = ["TB", "B", "AB", "P", "I", "AR"]

### Simulation des notes attibuees ###
notesAttribuees = []

for i in range(n):
    notes = []
    for j in range(n):
        if(i == j):
            notes.append("-")
        else :
            notes.append(listeNotes[random.randint(0,len(listeNotes)-1)])
    notesAttribuees.append(notes)

print("### Notes attribuées ###")
print()
for i in notesAttribuees:
    print(i)

print()

afficherGroupesPossibles(repartitionPossibles, listeEleve, notesAttribuees)


print("Temps d execution : %s secondes" % (time.time() - start_time))