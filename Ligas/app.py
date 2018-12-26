#-----------------------------------------------------------------------------------------------------------------------
#Datos de configuracion
#-----------------------------------------------------------------------------------------------------------------------
from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors
from Ligas.lib.Bbinaria import binaria
from Ligas.lib.Oquicksort import quicksort
from Ligas.lib.calendario import fechas_liga

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='perfume',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)

#-----------------------------------------------------------------------------------------------------------------------
#Inicio aplicacion
#-----------------------------------------------------------------------------------------------------------------------
@app.route("/")
def home():
    cursor=connection.cursor()
    # Read a single record
    sql = "SELECT * FROM liga " #
    cursor.execute(sql)
    result = cursor.fetchall()
    resultado = {}
    cont = 0
    for rows in result:
        idlig = rows["id"]
        nombre = rows["nombre"]
        pais = rows["pais"]
        continente = rows["continente"]
        url = "http://localhost:8000/clasificacion/" + str(idlig) + "/"
        resultado[cont] = (idlig,  nombre, pais, continente, url)
        cont = cont + 1
    sql1 = " select id from liga;"
    cursor.execute(sql1)
    ligas = cursor.fetchall()
    ligas_reg = []
    jornadas = []
    for rows in ligas:
        nro_liga = rows["id"]
        ligas_reg.append(nro_liga)
    liga_ext = len(ligas) + 1
    ligas_reg.append(liga_ext)
    for i in range(1, 45):
        jornadas.append(i)

    return render_template('home.html', result=resultado, ligas_reg = ligas_reg, jornadas = jornadas )
#-----------------------------------------------------------------------------------------------------------------------
#Datos clasificacion
#-----------------------------------------------------------------------------------------------------------------------
@app.route('/clasificacion/<id>/', methods=['POST', 'GET'])
def liga(id):
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM calendario WHERE id_liga=%s and estado='PENDIENTE'", str(id))
    result = cursor.fetchall()
    resultado = {}
    cont = 0
    Jornada = 1
    for rows in result:
        idlig = rows["id_liga"]
        nrofecha = rows["nro_fecha"]
        idp = rows["id"]
        ps = rows["equipo_1"]
        ps2 = rows["equipo_2"]
        gol_eq1 = rows["gol_eq1"]
        gol_eq2 = rows["gol_eq2"]
        cursor.execute("SELECT nombre FROM equipos WHERE id=%s", ps)
        nom_eq = cursor.fetchone()
        equipo_1 = nom_eq['nombre']
        cursor.execute("SELECT nombre FROM equipos WHERE id=%s", ps2)
        nom_eq2 = cursor.fetchone()
        equipo_2 = nom_eq2['nombre']
        url = "http://localhost:8000/resultado/" + str(idp) + "/" + str(idlig) + "/" + str(ps) + "/" + str(ps2)+ "/"
        urlrev = "http://localhost:8000/"
        if Jornada != nrofecha:
           Jornada = nrofecha
           cambio = 'true'
           idj = "J" + str(Jornada) + "-P" + str(idp)
           resultado[cont] = (equipo_1, gol_eq1, equipo_2, gol_eq2, url, idj, cambio)
        else:
           idj = "J" + str(Jornada) + "-P" + str(idp)
           cambio = 'false'
           resultado[cont] = (equipo_1, gol_eq1, equipo_2, gol_eq2, url, idj, cambio)

        cont = cont + 1

    return render_template('clasificacion.html', result=resultado, nombre=id, liga = 'española', url = urlrev )

