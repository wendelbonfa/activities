# -*- coding: UTF-8 -*-
import logging
import logging.handlers
import os

# diretorio onde esta rodando a aplicação
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# diretório onde o log será encontrado
LOG_FILE = os.path.join(BASE_DIR, u"log.log")

# nivel de log
log_level = logging.INFO

# template da mensagem de log
fmt_template = '%(asctime)s [%(levelname)4s] %(message)s'

# Preparação da infra instrutura do log
logger = logging.getLogger(LOG_FILE)
# cria rotação de log em 3 niveis a cada 10k
log_handler = logging.handlers.RotatingFileHandler(
              logger.name,
              maxBytes=10000,
              backupCount=3)
# formata mensagem de log
log_handler.setFormatter(
    logging.Formatter(
        fmt_template,
        datefmt='%d/%m/%Y %H:%M:%S')
    )
# seta por padrão nivel de log
log_handler.setLevel(log_level)
# adiciona o log no handle
logger.addHandler(log_handler)
# seta por padrão nivel de log
logger.setLevel(log_level)
logger.propagate = False
