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
    url = "https://www.google.com/search?client=ubuntu&channel=fs&ei=upFwW4ufMLLy5gKPyaOQBQ&q=consultar+resultados+ultima+temporada+liga+espa%C3%B1ola&oq=consultar+resultados+ultima+temporada+liga+es&gs_l=psy-ab.1.0.33i21k1.7103.26476.0.30172.45.39.0.6.6.0.169.5097.0j36.36.0....0...1c.1.64.psy-ab..3.42.5151...0j35i39k1j0i67k1j0i131k1j0i131i67k1j0i20i263k1j0i131i20i263k1j0i13k1j0i13i30k1j0i8i13i30k1j33i22i29i30k1j33i160k1j0i22i30k1.0.zRr94j_KOJY#sie=lg;/g/11c6w1q_2s;2;/m/09gqx;mt;fp;1"
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