#-----------------------------------------------------------------------------------------------------------------------
#Ingresar partido.
#-----------------------------------------------------------------------------------------------------------------------
@app.route('/reasignar/<idfecha>/<dliga>/', methods=['POST', 'GET'])
def reasignar(idfecha, dliga):
    cursor=connection.cursor()
    idlig = dliga
    idp = idfecha
    resultado = {}
    resultado2 = {}
    cont = 0
    jornadas = "select * from calendario where id_liga = %s and nro_fecha=%s;"
    cursor.execute(jornadas, (idlig, idp))
    nro_jornada = cursor.fetchall()
    for rows in nro_jornada:
        idlig = rows["id_liga"]
        nrofecha = rows["nro_fecha"]
        idp = rows["id"]
        ideq1 = rows["equipo_1"]
        ideq2= rows["equipo_2"]
        gol_eq1 = rows["gol_eq1"]
        gol_eq2 = rows["gol_eq2"]
        sql1 = "SELECT nombre FROM equipos WHERE id= %s "
        cursor.execute(sql1, (ideq1 ))
        nom_eq1 = cursor.fetchall()
        sql2 = "SELECT nombre FROM equipos WHERE id= %s "
        cursor.execute(sql2, (ideq2))
        nom_eq2 = cursor.fetchall()
        clud1 = nom_eq1[0]
        clud2 = nom_eq2[0]
        resultado2[cont] = (clud1, clud2)
        resultado[cont] = (idp, gol_eq1,gol_eq2)
        cont += 1

    return render_template('reasignacion.html', result2=resultado2, result=resultado, jornada=nro_jornada, idp=idp, idlig=idlig, liga = 'española', fecha = idfecha )




