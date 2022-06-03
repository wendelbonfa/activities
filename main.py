import os
import discord
import pytz
import asyncio
import db_manager
from dotenv import load_dotenv

# Carrega variáveis de ambiente para utilização no script
load_dotenv()

from discord.ext import commands
from datetime import datetime, timedelta
from logs import logger

loop = asyncio.get_event_loop()

# discord token activities daily
DAILY_TOKEN = os.getenv("DAILY")
# discord token activities weekly
WEEKLY_TOKEN = os.getenv("WEEKLY")

# cria conexão com banco de dados
# Carregar Configurações de Conexão
DB_HOST = os.getenv("DB_HOST") 
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWD = os.getenv("DB_PASSWD") 

# ajuda a adicionar os dias para notificação semanal quando checkado na mensagem
COUNT_DAYS_WEEKLY = {
    0: 1,
    1: 7,
    2: 6,
    3: 5,
    4: 4,
    5: 3,
    6: 2
}

# nome do projeto
PROJ_NAME = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

# Abre a conexão com o banco de dado
conn = db_manager.DbManager( 
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWD
    )

# pega o timezone America São paulo
tz = pytz.timezone('America/Sao_Paulo')   

# padrão de comando aceito pelo bot
bot_weekly = commands.Bot(command_prefix="!") 
bot_daily = commands.Bot(command_prefix="!!") 


@bot_weekly.command()
async def test(message):
    f"""
        Função que recebe comando !test do discord e retorna string
    :param message: mensagem recebida do discord
    :return: I'm alive
    """
    await message.send(f"I'm alive") 
 

@bot_weekly.command()
async def activate(message):
    f"""
        Função que recebe comando !test do discord e retorna string
    :param message: mensagem recebida do discord
    :return: I'm alive
    """
    try:
        # monta a mensagem de ativação do bot
        embed=discord.Embed(title="Atividades", description="✅ Atividades Diárias. \n☑️ Atividades Semanais.", color=0xFF5733)
        sent_message = await message.send(embed=embed)
        # envia as reações do bots
        await sent_message.add_reaction('✅')
        await sent_message.add_reaction('☑️')
        # testa se o registro ja existe no banco
        if len(conn.select_guild(message.guild.id)) == 0:
            # se não existe cria
            conn.insert_guild(message.guild.id, message.channel.id, sent_message.id)
        else:
            # se não existe atualiza
            conn.update_guild(message.guild.id, message.channel.id, sent_message.id)
    except Exception as err:
        logger.error(f'Erro na função de ativação: {err} guild: {message.guild.id}, channel: {message.channel.id}, message: {sent_message.id}')  


async def send_discord_pm_daily(user):
    u"""
      Função de envio das notificação com a tarefas diária
    :param user: usuário a ser notificado
    :return: None
    """
    try:
        now = datetime.now()-timedelta(hours=3) 
        notify_time = '{:02d}/{:02d}/{:04d} {:02d}:{:02d}'.format(
          now.day, now.month, now.year, now.hour, now.minute
        )    
        msg = "ESSAS SÃO AS ATIVIDADES DO DIA: {}".format(notify_time) 
        await user.send(msg)
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez as roletas diárias" 
        await user.send(msg)
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez Mini Cactpot" 
        await user.send(msg)   
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez Beast Tribes" 
        await user.send(msg)                 
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez Treasure Map" 
        await user.send(msg)   
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez Adventure Squadron's" 
        await user.send(msg)  
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez Retainer Adventure" 
        await user.send(msg) 
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já molhou/plantou as plantas" 
        await user.send(msg) 
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez a Free Company voyage" 
        await user.send(msg) 
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já zerou as Levequest Allowance" 
        await user.send(msg)  
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já as entregas da Grand Company de Craft/Gather" 
        await user.send(msg) 
    except Exception as err:
        logger.error(f'Erro na função de envio diário: {err} user: {user}')          


