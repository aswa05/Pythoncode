
from flask import Flask,render_template, session,url_for,redirect,request,flash
#from flask_mysqldb import MySQL
import mysql.connector

app=Flask(__name__)
#MYSQL CONNECTION

#Loading Home Page
@app.route("/", methods=['GET','POST'])
def login():
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']

        conn=mysql.connector.connect(host="localhost",user="root",password="1234",database="database1")
        cur=conn.cursor()
        sql="select * from login where username=%s and password=%s"
        cur.execute(sql,(username,password))
        res=cur.fetchone()
        print(res)
        
        if res:
            
            return redirect(url_for("changerequest",id=res[0]))
        else:
            flash('Incorrect username and password')

            
            

    return render_template("home.html")

@app.route("/Changerequest/<string:id>", methods=['GET','POST'])
def changerequest(id):
    conn=mysql.connector.connect(host="localhost",user="root",password="1234",database="database1")
    cur=conn.cursor()
    sql="select P.pr_name, M.mo_name, CR.cr_desc from projects P, modules M, changerequest CR where P.pr_id=CR.cr_pr_id and M.mo_id=CR.cr_mo_id"
    cur.execute(sql)
    res=cur.fetchall()
    return render_template("Changerequest.html", datas=res, id=id)

@app.route("/addChangerequest/<string:id>", methods=['GET','POST'])
def addchangerequest(id):
    
    return render_template("Addchangerequest.html")

if(__name__=='__main__'):
    app.secret_key="Aswa123"
    app.run(debug=True)