@app.route('/resultado/<id>/<liga>/<id_eq1>/<id_eq2>/', methods=['POST', 'GET'])
def form_resultados(id, liga, id_eq1, id_eq2):
    resultado = {}
    resultado1 = {}
    cursor = connection.cursor()
    # Read a single record
    url = "http://localhost:8000/actualizar/"+ str(id) + "/" + str(liga) + "/"

    sql1 = "SELECT nombre FROM equipos WHERE id= %s "
    cursor.execute(sql1, (id_eq1))
    nom_eq1 = cursor.fetchall()

    sql2 = "SELECT nombre FROM equipos WHERE id= %s "
    cursor.execute(sql2, (id_eq2))
    nom_eq2 = cursor.fetchall()

    sql3 = "select nro_fecha, equipo_1, equipo_2, gol_eq1, gol_eq2 from calendario where id_liga= %s and estado='JUGADO';"
    cursor.execute(sql3, (liga))
    goles_liga = cursor.fetchall()
    id_e1 =int(id_eq1)
    id_e2 =int(id_eq2)
    historial= []
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
            if id_e1==equipo_1:
                empate_eq1_local += 1

            if id_e2==equipo_2:
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
            #print(historial)
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

    resultado[0] = (0, 0, id, url,liga)

    ordenadoM = quicksort(historial, 0, len(historial) - 1, 9)

    cont=0
    for i in range(len(ordenadoM)):
        indice=len(ordenadoM)-1-i
        idclud = ordenadoM[indice][1]
        sql1 = "SELECT nombre FROM equipos WHERE id= %s "
        cursor.execute(sql1, (idclud ))
        nom_clud = cursor.fetchall()
        cont = cont + 1
        pos = i + 1
        clud = nom_clud[0]
        #clud = ordenadoM[indice][1]
        pj = ordenadoM[indice][2]
        gf = ordenadoM[indice][3]
        gc = ordenadoM[indice][4]
        dg = ordenadoM[indice][5]
        pg = ordenadoM[indice][6]
        pp = ordenadoM[indice][7]
        pe = ordenadoM[indice][8]
        ptos = ordenadoM[indice][9]
        #datos = binaria(ordenadoM, int(pos2))
        resultado1[i] = (pos, clud, pj, gf, gc, dg, pg, pp, pe, ptos)
        if idclud == id_e1:
            pos_eq1 = indice
        if idclud == id_e2:
            pos_eq2 = indice

    P_GJEQ1 = ordenadoM[pos_eq1][6]/ordenadoM[pos_eq1][2]
    P_GJLEQ1 = victoria_eq1_local / (derrota_eq1_local + empate_eq1_local + victoria_eq1_local)
    P_GJVEQ1 = victoria_eq1_visitante / (derrota_eq1_visitante + empate_eq1_visitante + victoria_eq1_visitante)
    P_PJEQ1 = ordenadoM[pos_eq1][7] / ordenadoM[pos_eq1][2]
    P_PJLEQ1 = derrota_eq1_local / (derrota_eq1_local + empate_eq1_local + victoria_eq1_local)
    P_PJVEQ1 = derrota_eq1_visitante / (derrota_eq1_visitante + empate_eq1_visitante + victoria_eq1_visitante)
    P_EJEQ1 = ordenadoM[pos_eq1][8] / ordenadoM[pos_eq1][2]
    P_EJLEQ1 = empate_eq1_local / (derrota_eq1_local + empate_eq1_local + victoria_eq1_local)
    P_EJVEQ1 = empate_eq1_visitante / (derrota_eq1_visitante + empate_eq1_visitante + victoria_eq1_visitante)

    P_GJEQ2 = ordenadoM[pos_eq2][6] / ordenadoM[pos_eq2][2]
    P_GJLEQ2 = victoria_eq2_local / (derrota_eq2_local + empate_eq2_local + victoria_eq2_local)
    P_GJVEQ2 = victoria_eq2_visitante / (derrota_eq2_visitante + empate_eq2_visitante + victoria_eq2_visitante)
    P_PJEQ2 = ordenadoM[pos_eq2][7] / ordenadoM[pos_eq2][2]
    P_PJLEQ2 = derrota_eq2_local / (derrota_eq2_local + empate_eq2_local + victoria_eq2_local)
    P_PJVEQ2 = derrota_eq2_visitante / (derrota_eq2_visitante + empate_eq2_visitante + victoria_eq2_visitante)
    P_EJEQ2 = ordenadoM[pos_eq2][8] / ordenadoM[pos_eq2][2]
    P_EJLEQ2 = empate_eq2_local / (derrota_eq2_local + empate_eq2_local + victoria_eq2_local)
    P_EJVEQ2 = empate_eq2_visitante / (derrota_eq2_visitante + empate_eq2_visitante + victoria_eq2_visitante)


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

    p_victoria_local = (P_GJEQ1  *  P_GJLEQ1 ) / (P_GJEQ1 * P_GJLEQ1 + P_PJEQ1 * P_PJLEQ1  +  P_EJEQ1 * P_EJLEQ1 )
    p_derrota_local = (P_PJEQ1 * P_PJLEQ1) / (P_GJEQ1 * P_GJLEQ1 + P_PJEQ1 * P_PJLEQ1 + P_EJEQ1 * P_EJLEQ1)
    p_empate_local = (P_EJEQ1 * P_EJLEQ1) / (P_GJEQ1 * P_GJLEQ1 + P_PJEQ1 * P_PJLEQ1 + P_EJEQ1 * P_EJLEQ1)
    p_victoria_visitante =(P_GJEQ2 * P_GJVEQ2) / (P_GJEQ2 * P_GJVEQ2 + P_PJEQ2 * P_PJVEQ2 + P_EJEQ2 * P_EJVEQ2)
    p_derrota_visitante = (P_PJEQ2 * P_PJVEQ2) / (P_GJEQ2 * P_GJVEQ2 + P_PJEQ2 * P_PJVEQ2 + P_EJEQ2 * P_EJVEQ2)
    p_empate_visitante = (P_EJEQ2 * P_EJVEQ2) / (P_GJEQ2 * P_GJVEQ2 + P_PJEQ2 * P_PJVEQ2 + P_EJEQ2 * P_EJVEQ2)

    if p_victoria_local > 0:
        p_victoria_local = 1/p_victoria_local
    else:
        p_victoria_local = 100

    if p_derrota_local > 0:
        p_derrota_local = 1/p_derrota_local
    else:
        p_derrota_local = 100

    if  p_empate_local > 0:
        p_empate_local = 1/ p_empate_local
    else:
        p_empate_local = 100

    if p_victoria_visitante >0:
        p_victoria_visitante = 1/p_victoria_visitante
    else:
        p_victoria_visitante = 100

    if p_derrota_visitante > 0:
        p_derrota_visitante = 1/p_derrota_visitante
    else:
        p_derrota_visitante = 100

    if p_empate_visitante  > 0:
        p_empate_visitante = 1/p_empate_visitante
    else:
        p_empate_visitante = 100

    cuota_local.append(p_victoria_local)
    cuota_local.append(p_derrota_local)
    cuota_local.append(p_empate_local)
    cuota_visitante.append(p_victoria_visitante)
    cuota_visitante.append(p_derrota_visitante)
    cuota_visitante.append(p_empate_visitante)

    return render_template('form_partido.html', nombre1 = nom_eq1, nombre2 = nom_eq2,  resultado = resultado,  victoria=victoria, empate=empate, derrota=derrota ,  pvictoria=p_victoria, pempate=p_empate , pderrota=p_derrota, clocal = cuota_local , cvisit = cuota_visitante, clasificacion = resultado1)

