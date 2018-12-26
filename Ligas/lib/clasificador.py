def clasificar(liga, id_eq1, id_eq2):
    import decimal
    import pymysql.cursors
    from Bbinaria import binaria
    from Oquicksort import quicksort
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='perfume',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    resultado = {}
    resultado1 = {}
    cursor = connection.cursor()
    # Read a single record
    url = "http://localhost:8000/actualizar/" + str(id) + "/" + str(liga) + "/"

    sql1 = "SELECT nombre FROM equipos WHERE id= %s "
    cursor.execute(sql1, (id_eq1))
    nom_eq1 = cursor.fetchall()

    sql2 = "SELECT nombre FROM equipos WHERE id= %s "
    cursor.execute(sql2, (id_eq2))
    nom_eq2 = cursor.fetchall()

    sql3 = "select nro_fecha, equipo_1, equipo_2, gol_eq1, gol_eq2 from calendario where id_liga= %s and estado='JUGADO';"
    cursor.execute(sql3, (liga))
    goles_liga = cursor.fetchall()
    id_e1 = int(id_eq1)
    id_e2 = int(id_eq2)
    historial = []
    cuota_local = []
    cuota_visitante = []
    p_derrota = []
    p_empate = []
    p_victoria = []
    derrota = []
    empate = []
    victoria = []
    empate_eq1_local = 0
    victoria_eq1_local = 0
    derrota_eq1_local = 0
    empate_eq1_visitante = 0
    victoria_eq1_visitante = 0
    derrota_eq1_visitante = 0
    empate_eq2 = 0
    victoria_eq2 = 0
    derrota_eq2 = 0
    empate_eq2_local = 0
    victoria_eq2_local = 0
    derrota_eq2_local = 0
    empate_eq2_visitante = 0
    victoria_eq2_visitante = 0
    derrota_eq2_visitante = 0

    for rows in goles_liga:
        gol_eq1 = int(rows["gol_eq1"])
        gol_eq2 = int(rows["gol_eq2"])
        equipo_1 = int(rows["equipo_1"])
        equipo_2 = int(rows["equipo_2"])
        nro_equipos = len(historial)
        empate_eq1 = 0
        victoria_eq1 = 0
        derrota_eq1 = 0
        empate_eq2 = 0
        victoria_eq2 = 0
        derrota_eq2 = 0
        Goles_favoreq1 = 0
        Goles_favoreq2 = 0
        Goles_contraeq1 = 0
        Goles_contraeq2 = 0
        puntos_eq1 = 0
        puntos_eq2 = 0

        if gol_eq1 == gol_eq2:
            victoria_eq1 += 0
            derrota_eq1 += 0
            empate_eq1 += 1
            victoria_eq2 += 0
            derrota_eq2 += 0
            empate_eq2 += 1
            Goles_favoreq1 += gol_eq1
            Goles_favoreq2 += gol_eq2
            Goles_contraeq1 += gol_eq2
            Goles_contraeq2 += gol_eq1
            puntos_eq1 += 1
            puntos_eq2 += 1
            if id_e1 == equipo_1:
                empate_eq1_local += 1

            if id_e2 == equipo_2:
                empate_eq2_visitante += 1

            if id_e2 == equipo_1:
                empate_eq2_local += 1

            if id_e1 == equipo_2:
                empate_eq1_visitante += 1

        if gol_eq1 > gol_eq2:
            victoria_eq1 += 1
            derrota_eq1 += 0
            empate_eq1 += 0
            victoria_eq2 += 0
            derrota_eq2 += 1
            empate_eq2 += 0
            Goles_favoreq1 += gol_eq1
            Goles_favoreq2 += gol_eq2
            Goles_contraeq1 += gol_eq2
            Goles_contraeq2 += gol_eq1
            puntos_eq1 += 3
            puntos_eq2 += 0
            if id_e1 == equipo_1:
                victoria_eq1_local += 1

            if id_e2 == equipo_2:
                derrota_eq2_visitante += 1

            if id_e2 == equipo_1:
                derrota_eq2_local += 1

            if id_e1 == equipo_2:
                victoria_eq1_visitante += 1

        if gol_eq1 < gol_eq2:
            victoria_eq1 += 0
            derrota_eq1 += 1
            empate_eq1 += 0
            victoria_eq2 += 1
            derrota_eq2 += 0
            empate_eq2 += 0
            Goles_favoreq1 += gol_eq1
            Goles_favoreq2 += gol_eq2
            Goles_contraeq1 += gol_eq2
            Goles_contraeq2 += gol_eq1
            puntos_eq1 += 0
            puntos_eq2 += 3
            if id_e1 == equipo_1:
                derrota_eq1_local += 1

            if id_e2 == equipo_2:
                victoria_eq2_visitante += 1

            if id_e2 == equipo_1:
                victoria_eq2_local += 1

            if id_e1 == equipo_2:
                derrota_eq1_visitante += 1

        if nro_equipos == 0:
            POS = len(historial) + 1
            Nre_E = int(equipo_1)
            PJ = 1
            GF = Goles_favoreq1
            GC = Goles_contraeq1
            GD = Goles_favoreq1 - Goles_contraeq1
            PG = victoria_eq1
            PP = derrota_eq1
            PE = empate_eq1
            PTOS = puntos_eq1
            historial.append([POS, Nre_E, PJ, GF, GC, GD, PG, PP, PE, PTOS])
            POS = len(historial)
            Nre_E = int(equipo_2)
            PJ = 1
            GF = Goles_favoreq2
            GC = Goles_contraeq2
            GD = Goles_favoreq2 - Goles_contraeq2
            PG = victoria_eq2
            PP = derrota_eq2
            PE = empate_eq2
            PTOS = puntos_eq2

            historial.append([POS, Nre_E, PJ, GF, GC, GD, PG, PP, PE, PTOS])
            # print(historial)
        else:
            derecha = len(historial) - 1
            ordenadoM = quicksort(historial, 0, derecha, 1)
            datos1 = binaria(ordenadoM, int(equipo_1), 1)
            datos2 = binaria(ordenadoM, int(equipo_2), 1)
            Nre_E = int(equipo_1)
            GF = Goles_favoreq1
            GC = Goles_contraeq1
            GD = Goles_favoreq1 - Goles_contraeq1
            PG = victoria_eq1
            PP = derrota_eq1
            PE = empate_eq1
            PTOS = puntos_eq1
            Nre_E2 = int(equipo_2)
            GF2 = Goles_favoreq2
            GC2 = Goles_contraeq2
            GD2 = Goles_favoreq2 - Goles_contraeq2
            PG2 = victoria_eq2
            PP2 = derrota_eq2
            PE2 = empate_eq2
            PTOS2 = puntos_eq2
            if datos1 != None:
                ordenadoM[datos1][0] = datos1 + 1
                ordenadoM[datos1][1] = Nre_E
                ordenadoM[datos1][3] = ordenadoM[datos1][3] + GF
                ordenadoM[datos1][4] = ordenadoM[datos1][4] + GC
                ordenadoM[datos1][5] = ordenadoM[datos1][5] + GD
                ordenadoM[datos1][6] = ordenadoM[datos1][6] + PG
                ordenadoM[datos1][7] = ordenadoM[datos1][7] + PP
                ordenadoM[datos1][8] = ordenadoM[datos1][8] + PE
                ordenadoM[datos1][2] = ordenadoM[datos1][6] + ordenadoM[datos1][7] + ordenadoM[datos1][8]
                ordenadoM[datos1][9] = ordenadoM[datos1][9] + PTOS
            if datos2 != None:
                ordenadoM[datos2][0] = datos2 + 1
                ordenadoM[datos2][1] = Nre_E2
                ordenadoM[datos2][2] = ordenadoM[datos2][2] + 1
                ordenadoM[datos2][3] = ordenadoM[datos2][3] + GF2
                ordenadoM[datos2][4] = ordenadoM[datos2][4] + GC2
                ordenadoM[datos2][5] = ordenadoM[datos2][5] + GD2
                ordenadoM[datos2][6] = ordenadoM[datos2][6] + PG2
                ordenadoM[datos2][7] = ordenadoM[datos2][7] + PP2
                ordenadoM[datos2][8] = ordenadoM[datos2][8] + PE2
                ordenadoM[datos2][9] = ordenadoM[datos2][9] + PTOS2
            if datos1 == None:
                POS = len(historial) + 1
                Nre_E = int(equipo_1)
                PJ = 1
                GF = Goles_favoreq1
                GC = Goles_contraeq1
                GD = Goles_favoreq1 - Goles_contraeq1
                PG = victoria_eq1
                PP = derrota_eq1
                PE = empate_eq1
                PTOS = puntos_eq1
                historial.append([POS, Nre_E, PJ, GF, GC, GD, PG, PP, PE, PTOS])
            if datos2 == None:
                POS = len(historial)
                Nre_E = int(equipo_2)
                PJ = 1
                GF = Goles_favoreq2
                GC = Goles_contraeq2
                GD = Goles_favoreq2 - Goles_contraeq2
                PG = victoria_eq2
                PP = derrota_eq2
                PE = empate_eq2
                PTOS = puntos_eq2
                historial.append([POS, Nre_E, PJ, GF, GC, GD, PG, PP, PE, PTOS])

    resultado[0] = (0, 0, id, url, liga)

    ordenadoM = quicksort(historial, 0, len(historial) - 1, 9)
    pos_eq1 = 0
    pos_eq2 = 0
    cont = 0
    for i in range(len(ordenadoM)):
        indice = len(ordenadoM) - 1 - i
        idclud = ordenadoM[indice][1]
        sql1 = "SELECT nombre FROM equipos WHERE id= %s "
        cursor.execute(sql1, (idclud))
        nom_clud = cursor.fetchall()
        cont = cont + 1
        pos = i + 1
        clud = nom_clud[0]
        # clud = ordenadoM[indice][1]
        pj = ordenadoM[indice][2]
        gf = ordenadoM[indice][3]
        gc = ordenadoM[indice][4]
        dg = ordenadoM[indice][5]
        pg = ordenadoM[indice][6]
        pp = ordenadoM[indice][7]
        pe = ordenadoM[indice][8]
        ptos = ordenadoM[indice][9]
        # datos = binaria(ordenadoM, int(pos2))
        resultado1[i] = (pos, clud, pj, gf, gc, dg, pg, pp, pe, ptos)
        if idclud == id_e1:
            pos_eq1 = indice
        if idclud == id_e2:
            pos_eq2 = indice

        #print(pos_eq1)
        #print(pos_eq2)
        division = decimal.Decimal(72) / decimal.Decimal(7)
       # print(division)

    P_GJEQ1 = decimal.Decimal(ordenadoM[pos_eq1][6]) / decimal.Decimal(ordenadoM[pos_eq1][2])
    P_GJLEQ1 = decimal.Decimal(victoria_eq1_local) / decimal.Decimal((derrota_eq1_local + empate_eq1_local + victoria_eq1_local))
    P_GJVEQ1 = decimal.Decimal(victoria_eq1_visitante) / decimal.Decimal((derrota_eq1_visitante + empate_eq1_visitante + victoria_eq1_visitante))
    P_PJEQ1 = decimal.Decimal(ordenadoM[pos_eq1][7]) / decimal.Decimal(ordenadoM[pos_eq1][2])
    P_PJLEQ1 = decimal.Decimal(derrota_eq1_local) / decimal.Decimal((derrota_eq1_local + empate_eq1_local + victoria_eq1_local))
    P_PJVEQ1 = decimal.Decimal(derrota_eq1_visitante) / decimal.Decimal((derrota_eq1_visitante + empate_eq1_visitante + victoria_eq1_visitante))
    P_EJEQ1 = decimal.Decimal(ordenadoM[pos_eq1][8]) / decimal.Decimal(ordenadoM[pos_eq1][2])
    P_EJLEQ1 = decimal.Decimal(empate_eq1_local) / decimal.Decimal((derrota_eq1_local + empate_eq1_local + victoria_eq1_local))
    P_EJVEQ1 = decimal.Decimal(empate_eq1_visitante )/ decimal.Decimal((derrota_eq1_visitante + empate_eq1_visitante + victoria_eq1_visitante))

    P_GJEQ2 = decimal.Decimal(ordenadoM[pos_eq2][6]) / decimal.Decimal(ordenadoM[pos_eq2][2])
    P_GJLEQ2 = decimal.Decimal(victoria_eq2_local) / decimal.Decimal((derrota_eq2_local + empate_eq2_local + victoria_eq2_local))
    P_GJVEQ2 = decimal.Decimal(victoria_eq2_visitante) / decimal.Decimal((derrota_eq2_visitante + empate_eq2_visitante + victoria_eq2_visitante))
    P_PJEQ2 = decimal.Decimal(ordenadoM[pos_eq2][7]) / decimal.Decimal(ordenadoM[pos_eq2][2])
    P_PJLEQ2 = decimal.Decimal(derrota_eq2_local) / decimal.Decimal((derrota_eq2_local + empate_eq2_local + victoria_eq2_local))
    P_PJVEQ2 = decimal.Decimal(derrota_eq2_visitante) / decimal.Decimal((derrota_eq2_visitante + empate_eq2_visitante + victoria_eq2_visitante))
    P_EJEQ2 = decimal.Decimal(ordenadoM[pos_eq2][8]) / decimal.Decimal(ordenadoM[pos_eq2][2])
    P_EJLEQ2 = decimal.Decimal(empate_eq2_local) / decimal.Decimal((derrota_eq2_local + empate_eq2_local + victoria_eq2_local))
    P_EJVEQ2 = decimal.Decimal(empate_eq2_visitante) / decimal.Decimal((derrota_eq2_visitante + empate_eq2_visitante + victoria_eq2_visitante))

    p_derrota.append(P_PJEQ1)
    p_derrota.append(P_PJLEQ1)
    p_derrota.append(P_PJVEQ1)
    p_derrota.append(P_PJEQ2)
    p_derrota.append(P_PJLEQ2)
    p_derrota.append(P_PJVEQ2)
    p_empate.append(P_EJEQ1)
    p_empate.append(P_EJLEQ1)
    p_empate.append(P_EJVEQ1)
    p_empate.append(P_EJEQ2)
    p_empate.append(P_EJLEQ2)
    p_empate.append(P_EJVEQ2)
    p_victoria.append(P_GJEQ1)
    p_victoria.append(P_GJLEQ1)
    p_victoria.append(P_GJVEQ1)
    p_victoria.append(P_GJEQ2)
    p_victoria.append(P_GJLEQ2)
    p_victoria.append(P_GJVEQ2)

    derrota.append(ordenadoM[pos_eq1][7])
    derrota.append(ordenadoM[pos_eq2][7])
    derrota.append(derrota_eq1_local)
    derrota.append(derrota_eq1_visitante)
    derrota.append(derrota_eq2_local)
    derrota.append(derrota_eq2_visitante)
    empate.append(ordenadoM[pos_eq1][8])
    empate.append(ordenadoM[pos_eq2][8])
    empate.append(empate_eq1_local)
    empate.append(empate_eq1_visitante)
    empate.append(empate_eq2_local)
    empate.append(empate_eq2_visitante)
    victoria.append(ordenadoM[pos_eq1][6])
    victoria.append(ordenadoM[pos_eq2][6])
    victoria.append(victoria_eq1_local)
    victoria.append(victoria_eq1_visitante)
    victoria.append(victoria_eq2_local)
    victoria.append(victoria_eq2_visitante)

    p_victoria_local = (P_GJEQ1 * P_GJLEQ1) / (P_GJEQ1 * P_GJLEQ1 + P_PJEQ1 * P_PJLEQ1 + P_EJEQ1 * P_EJLEQ1)
    p_derrota_local = (P_PJEQ1 * P_PJLEQ1) / (P_GJEQ1 * P_GJLEQ1 + P_PJEQ1 * P_PJLEQ1 + P_EJEQ1 * P_EJLEQ1)
    p_empate_local = (P_EJEQ1 * P_EJLEQ1) / (P_GJEQ1 * P_GJLEQ1 + P_PJEQ1 * P_PJLEQ1 + P_EJEQ1 * P_EJLEQ1)
    p_victoria_visitante = (P_GJEQ2 * P_GJVEQ2) / (P_GJEQ2 * P_GJVEQ2 + P_PJEQ2 * P_PJVEQ2 + P_EJEQ2 * P_EJVEQ2)
    p_derrota_visitante = (P_PJEQ2 * P_PJVEQ2) / (P_GJEQ2 * P_GJVEQ2 + P_PJEQ2 * P_PJVEQ2 + P_EJEQ2 * P_EJVEQ2)
    p_empate_visitante = (P_EJEQ2 * P_EJVEQ2) / (P_GJEQ2 * P_GJVEQ2 + P_PJEQ2 * P_PJVEQ2 + P_EJEQ2 * P_EJVEQ2)

    if p_victoria_local > 0:
        p_victoria_local = 1 / p_victoria_local
    else:
        p_victoria_local = 100

    if p_derrota_local > 0:
        p_derrota_local = 1 / p_derrota_local
    else:
        p_derrota_local = 100

    if p_empate_local > 0:
        p_empate_local = 1 / p_empate_local
    else:
        p_empate_local = 100

    if p_victoria_visitante > 0:
        p_victoria_visitante = 1 / p_victoria_visitante
    else:
        p_victoria_visitante = 100

    if p_derrota_visitante > 0:
        p_derrota_visitante = 1 / p_derrota_visitante
    else:
        p_derrota_visitante = 100

    if p_empate_visitante > 0:
        p_empate_visitante = 1 / p_empate_visitante
    else:
        p_empate_visitante = 100

    cuota_local.append(p_victoria_local)
    cuota_local.append(p_derrota_local)
    cuota_local.append(p_empate_local)
    cuota_local.append(p_victoria_visitante)
    cuota_local.append(p_derrota_visitante)
    cuota_local.append(p_empate_visitante)
    Equipo_ganador = 0

    if p_victoria_local < p_victoria_visitante:
        Equipo_ganador = id_e1
    else:
        Equipo_ganador = id_e2

    return  Equipo_ganador