async def send_discord_pm_weekly(user):
    u"""
      Função de envio das notificação com a tarefas semanais
    :param user: usuário a ser notificado
    :return: None
    """
    try:
        now = datetime.now()-timedelta(hours=3) 
        notify_time = '{:02d}/{:02d}/{:04d} {:02d}:{:02d}'.format(
          now.day, now.month, now.year, now.hour, now.minute
        )    
        msg = "ESSAS SÃO AS ATIVIDADES DA SEMANA: {}".format(notify_time)   
        await user.send(msg)
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já pegou e com :ballot_box_with_check: se entregou seu Wondrous Tails" 
        await user.send(msg)      
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez suas Custom Deliveries"
        await user.send(msg)                
        msg = f"Reaja com :zombie: P1S, :horse: P2S, :bird: P3S, :vampire: P4S nesta mensagem se você já fez suas Raids Savages"
        await user.send(msg)                    
        msg = f"Reaja com :white_check_mark: para tell e :ballot_box_with_check: par retell nesta mensagem se você já fez a Unreal Trial - Ultima's Bane"
        await user.send(msg)
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez a Alliance Raids (Aglaia)"
        await user.send(msg)                   
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez a Squadron's Mission"
        await user.send(msg)               
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já farmou seus 450 Allagan Tomestone of Astronomy"
        await user.send(msg)            
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez Fashion Report aconselhável domingo pois o Buff da FC Jackpot II estará ativo"
        await user.send(msg)            
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez Jumbo cactpot aconselhável domingo pois o Buff da FC Jackpot II estará ativo"
        await user.send(msg)                 
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez Challenge Log Eureka"
        await user.send(msg)                    
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez Triple Triade Tournament"
        await user.send(msg)             
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez Lord of Verminion Tournament"
        await user.send(msg)                  
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez Doman Enclave"
        await user.send(msg)            
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez Masked Carnivale"
        await user.send(msg)                 
        msg = f"Reaja com :white_check_mark: nesta mensagem se você já fez Challenge Log"
        await user.send(msg)   
    except Exception as err:
        logger.error(f'Erro na função de envio semanal: {err} user: {user}')        

  
@bot_weekly.event
async def on_raw_reaction_add(payload):
    u"""
        Função que recebe a reação do usuário na mensagem para ativação do recebimento
    :param payload: mensagem contendo informações da reação e mensagem
    """
    try:
        # avalia se o nome do usuário não é o mesmo do bot
        if payload.member.name != PROJ_NAME:
            # consulta no banco se a guilda existe
            guild_info = conn.select_guild(payload.guild_id)
            # valida se a guilda e a mesma que esta registrada
            if payload.channel_id == int(guild_info[0][1]):  
                # pega a data hora corrente para colocar como ultima notificação
                now = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(tz)
                # se o emoji for :white_check_mark: envia a primeira lista e adiciona no banco para as próximas
                if payload.emoji.name == '✅':
                    # Adiciona o date time da proxima notificação
                    next_date = f'{(now + timedelta(days=1)).strftime("%d/%m/%Y")} 12:00:00'              
                    user = await bot_daily.fetch_user(payload.user_id) 
                    try_times = 5
                    while(True):
                      try:
                        if len(conn.select_notified(payload.guild_id, payload.user_id, 'daily')) == 0:
                            # insere no banco que o usuário ja foi notificado
                            conn.insert_notified(payload.guild_id, payload.user_id, next_date, next_date, 'daily') 
                        else:
                            # insere no banco que o usuário ja foi notificado
                            conn.update_notified(payload.guild_id, payload.user_id, next_date, next_date, 'daily') 
                        break
                      except:
                        await asyncio.sleep(15)
                        try_times = try_times -1
                        if try_times == 0:
                            break                        
                        continue
                    await send_discord_pm_daily(user)
                # se o emoji for :ballot_box_with_check: envia a primeira lista e adiciona no banco para as próximas
                if payload.emoji.name == '☑️': 
                    amount_days = COUNT_DAYS_WEEKLY[now.weekday()]
                    next_date = f'{(now + timedelta(days=amount_days)).strftime("%d/%m/%Y")} 07:00:00'
                    user = await bot_weekly.fetch_user(payload.user_id) 
                    try_times = 5
                    while(True):
                      try:  
                        if len(conn.select_notified(payload.guild_id, payload.user_id, 'weekly')) == 0:
                            # insere no banco que o usuário ja foi notificado
                            conn.insert_notified(payload.guild_id, payload.user_id, next_date, next_date, 'weekly')
                        else:
                            # insere no banco que o usuário ja foi notificado
                            conn.update_notified(payload.guild_id, payload.user_id, next_date, next_date, 'weekly')
                        break
                      except:
                        await asyncio.sleep(15)
                        try_times = try_times -1
                        if try_times == 0:
                            break
                        continue                          
                    await send_discord_pm_weekly(user)     
    except Exception as err:
        logger.error(f'Erro na função de ativação do bot usando reação: {err} guild: {payload.guild_id}, user: {payload.user_id}, reaction: {payload.emoji.name}')                    


