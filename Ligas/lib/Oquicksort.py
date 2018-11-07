def quicksort(lista, izq, der, indice):
    i = izq
    j = der
    x = lista[int((izq + der) / 2)][indice]


    while (i <= j):
        while lista[i][indice] < x and j <= der:
            i = i + 1
        while x < lista[j][indice] and j > izq:
            j = j - 1
        if i <= j:
            aux = lista[i]
            lista[i] = lista[j]
            lista[j] = aux
            i = i + 1
            j = j - 1

        if izq < j:
            quicksort(lista, izq, j, indice)
    if i < der:
        quicksort(lista, i, der, indice)

    return lista


def imprimeLista(lista, tam):
    for i in range(0, tam):
        print (lista[i])
        print (lista)


def leeLista():
    lista = []
    cn = int(input("Cantidad de numeros a ingresar: "))

    for i in range(0, cn):
        lista.append(int(input("Ingrese numero %d : " % i)))
    return lista


#A = leeLista()
#A = [[5, 8, 5], [8, 5, 5], [2, 7, 5],[9, 6, 5], [20, 4, 5]]
#l=quicksort(A, 0, len(A) - 1)
#print(l)
#imprimeLista(A, len(A))