def porcentaje_acierto(liga):
    import decimal
    import pymysql.cursors
    from Bbinaria import binaria
    from Oquicksort import quicksort
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='perfume',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    resultado = {}
    resultado1 = {}
    cursor = connection.cursor()
    # Read a single record
    url = "http://localhost:8000/actualizar/" + str(id) + "/" + str(liga) + "/"

    sql3 = "select nro_fecha, equipo_1, equipo_2, gol_eq1, gol_eq2 from calendario where id_liga= %s and estado='JUGADO';"
    cursor.execute(sql3, (liga))
    goles_liga = cursor.fetchall()

    historial = []
    cuota_local = []
    cuota_visitante = []
    p_derrota = []
    p_empate = []
    p_victoria = []
    derrota = []
    empate = []
    victoria = []
    empate_eq1_local = 0
    victoria_eq1_local = 0
    derrota_eq1_local = 0
    empate_eq1_visitante = 0
    victoria_eq1_visitante = 0
    derrota_eq1_visitante = 0
    empate_eq2 = 0
    victoria_eq2 = 0
    derrota_eq2 = 0
    empate_eq2_local = 0
    victoria_eq2_local = 0
    derrota_eq2_local = 0
    empate_eq2_visitante = 0
    victoria_eq2_visitante = 0
    derrota_eq2_visitante = 0
    nro_partido = 0
    Aciertos = 0
    Desaciertos = 0
    Porcentaje = 0
    for rows in goles_liga:
        gol_eq1 = int(rows["gol_eq1"])
        gol_eq2 = int(rows["gol_eq2"])
        equipo_1 = int(rows["equipo_1"])
        equipo_2 = int(rows["equipo_2"])
        id_ganador = 0
        if gol_eq1 == gol_eq2:
            id_ganador = 0

        if gol_eq1 > gol_eq2:
                id_ganador = equipo_1

        if gol_eq1 < gol_eq2:
                id_ganador = equipo_2
        print(id_ganador)

        li = clasificar(liga, equipo_1, equipo_2)
        print(li)
        if li == id_ganador:
            Aciertos += 1
            nro_partido += 1
        else:
            Desaciertos += 1
            nro_partido += 1

        Porcentaje = (decimal.Decimal(Aciertos)/decimal.Decimal(nro_partido))*100

    cuota_local.append(nro_partido)
    cuota_local.append(Aciertos)
    cuota_local.append(Desaciertos)
    cuota_local.append(Porcentaje)

    return  cuota_local

#A = leeLista()
#A = [[5, 8, 5], [8, 5, 5], [2, 7, 5],[9, 6, 5], [20, 4, 5]]
liga= 9
l=porcentaje_acierto(liga)

print(l)
