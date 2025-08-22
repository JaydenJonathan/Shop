import os
import flask
import pymongo
import dotenv

dotenv.load_dotenv()

app = flask.Flask(__name__)

#MONGGO_URI = 'MONGGO_URI=mongodb+srv://18193453:qKtldsY4RIMfrFuL@cluster.5pjo4ux.mongodb.net/?retryWrites=true&w=majority&appName=Cluster%'

MONGGO_URI = os.getenv('MONGGO_URI')

client = pymongo.MongoClient(MONGGO_URI)
db = client['shop']
products = db['products']

print(MONGGO_URI)

@app.route('/')
def index():
    #
    items = list(products.find({}, {'_id': 0}))
    p_requests = list(products.find({}, {'request':1}))
    return flask.render_template('index.html', items=items, p_requests=p_requests)

@app.route('/add', methods=['POST'])
def add():
    name = flask.request.form.get('name')
    price = flask.request.form.get('price')
    c_name = flask.request.form.get('c_name')
    if name and price:
        products.insert_one({"name": name, "price": price, 'c_name': c_name})
    return flask.redirect(flask.url_for('index'))

@app.route('/buy', methods=['GET'])
def buy():
    p_n = flask.request.args.get('name')
    if p_n:
        products.insert_one({'request': p_n})
    return flask.redirect(flask.url_for('index'))

@app.route('/cancel', methods=['GET'])
def cancel():
    p_n = flask.request.args.get('name')
    if p_n:
        products.delete_one({'request': p_n})
    return flask.redirect(flask.url_for('index'))

@app.route('/delete', methods=['GET'])
def delete():
    p_n = flask.request.args.get('name')
    c_n = flask.request.args.get('c_name')
    p = flask.request.args.get('price')
    if p_n:
        products.delete_one({'name': p_n, 'c_name': c_n})
    return flask.redirect(flask.url_for('index'))

if __name__ == '__main__':
    app.run(port=8389, debug=True)





