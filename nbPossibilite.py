def nbRep(n):
    if (n == 0): 
    	return 1
    elif (n == 1):
    	return 0
    elif (n == 2):
    	return 1
    elif (n == 3):
    	return 1

    return (n - 1) * nbRep(n - 2) + (n - 1) * (n - 2) * nbRep(n - 3) / 2

n = int(input("n : "))

print(nbRep(n))