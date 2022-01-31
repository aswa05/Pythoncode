
from flask import Flask,render_template, session,url_for,redirect,request,flash
#from flask_mysqldb import MySQL
#import mysql.connector
import pyodbc
from datetime import datetime
import json

conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            "Server=LENOVO;"
            "Database=ChangeRequest;"
            "Trusted_Connection=yes;"
        )
app=Flask(__name__)
#MYSQL CONNECTION

#Loading Home Page
@app.route("/", methods=['GET','POST'])
def login():
    res=None
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']

        
        cur=conn.cursor()
        sql="select * from dbo.login where us_id=? and password=?"
        cur.execute(sql,(username,password))
        res=cur.fetchone()
        print(res)
        
        if res:
            
            return redirect(url_for("changerequest",id=res[0]))
        else:
            flash('Incorrect username and password')

        cur.close()
            

    return render_template("home.html")

@app.route("/Changerequest/<string:id>", methods=['GET','POST'])
def changerequest(id):
    if request.method == 'POST':
        pr_id=request.form['getproject']
        mo_id=request.form['module']
        desc=request.form['desc']
        cur=conn.cursor()
        sql="select cr_id from chgreq order by cr_id desc"
        cur.execute(sql)
        crid=cur.fetchone()
        cr_id=crid[0]+1

        

        now = datetime.now()
        dt = now.strftime("%Y/%m/%d %H:%M:%S")
        cur=conn.cursor()
        sql="insert into chgreq values (?,?,?,?,?,?)"
        cur.execute(sql,(cr_id, pr_id, mo_id, dt, id, desc))
        cur.commit()
        
    cur=conn.cursor()
    sql="select P.pr_name, M.mo_name, CR.cr_desc from projects P, mod M, chgreq CR where P.pr_id=CR.cr_pr_id and M.mo_id=CR.cr_mo_id"
    cur.execute(sql)
    res=cur.fetchall()

    

    return render_template("Changerequest.html", datas=res, id=id)

@app.route("/addChangerequest/<string:id>", methods=['GET','POST'])
def addchangerequest(id):
    res1=None
    cur=conn.cursor()
    sql="select pr_id, pr_name from projects"
    cur.execute(sql)
    res=cur.fetchall()
    if request.method == 'POST' and 'getproject' in request.form:
        pr_id=request.form['getproject']
        return redirect(url_for("addchangerequest1",id=id, pr_id=pr_id))

    return render_template("Addchangerequest.html", project=res, mod=res1, id=id)


@app.route("/addChangerequest1/<string:id>/<int:pr_id>", methods=['GET','POST'])
def addchangerequest1(id,pr_id):
    
    cur=conn.cursor()
    sql="select pr_id, pr_name from projects where pr_id=?"
    cur.execute(sql,pr_id)
    res=cur.fetchall()
    
    cur=conn.cursor()
    sql="select mo_id, mo_name from mod where mo_pr_id=?"
    cur.execute(sql,pr_id)
    res1=cur.fetchall()

    return render_template("Addchangerequest1.html", project=res, mod=res1, id=id)


if(__name__=='__main__'):
    app.secret_key="Aswa123"
    app.run(debug=True)