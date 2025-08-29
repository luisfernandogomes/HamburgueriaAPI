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


@app.route('/cadastrar_insumo', methods=['POST'])
def cadastrar_insumo():

    db_session = local_session()
    try:
        dados_insumo = request.get_json()

        if not 'nome_insumo' in dados_insumo or not 'qtd_insumo' in dados_insumo or not 'validade' in dados_insumo:
            return jsonify({
                "error": "Campo inexistente",
            })

        if dados_insumo['nome_insumo'] == "" or dados_insumo['qtd_insumo'] == "" or dados_insumo['validade'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
        })

        else:
            nome_insumo = dados_insumo['nome_insumo']
            qtd_insumo = dados_insumo['qtd_insumo']
            validade = dados_insumo['validade']
            form_novo_insumo = Insumo(
                nome_insumo = nome_insumo,
                qtde_insumo = qtd_insumo,
                validade = validade,
            )
            print(form_novo_insumo)
            form_novo_insumo.save(db_session)

            resultado = {
                "id_insumo": form_novo_insumo.id_insumo,
                "nome_insumo": nome_insumo,
                "qtde_insumo": qtd_insumo,
            }

            return jsonify(resultado), 201

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()


@app.route('/cadastrar_entrada', methods=['POST'])
def cadastrar_entrada():
    db_session = local_session()
    try:
        dados_entrada = request.get_json()

        if not 'data_entrada' in dados_entrada or not 'valor_entrada' in dados_entrada or not 'qtde_entrada' in dados_entrada or not 'validade_lote' in dados_entrada:
            return jsonify({
                "error": "Campo inexistente",
            })
        if dados_entrada['data_entrada'] == "" or dados_entrada['valor_entrada'] == "" or dados_entrada['qtde_entrada'] == "" or dados_entrada['validade_lote'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
            })
        else:
            data_entrada = dados_entrada['data_entrada']
            valor_entrada = dados_entrada['valor_entrada']
            qtde_entrada = dados_entrada['qtde_entrada']
            validade_lote = dados_entrada['validade_lote']
            form_novo_entrada = Entrada(
                data_entrada = data_entrada,
                valor_entrada = valor_entrada,
                qtde_entrada = qtde_entrada,
            )
            print(form_novo_entrada)
            form_novo_entrada.save(db_session)

            resultado = {
                "id_entrada": form_novo_entrada.id_entrada,
                "valor_entrada": valor_entrada,
                "qtde_entrada": qtde_entrada,
                "validade_lote": validade_lote
            }
            return jsonify(resultado), 201

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()


@app.route('/categoria_insumo', methods=['POST'])
def categoria_insumo():
    db_session = local_session()
    try:
        dados_categoria_insumo = request.get_json()

        if not 'nome_insumo' in dados_categoria_insumo:
            return jsonify({
                "error": "Campo inexistente",
            })
        if dados_categoria_insumo['nome_insumo'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
            })
        else:
            nome_insumo = dados_categoria_insumo['nome_insumo']
            form_novo_insumo = Insumo(
                nome_insumo = nome_insumo,
            )
            print(form_novo_insumo)
            form_novo_insumo.save(db_session)

            resultado = {
                "id_insumo": form_novo_insumo.id_insumo,
                "nome_insumo": nome_insumo,
            }

            return jsonify(resultado), 201
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()


@app.route('/listar_lanches', methods=['GET'])
def listar_lanches():
    db_session = local_session()
    try:

        sql_lanche = select(Lanche)
        resultado_lanches = db_session.execute(sql_lanche).scalars()
        lista_lanches = []

        for n in resultado_lanches:
            lista_lanches.append(n.serialize())
            print(lista_lanches[-1])
        return jsonify({
            "lista_lanches": lista_lanches
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()





if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)