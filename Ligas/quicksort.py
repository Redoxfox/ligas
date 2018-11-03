def quicksort(lista, izq, der):
    i = izq
    j = der
    x = lista[int((izq + der) / 2)][0]


    while (i <= j):
        while lista[i][0] < x and j <= der:
            i = i + 1
        while x < lista[j][0] and j > izq:
            j = j - 1
        if i <= j:
            aux = lista[i];
            lista[i] = lista[j];
            lista[j] = aux;
            i = i + 1;
            j = j - 1;

        if izq < j:
            quicksort(lista, izq, j);
    if i < der:
        quicksort(lista, i, der);


def imprimeLista(lista, tam):
    for i in range(0, tam):
        print (lista[i])


def leeLista():
    lista = []
    cn = int(input("Cantidad de numeros a ingresar: "))

    for i in range(0, cn):
        lista.append(int(input("Ingrese numero %d : " % i)))
    return lista


#A = leeLista()
A = [[5, 3, 5], [8, 4, 5], [2, 3, 5],[9, 4, 5], [20, 3, 5]]
quicksort(A, 0, len(A) - 1)
imprimeLista(A, len(A))
