# Bot Discord de envio de atividaes diárias e semanais
## Montagem do ambinete de desenvolvimento

Utilize a verão 3.8.13 do python [download](https://www.python.org/downloads/release/python-3813/) após efetuado o downalod instale.
Baixe o repositório [activities](https://github.com/wendelbonfa/activities)

Abra um terminal windows dentro da pasta do projeto e execute os comando

```sh
> cd activities
> python -m venv venv
> venv\Scripts\activate
(venv) > pip install -r requirements.txt
```

Crie as chaves dos seus bots em [applications discord](https://discordapp.com/developers/applications/).

Crie também um banco de dados por padrão o bot usa o postgres eu utilizo o [elephantsql](https://www.elephantsql.com/)

crie as tabelas usando os comando no seu banco de dados:

criar tabela discords

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

criar tabela notified

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

edite o arquivo .env colocando o token do bot para a notificação diária e semanal e as configurações de acesso ao banco

no mesmo terminal execute o comando 

```sh
(venv) > python mains.py
```
