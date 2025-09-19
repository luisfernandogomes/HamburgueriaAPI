from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from datetime import datetime
from models import *
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "03050710"
jwt = JWTManager(app)

# Login
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        print(f'c_user:{current_user}')
        db = local_session()
        try:
            sql = select(Pessoa).where(Pessoa.email == current_user)
            user = db.execute(sql).scalar()
            print(f'teste admin: {user and user.papel == "admin"} {user.papel}')
            if user and user.papel == "admin":
                return fn(*args, **kwargs)
            return jsonify(msg="Acesso negado: Requer privilégios de administrador"), 403
        finally:
            db.close()
    return wrapper

@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    db_session = local_session()

    try:
        # Verifica se email e senha foram fornecidos
        if not email or not senha:
            return jsonify({'msg': 'Email e senha são obrigatórios'}), 400

        # Consulta o usuário pelo CPF
        sql = select(Pessoa).where(Pessoa.email == email)
        user = db_session.execute(sql).scalar()

        # Verifica se o usuário existe e se a senha está correta
        if user and user.check_password_hash(senha):
            access_token = create_access_token(identity=email)  # Gera o token de acesso
            papel = user.papel  # Obtém o papel do usuário
            nome = user.nome_pessoa  # Obtém o nome do usuário
            print(f"Login bem-sucedido: {nome}, Papel: {papel}")  # Diagnóstico
            return jsonify(access_token=access_token, papel=papel, nome=nome)  # Retorna o nome também

        print("Credenciais inválidas.")  # Diagnóstico
        return jsonify({'msg': 'Credenciais inválidas'}), 401

    finally:
        db_session.close()

@app.route('/cadastro_pessoas_login', methods=['POST'])
def cadastro():
    dados = request.get_json()
    nome_pessoa = dados['nome_pessoa']
    cpf = dados['cpf']
    email = dados['email']
    papel = dados.get('papel', 'cliente')  # padrão vira cliente
    senha = dados['senha']
    salario = dados['salario']

    # 🔹 Sempre força status como "Ativo"
    status_pessoa = "Ativo"

    if not nome_pessoa or not email or not senha:
        return jsonify({"msg": "Nome, Email e senha são obrigatórios"}), 400

    # 🔹 Se o papel for admin → valida CPF
    if papel == "admin":
        if not cpf or len(cpf) != 11 or not cpf.isdigit():
            return jsonify({"msg": "O CPF do admin deve conter exatamente 11 dígitos numéricos."}), 400
    else:
        # 🔹 Se não for admin → ignora CPF e zera para evitar lixo
        cpf = None

    db_session = local_session()
    try:
        # Verificar se o usuário já existe
        user_check = select(Pessoa).where(Pessoa.email == email)
        usuario_existente = db_session.execute(user_check).scalar()

        if usuario_existente:
            return jsonify({"msg": "Usuário já existe"}), 400

        novo_usuario = Pessoa(
            nome_pessoa=nome_pessoa,
            cpf=cpf,
            papel=papel,
            salario=salario,
            status_pessoa=status_pessoa,  # sempre "Ativo"
            email=email
        )
        novo_usuario.set_senha_hash(senha)
        db_session.add(novo_usuario)
        db_session.commit()

        user_id = novo_usuario.id_pessoa
        return jsonify({"msg": "Usuário criado com sucesso", "user_id": user_id}), 201

    except Exception as e:
        db_session.rollback()
        return jsonify({"msg": f"Erro ao registrar usuário: {str(e)}"}), 500
    finally:
        db_session.close()

# Cadastro (POST)
@app.route('/usuarios', methods=['POST'])
def cadastro_usuarios():
    dados = request.get_json()
    nome_pessoa = dados['nome_pessoa']
    email = dados['email']
    papel = dados.get('papel','usuario')
    senha = dados['senha']
    cpf = dados['cpf']
    salario = dados['salario']

    if not nome_pessoa or not email or not senha:
        return jsonify({"msg": "Nome de usuário, email e senha são obrigatórios"}), 400

    banco = local_session()
    try:
        # Verificar se o usuário já existe
        user_check = select(Pessoa).where(Pessoa.nome_pessoa == nome_pessoa)
        usuario_existente = banco.execute(user_check).scalar()

        if usuario_existente:
            return jsonify({"msg": "Usuário já existe"}), 400

        novo_usuario = Pessoa(nome_pessoa=nome_pessoa, email=email, papel=papel)
        novo_usuario.set_senha_hash(senha)
        banco.add(novo_usuario)
        banco.commit()

        user_id = novo_usuario.id_pessoa
        return jsonify({"msg": "Usuário criado com sucesso", "user_id": user_id}), 201
    except Exception as e:
        banco.rollback()
        return jsonify({"msg": f"Erro ao registrar usuário: {str(e)}"}), 500
    finally:
        banco.close()

