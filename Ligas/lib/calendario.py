def fechas_liga(clubes,nro_fechas,nro_partidos_fecha):
    total_clubes = len(clubes)
    equipos = [ ]
    for i in range(0, nro_fechas):
      creciente = 0
      decreciente = total_clubes - 1
      impar = True if i % 2 != 0 else False
      for indiceP in range(0, nro_partidos_fecha):
         if impar: # seria el partido inicial de cada fecha
            partido = [clubes[creciente], clubes[decreciente]]
            equipos.append(partido)
            creciente += 1
            decreciente -= 1
         else:
             partido = [clubes[decreciente], clubes[creciente]]
             equipos.append(partido)
             creciente += 1
             decreciente -= 1
    return equipos
 #  jornada.append(equipos)

    """for i in range(0,len(equipos)-1):
      equipos[i]
      print(equipos[i])
      print(equipos[i][0])
      print(equipos[i][1])"""


#A = leeLista()
#A = [[5, 8, 5], [8, 5, 5], [2, 7, 5],[9, 6, 5], [20, 4, 5]]
#clubes = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
#l=fechas_liga(clubes,34,9)
#print(l)
#imprimeLista(A, len(A))