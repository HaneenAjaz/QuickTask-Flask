from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno}-{self.title}"


@app.route('/',methods=['GET','POST'])
def hell():
    if request.method=="POST":  #2
        # print(request.form['title'])
        title=request.form['title']
        description=request.form['desc']

        task=Todo(title=title,desc=description)
        db.session.add(task)
        db.session.commit()

    all_todos=Todo.query.all() # Fetch all todo items #1
    return render_template('index.html',todos=all_todos)


@app.route('/delete/<int:sno>')
def delete(sno):
    all_todos=Todo.query.filter_by(sno=sno).first()
    db.session.delete(all_todos)
    db.session.commit()
    # all_todos=Todo.query.all() #update changes
    # return render_template('index.html') -or simply just
    return redirect(url_for('hell'))

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
     if request.method=='POST':
        title=request.form['title'] #updated title fetching
        description=request.form['desc']
        all_todos=Todo.query.filter_by(sno=sno).first()

        all_todos.title=title
        all_todos.desc=description
        db.session.add(all_todos)
        db.session.commit()
        return redirect(url_for('hell'))
        
         
     tds=Todo.query.filter_by(sno=sno).first()
     return render_template('update.html',tds=tds)

           
if __name__ =="__main__":
    app.run(debug=True)