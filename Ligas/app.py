from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors
from Ligas.lib.Bbinaria import binaria
from Ligas.lib.Oquicksort import quicksort

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='perfume',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)


@app.route('/clasificacion/<id>/', methods=['POST', 'GET'])
def liga(id):
    cursor=connection.cursor()
    # Read a single record
    if id != '7':
        cursor.execute("SELECT * FROM calendario WHERE id_liga=%s and estado='PENDIENTE'", str(id))
    else:
        cursor.execute("SELECT * FROM calendario WHERE id_liga=%s and estado='PENDIENTE'", str(id))

    result = cursor.fetchall()
    #resultado= []
    print(result)
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
        # equipo_2 = rows["equipo_2"]
        gol_eq2 = rows["gol_eq2"]
        cursor.execute("SELECT nombre FROM equipos WHERE id=%s", ps)
        nom_eq = cursor.fetchone()
        equipo_1 = nom_eq['nombre']
        cursor.execute("SELECT nombre FROM equipos WHERE id=%s", ps2)
        nom_eq2 = cursor.fetchone()
        equipo_2 = nom_eq2['nombre']
        url = "http://localhost:8000/resultado/" + str(idp) + "/" + str(idlig) + "/" + str(ps) + "/" + str(ps2)+ "/"
        """registro['url'] = idp
            registro['equipo_1'] = equipo_1
            registro['gol_eq1'] = gol_eq1
            registro['equipo_2'] = equipo_2
            resultado.append(registro)
            registro['gol_eq2'] = gol_eq2"""
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

    return render_template('clasificacion.html', result=resultado, nombre=id, liga = 'española')

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

    return render_template('home.html', result=resultado)


@app.route('/resultado/<id>/<liga>/<id_eq1>/<id_eq2>/', methods=['POST', 'GET'])
def form_resultados(id, liga, id_eq1, id_eq2):
    resultado = {}
    resultado1 = {}
    cursor = connection.cursor()
    # Read a single record
    url = "http://localhost:8000/actualizar/"+ str(id) + "/" + str(liga) + "/"
    sql="SELECT * FROM calendario WHERE id_liga = %s and id= %s "
    cursor.execute(sql, (liga, id))
    equipos_liga = cursor.fetchall()
    for rows in equipos_liga:
        id_e1 = rows["equipo_1"]
        gol_eq1 = rows["gol_eq1"]
        id_e2 = rows["equipo_2"]
        gol_eq2 = rows["gol_eq2"]

    sql1 = "SELECT nombre FROM equipos WHERE id= %s "
    cursor.execute(sql1, (id_e1))
    nom_eq1 = cursor.fetchall()

    sql2 = "SELECT nombre FROM equipos WHERE id= %s "
    cursor.execute(sql2, (id_e2))
    nom_eq2 = cursor.fetchall()

    sql3 = "select nro_fecha, equipo_1, equipo_2, gol_eq1, gol_eq2 from calendario where id_liga= %s and estado='JUGADO';"
    cursor.execute(sql3, (liga))
    goles_liga = cursor.fetchall()
    id_e1 =id_eq1
    id_e2 =id_eq2
    historial = []
    derrota = []
    empate = []
    victoria = []
    empate_eq1 = 0
    victoria_eq1 = 0
    derrota_eq1 = 0
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
            datos1 = binaria(ordenadoM, int(equipo_1))
            datos2 = binaria(ordenadoM, int(equipo_2))
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

        if equipo_1 == str(id_e1):
            if gol_eq1 == gol_eq2:
                empate_eq1 += 1
                empate_eq1_local += 1

            if gol_eq2 < gol_eq1:
                victoria_eq1 += 1
                victoria_eq1_local += 1

            if gol_eq1 < gol_eq2:
                derrota_eq1 -= 1
                derrota_eq1_local += 1

        if equipo_2 == str(id_e1):
            if gol_eq1 == gol_eq2:
                empate_eq1 += 1
                empate_eq1_visitante += 1

            if gol_eq1 < gol_eq2:
                victoria_eq1 += 1
                victoria_eq1_visitante += 1

            if gol_eq2 < gol_eq1:
                derrota_eq1 -= 1
                derrota_eq1_visitante += 1

        if equipo_1 == str(id_e2):
            if gol_eq1 == gol_eq2:
                empate_eq2 += 1
                empate_eq2_local += 1


            if gol_eq2 < gol_eq1:
                victoria_eq2 += 1
                victoria_eq2_local += 1

            if gol_eq1 < gol_eq2:
                derrota_eq2 -= 1
                derrota_eq2_local += 1

        if equipo_2 ==  str(id_e2):
            if gol_eq1 == gol_eq2:
                empate_eq2 += 1
                empate_eq2_visitante += 1

            if gol_eq1 < gol_eq2:
                victoria_eq2 += 1
                victoria_eq2_visitante += 1

            if gol_eq2 < gol_eq1:
                derrota_eq2 -= 1
                derrota_eq2_visitante += 1

    derrota.append(derrota_eq1)
    derrota.append(derrota_eq2)
    empate.append(empate_eq1)
    empate.append(empate_eq2)
    victoria.append(victoria_eq1)
    victoria.append(victoria_eq2)

    resultado[0] = (gol_eq1, gol_eq2, id, url,liga)

    ordenadoM = quicksort(historial, 0, len(historial) - 1, 9)

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
        resultado1[i] = (pos, clud, pj, gf, gc, dg, pg, pp, pe, ptos)


    return render_template('form_partido.html', nombre1 = nom_eq1, nombre2 = nom_eq2,  resultado = resultado,  victoria=victoria, empate=empate, derrota=derrota, clasificacion = resultado1)

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
            datos1 = binaria(ordenadoM, int(equipo_1))
            datos2 = binaria(ordenadoM, int(equipo_2))
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
        return redirect(url_for('home'))
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug = True, port = 8000)