@app.route('/grafico/<liga>/' , methods=['POST', 'GET'])
def grafico(liga):
    cursor = connection.cursor()
    # Read a single record
    #cursor.execute("select nro_fecha, equipo_1, equipo_2, gol_eq1, gol_eq2 from calendario where id_liga=4 and estado='JUGADO';")
    clasificacion="select * from calendario where id_liga=%s and estado='JUGADO' and temporada='2018-2019';"
    cursor.execute(clasificacion, (liga))
    goles_liga = cursor.fetchall()
    M_clasificacion = []
    resultado = {}
    for rows in goles_liga:
        nro_equipos = len(M_clasificacion)
        gol_eq1 = int(rows["gol_eq1"])
        gol_eq2 = int(rows["gol_eq2"])
        equipo_1 = rows["equipo_1"]
        equipo_2 = rows["equipo_2"]
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

        if nro_equipos==0:
            POS = len(M_clasificacion) + 1
            Nre_E = int(equipo_1)
            PJ = 1
            GF = Goles_favoreq1
            GC = Goles_contraeq1
            GD = Goles_favoreq1 - Goles_contraeq1
            PG = victoria_eq1
            PP = derrota_eq1
            PE = empate_eq1
            PTOS = puntos_eq1
            M_clasificacion.append([POS, Nre_E, PJ, GF, GC, GD, PG, PP, PE, PTOS])
            POS = len(M_clasificacion)
            Nre_E = int(equipo_2)
            PJ = 1
            GF = Goles_favoreq2
            GC = Goles_contraeq2
            GD = Goles_favoreq2 - Goles_contraeq2
            PG = victoria_eq2
            PP = derrota_eq2
            PE = empate_eq2
            PTOS = puntos_eq2
            M_clasificacion.append([POS, Nre_E, PJ, GF, GC, GD, PG, PP, PE, PTOS])
            print(M_clasificacion)
        else:
            derecha = len(M_clasificacion) - 1
            ordenadoM = quicksort(M_clasificacion, 0, derecha, 1)
            datos1 = binaria(ordenadoM, int(equipo_1),1)
            datos2 = binaria(ordenadoM, int(equipo_2),1)
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
            if  datos1 != None :
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
            if  datos2 != None :
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
            if datos1 == None :
                POS = len(M_clasificacion) + 1
                Nre_E = int(equipo_1)
                PJ = 1
                GF = Goles_favoreq1
                GC = Goles_contraeq1
                GD = Goles_favoreq1 - Goles_contraeq1
                PG = victoria_eq1
                PP = derrota_eq1
                PE = empate_eq1
                PTOS = puntos_eq1
                M_clasificacion.append([POS, Nre_E, PJ, GF, GC, GD, PG, PP, PE, PTOS])
            if datos2 == None :
                POS = len(M_clasificacion)
                Nre_E = int(equipo_2)
                PJ = 1
                GF = Goles_favoreq2
                GC = Goles_contraeq2
                GD = Goles_favoreq2 - Goles_contraeq2
                PG = victoria_eq2
                PP = derrota_eq2
                PE = empate_eq2
                PTOS = puntos_eq2
                M_clasificacion.append([POS, Nre_E, PJ, GF, GC, GD, PG, PP, PE, PTOS])

    ordenadoM = quicksort(M_clasificacion, 0, len(M_clasificacion) - 1, 9)


    for i in range(len(ordenadoM)):
        indice=len(ordenadoM)-1-i
        idclud = ordenadoM[indice][1]
        sql1 = "SELECT nombre FROM equipos WHERE id= %s "
        cursor.execute(sql1, (idclud ))
        nom_eq1 = cursor.fetchall()

        pos = i + 1
        clud = nom_eq1[0]
        #clud = ordenadoM[indice][1]
        pj = ordenadoM[indice][2]
        gf = ordenadoM[indice][3]
        gc = ordenadoM[indice][4]
        dg = ordenadoM[indice][5]
        pg = ordenadoM[indice][6]
        pp = ordenadoM[indice][7]
        pe = ordenadoM[indice][8]
        ptos = ordenadoM[indice][9]
        #datos = binaria(ordenadoM, int(pos2))


        resultado[i] = (pos, clud, pj, gf, gc, dg, pg, pp, pe, ptos)



    return render_template('graficos.html', clasificacion = resultado )

