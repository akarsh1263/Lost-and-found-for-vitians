from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sntest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class SNTest(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    contact=db.Column(db.String(200),nullable=False)
    item=db.Column(db.String(200),nullable=False)
    dater=db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/',methods=['GET','POST'])
def create():
    db.create_all()
    if request.method=='POST':
        name=request.form['name']
        contact=request.form['contact']
        item=request.form['item']
        sntest=SNTest(name=name,contact=contact,item=item)
        db.session.add(sntest)
        db.session.commit()
        return redirect('/')
    all=SNTest.query.all()
    return render_template('index.html')

@app.route('/writing',methods=['GET','POST'])
def writing():
    return render_template('writing.html')

@app.route('/seeup',methods=['GET','POST'])
def seeup():
    all=SNTest.query.all()
    return render_template('seeup.html',all=all)

@app.route('/admin',methods=['GET','POST'])
def admin():
    return render_template('admin.html')

@app.route('/adminlist',methods=['GET','POST'])
def adminlist():
    if request.method=='POST':
        password=request.form['password']
        if password=='ajax1263':
            all=SNTest.query.all()
            return render_template('adminlist.html',all=all)
        else:
            return redirect('/')
    all=SNTest.query.all()
    return render_template('adminlist.html',all=all)

@app.route('/delete/<int:sno>')
def delete(sno):
    rec=SNTest.query.filter_by(sno=sno).first()
    db.session.delete(rec)
    db.session.commit()
    all=SNTest.query.all()
    return redirect('/adminlist')

if __name__=='__main__':
    app.run(debug='true',port=8000)