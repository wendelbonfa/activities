# -*- coding: utf-8 -*-
import os
import sqlite3
from logs import logger

class DBManager(object):
    u"""
        Manager do banco de dados sqlite 
    """

    def __init__(self, log=None):
        u"""Initialize internal  dictionaries."""
        
        # pega o coaminho onde a aplicaçãoesta executando para 
        #localizar o banco de dados
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(BASE_DIR, 'sqlite.db')
        
        # Inicia coneção do sql
        try:
            self._db = sqlite3.connect(self.db_path)
            self._cur = self._db.cursor()
        except Exception as err:  
            logger.error(f'Erro na conexão com o banco: {err}')


    def __del__(self):
        u"""
            limpa recursos do rbanco de dados
        """
        self._cur.close()
        self._db.close()          


    def exec_query(self, sql, fetch=True, commit=False):
        u"""
            Rotina genérica de consulta.
        :param sql: Contém a string com a instrução sql a ser executada
        :param fetch: define se o fetch será executado ou não
        :param commit: define a execuão será de commit
        """
        try:            
            result = self.query(sql, fetch=fetch, commit=commit)
        except:
            self.restablish_db_connection()
            raise
        if result:
            return result
        else:
            return []


    def query(self, sql, fetch=True, commit=False, dictret=False, many=0):
        u"""
            executa query passada como parâmetros retornando 
            possiveis resultados.
        :param sql: Contém a string com a instrução sql a ser executada
        :param fetch: define se o fetch será executado ou não
        :param commit: define a execuão será de commit
        :param dictret: define se o retorno será um um dicionário
        :return: resultados da consulta, se fetch verdadeiro
        """        
        self._cur = self._db.cursor()
        try:
            if many:
                self._cur.executemany(sql, many)
            else:
                self._cur.execute(sql)

            if fetch:
                return self._cur.fetchall()
        finally:
            if commit:
                self._db.commit()


    def restablish_db_connection(self):
        u"""
            Restabelece conexão global com banco de dados.
        """
        try:
            retries = 3
            while retries > 0:
                try:
                    if self._db:
                        self._db.close()
                        break
                except:
                    pass

                self._db.connect(self.db_path)
        except Exception as err:  
            logger.error(f'Erro na reconexão com o banco: {err}')              

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
            self._cur.execute(query)
            self._db.commit()
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
            return self.exec_query(query) or []   
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
            return self.exec_query(query) or []   
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
            self._cur.execute(query)
            self._db.commit() 
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
VALUES ('{guild_id}','{member_id}','{last_notify}','{next_notify}','{context}')"""
            self._cur.execute(query)
            self._db.commit()
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
UPDATE notified set last_notify = '{last_notify}', next_notify = '{next_notify}'
WHERE guild_id = '{guild_id}' AND member_id = '{member_id}' AND context = '{context}'"""
            self._cur.execute(query)
            self._db.commit() 
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
            return self.exec_query(query) or []   
        except Exception as e:                 
            logger.error(f'selection notified erro: {e}')       

    def select_all_notified(self):
        u"""
            seleciona todos usuário que serão checados e notificados
        """
        try:
            query = f"""SELECT guild_id, member_id, last_notify, next_notify, context from notified"""
            return self.exec_query(query) or []   
        except Exception as e:                 
            logger.error(f'selection notified erro: {e}')    