@app.route('/nueva_liga/', methods=['POST', 'GET'])
def nueva_liga(liga):
    cursor = connection.cursor()
    # Read a single record
    #cursor.execute("select nro_fecha, equipo_1, equipo_2, gol_eq1, gol_eq2 from calendario where id_liga=4 and estado='JUGADO';")
    equipos_liga="select id from equipos where id_liga = %s and estado='ACTIVADO';"
    cursor.execute(equipos_liga, (liga))
    fixture = cursor.fetchall()
    partidos = []
    lista_equipos = []
    resultado = {}
    for rows in fixture:
        nro_equipo = int(rows["id"])
        lista_equipos.append(nro_equipo)

    nro_clubes = len(lista_equipos)
    partidos = fechas_liga(lista_equipos, 25, 13)

    for i in range(len(partidos)-1):
        indice=i
        ideq1= partidos[indice][0]
        ideq2 = partidos[indice][1]
        sql1 = "SELECT nombre FROM equipos WHERE id= %s "
        cursor.execute(sql1, (ideq1 ))
        nom_eq1 = cursor.fetchall()

        sql2 = "SELECT nombre FROM equipos WHERE id= %s "
        cursor.execute(sql2, (ideq2))
        nom_eq2 = cursor.fetchall()

        pos = i + 1
        clud1 = nom_eq1[0]
        clud2 = nom_eq2[0]


        resultado[i] = (clud1, clud2)

    return render_template('calendario.html', clasificacion = resultado )

@app.route('/NuevoEquipo/', methods=['POST', 'GET'])
def NuevoEquipo():
    url = "http://localhost:8000/IngresarEquipo/"
    cursor = connection.cursor()
    equipos_liga="select id from equipos;"
    cursor.execute(equipos_liga)
    fixture = cursor.fetchall()
    lista_equipos = []
    for rows in fixture:
        nro_equipo = int(rows["id"])
        lista_equipos.append(nro_equipo)
    nro_clubes = len(lista_equipos) + 1
    lista_paises = {}
    paises = "select id, pais from paises;"
    cursor.execute(paises)
    lista_paises = cursor.fetchall()
    sql = " select id from liga;"
    cursor.execute(sql)
    ligas = cursor.fetchall()
    ligas_reg = []
    for rows in ligas:
        nro_liga = rows["id"]
        ligas_reg.append(nro_liga)
    liga_ext = len(ligas) + 1
    ligas_reg.append(liga_ext)
    sql_lista = "select * from equipos order by id desc;"
    cursor.execute(sql_lista)
    lista_clubes= cursor.fetchall()
    lista = {}
    cont = 0
    for rows in lista_clubes:
        id = rows["id"]
        id_liga = rows["id_liga"]
        nombre = rows["nombre"]
        ciudad = rows["ciudad"]
        estado = rows["estado"]
        lista[cont]=(id,id_liga,nombre,ciudad,estado)
        cont += 1

    return render_template('form_equipos.html', nro_liga=nro_clubes, pais= lista_paises, ligas_reg = ligas_reg, url = url, lista_clubes=lista)

