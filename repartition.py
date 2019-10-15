from itertools import chain, combinations
import time
import random

#### Fonctions ####

def toutesLesRepartitions(n):
    listeRepartition = []
    nb2 = n//2
    reste = n - (2 * nb2)

    if(reste == 0):
        queDesDeux = []
        for i in range(nb2):
            queDesDeux.append(2)

        listeRepartition.append(queDesDeux)

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

                listeRepartition.append(possibilite)

            nb3 += 1
            somme = 2*nb2 + 3*nb3

        nb2 = nb2 - 1

    return listeRepartition
    
    

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def afficherMeilleurGroupes(listeRepartition, listeEleve):
    nbRep = 0
    listeSolutionsAvecNotes = dict()

    for repartition in listeRepartition:
        solution = []
        listeSolutions = []
        uneSolution(repartition, listeEleve, solution, listeSolutions)

        for repartition in listeSolutions:
            print(repartition)

        nbRep += len(listeSolutions)

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
            if(repartition.count(2) == 0):
                diviseur = repartition.count(tailleGroupe)
            else:
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



#### Programme principale ####

start_time=time.time()

n = int(input("n : "))

repartitionPossibles = toutesLesRepartitions(n)

#for repartition in repartitionPossibles:
#    print(repartition)

listeEleve = []
for i in range(65,n+65):
    listeEleve.append(chr(i))



afficherMeilleurGroupes(repartitionPossibles, listeEleve)


print("Temps d execution : %s secondes" % (time.time() - start_time))