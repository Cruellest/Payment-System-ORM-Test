import os

"""
    Ao subir o container via compose, as variáveis do postgres serão reconhecidas pelo arquivo `.env`
"""
class Config:
    
    #Usuario da Database
    DB_USER = os.getenv('DB_USER')
    #Senha do usuario da DB
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')    
    #Endereco do Servidor DB
    DB_HOST = os.getenv('DB_HOST', '172.20.0.2')
    #Porta de Conexao ao DB
    DB_PORT = os.getenv('DB_PORT', '3306')
    #Tipo de database
    DB_DATABASE = os.getenv('DB_DATABASE', 'mydb')

    # >>> ORM <<<
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False')
    SECRET_KEY = os.getenv('SECRET_KEY')

    @staticmethod
    def get_database_uri():
        
        DB_TYPE = os.getenv('DB_TYPE','sqlite')
        
        if DB_TYPE == "mysql":
            #Usuario MySQL
            MYSQL_USER = os.getenv('DB_USER', '')
            #Senha MySQL
            MYSQL_PASSWORD = os.getenv('DB_PASSWORD', '')
            #Endereco do Servidor MySQL
            MYSQL_HOST = os.getenv('DB_HOST', 'mysql')
            #Porta de Conexao ao MySQL
            MYSQL_PORT = os.getenv('DB_PORT', '3306')
            #Tipo de database MySQL
            MYSQL_DB = os.getenv('DB_DATABASE', 'mydb')
            return f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        
        elif DB_TYPE == "postgres":
            #Usuario da Database
            POSTGRES_USER = os.getenv('DB_USER')
            #Senha do usuario da DB
            POSTGRES_PASSWORD = os.getenv('DB_PASSWORD', '')    
            #Endereco do Servidor DB
            POSTGRES_HOST = os.getenv('DB_HOST', 'postgres')
            #Porta de Conexao ao DB
            POSTGRES_PORT = os.getenv('DB_PORT', '5432')
            #Tipo de database
            POSTGRES_DB = os.getenv('DB_DATABASE', 'mydb')
            return f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

        else:
            return 'sqlite:///mydb.sqlite3'
    
    SQLALCHEMY_DATABASE_URI = get_database_uri()
        