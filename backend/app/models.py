from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Aula(db.Model):
    __tablename__ = 'planos_aula'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False) # 
    disciplina = db.Column(db.String(100), nullable=False) # 
    objetivo = db.Column(db.Text, nullable=False) # 
    ementa = db.Column(db.Text, nullable=False) # 
    data_prevista = db.Column(db.Date, nullable=False) # 
    conteudos = db.Column(db.Text) # 
    recursos_apoio = db.Column(db.Text) # 
    tags = db.Column(db.String(255)) # [cite: 12, 16]
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow) # 

    def __repr__(self):
        return f'<Aula {self.titulo}>'