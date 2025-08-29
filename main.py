from sys import exception
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from datetime import datetime
from models import *
from dateutil.relativedelta import relativedelta
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from functools import wraps



app = Flask (__name__)
app.config['JWT_SECRET_KEY'] = "03050710"
jwt = JWTManager(app)



@app.route('/cadastrar_lanche', methods=['POST'])
def cadastrar_lanche():

    db_session = local_session()
    try:
        dados_lanche = request.get_json()

        if not 'nome_lanche' in dados_lanche or not 'descricao_lanche' in dados_lanche or not 'disponivel' in dados_lanche:
            return jsonify({
                'error': 'Campo inexistente',
            })

        if dados_lanche['nome_lanche'] == "" or dados_lanche['descricao_lanche'] == "" or dados_lanche['disponivel'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
            })

        else:
            nome_lanche = dados_lanche['nome_lanche']
            descricao_lanche = dados_lanche['descricao_lanche']
            disponivel = dados_lanche['disponivel']
            form_novo_lanche = Lanche(
                nome_lanche = nome_lanche,
                descricao_lanche = descricao_lanche,
                disponivel = disponivel,
            )
            print(form_novo_lanche)
            form_novo_lanche.save(db_session)

            resultado = {
                "id_lanche": form_novo_lanche.id_lanche,
                "nome_lanche": nome_lanche,
                "descricao_lanche": descricao_lanche,
                "disponivel": disponivel,
            }

            return jsonify(resultado), 201

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()