@app.route('/lanches', methods=['POST'])
def cadastrar_lanche():
    db_session = local_session()
    try:
        dados_lanche = request.get_json()

        campos_obrigatorios = ["nome_lanche", "descricao_lanche", "valor_lanche"]

        if not all(campo in dados_lanche for campo in campos_obrigatorios):
            return jsonify({"error": "Campo inexistente"}), 400

        if any(not dados_lanche[campo] for campo in campos_obrigatorios):
            return jsonify({"error": "Preencher todos os campos"}), 400

        else:
            nome_lanche = dados_lanche['nome_lanche']
            descricao_lanche = dados_lanche['descricao_lanche']
            valor_lanche = dados_lanche['valor_lanche']
            form_novo_lanche = Lanche(
                nome_lanche=nome_lanche,
                descricao_lanche=descricao_lanche,
                valor_lanche=valor_lanche
            )
            print(form_novo_lanche)
            form_novo_lanche.save(db_session)
            dicio = form_novo_lanche.serialize()
            resultado = {"success": "Cadastrado com sucesso", "lanches": dicio}

            return jsonify(resultado), 201

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route("/entradas", methods=["POST"])
def cadastrar_entrada():
    dados = request.json

    # Campos obrigatórios
    campos_obrigatorios = ["insumo_id", "qtd_entrada", "data_entrada", "nota_fiscal", "valor_entrada"]
    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"error": "Campos obrigatórios ausentes"}), 400

    if any(dados[campo] == "" for campo in campos_obrigatorios):
        return jsonify({"error": "Preencha todos os campos"}), 400

    # Verificar se o insumo existe
    insumo = local_session.query(Insumo).filter_by(id_insumo=dados["insumo_id"]).first()
    if not insumo:
        return jsonify({"error": "Insumo não encontrado"}), 404

    # Validações numéricas
    try:
        qtd = int(dados["qtd_entrada"])
        valor = float(dados["valor_entrada"])
    except ValueError:
        return jsonify({"error": "Quantidade e valor devem ser numéricos"}), 400

    if qtd <= 0 or valor <= 0:
        return jsonify({"error": "Quantidade e valor devem ser maiores que zero"}), 400

    # Atualiza o estoque do insumo
    insumo.qtd_insumo += qtd

    # Cria a entrada
    nova_entrada = Entrada(
        nota_fiscal=dados["nota_fiscal"],
        data_entrada=dados["data_entrada"],
        qtd_entrada=qtd,
        valor_entrada=valor,
        insumo_id=insumo.id_insumo
    )

    try:
        nova_entrada.save(local_session)
        insumo.save(local_session)

        return jsonify({
            "success": "Entrada cadastrada com sucesso",
            "entrada": nova_entrada.serialize()
        }), 201

    except Exception as e:
        return jsonify({"error": f"Erro ao salvar entrada: {str(e)}"}), 500

