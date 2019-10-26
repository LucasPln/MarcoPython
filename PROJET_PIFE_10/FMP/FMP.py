from itertools import chain, combinations
from collections import OrderedDict
from functools import reduce
import time
import random
import sys
import csv
import os

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

    listeSolutionsAvecNotes = dict()
    dictResultat = dict()
    for repartition in listePossibilite:
        solution = []
        listeSolutions = []
        uneSolution(repartition, listeEleve, solution, listeSolutions)
        # mettre toutes les possibilites dans un dictionnaire avec la cle unique pour chaque enumeration
        for possibilite in listeSolutions:
            dictResultat[','.join(map(str, sorted(list(map(lambda x: reduce(
                (lambda y, z: int(y) + (int(z) ** 3.23)), x), possibilite)))))] = possibilite
            # trouver les solutions avec notes
            listeSolutionsAvecNotes[str(possibilite)] = notePossibilite(
                possibilite, listeEleve, notesAttribuees)

    meilleurNote = meilleureNoteDesPossibilites(listeSolutionsAvecNotes)

    if os.path.exists('FMP.csv'):
        os.remove('FMP.csv')
    f = open("FMP.csv", "w", newline='')
    writer = csv.DictWriter(
        f, fieldnames=[''])
    for possibilite, note in listeSolutionsAvecNotes.items():
        if (note == meilleurNote):
            # mettre les numeros etudiants
            tabPos = eval(possibilite.split('~')[0])
            pos = list(
                map(lambda y: tuple(map(lambda z: TAB_ETUDIANTS[int(z)], y)), tabPos))
            writer.writerow({'': pos})
    f.close()


def uneSolution(repartition, listeEleve, solution, listeSolutions):

    if(len(repartition) == 0):

        listeSolutions.append(solution)    # Compte le nb de solutions trouvees
    else:
        tailleGroupe = repartition[0]
        allSet = []

        for s in list(powerset(listeEleve)):
            if(len(s) == tailleGroupe):
                allSet.append(s)

        diviseur = 0
        if(tailleGroupe == 2):
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

            uneSolution(newRepartition, listeTemp,
                        solutionTemp, listeSolutions)


def notePossibilite(possibilite, listeEleve, notesAttribuees):
    medianeGroupe = []
    for groupe in possibilite:
        notesGroupe = []
        for eleve1 in groupe:
            for eleve2 in groupe:
                note = notesAttribuees[listeEleve.index(
                    eleve1)][listeEleve.index(eleve2)]
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

listeEleve = []

listeNotes = ["TB", "B", "AB", "P", "I", "AR"]

notesAttribuees = []

TAB_ETUDIANTS = []

with open('../DONNEES/preferencesIG4MD.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    i = 0
    row = next(spamreader)
    TAB_ETUDIANTS = row[0].split(",")
    n = (len(row[0].split(",")) - 1)

    if (n > 10):
        n = 10
        
    repartitionPossibles = toutesLesRepartitions(n)
    while(i <= n):
        if (i != 0):
            row = next(spamreader)
            notes = []
            liste = row[0].split(",")
            for k in range(n + 1):
                if (k == 0):
                    listeEleve.append(str(i))
                else:
                    notes.append(liste[k])
            notesAttribuees.append(notes)
        i += 1

afficherMeilleurGroupes(repartitionPossibles, listeEleve, notesAttribuees)