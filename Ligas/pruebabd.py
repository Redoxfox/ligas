from flask import Flask, render_template, request, json, redirect, url_for
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='perfume',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)


@app.route("/")
def login():
    cursor=connection.cursor()
    # Read a single record
    sql = "SELECT * FROM calendario"
    cursor.execute(sql)
    result = cursor.fetchall()
    #resultado= []
    resultado = {}
    cont = 0
    for rows in result:
        idlig = rows["id_liga"]
        idp = rows["id"]
        ps = rows["equipo_1"]
        ps2 = rows["equipo_2"]
        gol_eq1 = rows["gol_eq1"]
        #equipo_2 = rows["equipo_2"]
        gol_eq2= rows["gol_eq2"]
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
        resultado[cont] = (equipo_1, gol_eq1, equipo_2, gol_eq2, url)
        cont = cont + 1

    return render_template('index.html', result=resultado, nombre = ps)


@app.route('/resultado/<id>/<liga>/', methods=['POST', 'GET'])
def form_resultados(id, liga):
    cursor = connection.cursor()
    # Read a single record
    url = "http://localhost:8000/actualizar/"
    cursor.execute("SELECT id, nombre FROM equipos WHERE id_liga = %s", liga)
    equipos_liga = cursor.fetchall()

    return render_template('form_partido.html', equipos = equipos_liga, idp = id, url = url)


@app.route('/actualizar/', methods=['POST', 'GET'])
def actualizar():
    if request.method == 'POST':
        idp = request.form['idp']
        cursor = connection.cursor()
        # Create a new record
        equipo1 = request.form['equipo1']
        gol_eq1 = request.form['gol_eq1']
        equipo2 = request.form['equipo2']
        gol_eq2 = request.form['gol_eq2']
        estado = "JUGADO"
        sql = "UPDATE calendario SET equipo_1 = %s, gol_eq1= %s, equipo_2 = %s, gol_eq2 = %s,  local_eq1 = %s,  local_eq2 = %s, estado = %s WHERE id = %s"
        cursor.execute(sql, (equipo1, gol_eq1, equipo2, gol_eq2, equipo1, equipo2, estado, idp))
        cursor.close()
        connection.commit()
        return redirect(url_for('login'))
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug = True, port = 8000)