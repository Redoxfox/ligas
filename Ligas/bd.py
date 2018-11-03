import pymysql.cursors
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='perfume',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
sql = "SELECT * FROM calendario"
cursor.execute(sql)
result = cursor.fetchall()
print (result)
resultado = {}

cont = 0


for rows in result:
    ps = rows["id"]
    gol_eq1 = rows["gol_eq1"]
    equipo_2 = rows["equipo_2"]
    gol_eq2= rows["gol_eq2"]
    cursor.execute("SELECT nombre FROM equipos WHERE id=%s", ps)
    equipo_1 = cursor.fetchone()
    resultado[cont] = (equipo_1, gol_eq1, equipo_2, gol_eq2)

    cont = cont + 1

