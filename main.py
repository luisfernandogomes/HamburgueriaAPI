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

        if dados_lanche['nome_lanche'] == "" or dados_lanche['descricao_lanche'] == "" or dados_lanche['valor'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
            })

        else:
            nome_lanche = dados_lanche['nome_lanche']
            descricao_lanche = dados_lanche['descricao_lanche']
            valor = dados_lanche['valor']
            form_novo_lanche = Lanche(
                nome_lanche = nome_lanche,
                descricao_lanche = descricao_lanche,
                valor = valor
            )
            print(form_novo_lanche)
            form_novo_lanche.save(db_session)

            resultado = {
                "id_lanche": form_novo_lanche.id_lanche,
                "nome_lanche": nome_lanche,
                "descricao_lanche": descricao_lanche,
                "valor": valor,
                "success":"Cadastrado com sucesso"
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
                "success": "Insumo cadastrado com sucesso"
            }

            return jsonify(resultado), 201

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/vendas', methods=['POST'])
def cadastrar_venda():
    db_session = local_session()
    try:
        dados_venda = request.get_json()

        if not 'valor_venda' in dados_venda or not 'data_venda' in dados_venda or not 'status_concluida' in dados_venda:
            return jsonify({
                "error": "Campo inexistente",
            })
        if dados_venda['valor_venda'] == "" or dados_venda['data_venda'] == "" or dados_venda['status_concluida'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
            })

        else:
            valor_venda = dados_venda['valor_venda']
            data_venda = dados_venda['data_venda']
            status_concluida = dados_venda['status_concluida']

            form_nova_venda = Venda(
                valor_venda = valor_venda,
                data_venda = data_venda,
                status_concluida = status_concluida,
            )
            print(form_nova_venda)
            form_nova_venda.save(db_session)

            resultado = {
                "id_venda": form_nova_venda.id_venda,
                "valor_venda": valor_venda,
                "data_venda": data_venda,
                "status_concluida": status_concluida,
                "success": "venda cadastrada com sucesso",
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
def cadastrar_categoria():
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
                "success": "insumo cadastrado com sucesso",
            }

            return jsonify(resultado), 201
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

# LISTAR (GET)
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

