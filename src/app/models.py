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
    logs = db.relationship("UsuarioLog", back_populates="usuario")
    
    def __repr__(self):
        return f"<Usuario {self.nome}>"

class UsuarioLog(db.Model):

    __tablename__ = 'usuario_log'
    
    log_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'))
    data = db.Column(db.Date)
    tipo_alteracao = db.Column(db.String(255))

    usuario = db.relationship("Usuario", back_populates="logs")
    
    def __repr__(self):
        return f"<UsuarioLog {self.log_id}>"


# Define the ContaPagamento model
class ContaPagamento(db.Model):
    __tablename__ = 'conta_pagamento'
    
    conta_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'), unique=True)
    saldo = db.Column(db.Numeric(10, 2))
    
    usuario = db.relationship("Usuario", back_populates="conta_pagamento")
    transacoes_origem = db.relationship("Transacao", foreign_keys="Transacao.conta_origem", back_populates="conta_origem_ref")
    transacoes_destino = db.relationship("Transacao", foreign_keys="Transacao.conta_destino", back_populates="conta_destino_ref")
    logs = db.relationship("ContaPagamentoLog", back_populates="conta")
    
    def __repr__(self):
        return f"<ContaPagamento {self.conta_id}>"

class ContaPagamentoLog(db.Model):
    __tablename__ = 'conta_pagamento_log'
    
    log_id = db.Column(db.Integer, primary_key=True)
    conta_id = db.Column(db.Integer, db.ForeignKey('conta_pagamento.conta_id'))
    data = db.Column(db.Date)
    tipo_alteracao = db.Column(db.String(255))
    
    conta = db.relationship("ContaPagamento", back_populates="logs")
    
    def __repr__(self):
        return f"<ContaPagamentoLog {self.log_id}>"


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
    logs = db.relationship("TransacaoLog", back_populates="transacao")

    def __repr__(self):
        return f"<Transacao {self.transacao_id}>"

class TransacaoLog(db.Model):
    __tablename__ = 'transacao_log'
    
    log_id = db.Column(db.Integer, primary_key=True)
    transacao_id = db.Column(db.Integer)
    data = db.Column(db.Date)
    tipo_alteracao = db.Column(db.String(255))

    transacao = db.relationship("Transacao", back_populates="logs")

    def __repr__(self):
        return f"<TransacaoLog {self.log_id}>"


class TransacaoMetodo(db.Model):
    __tablename__ = 'transacao_metodo'
    
    transacao_id = db.Column(db.Integer, db.ForeignKey('transacao.transacao_id'), primary_key=True)
    metodo_id = db.Column(db.Integer, db.ForeignKey('metodo_pagamento.metodo_id'), primary_key=True)
    
    # Relacionamentos com back_populates
    transacao = db.relationship("Transacao", back_populates="metodos_pagamento")
    metodo_pagamento = db.relationship("MetodoPagamento", back_populates="transacoes")

    logs = db.relationship("TransacaoMetodoLog", back_populates="transacao")
    
    def __repr__(self):
        return f"<TransacaoMetodo transacao_id={self.transacao_id} metodo_id={self.metodo_id}>"

class TransacaoMetodoLog(db.Model):
    __tablename__ = 'transacao_metodo_log'
    
    log_id = db.Column(db.Integer, primary_key=True)
    transacao_id = db.Column(db.Integer, db.ForeignKey('transacao.transacao_id'))
    metodo_id = db.Column(db.Integer, db.ForeignKey('metodo_pagamento.metodo_id'))
    data = db.Column(db.Date)
    tipo_alteracao = db.Column(db.String(255))

    transacao = db.relationship("TransacaoMetodo", back_populates="logs")


# Define the MetodoPagamento model
class MetodoPagamento(db.Model):
    __tablename__ = 'metodo_pagamento'
    
    metodo_id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255))
    
    transacoes = db.relationship("TransacaoMetodo", back_populates="metodo_pagamento")
    logs = db.relationship("MetodoPagamentoLog", back_populates="metodo")
    
    def __repr__(self):
        return f"<MetodoPagamento {self.descricao}>"

class MetodoPagamentoLog(db.Model):
    __tablename__ = 'metodo_pagamento_log'
    
    log_id = db.Column(db.Integer, primary_key=True)
    metodo_id = db.Column(db.Integer, db.ForeignKey('metodo_pagamento.metodo_id'))
    data = db.Column(db.Date)
    tipo_alteracao = db.Column(db.String(255))

    metodo = db.relationship("MetodoPagamento", back_populates="logs")

    def __repr__(self):
        return f"<MetodoPagamentoLog {self.log_id}>"