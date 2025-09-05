from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
# Configuração do banco de dados
engine = create_engine('sqlite:///BancoRoyal.db', connect_args={"check_same_thread": False})
local_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


class Lanche(Base):
    __tablename__ = 'lanches'
    id_lanche = Column(Integer, primary_key=True)
    nome_lanche = Column(String(20), nullable=False, index=True)
    descricao_lanche = Column(String(255), index=True)
    valor_lanche = Column(Float, index=True)
    disponivel = Column(Boolean, default=True, index=True)

    def __repr__(self):
        return '<Lanche: {} {}>'.format(self.id_lanche, self.nome_lanche)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def delete(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def serialize(self):
        var_lanche = {
            'id_lanche': self.id_lanche,
            'nome_lanche': self.nome_lanche,
            'descricao_lanche': self.descricao_lanche,
            'disponivel': self.disponivel,
            'valor_lanche': self.valor_lanche,
        }
        return var_lanche

class Insumo(Base):
    __tablename__ = 'insumos'
    id_insumo = Column(Integer, primary_key=True)
    nome_insumo = Column(String(20), nullable=False, index=True)
    qtde_insumo = Column(Integer, nullable=False, index=True)
    validade = Column(String(10), index=True)
    categoria_id = Column(Integer, ForeignKey('categorias.id_categoria'), nullable=False)

    def __repr__(self):
        return '<Insumo: {} {}>'.format(self.id_insumo, self.nome_insumo)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def delete(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def serialize(self):
        var_insumo = {
            'id_insumo': self.id_insumo,
            'nome_insumo': self.nome_insumo,
            'qtde_insumo': self.qtde_insumo,
            'validade': self.validade,
            'categoria_id': self.categoria_id,
        }
        return var_insumo

class Categoria(Base):
    __tablename__ = 'categorias'
    id_categoria= Column(Integer, primary_key=True)
    nome_categoria = Column(String(20), nullable=False, index=True)

    def __repr__(self):
        return '<Categoria: {} {}>'.format(self.id_categoria, self.nome_categoria)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def delete(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def serialize(self):
        var_categoria = {
            'id_categoria': self.id_categoria,
            'nome_categoria': self.nome_categoria,
        }
        return var_categoria

class Venda(Base):
    __tablename__ = 'vendas'
    id_venda = Column(Integer, primary_key=True)
    data_venda = Column(String(10), nullable=False, index=True)
    valor_venda = Column(Float, nullable=False, index=True)
    status_concluida = Column(Boolean, default=True, index=True)

    def __repr__(self):
        return '<Venda: {} {}>'.format(self.id_venda, self.data_venda)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def delete(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def serialize(self):
        var_venda = {
            'id_venda': self.id_venda,
            'data_venda': self.data_venda,
            'valor_venda': self.valor_venda,
            'status_concluida': self.status_concluida,
        }
        return var_venda

class Entrada(Base):
    __tablename__ = 'entradas'
    id_entrada = Column(Integer, primary_key=True)
    data_entrada = Column(String(10), nullable=False, index=True)
    valor_entrada = Column(Float, nullable=False, index=True)
    qtde_entrada = Column(Integer, nullable=False, index=True)
    validade_lote = Column(String(10), nullable=False, index=True)

    def __repr__(self):
        return '<Entrada: {} {}>'.format(self.id_entrada, self.data_entrada)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def delete(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def serialize(self):
        var_entrada = {
            'id_entrada': self.id_entrada,
            'data_entrada': self.data_entrada,
            'valor_entrada': self.valor_entrada,
            'qtde_entrada': self.qtde_entrada,
            'validade_lote': self.validade_lote,
        }
        return var_entrada

class Pessoa(Base):
    __tablename__ = 'pessoas'
    id_pessoa = Column(Integer, primary_key=True)
    nome_pessoa = Column(String(20), nullable=False, index=True)
    cpf = Column(String(11), nullable=False, index=True)
    salario = Column(Float, nullable=False, index=True)
    papel = Column(String(20), nullable=False, index=True)
    status_ativo = Column(Boolean, default=True, index=True)
    senha_hash = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)


    def __repr__(self):
        return 'Pessoa: {} {}>'.format(self.id_pessoa, self.nome_pessoa)

    def set_senha_hash(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def delete(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def serialize(self):
        var_pessoa = {
            'id_pessoa': self.id_pessoa,
            'nome_pessoa': self.nome_pessoa,
            'cpf': self.cpf,
            'salario': self.salario,
            'papel': self.papel,
            'status_ativo': self.status_ativo,
            'email': self.email,

        }
        return var_pessoa

def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()