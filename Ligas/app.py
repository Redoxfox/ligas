from flask import Flask, render_template, request, json, redirect, url_for, jsonify
import pymysql.cursors

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
        url = "http://localhost:8000/resultado/" + str(idp) + "/" + str(idlig) + "/"
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


@app.route('/resultado/<id>/<liga>/', methods=['POST', 'GET'])
def form_resultados(id, liga):
    resultado = {}
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
        gol_eq1 = rows["gol_eq1"]
        gol_eq2 = rows["gol_eq2"]
        nro_fecha = rows["nro_fecha"]
        equipo_1 = rows["equipo_1"]
        equipo_2 = rows["equipo_2"]

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

    return render_template('form_partido.html', nombre1 = nom_eq1, nombre2 = nom_eq2,  resultado = resultado,  victoria=victoria, empate=empate, derrota=derrota)

@app.route('/grafico/')
def grafico():
    cursor = connection.cursor()
    # Read a single record
    cursor.execute("select nro_fecha, equipo_1, equipo_2, gol_eq1, gol_eq2 from calendario where id_liga=4 and estado='JUGADO';")
    goles_liga = cursor.fetchall()
    derrota = []
    empate = []
    victoria = []
    empate_eq1 = 0
    victoria_eq1 = 0
    derrota_eq1 = 0
    empate_eq2 = 0
    victoria_eq2 = 0
    derrota_eq2 = 0

    for rows in goles_liga:
        gol_eq1 = rows["gol_eq1"]
        gol_eq2 = rows["gol_eq2"]
        nro_fecha = rows["nro_fecha"]
        equipo_1 = rows["equipo_1"]
        equipo_2 = rows["equipo_2"]

        if equipo_1 == '62':
            if gol_eq1 == gol_eq2:
                empate_eq1 += 1


            if gol_eq2 < gol_eq1:
                victoria_eq1 += 1


            if gol_eq1 < gol_eq2:
                derrota_eq1 -= 1

        if equipo_2 == '62':
            if gol_eq1 == gol_eq2:
                empate_eq1 += 1


            if gol_eq1 < gol_eq2:
                victoria_eq1 += 1


            if gol_eq2 < gol_eq1:
                derrota_eq1 -= 1

        if equipo_1 == '72':
            if gol_eq1 == gol_eq2:
                empate_eq2 += 1

            if gol_eq2 < gol_eq1:
                victoria_eq2 += 1


            if gol_eq1 < gol_eq2:
                derrota_eq2 -= 1

        if equipo_2 == '72':
            if gol_eq1 == gol_eq2:
                empate_eq2 += 1

            if gol_eq1 < gol_eq2:
                victoria_eq2 += 1


            if gol_eq2 < gol_eq1:
                derrota_eq2 -= 1

    derrota.append(derrota_eq1)
    derrota.append(derrota_eq2)
    empate.append(empate_eq1)
    empate.append(empate_eq2)
    victoria.append(victoria_eq1)
    victoria.append(victoria_eq2)

    return render_template('graficos.html', victoria = victoria, empate = empate, derrota = derrota )


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