@app.route('/calendario/', methods=['POST', 'GET'])
def calendario():
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['nom_lig']
        pais = request.form['pais']
        continente = request.form['continente']
        nro_equipos = request.form['equipos']
        nro_fh_tor = request.form['jornadas']
        partidos_jorn = request.form['partidosjornada']
        cursor = connection.cursor()
        sql = "INSERT INTO liga (id, nombre, pais, continente, nro_equipos, nro_fh_tor) VALUES (%s, %s, %s,  %s,  %s,  %s);"
        cursor.execute(sql, (id, nombre, pais, continente, nro_equipos, nro_fh_tor))
        cursor.close()
        connection.commit()

    # Read a single record
    #cursor.execute("select nro_fecha, equipo_1, equipo_2, gol_eq1, gol_eq2 from calendario where id_liga=4 and estado='JUGADO';")
    cursor = connection.cursor()

    equipos_liga="select id from equipos where id_liga = %s and estado='ACTIVADO';"
    cursor.execute(equipos_liga, (id))
    fixture = cursor.fetchall()
    partidos = []
    lista_equipos = []
    resultado = {}
    for rows in fixture:
        nro_equipo = int(rows["id"])
        lista_equipos.append(nro_equipo)

    nro_clubes = len(lista_equipos)
    jor = int(nro_fh_tor)
    par_jor = int(partidos_jorn)
    partidos = fechas_liga(lista_equipos, jor, par_jor)
    Jornada = 1
    nro_fecha = 0
    partidosc= "select id from calendario;"
    cursor.execute(partidosc)
    fixture = cursor.fetchall()
    lista_partidos = []
    for rows in fixture:
        nro_equipo = int(rows["id"])
        lista_partidos.append(nro_equipo)
    #idp = len(lista_equipos) + 2


    for i in range(0, len(partidos)-1):
        indice=i
        ideq1= partidos[indice][0]
        ideq2 = partidos[indice][1]
        sql1 = "SELECT nombre FROM equipos WHERE id= %s "
        cursor.execute(sql1, (ideq1 ))
        nom_eq1 = cursor.fetchall()
        sql2 = "SELECT nombre FROM equipos WHERE id= %s "
        cursor.execute(sql2, (ideq2))
        nom_eq2 = cursor.fetchall()
        pos = i + 1
        clud1 = nom_eq1[0]
        clud2 = nom_eq2[0]
        resultado[i] = (clud1, clud2)
        gol_eq1 = 0
        gol_eq2 = 0
        equipo_1 = ideq1
        equipo_2 = ideq2
        local_eq1 = ideq1
        local_eq2 = ideq2
        estado = "PENDIENTE"
        temporada = "2018-2019"
        fecha = "2018-12-04"
        idp = "null"

        if nro_fecha < par_jor:
            cursor = connection.cursor()
            sql2 = "INSERT INTO calendario (id, nro_fecha, id_liga, equipo_1, gol_eq1, equipo_2, gol_eq2, local_eq1, local_eq2, estado, temporada, fecha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql2, (idp, Jornada, id, equipo_1, gol_eq1, equipo_2, gol_eq2, local_eq1, local_eq2, estado, temporada,fecha))
            connection.commit()
        else:
            Jornada += 1
            nro_fecha = 0
            cursor = connection.cursor()
            sql2 = "INSERT INTO calendario (id, nro_fecha, id_liga, equipo_1, gol_eq1, equipo_2, gol_eq2, local_eq1, local_eq2, estado, temporada, fecha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql2, (idp, Jornada, id, equipo_1, gol_eq1, equipo_2, gol_eq2, local_eq1, local_eq2, estado, temporada, fecha))
            connection.commit()
        nro_fecha += 1


    return render_template('calendario.html', clasificacion =  resultado )


