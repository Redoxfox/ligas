from flask import Flask
from flask import request

app= Flask(__name__)

@app.route('/')
def index():
  return 'Hola Mundo modificacion True'
#?params=1
@app.route('/params/<name>/')
def params(name):
    return 'El parametro es: {}'.format(name)

if __name__ == '__main__':
    app.run(debug = True, port = 8000)