@bot_weekly.event
async def on_raw_reaction_remove(payload):
    u"""
        Função que recebe a reação do usuário na mensagem para ativação do recebimento
    :param payload: mensagem contendo informações da reação e mensagem
    """
    try:    
        # consulta no banco se a guilda existe 
        guild_info = conn.select_guild(payload.guild_id)
        if payload.channel_id == int(guild_info[0][1]):  
            if payload.emoji.name == '✅':
                # remove da lista de notificações
                conn.remove_notified(payload.guild_id, payload.user_id, 'daily')
            if payload.emoji.name == '☑️':
                # remove da lista de notificações
                conn.remove_notified(payload.guild_id, payload.user_id, 'weekly')
    except Exception as err:
        logger.error(f'Erro na função de desativação do bot usando reação: {err} guild: {payload.guild_id}, user: {payload.user_id}, reaction: {payload.emoji.name}')                


async def discord_async_method():
    u"""
        Função em loop ifinito para avaliar a data hora e efetuar a notificação
    """
    while True:
        try:
            # aguarda 30 segundos por execução
            await asyncio.sleep(30)
            # pega data hora corrente e converte para america ssão paulo
            now = datetime.now()-timedelta(hours=3)  
            # pega todos usuário que receberam notificação
            users = conn.select_all_notified()
            # faz loop nnos usuários para avaliar quais serão notificados
            for user in users:
                # pega data hora do proximo envio
                next_date = datetime.strptime(user[3], '%d/%m/%Y %H:%M:%S')   
                # Avalia e notifica para diárias
                if user[4] == 'daily':              
                    if next_date <= now:
                        try:
                            # pega usuário do disscord para mandar pm
                            for i in range(1, 5):
                                try:
                                    user_disc = await bot_daily.fetch_user(int(user[1]))
                                    break
                                except:
                                    continue
                            # preenche próxima notificação
                            next_date = f'{(now + timedelta(days=1)).strftime("%d/%m/%Y")} 12:00:00'  
                            # atualiza banco de dados
                            try_times = 5
                            while(True):
                              try:                            
                                conn.update_notified(user[0], user[1], next_date, next_date, 'daily')  
                                break
                              except:
                                await asyncio.sleep(15)
                                try_times = try_times -1
                                if try_times == 0:
                                    break
                                continue                          
                            logger.error(f"proxima: {next_date} now: {now}") 
                            # envia notificação diária
                            await send_discord_pm_daily(user_disc) 
                        except:
                            continue
                if user[4] == 'weekly':
                    if next_date <= now:
                        try:
                            # pega usuário do disscord para mandar pm
                            for i in range(1, 5):
                                try:
                                    user_disc = await bot_weekly.fetch_user(int(user[1]))
                                    break
                                except:
                                    continue                      
                            # preenche próxima notificação
                            amount_days = COUNT_DAYS_WEEKLY[now.weekday()]
                            # atualiza banco de dados
                            next_date = f'{(now + timedelta(days=amount_days)).strftime("%d/%m/%Y")} 07:00:00'
                            try_times = 5
                            while(True):
                              try:                            
                                conn.update_notified(user[0], user[1], next_date, next_date, 'weekly')  
                                break
                              except:
                                await asyncio.sleep(15)
                                try_times = try_times -1
                                if try_times == 0:
                                    break
                                continue
                            # envia notificação semanal
                            await send_discord_pm_weekly(user_disc) 
                        except:
                            continue   
        except Exception as err:
            logger.error(f'Erro loop de checagem para envio de notificação: {err}')                             
            continue


asyncio.get_event_loop().create_task(discord_async_method())

# padrão do replit para deixar a plicação executando
#keep_alive()

# inicializa os bots
# bot_weekly notificações diárias
weekly = loop.create_task(bot_weekly.start(WEEKLY_TOKEN))
# bot_daily notificações diárias
daily = loop.create_task(bot_daily.start(DAILY_TOKEN))
# ativa os bot
running = asyncio.gather(daily, weekly, loop=loop)
#executa em loop infinito
loop.run_until_complete(running)
