from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'ind ettx'


@app.route('/test')
def tset():
    pass

#   Kompatybilnosc z uruchomieniem przez python
if __name__ == '__main__':
    app.run()