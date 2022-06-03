# Bot Discord de envio de atividades diárias e semanais
## Montagem do ambinete de desenvolvimento

Utilize a verão 3.8.13 do python [download](https://www.python.org/downloads/release/python-3813/) após efetuado o downalod efetue a instalação do mesmo.
Baixe o repositório [activities](https://github.com/wendelbonfa/activities)

usando o comando git acesse a aplicação seguindo os comando abaixo

```sh
> git clone https://github.com/wendelbonfa/activities.git
> cd activities
> python -m venv venv
> venv\Scripts\activate
(venv) > pip install -r requirements.txt
```

Crie as chaves dos seus bots em [applications discord](https://discordapp.com/developers/applications/).

Crie também um banco de dados por padrão o bot usa o postgres eu utilizo o [elephantsql](https://www.elephantsql.com/)

Crie as tabelas usando os comando no seu banco de dados conforme SQL's abaixo:

SQL para criar tabela discords.

```sh
-- Table: public.discords

-- DROP TABLE public.discords;

CREATE TABLE IF NOT EXISTS public.discords
(
    channel_id character varying(1000) COLLATE pg_catalog."default",
    guild_id character varying(1000) COLLATE pg_catalog."default",
    msg_id character varying(1000) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.discords
    OWNER to hqelnelu;
```

SQL para criar tabela notified

```sh
-- Table: public.notified

-- DROP TABLE public.notified;

CREATE TABLE IF NOT EXISTS public.notified
(
    next_notify character varying(1000) COLLATE pg_catalog."default",
    guild_id character varying(1000) COLLATE pg_catalog."default",
    member_id character varying(1000) COLLATE pg_catalog."default",
    last_notify character varying(1000) COLLATE pg_catalog."default",
    context character varying(100) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.notified
    OWNER to hqelnelu;
```

Edite o arquivo .env colocando o token do bot gerado no discord para a notificação diária e semanal e as configurações de acesso ao banco.

no mesmo terminal execute o comando com o venv ativo execute.

```sh
(venv) > python mains.py
```