@app.route('/insumos', methods=['POST'])
def cadastrar_insumo():
    db_session = local_session()
    try:
        dados_insumo = request.get_json()

        campos_obrigatorios = ["nome_insumo", "categoria_id"]

        if not all(campo in dados_insumo for campo in campos_obrigatorios):
            return jsonify({"error": "Campo inexistente"}), 400

        if any(not dados_insumo[campo] for campo in campos_obrigatorios):
            return jsonify({"error": "Preencher todos os campos"}), 400

        else:
            form_novo_insumo = Insumo(
                nome_insumo=dados_insumo['nome_insumo'],
                categoria_id=dados_insumo['categoria_id'],
            )
            print(form_novo_insumo)
            form_novo_insumo.save(db_session)

            dicio = form_novo_insumo.serialize()
            resultado = {"success": "Insumo cadastrado com sucesso", "insumos": dicio}

            return jsonify(resultado), 201

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route("/lanche_insumos", methods=["POST"])
def cadastrar_lanche_insumo():
    dados = request.json

    # Verificar campos obrigatórios
    campos_obrigatorios = ["lanche_id", "insumo_id", "qtd_insumo"]
    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"error": "Campos obrigatórios não informados"}), 400

    if any(dados[campo] == "" for campo in campos_obrigatorios):
        return jsonify({"error": "Preencher todos os campos"}), 400

    lanche_id = dados["lanche_id"]
    insumo_id = dados["insumo_id"]
    qtd_insumo = dados["qtd_insumo"]

    # Verificar se o lanche existe
    lanche = local_session.query(Lanche).filter_by(id_lanche=lanche_id).first()
    if not lanche:
        return jsonify({"error": "Lanche não encontrado"}), 404

    # Verificar se o insumo existe
    insumo = local_session.query(Insumo).filter_by(id_insumo=insumo_id).first()
    if not insumo:
        return jsonify({"error": "Insumo não encontrado"}), 404

    # Verificar se esse insumo já está vinculado ao lanche
    ja_existe = local_session.query(Lanche_insumo).filter_by(
        lanche_id=lanche_id, insumo_id=insumo_id
    ).first()

    if ja_existe:
        return jsonify({"error": "Esse insumo já está vinculado a esse lanche"}), 409

    try:
        qtd = int(qtd_insumo)
        if qtd <= 0:
            return jsonify({"error": "Quantidade deve ser maior que zero"}), 400
    except ValueError:
        return jsonify({"error": "Quantidade deve ser numérica"}), 400

    # Criar o vínculo lanche-insumo
    novo_item_receita = Lanche_insumo(
        lanche_id=lanche_id,
        insumo_id=insumo_id,
        qtd_insumo=qtd
    )

    try:
        novo_item_receita.save(local_session)
        return jsonify({
            "success": "Insumo adicionado à receita do lanche com sucesso",
            "lanche_insumo": novo_item_receita.serialize()
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/vendas', methods=['POST'])
def cadastrar_venda():
    db_session = local_session()
    try:
        dados = request.get_json()
        campos = ["data_venda", "lanche_id", "pessoa_id", "qtd_lanche"]

        if not all(campo in dados for campo in campos):
            return jsonify({"error": "Campos obrigatórios não informados"}), 400

        lanche_id = dados["lanche_id"]
        pessoa_id = dados["pessoa_id"]
        data_venda = dados["data_venda"]
        qtd_lanche = int(dados["qtd_lanche"])

        observacoes = dados.get("observacoes", {"adicionar": [], "remover": []})

        lanche = db_session.query(Lanche).filter_by(id_lanche=lanche_id).first()
        pessoa = db_session.query(Pessoa).filter_by(id_pessoa=pessoa_id).first()

        if not lanche:
            return jsonify({"error": "Lanche não encontrado"}), 404
        if not pessoa:
            return jsonify({"error": "Pessoa não encontrada"}), 404

        # Receita base do lanche
        receita = db_session.query(Lanche_insumo).filter_by(lanche_id=lanche_id).all()
        if not receita:
            return jsonify({"error": "Esse lanche não tem receita cadastrada"}), 400

        # Montar receita ajustada
        receita_final = {item.insumo_id: item.qtd_insumo for item in receita}

        # Remover insumos
        for rem in observacoes.get("remover", []):
            if rem["insumo_id"] in receita_final:
                receita_final[rem["insumo_id"]] = max(
                    0, receita_final[rem["insumo_id"]] - rem["qtd"]
                )

        # Adicionar insumos extras
        for add in observacoes.get("adicionar", []):
            receita_final[add["insumo_id"]] = receita_final.get(add["insumo_id"], 0) + add["qtd"]

        # Verificar estoque
        for insumo_id, qtd in receita_final.items():
            insumo = db_session.query(Insumo).filter_by(id_insumo=insumo_id).first()
            if not insumo:
                return jsonify({"error": f"Insumo ID {insumo_id} não encontrado"}), 404
            if insumo.qtd_insumo < qtd * qtd_lanche:
                return jsonify({"error": f"Estoque insuficiente para: {insumo.nome_insumo}"}), 400

        # Dar baixa nos insumos
        for insumo_id, qtd in receita_final.items():
            insumo = db_session.query(Insumo).filter_by(id_insumo=insumo_id).first()
            insumo.qtd_insumo -= qtd * qtd_lanche
            db_session.add(insumo)

        # Registrar vendas
        vendas_registradas = []
        for _ in range(qtd_lanche):
            nova_venda = Venda(
                data_venda=data_venda,
                lanche_id=lanche_id,
                pessoa_id=pessoa_id,
                valor_venda=lanche.valor_lanche,
                status_venda=True
            )
            nova_venda.save(db_session)
            vendas_registradas.append(nova_venda.serialize())

        return jsonify({
            "success": f"{qtd_lanche} vendas registradas com sucesso",
            "vendas": vendas_registradas,
            "ajustes_receita": receita_final
        }), 201

    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()

@app.route('/categorias', methods=['POST'])
def cadastrar_categoria():
    db_session = local_session()
    try:
        dados_categoria = request.get_json()

        if not 'nome_categoria' in dados_categoria:
            return jsonify({
                "error": "Campo inexistente",
            })
        if dados_categoria['nome_categoria'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
            })
        else:
            nome_categoria = dados_categoria['nome_categoria']
            form_nova_categoria = Categoria(
                nome_categoria=nome_categoria,
            )
            print(form_nova_categoria)
            form_nova_categoria.save(db_session)

            dicio = form_nova_categoria.serialize()
            resultado = {"success": "Categoria cadastrada com sucesso", "categorias": dicio}

            return jsonify(resultado), 201
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

# LISTAR (GET)
@app.route('/lanches', methods=['GET'])
@jwt_required
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
            "lanches": lanches,
            "success": "Listado com sucesso",
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
            "insumos": insumos,
            "success": "Listado com sucesso",
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/lanche_insumos', methods=['GET'])
def listar_lanche_insumos():
    db_session = local_session()
    try:

        sql_lanche_insumo = select(Lanche_insumo)
        resultado_lanche_insumos = db_session.execute(sql_lanche_insumo).scalars()
        lanche_insumos = []

        for n in resultado_lanche_insumos:
            lanche_insumos.append(n.serialize())
            print(lanche_insumos[-1])
        return jsonify({
            "lanche_insumos": lanche_insumos,
            "success": "Listado com sucesso",
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
            "categorias": categorias,
            "success": "Listado com sucesso",
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
            "entradas": entradas,
            "success": "Listado com sucesso",
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
            "pessoas": pessoas,
            "success": "Listado com sucesso"
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
                "error": "Insumo encontrado"
            })

        return jsonify({
            "success": "Insumo encontrado com sucesso",
            "id_insumo": insumo.id_insumo,
            "nome_insumo": insumo.nome_insumo,
            "qtd_insumo": insumo.qtd_insumo,
            "validade": insumo.validade,
            "categoria_id": insumo.categoria_id,
        })
    except Exception as e:
        return jsonify({
            "error": "Valor inválido"
        })
    finally:
        db_session.close()

# EDITAR (PUT)
@app.route('/lanches/<id_lanche>', methods=['PUT'])
def editar_lanche(id_lanche):
    db_session = local_session()
    try:
        dados_editar_lanche = request.get_json()

        lanche_resultado = db_session.execute(select(Lanche).filter_by(id_lanche=int(id_lanche))).scalar()
        print(lanche_resultado)

        if not lanche_resultado:
            return jsonify({"error": "Lanche não encontrado"}), 400

        campos_obrigatorios = ["nome_lanche", "descricao_lanche", "valor_lanche"]

        if not all(campo in dados_editar_lanche for campo in campos_obrigatorios):
            return jsonify({"error": "Campo inexistente"}), 400

        if any(not dados_editar_lanche[campo] for campo in campos_obrigatorios):
            return jsonify({"error": "Preencher todos os campos"}), 400

        else:
            lanche_resultado.nome_lanche = dados_editar_lanche['nome_lanche']
            lanche_resultado.valor_lanche = dados_editar_lanche['valor_lanche']
            lanche_resultado.descricao_lanche = dados_editar_lanche['descricao_lanche']

            lanche_resultado.save(db_session)
            dicio = lanche_resultado.serialize()
            resultado = {"success": "lanche editado com sucesso", "lanches": dicio}

            return jsonify(resultado), 201

    except ValueError:
        return jsonify({
            "error": "Valor inserido inválido"
        }), 400

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/insumos/<id_insumo>', methods=['PUT'])
def editar_insumo(id_insumo):
    db_session = local_session()
    try:
        dados_editar_insumo = request.get_json()

        insumo_resultado = db_session.execute(select(Insumo).filter_by(id_insumo=int(id_insumo))).scalar()
        print(insumo_resultado)

        if not insumo_resultado:
            return jsonify({"error": "Insumo não encontrado"}), 400

        campos_obrigatorios = ["nome_insumo", "categoria_id"]

        if not all(campo in dados_editar_insumo for campo in campos_obrigatorios):
            return jsonify({"error": "Campo inexistente"}), 400

        if any(not dados_editar_insumo[campo] for campo in campos_obrigatorios):
            return jsonify({"error": "Preencher todos os campos"}), 400

        else:
            insumo_resultado.nome_lanche = dados_editar_insumo['nome_insumo']
            insumo_resultado.categoria_id = dados_editar_insumo['categoria_id']

            insumo_resultado.save(db_session)
            dicio = insumo_resultado.serialize()
            resultado = {"success": "insumo editado com sucesso", "insumos": dicio}

            return jsonify(resultado), 201

    except ValueError:
        return jsonify({
            "error": "Valor inserido inválido"
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

        categoria_resultado = db_session.execute(select(Categoria).filter_by(id_categoria=int(id_categoria))).scalar()
        print(categoria_resultado)

        if not categoria_resultado:
            return jsonify({
                "error": "Categoria não encontrada"
            })

        if not 'nome_categoria' in dados_editar_categoria:
            return jsonify({
                "error": "Campo inexistente"
            }), 400

        if dados_editar_categoria['nome_categoria'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
            }), 400

        else:
            categoria_resultado.nome_categoria = dados_editar_categoria['nome_categoria']

            categoria_resultado.save(db_session)

            dicio = categoria_resultado.serialize()
            resultado = {"success": "categoria editado com sucesso", "categorias": dicio}

            return jsonify(resultado), 200

    except ValueError:
        return jsonify({
            "error": "Valor inserido inválido"
        }), 400

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/pessoas/<id_pessoa>', methods=['PUT'])
def editar_pessoa(id_pessoa):
    db_session = local_session()
    try:
        dados_editar_pessoa = request.get_json()

        pessoa_resultado = db_session.execute(select(Pessoa).filter_by(id_pessoa=int(id_pessoa))).scalar()
        print(pessoa_resultado)

        if not pessoa_resultado:
            return jsonify({"error": "Pessoa não encontrada"}), 400

        campos_obrigatorios = ["nome_pessoa", "cpf", "salario", "papel", "senha_hash", "email"]

        if not all(campo in dados_editar_pessoa for campo in campos_obrigatorios):
            return jsonify({"error": "Campo inexistente"}), 400

        if any(not dados_editar_pessoa[campo] for campo in campos_obrigatorios):
            return jsonify({"error": "Preencher todos os campos"}), 400

        else:
            pessoa_resultado.nome_pessoa = dados_editar_pessoa['nome_pessoa']
            pessoa_resultado.cpf = dados_editar_pessoa['cpf']
            pessoa_resultado.salario = dados_editar_pessoa['salario']
            pessoa_resultado.papel = dados_editar_pessoa['papel']
            pessoa_resultado.senha_hash = dados_editar_pessoa['senha_hash']
            pessoa_resultado.email = dados_editar_pessoa['email']

            pessoa_resultado.save(db_session)

            dicio = pessoa_resultado.serialize()
            resultado = {"success": "Pessoa editada com sucesso", "pessoas": dicio}

            return jsonify(resultado), 200

    except ValueError:
        return jsonify({
            "error": "Valor inserido inválido"
        })

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route("/lanche_insumo", methods=["DELETE"])
def deletar_lanche_insumo():
    dados = request.json

    # Verificação dos campos obrigatórios
    if not dados or "lanche_id" not in dados or "insumo_id" not in dados:
        return jsonify({"error": "Informe 'lanche_id' e 'insumo_id' no corpo da requisição"}), 400

    lanche_id = dados["lanche_id"]
    insumo_id = dados["insumo_id"]

    # Verificar se o vínculo existe
    relacionamento = local_session.query(Lanche_insumo).filter_by(
        lanche_id=lanche_id, insumo_id=insumo_id
    ).first()

    if not relacionamento:
        return jsonify({"error": "Esse insumo não está vinculado a esse lanche"}), 404

    try:
        relacionamento.delete(local_session)
        return jsonify({"success": "Relacionamento removido com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
