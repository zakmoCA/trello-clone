from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psychopg2://trello_dev:spameggs123@localhost:5432'

@app.route('/')
def index():
    return 'Hello world!'

if __name__ == '__main__':
    app.run(debug=True)