@app.route('/actualizar/<id>/<liga>/', methods=['POST', 'GET'])
def actualizar(id, liga):
    if request.method == 'POST':
        #idp = request.form['idp']
        cursor = connection.cursor()
        # Create a new record
        #equipo1 = request.form['equipo1']
        gol_eq1 = request.form['gol_eq1']
        #equipo2 = request.form['equipo2']
        gol_eq2 = request.form['gol_eq2']
        estado = "JUGADO"
        sql = "UPDATE calendario SET  gol_eq1= %s, gol_eq2 = %s, estado = %s WHERE id = %s and id_liga = %s"
        cursor.execute(sql, (gol_eq1, gol_eq2, estado, id, liga))
        cursor.close()
        connection.commit()
        #return redirect(url_for('home'))
        return redirect(url_for('liga', id=liga))
    else:
        return render_template('index.html')

@app.route('/gestion/', methods=['POST', 'GET'])
def gestion():
    url = "http://localhost:8000/calendario/"
    jornadas = []
    cursor = connection.cursor()
    sql = " select id from liga;"
    cursor.execute(sql)
    fixture = cursor.fetchall()

    Nueva_liga = len(fixture) + 1
    for i in range(1,45):
        jornadas.append(i)

    sql2 = "select pais from paises;"
    cursor.execute(sql2)
    pais = cursor.fetchall()

    sql3 = "select continente from paises group by continente;"
    cursor.execute(sql3)
    continente = cursor.fetchall()

    return render_template('gestion.html', nro_liga = Nueva_liga, jornadas = jornadas, continente= continente, pais = pais, url = url)

@app.route('/IngresarEquipo/', methods=['POST', 'GET'])
def IngresarEquipo():
    if request.method == 'POST':
        cursor = connection.cursor()
        id_liga = request.form['id_liga']
        nombre = request.form['nom_eq']
        id = request.form['id_equipo']
        ciudad = request.form['pais']
        estado = "ACTIVADO"
        sql = "INSERT INTO equipos (id, id_liga, nombre, ciudad, estado) VALUES (%s, %s, %s,  %s,  %s);"
        cursor.execute(sql, (id, id_liga, nombre, ciudad, estado))
        cursor.close()
        connection.commit()

    return redirect(url_for('NuevoEquipo'))


@app.route('/encuentros/<idp>/<idliga>/<fecha>/', methods=['POST', 'GET'])
def encuentros(idp, idliga, fecha):
    cursor = connection.cursor()
    idlig = idliga
    equipos_liga = "select * from equipos where id_liga = %s;"
    cursor.execute(equipos_liga, (idlig))
    equipos = cursor.fetchall()

    return render_template('encuentros.html',  result=equipos, idpt = idp, liga = idliga, fecha = fecha )

@app.route('/partido_actualizado/', methods=['POST', 'GET'])
def partido_actualizado():
    if request.method == 'POST':
        cursor = connection.cursor()
        liga = request.form['id_liga']
        idp = request.form['id_partido']
        fecha = request.form['fecha']
        # Create a new record
        equipo1 = request.form['clud1']
        gol_eq1 = request.form['gol_eq1']
        equipo2 = request.form['clud2']
        gol_eq2 = request.form['gol_eq2']
        estado="PENDIENTE"
        sql = "UPDATE calendario SET equipo_1= %s, gol_eq1= %s, equipo_2= %s, gol_eq2 = %s, local_eq1= %s, local_eq2= %s, estado= %s WHERE id = %s and id_liga = %s"
        cursor.execute(sql, (equipo1, gol_eq1, equipo2, gol_eq2,  equipo1, equipo2, estado, idp, liga))
        cursor.close()
        connection.commit()
        #return redirect(url_for('home'))
        return redirect(url_for('reasignar', idfecha=fecha, dliga=liga))
@app.route('/gestion_partido/', methods=['POST', 'GET'])
def gestion_partido():
    if request.method == 'POST':
        urlrev = "http://localhost:8000/"
        cursor = connection.cursor()
        liga = request.form['id_liga']
        fecha = request.form['jornadas']
        return redirect(url_for('reasignar', idfecha=fecha, dliga=liga))


if __name__ == "__main__":
    app.run(debug = True, port = 8000)