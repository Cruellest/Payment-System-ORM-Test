import os
from app.db import db
from app.api import api
from app.views import CustomModelView
from app.models import Usuario, ContaPagamento, Transacao, MetodoPagamento, TransacaoMetodo
from app.config import Config
from flasgger import Swagger 
from flask_admin import Admin
from flask_migrate import Migrate
from flask import Flask, redirect
from flask_admin.contrib.sqla import ModelView

# >>> Criar a aplicação <<<
def create_app(db=db):
    app = Flask("Trabalho de LBD - Sistema de Pagamentos")
    app.config.from_object(Config)

    # >>> Banco de Dados <<<
    db.init_app(app)
    Migrate(app, db)
    # Registra as tabelas
    with app.app_context():
        db.create_all()

    return app

#App and Database Starter
app = create_app()

#Api Starter
api.init_app(app)

#Swagger Starter
swagger_config = {
    "swagger": "2.0",
    "info": {
        "title": "Payment System API",
        "description": (
            "Bem-vindo à documentação da API! Para gerenciar o banco de dados, "
            "você pode acessar o phpMyAdmin em [phpMyAdmin](http://localhost:8080)."
        ),
        "version": "1.0.0",
    },
    "host": "localhost:5001",
    "basePath": "/",
    "schemes": ["http"],
    "operationId": "getmyData",
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "headers": [
        ("Cache-Control", "no-cache"),        # Evita que os dados sejam armazenados em cache.
        ("Access-Control-Allow-Origin", "*")  # Permite o acesso à API de qualquer origem (CORS aberto).
    ],
    "specs_route": "/apidocs/",
}

swagger = Swagger(app)
# TODO: >>> Verificar pq não funciona:
# swagger = Swagger(app, config=swagger_config) 

#Admin Page Starter
adminPage = Admin(app, name='Admin Page', template_mode="bootstrap4")

#Admin Page Views
adminPage.add_view(CustomModelView(Usuario, db.session))
adminPage.add_view(CustomModelView(ContaPagamento, db.session))
adminPage.add_view(CustomModelView(Transacao, db.session))
adminPage.add_view(CustomModelView(MetodoPagamento, db.session))
adminPage.add_view(CustomModelView(TransacaoMetodo, db.session))

#Routes
@app.route("/")
def home():
    return redirect('/admin')

#Host
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('APP_PORT'), debug=True)
