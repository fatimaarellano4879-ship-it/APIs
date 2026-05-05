from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from werkzeug.exceptions import HTTPException, BadRequest, MethodNotAllowed
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required

app = Flask(__name__)

# CONFIGURACION DE SENTRY Y LOGGING
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# CONFIGURACIÓN DE SENTRY
sentry_sdk.init(
    dsn='',
    integrations=[FlaskIntegration()]
)

# CONFIGURACIÓN DE LOGGING
file_handler = logging.FileHandler('errors.log')
file_handler.setLevel(logging.ERROR)
app.logger.addHandler(file_handler)
#----------------------------------

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

# MANEJO DE ERRORES
@app.errorhandler(BadRequest)
def handle_400(e):
    return render_template("400.html"), 400

@app.errorhandler(404)
def handle_404(e):
    return render_template("404.html"), 404

@app.errorhandler(MethodNotAllowed)
def handle_405(e):
    return render_template("405.html"), 405

@app.errorhandler(500)
def handle_500(e):
    return render_template("500.html"), 500

@app.errorhandler(HTTPException)
def handle_api_errors(e):
    if request.path.startswith("/api/"):
        response = e.get_response()
        response.data = jsonify(code=e.code, name=e.name, description=e.description).data
        response.content_type = "application/json"
        return response
    return e

# MANEJADORES DE ERROR
from werkzeug.exceptions import HTTPException, BadRequest, MethodNotAllowed
from flask import jsonify, render_template, request

@app.errorhandler(400)
def handle_400(e):
    return render_template('400.html'), 400

@app.errorhandler(404)
def handle_404(e):
    return render_template('404.html'), 404

@app.errorhandler(405)
def handle_405(e):
    return render_template('405.html'), 405

@app.errorhandler(500)
def handle_500(e):
    return render_template('500.html'), 500

@app.errorhandler(HTTPException)
def handle_api_error(e):
    if request.path.startswith('/api/'):
        response = e.get_response()
        response.data = jsonify(code=e.code, name=e.name, description=e.description).data
        response.content_type = 'application/json'
        return response
    return e
    
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
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    precio = request.form.get("precio")

    if not nombre or not descripcion or not precio:
        from flask import abort
        abort(400)

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

    if id <=0:
        from flask import abort
        abort(400)

    import controlador_juegos
    j = controlador_juegos.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=j)

@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    import controlador_juegos
    controlador_juegos.actualizar_juego(request.form["id"], request.form["nombre"], request.form["descripcion"], request.form["precio"])
    return redirect(url_for("juegos"))

# --- RUTA PARA PROBAR EL ERROR 500 ---
@app.route("/forzar_error")
def forzar_error():
    resultado = 1 / 0 
    return "Esto nunca se mostrará"

if __name__ == "__main__":
    app.run(debug=False)