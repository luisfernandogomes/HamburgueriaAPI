from sqlalchemy import create_engine, Column, Integer, String, Boolean
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
    disponivel = Column(Boolean, default=False, index=True)

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

def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()