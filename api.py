from flask import Flask, g, render_template,send_file, request, make_response, session, Response
import sqlite3

conn = sqlite3.connect("customersdb.db") # ou use :memory: para colocar na memória RAM
app = Flask(__name__)
app.secret_key = 'You Will Never Guess'

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/enternew')
def new_register():
    return render_template('customer.html')

@app.route('/list')
def list():
   conn = sqlite3.connect("customersdb.db")
   conn.row_factory = sqlite3.Row
   cur = conn.cursor()
   cur.execute("select * from customers")

   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         ID = request.form.get('ID')
         nome = request.form.get('nome')
         balance = request.form.get('balance')
      #try:
         #ID = request.form['ID']
         #Name = request.form['nome']
         #Balance = request.form['balance']

         print(ID+' '+nome+' '+balance);
         #conn = sqlite3.connect('database.db')
         with sqlite3.connect("customersdb.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO customers VALUES (?,?,?)",(ID, nome, balance))
            #cursor.execute("INSERT INTO customers VALUES ('1001', 'Juca Jones', '10000')")
            conn.commit()
            msg = "Record successfully added"
      except:
         conn.rollback()
         msg = "error in insert operation"

      finally:
         return render_template("result.html", msg = msg)
         conn.close()


@app.route('/createdatabases/')
def createdatabases():
    #import sqlite3
    conn = sqlite3.connect("customersdb.db") # ou use :memory: para colocar na memória RAM

    cursor = conn.cursor()

    # cria uma tabela
    cursor.execute("""CREATE TABLE customers
                    (ID text, nome text, balance text)
                    """)
    conn.commit()

    customers = [('1002', 'John Lennon', '20000'),
             ('1003', 'Paul Mcartney', '30000'),
             ('1004', 'Ringo Star', '40000')]
    cursor.executemany("INSERT INTO customers VALUES (?,?,?)", customers)
    conn.commit()

    return conn #render_template('index.html',asset=session['asset'])

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
