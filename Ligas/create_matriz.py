
class CreateMatix:
    def matrix(self, fil, col):
        self.fil = fil
        self.col = col
        self.matrix=[]
        for i  in range(self.fil):
            self.matrix.append([0]*self.col)

        return self.matrix

miMatrix = CreateMatix()
print(miMatrix.matrix(100,100))

""" derrota = []
    empate = []
    victoria = []
    empate_eq1 = 0
    victoria_eq1 = 0
    derrota_eq1 = 0
    empate_eq2 = 0
    victoria_eq2 = 0
    derrota_eq2 = 0
    quicksort(A, 0, len(A) - 1)
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

    return render_template('graficos.html', victoria = victoria, empate = empate, derrota = derrota )"""

    <script>
Highcharts.chart('containerx', {
    chart: {
        type: 'column'
    },
    title: {
        text: '{{nombre1}} vs {{nombre2}}'
    },
    xAxis: {
        categories: ['local', 'visitante']
    },dd
    credits: {
        enabled: false
    },
    series: [{
        name: 'victoria',
        data: {{victoria}}
    }, {
        name: 'empates',
        data: {{empate}}
    }, {
        name: 'Derrotas',
        data: {{derrota}}
    }]
});
    </script>