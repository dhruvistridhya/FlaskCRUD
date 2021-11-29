from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(200), nullable = False)
	completed = db.Column(db.Integer, default=0)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Task %r>' % self.id 


@app.route('/',methods=['POST','GET'])
def example():

	if request.method == 'POST':
		content = request.form["content"]
		if content == "":
			return "Enter task description"
		else:
			new_task = Todo(content=content)

			try:
				db.session.add(new_task)
				db.session.commit()
				return redirect('/')
		
			except:
				return "Something went wrong"

	else:
		tasks = Todo.query.order_by(Todo.date_created).all()
		return render_template('home.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete_task(id):
	task = Todo.query.get_or_404(id)
	print("*"*100)
	try:
		print("*"*100)
		db.session.delete(task)
		db.session.commit()
		return redirect('/')
	
	except:
		return "Something went wrong"

@app.route('/update/<int:id>',methods=['POST','GET'])
def update_task(id):
	task = Todo.query.get_or_404(id)

	if request.method == 'POST':
		try:
			print("*"*100)
			task.content = request.form["content"]
			db.session.commit()
			return redirect('/')
		
		except:
			return "Something went wrong"

	else:
		return render_template('update.html',task=task)


if __name__ == "__main__":
	app.run(debug=True)