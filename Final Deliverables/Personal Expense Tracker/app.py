# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 14:27:20 2022

@author: user
"""


from flask import Flask,render_template, request,redirect,url_for,session
import ibm_db
import re

app=Flask(__name__)
app.secret_key= 'a'

conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=zbf09733;PWD=dLNuxrT4JZsamhxF",'','')


@app.route('/')

def homer():
    return render_template('home.html')

@app.route('/contact')

def contact():
    return render_template('contact.html')


@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            return render_template('base.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

        

   
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            insert_sql = "INSERT INTO  users VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/Homepage', methods =['GET', 'POST'])
def dash():
    
    return render_template('Homepage.html')


@app.route('/addexpense',methods =['GET', 'POST'])
def addexpense():
     msg = ''
     if request.method == 'POST' :
         username = request.form['username']
         date = request.form['date']
         expensename = request.form['expensename']
         amount = request.form['amount']
         paymode = request.form['paymode']
         category = request.form['category']
         sql = "SELECT * FROM users WHERE username =?"
         stmt = ibm_db.prepare(conn, sql)
         ibm_db.bind_param(stmt,1,username)
         ibm_db.execute(stmt)
         account = ibm_db.fetch_assoc(stmt)
         print(account)
         if account:
            
            
         
            insert_sql = "INSERT INTO  add VALUES (?, ?, ?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, date)
            ibm_db.bind_param(prep_stmt, 3, expensename)
            ibm_db.bind_param(prep_stmt, 4, amount)
            ibm_db.bind_param(prep_stmt, 5, paymode)
            ibm_db.bind_param(prep_stmt, 6, category)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully added'
         else:
            msg = 'Enter correct username !'
       
     elif request.method == 'POST':
         msg = 'Please fill out the form !'
     return render_template('add.html', msg = msg)

@app.route('/delete/<string:id>', methods = ['POST', 'GET' ])
def delete(id):
     print(id)
     sql = "DELETE FROM expenses WHERE  id =?"
     stmt = ibm_db.prepare(conn, sql)
     ibm_db.bind_param(stmt,1,id)
     ibm_db.execute(stmt)
         
     return redirect("/display")

 
    


@app.route('/edit/<id>', methods = ['POST', 'GET' ])
def edit(id):
    

    sql = "SELECT * FROM expenses WHERE  id =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,id)
    ibm_db.execute(stmt)
    row=ibm_db.fetch_tuple(stmt)
   
    print(row)
    return render_template('edit.html', expenses = row)



@app.route("/limitnum" , methods = ['POST' ])
def limitnum():
     if request.method == "POST":
         number= request.form['number']
         
        
         insert_sql = "INSERT INTO  limits VALUES (?, ?)"
         prep_stmt = ibm_db.prepare(conn, insert_sql)
         ibm_db.bind_param(prep_stmt, 1, session['id'])
         ibm_db.bind_param(prep_stmt, 2, number)
         ibm_db.execute(prep_stmt)
         msg = 'You have successfully added'
        
       
     elif request.method == 'POST':
         msg = 'Please fill out the form !'
     return render_template('limitm.html', msg = msg)





   



@app.route("/display")
def display():
    print(session["username"],session['id'])
    
    sql = "SELECT * FROM add WHERE USERID=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,session['id'])
    ibm_db.execute(stmt)
    list1=[]
    row = ibm_db.fetch_tuple(stmt)
    while(row):
        list1.append(row)
        row = ibm_db.fetch_tuple(stmt)
    print(list1)

    total=0
    t_food=0
    t_entertainment=0
    t_business=0
    t_rent=0
    t_EMI=0
    t_other=0
 
     
    for x in list1:
        total += x[4]
        if x[6] == "food":
            t_food += x[4]    
        elif x[6] == "entertainment":
            t_entertainment  += x[4]
        elif x[6] == "business":
            t_business  += x[4]
        elif x[6] == "rent":
            t_rent  += x[4]
        elif x[6] == "EMI":
            t_EMI  += x[4]
        elif x[6] == "other":
            t_other  += x[4]
    

    

    
    return render_template('display.html' ,expense = list1,total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other)
                          
@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('thanks.html')

if __name__ == '__main__':
   app.run(host='0.0.0.0')
    
    