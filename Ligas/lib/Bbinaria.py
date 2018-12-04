def binaria(vector, numero, indice):
    puntero = 0
    vectorLen = len(vector) - 1
    encontrado = False
    while not (encontrado) and puntero <= vectorLen:
        mitad = int((puntero + vectorLen) / 2)
        if numero == vector[mitad][indice]:
            encontrado = True
        elif numero < vector[mitad][indice]:
            vectorLen = mitad - 1
        else:
            puntero = mitad + 1
    if (encontrado):
        return mitad
    else:
        return None
