from flask import Flask
from flask import request

app= Flask(__name__)

@app.route('/')
def index():
  return 'Hola Mundo modificacion True'
#?params=1
@app.route('/params')
def params():
    param = request.args.get('param1', 'no contiene este parametro')
    param_2 = request.args.get('param2', 'no contiene este parametro')
    return 'El parametro es: {} , {}'.format(param, param_2)

if __name__ == '__main__':
    app.run(debug = True, port = 8000)
