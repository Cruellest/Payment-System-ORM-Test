#!/bin/sh

echo " "
echo "Iniciando a aplicação..."

# WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv

# Verificar se a pasta .venv já existe
if [ -d ".venv" ]; then
    echo " "
    echo ">>> A pasta .venv já existe. >>>"
    echo " "
    source .venv/bin/activate
    echo " "
else
    echo ">>> A pasta .venv não existe. Criando o ambiente virtual... <<<"
    echo " "
    python3 -m venv .venv
    echo " "
    source .venv/bin/activate
    echo " "    
fi

# Verificar se o ambiente virtual está ativado
if [ -z "$VIRTUAL_ENV" ]; then
    echo ">>> Erro: O ambiente virtual não foi ativado. <<<"
    exit 1
fi

# Atualizar o gerenciador de pacotes pip
pip install --upgrade pip

# Instalando dependências
if [ -f "requirements.txt" ]; then
    echo " "
    echo ">>> Instalando dependências... <<<"
    echo " "
    pip install -r requirements.txt
else
    echo " "
    echo ">>> Arquivo requirements.txt não encontrado. Verifique o arquivo requirements.txt. >>>"
fi

echo " "

# Entrar no diretório da aplicação
cd app/

# Iniciar a migração do banco de dados
flask db init
if [ ! -d "migrations" ]; then
    flask db migrate -m "Initial migration"
else
    flask db init
fi
flask db upgrade

echo " "
echo ">>> Servidor será executado em http://localhost:5001 <<<"
echo ">>> O Banco de Dados pode ser encontrado em http://localhost:8080 <<<"
echo ">>> ------------------------------------------------------------- >>>"

# >> Servidor de desenvolvimento 
# Ajustar os caminhos dos modulos para relativo (from .db import db)
flask --app app:app run --host='0.0.0.0' --port 5001 --debugger --reload 
# tail -f /dev/null

# >> Servidor de produção
# Ajustar o caminho dos modulos para absoluto (from app.db import db)
# gunicorn --reload -w 2 -b 0.0.0.0:5001 'app:app' 

echo "Saindo do script..."
echo ">>> ------------------------------------------------------------- >>>"
deactivate
exit 0
