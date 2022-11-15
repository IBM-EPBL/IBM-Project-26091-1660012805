from __future__ import print_function
from flask import Flask, render_template, url_for, request, redirect, session
import sqlite3 as sql
import re
import ibm_db
conn =ibm_db.connect("DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-40d-d791d0218660.bs2io9l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=jpy41264;PWD=dcC5L2PYRESPxhxh",'','')

app=Flask(__name__)
app.secret_key ='shreesathyam'
@app.route('/')
def signin():
    return render_template('signin.html')
@app.route('/retailers')
def retailers():
    return render_template('retailers.html')
@app.route('/products')
def product():
    return render_template('products.html')
@app.route('/low-stock')
def lowStock():
    return render_template('low-stock.html')





@app.route('/user/<id>')
def user_info(id):
    with sql.connect('inventorymanagement.db') as con:
        con.row_factory=sql.row
        cur =con.cursor()
        cur.execute(f'SELECT * FROM register WHERE email="{id}"')
        user = cur.fetchall()
    return render_template("user_info.html", user=user[0])

@app.route('/index',methods =['GET', 'POST'])
def index():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        try:
            un = request.form['username']
            pd = request.form['password_1']
            msg+=un 
            msg+=pd
            sql = "SELECT * FROM register WHERE username =? AND password=?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_para(stmt,1,un)
            msg+='hello'
            ibm_db.bind_para(stmt,2,pd)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            print (account)
            if account:
                session['loggedin'] = True
                session['id'] = account['USERNAME']
                userid=  account['USERNAME']
                session['username'] = account['USERNAME']
                msg = 'Logged in successfully !'
                return render_template('index.html', msg = msg)
        except:
            msg += 'Incorrect username or password !'
    return render_template('index.html')

@app.route('/accessbackend', methods=['POST','GET'])
def accessbackend():
    msg=''
    if request.method == "POST":
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        pno=request.form['pno']
        pw=request.form['password'] 
        sql='SELECT * FROM register WHERE email =?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acnt=ibm_db.fetch_assoc(stmt)
        print(acnt)
            
        if acnt:
            msg='Account already exits!!'
            
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg='Please enter the avalid email address'
        else:
            insert_sql='INSERT INTO register VALUES (?,?,?,?,?)'
            pstmt=ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(pstmt,1,firstname)
            ibm_db.bind_param(pstmt,2,lastname)
            ibm_db.bind_param(pstmt,3,email)
            ibm_db.bind_param(pstmt,4,pno)
            ibm_db.bind_param(pstmt,5,pw)
            ibm_db.execute(pstmt)
            msg='You have successfully registered click signin!!'
            return render_template("retailers.html")    

            
            
         
    elif request.method == 'POST':
        msg="fill out the form first!"
    return render_template("retailers.html")  
 

if __name__ == '__main__':
    app.run(debug=True)
