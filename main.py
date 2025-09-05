from sys import exception
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from datetime import datetime
from models import *
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from functools import wraps



app = Flask (__name__)
app.config['JWT_SECRET_KEY'] = "03050710"
jwt = JWTManager(app)



@app.route('/lanches', methods=['POST'])
def cadastrar_lanche():

    db_session = local_session()
    try:
        dados_lanche = request.get_json()

        if not 'nome_lanche' in dados_lanche or not 'descricao_lanche' in dados_lanche or not 'valor' in dados_lanche:
            return jsonify({
                'error': 'Campo inexistente',
            })

        if dados_lanche['nome_lanche'] == "" or dados_lanche['descricao_lanche'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
            })

        else:
            nome_lanche = dados_lanche['nome_lanche']
            descricao_lanche = dados_lanche['descricao_lanche']
            form_novo_lanche = Lanche(
                nome_lanche = nome_lanche,
                descricao_lanche = descricao_lanche
            )
            print(form_novo_lanche)
            form_novo_lanche.save(db_session)

            resultado = {
                "id_lanche": form_novo_lanche.id_lanche,
                "nome_lanche": nome_lanche,
                "descricao_lanche": descricao_lanche,
            }

            return jsonify(resultado), 201

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/insumos', methods=['POST'])
def cadastrar_insumo():

    db_session = local_session()
    try:
        dados_insumo = request.get_json()

        if not 'nome_insumo' in dados_insumo or not 'qtd_insumo' in dados_insumo or not 'validade' in dados_insumo or not 'categoria_id' in dados_insumo:
            return jsonify({
                "error": "Campo inexistente",
            }), 400

        if dados_insumo['nome_insumo'] == "" or dados_insumo['qtd_insumo'] == "" or dados_insumo['validade'] == "" or dados_insumo['categoria_id'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
        }), 400

        else:
            nome_insumo = dados_insumo['nome_insumo']
            qtd_insumo = dados_insumo['qtd_insumo']
            validade = dados_insumo['validade']
            categoria_id = dados_insumo['categoria_id']
            form_novo_insumo = Insumo(
                nome_insumo = nome_insumo,
                qtde_insumo = qtd_insumo,
                validade = validade,
                categoria_id = categoria_id,
            )
            print(form_novo_insumo)
            form_novo_insumo.save(db_session)

            resultado = {
                "id_insumo": form_novo_insumo.id_insumo,
                "nome_insumo": nome_insumo,
                "qtde_insumo": qtd_insumo,
                "categoria_id": categoria_id,
            }

            return jsonify(resultado), 201

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()


@app.route('/entradas', methods=['POST'])
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


@app.route('/categorias', methods=['POST'])
def listar_categoria():
    db_session = local_session()
    try:
        dados_categoria = request.get_json()

        if not 'nome_insumo' in dados_categoria:
            return jsonify({
                "error": "Campo inexistente",
            })
        if dados_categoria['nome_insumo'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
            })
        else:
            nome_insumo = dados_categoria['nome_insumo']
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


@app.route('/lanches', methods=['GET'])
def listar_lanches():
    db_session = local_session()
    try:

        sql_lanche = select(Lanche)
        resultado_lanches = db_session.execute(sql_lanche).scalars()
        lanches = []

        for n in resultado_lanches:
            lanches.append(n.serialize())
            print(lanches[-1])
        return jsonify({
            "lanches": lanches
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()


@app.route('/insumos', methods=['GET'])
def listar_insumos():
    db_session = local_session()
    try:

        sql_insumos = select(Insumo)
        resultado_insumos = db_session.execute(sql_insumos).scalars()
        insumos = []
        for n in resultado_insumos:
            insumos.append(n.serialize())
            print(insumos[-1])
        return jsonify({
            "insumos": insumos
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()


@app.route('/categorias', methods=['GET'])
def listar_categorias():
    db_session = local_session()
    try:
        sql_categorias = select(Categoria)
        resultado_categorias = db_session.execute(sql_categorias).scalars()
        categorias = []
        for n in resultado_categorias:
            categorias.append(n.serialize())
            print(categorias[-1])
        return jsonify({
            "categorias": categorias
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()



@app.route('/get_insumdo_id/<id_insumo>', methods=['GET'])
def get_insumo_id(id_insumo):
    db_session = local_session()
    try:
        insumo = db_session.execute(select(Insumo).filter_by(id=int(id_insumo))).scalar()

        if not insumo:
            return jsonify({
                "error":"Insumo encontrado"
            })

        return jsonify({
            "sucess": "Insumo encontrado com sucesso",
            "id_insumo": insumo.id_insumo,
            "nome_insumo": insumo.nome_insumo,
            "qtde_insumo": insumo.qtde_insumo,
            "validade": insumo.validade,
            "categoria_id": insumo.categoria_id,
        })
    except Exception as e:
        return jsonify({
            "error": "Valor invalido"
        })
    finally:
        db_session.close()
# @app.route('/editar_lanche/<id_lanche>', methods=['PUT']))
# def editar_lanche(id_lanche):
#     db_session = local_session()
#     try:
#         dados_editar_lanche = request.get_json()
#
#         lanche_resultado = local_session.execute(select(Lanche).filter_by(id=int(id_lanche))).scalar()
#         print(lanche_resultado)
#
#         if not lanche_resultado:
#             return jsonify({
#                 "error": "Lanche não encontrado"
#             }), 400
#
#         if not 'nome_lanche' in dados_editar_lanche or not 'descricao_lanche' in dados_editar_lanche or not 'disponivel' in dados_editar_lanche:
#             return jsonify({
#                 'error': 'Campo inexistente',
#             }), 400
#
#         if dados_editar_lanche['nome_lanche'] == "" or dados_editar_lanche['descricao_lanche'] == "" or \
#                 dados_editar_lanche['disponivel'] == "":
#             return jsonify({
#                 "error": "Preencher todos os campos"
#             }), 400
#
#         else:
#             lanche_resultado.nome_lanche = dados_editar_lanche['nome_lanche']
#             lanche_resultado.disponivel = dados_editar_lanche['disponivel']
#             lanche_resultado.descricao_lanche = dados_editar_lanche['descricao_lanche']
#
#             lanche_resultado.save(db_session)
#
#             resultado = {
#                 "id_lanche": lanche_resultado.id_lanche,
#                 "nome_lanche": lanche_resultado.nome_lanche,
#                 "disponivel": lanche_resultado.disponivel,
#                 "descricao_lanche": lanche_resultado.descricao_lanche,
#                 "success": "lanche editado com sucesso"
#             }
#
#             return jsonify(resultado), 201
#
#     except ValueError:
#         return jsonify({
#             "error": "Valor inserido invalido"
#         }), 400
#
#     except Exception as e:
#         return jsonify({"error": str(e)})
#     finally:
#         db_session.close()


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)