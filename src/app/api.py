from flask import request, jsonify
from flasgger import swag_from
from flask_restful import Api, Resource
from .models import Usuario, ContaPagamento, Transacao, TransacaoMetodo, MetodoPagamento

api = Api()

#User Table General Listing API
class UsuarioListResource(Resource):
    @swag_from({
        
        'tags': ['Usuário'],
        
        'responses': {
            200: {
                'description': 'Lista de todos os usuários',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'usuario_id': {'type': 'integer'},
                            'nome': {'type': 'string'},
                            'email': {'type': 'string'},
                            'telefone': {'type': 'string'},
                            'cpf': {'type': 'string'}
                        }
                    }
                }
            }
        }
    })
    def get(self):
        usuarios = Usuario.query.all()
        return [
            {
                "usuario_id": u.usuario_id,
                "nome": u.nome,
                "email": u.email,
                "telefone": u.telefone,
                "cpf": u.cpf
            }
            for u in usuarios
        ]
    
    @swag_from({
        
        'tags': ['Usuário'],
        
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'nome': {'type': 'string'},
                        'email': {'type': 'string'},
                        'telefone': {'type': 'string'},
                        'cpf': {'type': 'string'}
                    },
                    'required': ['nome', 'email', 'telefone', 'cpf']
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Usuário criado com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def post(self):
        data = request.get_json()
        usuario = Usuario(
            nome=data['nome'], 
            email=data['email'], 
            telefone=data['telefone'], 
            cpf=data['cpf']
        )
        db.session.add(usuario)
        db.session.commit()
        return {"message": "Usuário criado com sucesso"}, 201

#User Table Detailed API
class UsuarioDetailResource(Resource):
    @swag_from({
        'tags': ['Usuário'],
        'parameters': [
            {
                'name': 'usuario_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID do usuário'
            }
        ],
        'responses': {
            200: {
                'description': 'Detalhes de um usuário',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'usuario_id': {'type': 'integer'},
                        'nome': {'type': 'string'},
                        'email': {'type': 'string'},
                        'telefone': {'type': 'string'},
                        'cpf': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Usuário não encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def get(self, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return {"message": "Usuário não encontrado"}, 404
        return {
            "usuario_id": usuario.usuario_id,
            "nome": usuario.nome,
            "email": usuario.email,
            "telefone": usuario.telefone,
            "cpf": usuario.cpf
        }
    
    @swag_from({
        'tags': ['Usuário'],
        'parameters': [
            {
                'name': 'usuario_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID do usuário a ser atualizado'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'nome': {'type': 'string'},
                        'email': {'type': 'string'},
                        'telefone': {'type': 'string'},
                        'cpf': {'type': 'string'}
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Usuário atualizado com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Usuário não encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def put(self, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return {"message": "Usuário não encontrado"}, 404

        data = request.get_json()
        usuario.nome = data.get('nome', usuario.nome)
        usuario.email = data.get('email', usuario.email)
        usuario.telefone = data.get('telefone', usuario.telefone)
        usuario.cpf = data.get('cpf', usuario.cpf)
        db.session.commit()
        return {"message": "Usuário atualizado com sucesso"}, 200
    
    @swag_from({
        'tags': ['Usuário'],
        'parameters': [
            {
                'name': 'usuario_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID do usuário a ser deletado'
            }
        ],
        'responses': {
            200: {
                'description': 'Usuário deletado com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Usuário não encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def delete(self, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return {"message": "Usuário não encontrado"}, 404
        
        db.session.delete(usuario)
        db.session.commit()
        return {"message": "Usuário deletado com sucesso"}, 200

api.add_resource(UsuarioListResource, "/api/usuarios")
api.add_resource(UsuarioDetailResource, "/api/usuarios/<int:usuario_id>")

#Conta Pagamento Table General Listing API
class ContaPagamentosResourceList(Resource):
    
    @swag_from({
        'tags': ['Conta Pagamento'],
        'parameters': [
            {
                'name': 'conta_id',
                'in': 'path',
                'required': False,
                'type': 'integer',
                'description': 'ID da conta para buscar detalhes específicos'
            }
        ],
        'responses': {
            200: {
                'description': 'List of payment accounts or specific account details',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'conta_id': {'type': 'integer'},
                            'usuario_id': {'type': 'integer'},
                            'saldo': {'type': 'string'},
                            'chaves_relacionadas': {
                                'type': 'object',
                                'properties': {
                                    'transacoes_origem': {
                                        'type': 'array',
                                        'items': {'type': 'integer'}
                                    },
                                    'transacoes_destino': {
                                        'type': 'array',
                                        'items': {'type': 'integer'}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            404: {
                'description': 'Account not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def get(self, conta_id=None):
        if conta_id:
            conta = ContaPagamento.query.get(conta_id)
            if not conta:
                return {"message": "Conta não encontrada"}, 404
            return {
                "conta_id": conta.conta_id,
                "usuario_id": conta.usuario_id,
                "saldo": str(conta.saldo),
                "chaves_relacionadas": {
                    "transacoes_origem": [t.transacao_id for t in conta.transacoes_origem],
                    "transacoes_destino": [t.transacao_id for t in conta.transacoes_destino]
                }
            }
        contas = ContaPagamento.query.all()
        return [
            {
                "conta_id": c.conta_id,
                "usuario_id": c.usuario_id,
                "saldo": str(c.saldo),
                "chaves_relacionadas": {
                    "transacoes_origem": [t.transacao_id for t in c.transacoes_origem],
                    "transacoes_destino": [t.transacao_id for t in c.transacoes_destino]
                }
            }
            for c in contas
        ]

    @swag_from({
        'tags': ['Conta Pagamento'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'usuario_id': {'type': 'integer'},
                        'saldo': {'type': 'string'}
                    },
                    'required': ['usuario_id', 'saldo']
                },
                'description': 'Dados para criar uma nova conta de pagamento'
            }
        ],
        'responses': {
            201: {
                'description': 'Payment account created successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            400: {
                'description': 'Invalid input data',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def post(self):
        data = request.get_json()
        usuario_id = data.get('usuario_id')
        saldo = data.get('saldo')
        
        if not usuario_id or not saldo:
            return {"message": "Missing required fields"}, 400
        
        conta = ContaPagamento(usuario_id=usuario_id, saldo=saldo)
        db.session.add(conta)
        db.session.commit()
        return {"message": "Payment account created successfully"}, 201

#Conta Pagamento Table Detailed API
class ContaPagamentoResourceDetail(Resource):
    @swag_from({
        'tags': ['Conta Pagamento'],
        'parameters': [
            {
                'name': 'conta_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID da conta para buscar detalhes'
            }
        ],
        'responses': {
            200: {
                'description': 'Detalhes da conta de pagamento',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'conta_id': {'type': 'integer'},
                        'usuario_id': {'type': 'integer'},
                        'saldo': {'type': 'string'},
                        'chaves_relacionadas': {
                            'type': 'object',
                            'properties': {
                                'transacoes_origem': {
                                    'type': 'array',
                                    'items': {'type': 'integer'}
                                },
                                'transacoes_destino': {
                                    'type': 'array',
                                    'items': {'type': 'integer'}
                                }
                            }
                        }
                    }
                }
            },
            404: {
                'description': 'Conta não encontrada',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def get(self, conta_id):
        conta = ContaPagamento.query.get(conta_id)
        if not conta:
            return {"message": "Conta não encontrada"}, 404
        return {
            "conta_id": conta.conta_id,
            "usuario_id": conta.usuario_id,
            "saldo": str(conta.saldo),
            "chaves_relacionadas": {
                "transacoes_origem": [t.transacao_id for t in conta.transacoes_origem],
                "transacoes_destino": [t.transacao_id for t in conta.transacoes_destino]
            }
        }

    @swag_from({
        'tags': ['Conta Pagamento'],
        'parameters': [
            {
                'name': 'conta_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID da conta a ser atualizada'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'saldo': {'type': 'string'}
                    },
                    'required': ['saldo']
                },
                'description': 'Dados para atualizar a conta de pagamento'
            }
        ],
        'responses': {
            200: {
                'description': 'Conta de pagamento atualizada com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Conta não encontrada',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def put(self, conta_id):
        conta = ContaPagamento.query.get(conta_id)
        if not conta:
            return {"message": "Conta não encontrada"}, 404
        
        data = request.get_json()
        conta.saldo = data.get('saldo', conta.saldo)
        db.session.commit()
        return {"message": "Conta de pagamento atualizada com sucesso"}, 200

    @swag_from({
        'tags': ['Conta Pagamento'],
        'parameters': [
            {
                'name': 'conta_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID da conta a ser deletada'
            }
        ],
        'responses': {
            200: {
                'description': 'Conta de pagamento deletada com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Conta não encontrada',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def delete(self, conta_id):
        conta = ContaPagamento.query.get(conta_id)
        if not conta:
            return {"message": "Conta não encontrada"}, 404
        
        db.session.delete(conta)
        db.session.commit()
        return {"message": "Conta de pagamento deletada com sucesso"}, 200

api.add_resource(ContaPagamentosResourceList, "/api/contas")
api.add_resource(ContaPagamentoResourceDetail,"/api/contas/<int:conta_id>")

#Transacao Table General Listing API
class TransacaoResourceList(Resource):
    @swag_from({
        'tags': ['Transação'],
        'parameters': [
            {
                'name': 'transacao_id',
                'in': 'path',
                'required': False,
                'type': 'integer',
                'description': 'ID da transação para buscar detalhes (opcional)'
            }
        ],
        'responses': {
            200: {
                'description': 'Lista de transações',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'transacao_id': {'type': 'integer'},
                            'conta_origem_id': {'type': 'integer'},
                            'conta_destino_id': {'type': 'integer'},
                            'valor': {'type': 'string'},
                            'status': {'type': 'string'}
                        }
                    }
                }
            },
            404: {
                'description': 'Transação não encontrada',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def get(self, transacao_id=None):
        if transacao_id:
            transacao = Transacao.query.get(transacao_id)
            if not transacao:
                return {"message": "Transação não encontrada"}, 404
            return {
                "transacao_id": transacao.transacao_id,
                "conta_origem_id": transacao.conta_origem_id,
                "conta_destino_id": transacao.conta_destino_id,
                "valor": str(transacao.valor),
                "status": transacao.status
            }
        transacoes = Transacao.query.all()
        return [
            {
                "transacao_id": t.transacao_id,
                "conta_origem_id": t.conta_origem_id,
                "conta_destino_id": t.conta_destino_id,
                "valor": str(t.valor),
                "status": t.status
            }
            for t in transacoes
        ]

    @swag_from({
        'tags': ['Transação'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'conta_origem_id': {'type': 'integer'},
                        'conta_destino_id': {'type': 'integer'},
                        'valor': {'type': 'string'},
                        'status': {'type': 'string'}
                    },
                    'required': ['conta_origem_id', 'conta_destino_id', 'valor']
                },
                'description': 'Dados da transação a ser criada'
            }
        ],
        'responses': {
            201: {
                'description': 'Transação criada com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            400: {
                'description': 'Dados de entrada inválidos',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def post(self):
        data = request.get_json()
        conta_origem_id = data.get('conta_origem_id')
        conta_destino_id = data.get('conta_destino_id')
        valor = data.get('valor')
        status = data.get('status', 'pendente')  # Status padrão se não fornecido

        if not conta_origem_id or not conta_destino_id or not valor:
            return {"message": "Campos obrigatórios ausentes"}, 400
        
        transacao = Transacao(
            conta_origem_id=conta_origem_id,
            conta_destino_id=conta_destino_id,
            valor=valor,
            status=status
        )
        db.session.add(transacao)
        db.session.commit()
        return {"message": "Transação criada com sucesso"}, 201

#Transacao Table Detailed API
class TransacaoResourceDetail(Resource):
    
    @swag_from({
        'tags': ['Transação'],
        'parameters': [
            {
                'name': 'transacao_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID da transação para buscar detalhes'
            }
        ],
        'responses': {
            200: {
                'description': 'Detalhes da transação',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'transacao_id': {'type': 'integer'},
                        'conta_origem_id': {'type': 'integer'},
                        'conta_destino_id': {'type': 'integer'},
                        'valor': {'type': 'string'},
                        'status': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Transação não encontrada',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def get(self, transacao_id=None):
        if transacao_id:
            transacao = Transacao.query.get(transacao_id)
            if not transacao:
                return {"message": "Transação não encontrada"}, 404
            return {
                "transacao_id": transacao.transacao_id,
                "conta_origem_id": transacao.conta_origem_id,
                "conta_destino_id": transacao.conta_destino_id,
                "valor": str(transacao.valor),
                "status": transacao.status
            }
        transacoes = Transacao.query.all()
        return [
            {
                "transacao_id": t.transacao_id,
                "conta_origem_id": t.conta_origem_id,
                "conta_destino_id": t.conta_destino_id,
                "valor": str(t.valor),
                "status": t.status
            }
            for t in transacoes
        ]
        
    @swag_from({
        'tags': ['Transação'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'string'}
                    }
                },
                'description': 'Dados para atualizar a transação'
            },
            {
                'name': 'transacao_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID da transação a ser atualizada'
            }
        ],
        'responses': {
            200: {
                'description': 'Transação atualizada com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Transação não encontrada',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def put(self, transacao_id):
        transacao = Transacao.query.get(transacao_id)
        if not transacao:
            return {"message": "Transação não encontrada"}, 404
        
        data = request.get_json()
        transacao.status = data.get('status', transacao.status)
        db.session.commit()
        return {"message": "Transação atualizada com sucesso"}, 200
    
    @swag_from({
        'tags': ['Transação'],
        'parameters': [
            {
                'name': 'transacao_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID da transação a ser excluída'
            }
        ],
        'responses': {
            200: {
                'description': 'Transação excluída com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Transação não encontrada',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def delete(self, transacao_id):
        transacao = Transacao.query.get(transacao_id)
        if not transacao:
            return {"message": "Transação não encontrada"}, 404
        
        db.session.delete(transacao)
        db.session.commit()
        return {"message": "Transação excluída com sucesso"}, 200


api.add_resource(TransacaoResourceList, "/api/transacoes")
api.add_resource(TransacaoResourceDetail,"/api/transacoes/<int:transacao_id>")

#Metodo Pagamento Table General Listing API
class MetodoPagamentoResourceList(Resource):
    @swag_from({
        'tags': ['Método de Pagamento'],
        'parameters': [
            {
                'name': 'metodo_id',
                'in': 'path',
                'required': False,
                'type': 'integer',
                'description': 'ID do método de pagamento para buscar detalhes (opcional)'
            }
        ],
        'responses': {
            200: {
                'description': 'Lista de métodos de pagamento ou detalhes de um método específico',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'metodo_id': {'type': 'integer'},
                            'nome': {'type': 'string'},
                            'descricao': {'type': 'string'}
                        }
                    }
                }
            },
            404: {
                'description': 'Método de pagamento não encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def get(self, metodo_id=None):
        if metodo_id:
            metodo = MetodoPagamento.query.get(metodo_id)
            if not metodo:
                return {"message": "Método de pagamento não encontrado"}, 404
            return {
                "metodo_id": metodo.metodo_id,
                "nome": metodo.nome,
                "descricao": metodo.descricao
            }
        metodos = MetodoPagamento.query.all()
        return [
            {
                "metodo_id": m.metodo_id,
                "nome": m.nome,
                "descricao": m.descricao
            }
            for m in metodos
        ]
    
    @swag_from({
        'tags': ['Método de Pagamento'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'nome': {'type': 'string', 'description': 'Nome do método de pagamento'},
                        'descricao': {'type': 'string', 'description': 'Descrição do método de pagamento'}
                    }
                },
                'description': 'Dados para criar um novo método de pagamento'
            }
        ],
        'responses': {
            201: {
                'description': 'Método de pagamento criado com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            400: {
                'description': 'Dados inválidos',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def post(self):
        data = request.get_json()
        nome = data.get('nome')
        descricao = data.get('descricao')

        if not nome or not descricao:
            return {"message": "Campos obrigatórios ausentes"}, 400
        
        metodo = MetodoPagamento(nome=nome, descricao=descricao)
        db.session.add(metodo)
        db.session.commit()
        return {"message": "Método de pagamento criado com sucesso"}, 201

#Metodo Pagamento Table Detailed API
class MetodoPagamentoResourceDetail(Resource):
    @swag_from({
        'tags': ['Método de Pagamento'],
        'parameters': [
            {
                'name': 'metodo_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID do método de pagamento a ser buscado'
            }
        ],
        'responses': {
            200: {
                'description': 'Detalhes do método de pagamento',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'metodo_id': {'type': 'integer'},
                        'nome': {'type': 'string'},
                        'descricao': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Método de pagamento não encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def get(self, metodo_id):
        metodo = MetodoPagamento.query.get(metodo_id)
        if not metodo:
            return {"message": "Método de pagamento não encontrado"}, 404
        return {
            "metodo_id": metodo.metodo_id,
            "nome": metodo.nome,
            "descricao": metodo.descricao
        }
    
    @swag_from({
        'tags': ['Método de Pagamento'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'nome': {'type': 'string', 'description': 'Novo nome do método de pagamento'},
                        'descricao': {'type': 'string', 'description': 'Nova descrição do método de pagamento'}
                    }
                },
                'description': 'Dados para atualizar o método de pagamento'
            },
            {
                'name': 'metodo_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID do método de pagamento a ser atualizado'
            }
        ],
        'responses': {
            200: {
                'description': 'Método de pagamento atualizado com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Método de pagamento não encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def put(self, metodo_id):
        metodo = MetodoPagamento.query.get(metodo_id)
        if not metodo:
            return {"message": "Método de pagamento não encontrado"}, 404
        
        data = request.get_json()
        metodo.nome = data.get('nome', metodo.nome)
        metodo.descricao = data.get('descricao', metodo.descricao)
        db.session.commit()
        return {"message": "Método de pagamento atualizado com sucesso"}, 200
    
    @swag_from({
        'tags': ['Método de Pagamento'],
        'parameters': [
            {
                'name': 'metodo_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID do método de pagamento a ser excluído'
            }
        ],
        'responses': {
            200: {
                'description': 'Método de pagamento excluído com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Método de pagamento não encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def delete(self, metodo_id):
        metodo = MetodoPagamento.query.get(metodo_id)
        if not metodo:
            return {"message": "Método de pagamento não encontrado"}, 404
        
        db.session.delete(metodo)
        db.session.commit()
        return {"message": "Método de pagamento excluído com sucesso"}, 200


api.add_resource(MetodoPagamentoResourceList,"/api/metodos-pagamento")
api.add_resource(MetodoPagamentoResourceDetail, "/api/metodos-pagamento/<int:metodo_id>")

#Transacao_Metodo Table General Listing API
class TransacaoMetodoResourceList(Resource):
    @swag_from({
        'tags': ['Transacao_metodo'],
        'responses': {
            200: {
                'description': 'Lista de métodos de transação',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'transacao_id': {'type': 'integer'},
                            'metodo_id': {'type': 'integer'},
                            'data': {'type': 'string'}
                        }
                    }
                }
            },
            404: {
                'description': 'Método de transação não encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def get(self):
        transacoes_metodo = TransacaoMetodo.query.all()
        return [
            {
                "transacao_id": tm.transacao_id,
                "metodo_id": tm.metodo_id,
                "data": str(tm.data)
            }
            for tm in transacoes_metodo
        ]
    
    @swag_from({
        'tags': ['Transacao_metodo'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'transacao_id': {'type': 'integer'},
                        'metodo_id': {'type': 'integer'},
                        'data': {'type': 'string'}
                    }
                },
                'description': 'Dados para criar um método de transação'
            }
        ],
        'responses': {
            201: {
                'description': 'Método de transação criado com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            400: {
                'description': 'Dados de entrada inválidos',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def post(self):
        data = request.get_json()
        transacao_id = data.get('transacao_id')
        metodo_id = data.get('metodo_id')
        data_transacao = data.get('data')

        if not transacao_id or not metodo_id or not data_transacao:
            return {"message": "Campos obrigatórios ausentes"}, 400
        
        transacao_metodo = TransacaoMetodo(
            transacao_id=transacao_id,
            metodo_id=metodo_id,
            data=data_transacao
        )
        db.session.add(transacao_metodo)
        db.session.commit()
        return {"message": "Método de transação criado com sucesso"}, 201

#Transacao_Metodo Table Detailed API
class TransacaoMetodoResourceDetail(Resource):
    @swag_from({
        'tags': ['Transacao_metodo'],
        'parameters': [
            {
                'name': 'transacao_metodo_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID do método de transação a ser consultado'
            }
        ],
        'responses': {
            200: {
                'description': 'Detalhes do método de transação',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'transacao_id': {'type': 'integer'},
                        'metodo_id': {'type': 'integer'},
                        'data': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Método de transação não encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def get(self, transacao_metodo_id):
        transacao_metodo = TransacaoMetodo.query.get(transacao_metodo_id)
        if not transacao_metodo:
            return {"message": "Método de transação não encontrado"}, 404
        return {
            "transacao_id": transacao_metodo.transacao_id,
            "metodo_id": transacao_metodo.metodo_id,
            "data": str(transacao_metodo.data)
        }
    
    @swag_from({
        'tags': ['Transacao_metodo'],
        'parameters': [
            {
                'name': 'transacao_metodo_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID do método de transação a ser atualizado'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'data': {'type': 'string'}
                    }
                },
                'description': 'Dados para atualizar o método de transação'
            }
        ],
        'responses': {
            200: {
                'description': 'Método de transação atualizado com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Método de transação não encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def put(self, transacao_metodo_id):
        transacao_metodo = TransacaoMetodo.query.get(transacao_metodo_id)
        if not transacao_metodo:
            return {"message": "Método de transação não encontrado"}, 404
        
        data = request.get_json()
        transacao_metodo.data = data.get('data', transacao_metodo.data)
        db.session.commit()
        return {"message": "Método de transação atualizado com sucesso"}, 200
    
    @swag_from({
        'tags': ['Transacao_metodo'],
        'parameters': [
            {
                'name': 'transacao_metodo_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID do método de transação a ser excluído'
            }
        ],
        'responses': {
            200: {
                'description': 'Método de transação excluído com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Método de transação não encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    })
    def delete(self, transacao_metodo_id):
        transacao_metodo = TransacaoMetodo.query.get(transacao_metodo_id)
        if not transacao_metodo:
            return {"message": "Método de transação não encontrado"}, 404
        
        db.session.delete(transacao_metodo)
        db.session.commit()
        return {"message": "Método de transação excluído com sucesso"}, 200


api.add_resource(TransacaoMetodoResourceList, "/api/transacao-metodos")
api.add_resource(TransacaoMetodoResourceDetail,"/api/transacao-metodos/<int:transacao_metodo_id>")
