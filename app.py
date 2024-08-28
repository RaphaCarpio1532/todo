from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Definir el modelo
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Definir la ruta principal
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error adding task: {e}")  # Imprime el error en la consola para depuración
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks= tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:

        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(f"Error deleting task: {e}")
        return 'There was a problem deleting that task'
    


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error updating task: {e}")
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

    

# Ejecutar el código dentro de un contexto de aplicación si el archivo se ejecuta directamente
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crear las tablas en la base de datos
    app.run(debug=True)

