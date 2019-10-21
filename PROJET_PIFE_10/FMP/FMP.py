from itertools import chain, combinations
import time
import random
import sys
import csv

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

def afficherMeilleurGroupes(listePossibilite, listeEleve, notesAttribuees):
    nbRep = 0
    listeSolutionsAvecNotes = dict()

    for repartition in listePossibilite:
        solution = []
        listeSolutions = []
        uneSolution(repartition, listeEleve, solution, listeSolutions)

        for possibilite in listeSolutions:
            listeSolutionsAvecNotes[str(possibilite)] = notePossibilite(possibilite, listeEleve, notesAttribuees)


        nbRep += len(listeSolutions)

    meilleurNote = meilleureNoteDesPossibilites(listeSolutionsAvecNotes)

    print("Meilleure note trouvée :",meilleurNote)
    print("Liste des possibilités ayant cette note : ")
    for possibilite, note in listeSolutionsAvecNotes.items():
        if(note == meilleurNote):
            with open('FMP.csv', 'a', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(possibilite)
            print("{}, note de la repartition : {}".format(possibilite, note))

    print()
    print(nbRep,"possibilites au total")

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


def meilleureNoteDesPossibilites(listeSolutionsAvecNotes):
    if("TB" in listeSolutionsAvecNotes.values()):
        return "TB"

    elif("B" in listeSolutionsAvecNotes.values()):
        return "B"

    elif("AB" in listeSolutionsAvecNotes.values()):
        return "AB"

    elif("P" in listeSolutionsAvecNotes.values()):
        return "P"

    elif("I" in listeSolutionsAvecNotes.values()):
        return "I"

    elif("AR" in listeSolutionsAvecNotes.values()):
        return "AR"



#### Programme principale ####

start_time = time.time()
n = int(input("n : "))
"""
ext = ""

nlimit = -1

argument = "reel"

for arg in sys.argv:
    print(arg)
    # Remove the "-" to just keep what is behind
    if arg == "-a" or arg == "--all":
        argument = "exhaustif"
    elif arg == "-r" or arg == "--real":
        argument = "reel"
    elif arg.find("--ext=") != -1:
        ext = arg[6:]
    elif arg.find("--number=") != -1:
        nlimit = int(arg[9:])
"""

repartitionPossibles = toutesLesRepartitions(n)

listeEleve = []

listeNotes = ["TB", "B", "AB", "P", "I", "AR"]

notesAttribuees = []

with open('../DONNEES/preferencesIG4MD.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	i = 0
	while(i <= n):

		row = next(spamreader)
		if(i != 0):
			notes = []
			liste = row[0].split(",")
			for k in range(n+1):
				if(k == 0):
					listeEleve.append("e"+str(i))
				else:
					notes.append(liste[k])
			notesAttribuees.append(notes)
		i += 1

print()
print("### Notes attribuées ###")
for i in notesAttribuees:
    print(i)

print()

afficherMeilleurGroupes(repartitionPossibles, listeEleve, notesAttribuees)


print("Temps d execution : %s secondes" % (time.time() - start_time))
