from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# Configuração do banco de dados
engine = create_engine('sqlite:///banco_rb.db', connect_args={"check_same_thread": False})
local_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


class Lanche(Base):
    __tablename__ = 'lanches'
    id_lanche = Column(Integer, primary_key=True)
    nome_lanche = Column(String(20), nullable=False, index=True)
    descricao_lanche = Column(String(255), index=True)
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
        }
        return var_lanche

class Insumo(Base):
    __tablename__ = 'insumos'
    id_insumo = Column(Integer, primary_key=True)
    nome_insumo = Column(String(20), nullable=False, index=True)
    qtde_insumo = Column(Integer, nullable=False, index=True)
    validade = Column(String(10), index=True)

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
        }
        return var_insumo

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


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()