# -*- coding: UTF-8 -*-
from logs import logger
import psycopg2
import psycopg2.extras
import psycopg2.extensions
from datetime import datetime
import platform

u"""
   Testa se execução é feita no windows ou linux para ativar DEBUG 
"""
if platform.system() == 'Windows':
    u""" ativa modo debug """
    DEBUG = True
else:
    u""" Desativa modo debug """
    DEBUG = False

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)


class DbManager(object):
    """
        Gerenciador da conexão com o banco de dados
    """
    def __init__(self, host, port, dbname, user, pwd):
        """
            inicializador das variáveis
        :param host: IP ou HOST do local onde o banco de dados esta instalado
        :param port: Porta configurado no banco de dados
        :param dbname: Nome do Banco de dados
        :param user: Usuário do banco de dados
        :param pwd: Password do banco de dados
        """
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.pwd = pwd
        self.conn = None
        self.cursor = None
        self.open_connection()

    def open_connection(self):
        u"""
            Abre a conexão com banco de dados
        :return: None
        """
        try:
            self.conn = psycopg2.connect(host=self.host,
                                         port=self.port,
                                         database=self.dbname,
                                         user=self.user,
                                         password=self.pwd)

        except (psycopg2.DatabaseError, psycopg2.OperationalError):
            logger.error(u"Erro ao tentar conexão ao banco de dados.")

    def close_connection(self):
        u"""
            Close a conexão com banco de dados
        :return: None
        """
        try:
            self.conn.close()
        except (psycopg2.DatabaseError, psycopg2.OperationalError):
            logger.error(u"Erro ao tentar fechar conexÃ£o ao banco de dados.")

    def execute_query(self, query, dict_result=False):
        u"""
            Execute sql query no banco de dados
        :return: None
        """
        try:
            if dict_result:
                self.dict_cursor.execute(query)
            else:
                self.cursor.execute(query)
        except Exception as e:
            logger.error(f"Erro: {e}")

    def query(self, sql, fetch=True, commit=False, dict_result=False, many=0):
        u"""
            executa query passada como parâmetros retornando possíveis resultados
        :param sql: query a ser executada
        :param fetch: define se o fetch ser executado ou não
        :param commit: define a execucão de commit
        :param dict_result: define se o retorno será um dicionário
        :param many: define multiplos parâmetros
        :return: resultados da consulta, se fetch com valor 'True'
        """
        rowcount = 0
        try:
            if dict_result:
                self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            else:
                self.cursor = self.conn.cursor()

            if many:
                self.cursor.executemany(sql, many)
            else:
                self.cursor.execute(sql)

            if fetch:
                return self.cursor.fetchall()

            rowcount = self.cursor.rowcount
        except:
            self.restablish_db_connection()

        finally:
            if commit:
                self.conn.commit()
            self.cursor.close()
        return rowcount

    def exec_query(self, sql, *params):
        u"""
            Rotina genérica de consulta.
        :param sql: query a ser executada
        :param params: parâmetros de consulta
        :return: Resultado da consulta
        """
        if params:
            sql_query = sql % params
        else:
            sql_query = sql
        try:
            result = self.query(sql_query, dictret=True)
        except:
            self.restablish_db_connection()
            raise
        if result:
            return result
        else:
            return

    def restablish_db_connection(self):
        u"""
            Restabelece conexão global com banco de dados.
        :return: None
        """
        try:
            if self.conn:
                self.close_connection()
        except Exception as e:
            logger.error(f"Erro: {e}")

        self.open_connection()

    def insert_guild(self, guild_id, channel_id, msg_id):
        u"""
            Registra um novo servidor que será avaliado para notificação
        :param guild_id: Id do server do discord
        :param channel_id: Id do canal do discord 
        :param msg_id: id da mensagem do discord
        """
        try:
            query = f"""
INSERT INTO discords (guild_id, channel_id, msg_id) 
VALUES ('{guild_id}','{channel_id}','{msg_id}')"""            
            self.query(query, fetch=False, commit=True)
        except Exception as e:                 
            logger.error(f'discord server erro: {e}')

  
    def select_guild(self, guild_id):
        u"""
            verifica se a guild ja esta cadastrada
        :param guild_id: Id do server do discord
        """
        try:
            query = f"""
SELECT guild_id, channel_id, msg_id FROM discords 
WHERE guild_id = '{guild_id}'"""      
            results = self.query(query, dict_result=True)
            if results == None:
                return None
            else:
                return results   
        except Exception as e:                 
            logger.error(f'select discord server erro: {e}') 
            return []

    def all_guild(self, guild_id):
        u"""
            pega todos as guilds
        :param guild_id: Id do server do discord
        """
        try:
            query = f"SELECT guild_id, channel_id, msg_id FROM discords"      
            results = self.query(query, dict_result=True)
            if results == None:
                return None
            else:
                return results 
        except Exception as e:                 
            logger.error(f'select discord server erro: {e}') 
            return []             

  
    def update_guild(self, guild_id, channel_id, msg_id):
        u"""
            Faz o update da guild
        :param guild_id: Id do server do discord
        :param channel_id: Id do canal do discord 
        :param msg_id: id da mensagem do discord
        """
        try:
            query = f"""
UPDATE discords set channel_id = {channel_id}, msg_id = {msg_id} 
WHERE guild_id = '{guild_id}'"""
            self.query(query, fetch=False, commit=True)
        except Exception as e:                 
            logger.error(f'update discord server erro: {e}')  

  
    def insert_notified(self, guild_id, member_id, last_notify, next_notify, context):
        u"""
            Registra um membro que será notificado
        :param guild_id: Id do server do discord
        :param member_id: Id do membro do discord 
        :param last_notify: ultima datahora de notificação
        :param next_notify: ultima datahora da proxima notificação
        :param context: contexto da notificação
        """
        try:
            query = f"""
INSERT INTO notified (guild_id, member_id, last_notify, next_notify, context) 
VALUES ('{guild_id}','{member_id}','{next_notify}','{next_notify}','{context}')"""
            self.query(query, fetch=False, commit=True)
        except Exception as e:                 
            logger.error(f'insert notified erro: {e}')

    def remove_notified(self, guild_id, member_id, context):
        u"""
            remove um membro que será notificado
        :param guild_id: Id do server do discord
        :param member_id: Id do membro do discord 
        :param context: contexto da notificação
        """
        try:
            query = f"""
DELETE FROM notified 
WHERE guild_id = '{guild_id}' AND member_id = '{member_id}' AND context = '{context}'"""
            self._cur.execute(query)
            self._db.commit()
        except Exception as e:                 
            logger.error(f'delete notified erro: {e}')  
  
    def update_notified(self, guild_id, member_id, last_notify, next_notify, context):
        u"""
            Update das ultima e próxima notificão
        :param guild_id: Id do server do discord
        :param member_id: Id do membro do discord 
        :param last_notify: datahora d última notificação
        :param next_notify: datahora da proxima notificação
        :param context: contexto da notificação
        """
        try:
            query = f"""
UPDATE notified set last_notify = '{next_notify}', next_notify = '{next_notify}'
WHERE guild_id = '{guild_id}' AND member_id = '{member_id}' AND context = '{context}'"""
            self.query(query, fetch=False, commit=True) 
        except Exception as e:                 
            logger.error(f'update notified erro: {e}')       

    def select_notified(self, guild_id, member_id, context):
        u"""
            Seleciona a mensagem notificada
        :param guild_id: Id do server do discord
        :param member_id: Id do membro do discord 
        :param context: contexto da notificação
        """
        try:
            query = f"""
SELECT guild_id, member_id, last_notify, next_notify, context from notified
WHERE guild_id = '{guild_id}' AND member_id = '{member_id}' AND context = '{context}'"""
            results = self.query(query, dict_result=True)
            if results == None:
                return None
            else:
                return results   
        except Exception as e:                 
            logger.error(f'selection notified erro: {e}')       

    def select_all_notified(self):
        u"""
            seleciona todos usuário que serão checados e notificados
        """
        try:
            query = f"""SELECT guild_id, member_id, last_notify, next_notify, context from notified"""
            results = self.query(query, dict_result=True)
            if results == None:
                return None
            else:
                return results 
        except Exception as e:                 
            logger.error(f'selection notified erro: {e}')            