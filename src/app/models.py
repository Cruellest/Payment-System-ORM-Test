from .db import db

# Define the Usuario model
class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    usuario_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    email = db.Column(db.String(255))
    telefone = db.Column(db.String(20))
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    
    conta_pagamento = db.relationship("ContaPagamento", back_populates="usuario", uselist=False)
    
    def __repr__(self):
        return f"<Usuario {self.nome}>"

# Define the ContaPagamento model
class ContaPagamento(db.Model):
    __tablename__ = 'conta_pagamento'
    
    conta_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'), unique=True)
    saldo = db.Column(db.Numeric(10, 2))
    
    usuario = db.relationship("Usuario", back_populates="conta_pagamento")
    transacoes_origem = db.relationship("Transacao", foreign_keys="Transacao.conta_origem", back_populates="conta_origem_ref")
    transacoes_destino = db.relationship("Transacao", foreign_keys="Transacao.conta_destino", back_populates="conta_destino_ref")
    
    def __repr__(self):
        return f"<ContaPagamento {self.conta_id}>"

# Define the Transacao model
class Transacao(db.Model):
    __tablename__ = 'transacao'
    
    transacao_id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date)
    valor = db.Column(db.Numeric(10, 2))
    tipo = db.Column(db.String(50))
    status = db.Column(db.String(50))
    conta_origem = db.Column(db.Integer, db.ForeignKey('conta_pagamento.conta_id'))
    conta_destino = db.Column(db.Integer, db.ForeignKey('conta_pagamento.conta_id'))
    
    conta_origem_ref = db.relationship("ContaPagamento", foreign_keys=[conta_origem], back_populates="transacoes_origem")
    conta_destino_ref = db.relationship("ContaPagamento", foreign_keys=[conta_destino], back_populates="transacoes_destino")
    metodos_pagamento = db.relationship("TransacaoMetodo", back_populates="transacao")
    
    def __repr__(self):
        return f"<Transacao {self.transacao_id}>"

class TransacaoMetodo(db.Model):
    __tablename__ = 'transacao_metodo'
    
    transacao_id = db.Column(db.Integer, db.ForeignKey('transacao.transacao_id'), primary_key=True)
    metodo_id = db.Column(db.Integer, db.ForeignKey('metodo_pagamento.metodo_id'), primary_key=True)
    
    # Relacionamentos com back_populates
    transacao = db.relationship("Transacao", back_populates="metodos_pagamento")
    metodo_pagamento = db.relationship("MetodoPagamento", back_populates="transacoes")
    
    def __repr__(self):
        return f"<TransacaoMetodo transacao_id={self.transacao_id} metodo_id={self.metodo_id}>"

# Define the MetodoPagamento model
class MetodoPagamento(db.Model):
    __tablename__ = 'metodo_pagamento'
    
    metodo_id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255))
    
    transacoes = db.relationship("TransacaoMetodo", back_populates="metodo_pagamento")
    
    def __repr__(self):
        return f"<MetodoPagamento {self.descricao}>"

