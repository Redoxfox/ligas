import sys
import re
import requests


def download(url):
    """Returns the HTML source code from the given URL
        :param url: URL to get the source from.
    """
    r = requests.get(url)
    if r.status_code != 200:
        sys.stderr.write("! Error {} retrieving url {}".format(r.status_code, url))
        return None

    return r.text


if __name__ == '__main__':
    url = "https://www.resultados-futbol.com/ligue_12017"
    r = download(url)
    lista = []
    lista_apertura = []
    lista_cierre = []
    if r:
        #print(r)
        ruta = "/home/redox/ligas/Ligas/francesa.txt"
        archivo = open(ruta, 'r+')
        archivo.write(r)
        #linea =
        cont = 0
        contap = 0
        contcr = 0

        for rows in archivo:
            lista.append(rows)
            print (rows)

            """regex = re.compile(r'<*?>')
            if regex.search(cadena) != 'none':
                lista_apertura.append(rows)
                print(contap, lista_apertura[contap])
                contap = contap + 1"""


        for fila in lista:
            cadena = lista[cont]
            apertura = cadena.find("<td>")
            print(cadena)
            cierre = cadena.find("</td>")
            if apertura != -1:
                lista_apertura.append(fila)
                print(contap, lista_apertura[contap])
                #print(contcr, lista_cierre[contcr])
                contcr = contcr + 1

           # print(cont, lista[cont])
            cont = cont + 1

        archivo.close()
        #sys.stdout.write(r[:200])
    #else:
     #   sys.stdout.write("Nothing was retrieved.")
