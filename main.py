from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required

app = Flask(__name__)

app.config['SECRET_KEY'] = '1234'

# CONFIGURACIÓN DE LA BASE DE DATOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from extensiones import db
db.init_app(app)

# CONFIGURACIÓN DE LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix="/auth")

from api.routes import api_blueprint
app.register_blueprint(api_blueprint, url_prefix="/api")


# RUTAS DE JUEGOS
@app.route("/")
@app.route("/juegos")
@login_required
def juegos():
    import controlador_juegos
    lista_juegos = controlador_juegos.obtener_juegos()
    return render_template("juegos.html", juegos=lista_juegos)

@app.route("/agregar_juego")
@login_required
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
@login_required
def guardar_juego():
    import controlador_juegos
    controlador_juegos.insertar_juego(request.form["nombre"], request.form["descripcion"], request.form["precio"])
    return redirect(url_for("juegos"))

@app.route("/eliminar_juego", methods=["POST"])
@login_required
def eliminar_juego():
    import controlador_juegos
    controlador_juegos.eliminar_juego(request.form["id"])
    return redirect(url_for("juegos"))

@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    import controlador_juegos
    j = controlador_juegos.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=j)

@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    import controlador_juegos
    controlador_juegos.actualizar_juego(request.form["id"], request.form["nombre"], request.form["descripcion"], request.form["precio"])
    return redirect(url_for("juegos"))

if __name__ == "__main__":
    app.run(debug=True)