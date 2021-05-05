from flask import Flask, g, render_template,send_file, request, make_response, session, Response, jsonify
from sqlite3 import dbapi2 as sqlite3 #import sqlite3
DATABASE = 'toptraderdb.db'

app = Flask(__name__)
app.secret_key = 'You Will Never Guess '

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
		db.row_factory = sqlite3.Row
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None: db.close()

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

def find_id(ID=''):
	sql = "select * from tb_customers where CUSTOMERS_ID = '%s' limit 1" %(ID)
	#print(sql)
	db = get_db()
	rv = db.execute(sql)
	res = rv.fetchall()
	rv.close()
	return res[0]

def add_customer(ID='', nome='', balance=''):
	sql = "INSERT INTO tb_customers (CUSTOMERS_ID, CUSTOMERS_NAME, CUSTOMERS_BALANCE) VALUES('%s', '%s', %s)" %(ID, nome, balance)
	print(sql)
	db = get_db()
	db.execute(sql)
	res = db.commit()
	return res

@app.route("/json", methods=["POST"])
def json_example():

    if request.is_json:
        req = request.get_json()
        customer = find_id(req.get("CUSTOMERS_ID"))

        response_body = {
            "message": "JSON received with ID POST ok!",
            "CUSTOMERS_ID": customer['CUSTOMERS_ID'],
            "CUSTOMERS_NAME": customer['CUSTOMERS_NAME'],
            "CUSTOMERS_BALANCE":customer['CUSTOMERS_BALANCE']
        }
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/newcustomer')
def new_register():
    return render_template('customer.html')

@app.route('/list')
def list():
   conn = sqlite3.connect("toptraderdb.db")
   conn.row_factory = sqlite3.Row
   cur = conn.cursor()
   cur.execute("select * from tb_customers")

   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         ID = request.form.get('ID')
         nome = request.form.get('nome')
         balance = request.form.get('balance')
         add_customer(ID,nome,balance)
         msg = "Record successfully added"

      except:
         conn.rollback()
         msg = "error in insert operation"

      finally:
         return render_template("result.html", msg = msg)
         conn.close()


@app.route('/createdatabases/')
def createdatabases():

    conn = sqlite3.connect("toptraderdb.db") # ou use :memory: para colocar na memória RAM
    cursor = conn.cursor()

    # cria uma tabela
    cursor.execute("""CREATE TABLE tb_customers
                    (CUSTOMERS_ID text, CUSTOMERS_NAME text, CUSTOMERS_BALANCE text)
                    """)
    conn.commit()

    customers = [('1002', 'John Lennon', '20000'),
             ('1003', 'Paul Mcartney', '30000'),
             ('1004', 'Ringo Star', '40000')]
    cursor.executemany("INSERT INTO tb_customers VALUES (?,?,?)", customers)
    conn.commit()

    return "Database has been created"

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':

    app.run(debug=True, host = '0.0.0.0')
