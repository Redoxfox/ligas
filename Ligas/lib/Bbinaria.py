def binaria(vector, numero):
    puntero = 0
    vectorLen = len(vector) - 1
    encontrado = False
    while not (encontrado) and puntero <= vectorLen:
        mitad = int((puntero + vectorLen) / 2)
        if numero == vector[mitad][1]:
            encontrado = True
        elif numero < vector[mitad][1]:
            vectorLen = mitad - 1
        else:
            puntero = mitad + 1
    if (encontrado):
        return mitad
    else:
        return None