@app.route('/entradas', methods=['GET'])
def listar_entradas():
    db_session = local_session()
    try:
        sql_entradas = select(Entrada)
        resultado_entradas = db_session.execute(sql_entradas).scalars()
        entradas = []
        for n in resultado_entradas:
            entradas.append(n.serialize())
            print(entradas[-1])
        return jsonify({
            "entradas": entradas
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/vendas', methods=['GET'])
def listar_vendas():
    db_session = local_session()
    try:
        sql_vendas = select(Venda)
        venda_resultado = db_session.execute(sql_vendas).scalars()
        vendas = []

        for n in venda_resultado:
            vendas.append(n.serialize())
            print(vendas[-1])
        return jsonify({
            "vendas": vendas
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/pessoas', methods=['GET'])
def listar_pessoas():
    db_session = local_session()
    try:
        sql_pessoa = select(Pessoa)
        resultado_pessoas = db_session.execute(sql_pessoa).scalars()
        pessoas = []
        for n in resultado_pessoas:
            pessoas.append(n.serialize())
            print(pessoas[-1])

        return jsonify({
            "pessoas": pessoas
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/get_insumo_id/<id_insumo>', methods=['GET'])
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

# EDITAR (PUT)
@app.route('/lanches/<id_lanche>', methods=['PUT'])
def editar_lanche(id_lanche):
    db_session = local_session()
    try:
        dados_editar_lanche = request.get_json()

        lanche_resultado = local_session.execute(select(Lanche).filter_by(id=int(id_lanche))).scalar()
        print(lanche_resultado)

        if not lanche_resultado:
            return jsonify({
                "error": "Lanche não encontrado"
            }), 400

        if not 'nome_lanche' in dados_editar_lanche or not 'descricao_lanche' in dados_editar_lanche or not 'disponivel' in dados_editar_lanche:
            return jsonify({
                'error': 'Campo inexistente',
            }), 400

        if dados_editar_lanche['nome_lanche'] == "" or dados_editar_lanche['descricao_lanche'] == "" or \
                dados_editar_lanche['disponivel'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
            }), 400

        else:
            lanche_resultado.nome_lanche = dados_editar_lanche['nome_lanche']
            lanche_resultado.disponivel = dados_editar_lanche['disponivel']
            lanche_resultado.descricao_lanche = dados_editar_lanche['descricao_lanche']

            lanche_resultado.save(db_session)

            resultado = {
                "id_lanche": lanche_resultado.id_lanche,
                "nome_lanche": lanche_resultado.nome_lanche,
                "disponivel": lanche_resultado.disponivel,
                "descricao_lanche": lanche_resultado.descricao_lanche,
                "success": "lanche editado com sucesso"
            }

            return jsonify(resultado), 201

    except ValueError:
        return jsonify({
            "error": "Valor inserido invalido"
        }), 400

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/categorias/<id_categoria>', methods=['PUT'])
def editar_categoria(id_categoria):
    db_session = local_session()
    try:
        dados_editar_categoria = request.get_json()

        categoria_resultado = local_session.execute(select(Categoria).filter_by(id=int(id_categoria))).scalar()
        print(categoria_resultado)

        if not categoria_resultado:
            return jsonify({
                "error":"Categoria não encontrada"
            })

        if not 'nome_categoria' in dados_editar_categoria:
            return jsonify({
                "error":"Campo inexistente"
            }), 400

        if dados_editar_categoria['nome_categoria'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
            }), 400

        else:
            categoria_resultado.nome_categoria = dados_editar_categoria['nome_categoria']

            dados_editar_categoria.save(db_session)

            resultado = {
                "id_categoria": categoria_resultado.id_categoria,
                "nome_categoria": categoria_resultado.nome_categoria,
                "sucesso": "categoria editado com sucesso"
            }

            return jsonify(resultado), 200

    except ValueError:
        return jsonify({
            "error": "Valor inserido invalido"
        }),400

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/pessoas/<id_pessoa>', methods=['PUT'])
def editar_pessoa(id_pessoa):
    db_session = local_session()
    try:
        dados_editar_pessoa = request.get_json()

        pessoa_resultado = local_session.execute(select(Pessoa).filter_by(id=int(id_pessoa))).scalar()
        print(pessoa_resultado)

        if not pessoa_resultado:
            return jsonify({
                "error": "Pessoa não encontrada"
            }), 400

        if not 'nome' in dados_editar_pessoa or not 'salario' in dados_editar_pessoa or not 'cpf' in dados_editar_pessoa or not 'papel' in dados_editar_pessoa or not 'status_ativo' in dados_editar_pessoa:
            return jsonify({
                'error': 'Campo inexistente'
            }), 400

        if dados_editar_pessoa['nome'] == "" or dados_editar_pessoa['salario'] == "" or dados_editar_pessoa['cpf'] == "" or dados_editar_pessoa['status_ativo'] == "" or dados_editar_pessoa['papel'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
            }), 400

        else:
            pessoa_resultado.nome = dados_editar_pessoa['nome']
            pessoa_resultado.salario = dados_editar_pessoa['salario']
            pessoa_resultado.cpf = dados_editar_pessoa['cpf']
            pessoa_resultado.status_ativo = dados_editar_pessoa['status_ativo']
            pessoa_resultado.papel = dados_editar_pessoa['papel']

            pessoa_resultado.save(db_session)

            resultado = {
                "id_pessoa": pessoa_resultado.id_pessoa,
                "nome": pessoa_resultado.nome,
                "salario": pessoa_resultado.salario,
                "status_ativos": pessoa_resultado.status_ativos,
                "cpf": pessoa_resultado.cpf,
                "papel": pessoa_resultado.papel,
                "success": "pessoa editado com sucesso"
            }

            return jsonify(resultado), 200

    except ValueError:
        return jsonify({
            "error": "Valor inserido invalido"
        })

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/insumos/<id_insumo>', methods=['PUT'])
def editar_insumo(id_insumo):
    db_session = local_session()
    try:
        dados_editar_insumo = request.get_json()

        insumo_resultado = local_session.execute(select(Insumo).filter_by(id=int(id_insumo))).scalar()
        print(insumo_resultado)

        if not insumo_resultado:
            return jsonify({
                "error": "Insumo não encontrada"
            }), 400

        if not 'nome_insumo' in dados_editar_insumo or not "qtde_insumo" in dados_editar_insumo or not "validade" in dados_editar_insumo or not "categoria_id" in dados_editar_insumo:
            return jsonify({
                "error": "Campo inexistente"
            }), 400

        if dados_editar_insumo['nome_insumo'] == "" or dados_editar_insumo['qtde_insumo'] == "" or dados_editar_insumo['categoria_id'] == "" or dados_editar_insumo['validade'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
            }), 400

        else:
            insumo_resultado.nome_insumo = dados_editar_insumo['nome_insumo']
            insumo_resultado.categoria_id = dados_editar_insumo['categoria_id']
            insumo_resultado.validade = dados_editar_insumo['validade']
            insumo_resultado.qtde_insumo = dados_editar_insumo['qtde_insumo']

            insumo_resultado.save(db_session)

            resultado = {
                "id_insumo": insumo_resultado.id_insumo,
                "nome_insumo": insumo_resultado.nome_insumo,
                "categoria_id": insumo_resultado.categoria_id,
                "validade": insumo_resultado.validade,
                "qtde_insumo": insumo_resultado.qtde_insumo,
                "success": "insumo editado com sucesso"
            }

            return jsonify(resultado), 200

    except ValueError:
        return jsonify({
            "error": "Valor inserido invalido"
        })

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)