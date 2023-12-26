from fastapi import FastAPI, HTTPException
from peewee import Model, CharField, DateField, UUIDField, PostgresqlDatabase
from playhouse.postgres_ext import ArrayField
from pydantic import BaseModel, UUID4
from typing import Optional, List
from uuid import uuid4

# Configuração do banco de dados com Peewee
db = PostgresqlDatabase('rinhadb', user='lutador', password='umasenhasegura', host='db')

class Pessoa(Model):
    id = UUIDField(primary_key=True, default=uuid4)
    apelido = CharField(max_length=32, unique=True, index=True)
    nome = CharField(max_length=100)
    nascimento = DateField()
    stack = ArrayField(CharField, max_length=32)

    class Meta:
        database = db
        table_name = 'pessoas'

# Conectar ao banco de dados
db.connect()
db.create_tables([Pessoa], safe=True)

class PessoaBase(BaseModel):
    apelido: str
    nome: str
    nascimento: str
    stack: Optional[List[str]] = None

class PessoaCreate(PessoaBase):
    pass

class PessoaResponse(PessoaBase):
    id: UUID4

app = FastAPI()

@app.post("/pessoas/", response_model=PessoaResponse)
def criar_pessoa(pessoa: PessoaCreate):
    nova_pessoa = Pessoa.create(**pessoa.dict())
    return nova_pessoa

@app.get("/pessoas/{id}", response_model=PessoaResponse)
def ler_pessoa(id: UUID4):
    try:
        pessoa = Pessoa.get(Pessoa.id == id)
        return pessoa
    except Pessoa.DoesNotExist:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")

@app.get("/pessoas", response_model=List[PessoaResponse])
def buscar_pessoas(t: Optional[str]):
    query = Pessoa.select().where(
        Pessoa.apelido.contains(t) | Pessoa.nome.contains(t) | Pessoa.stack.contains(t)
    ).limit(50)
    return list(query)

@app.get("/contagem-pessoas")
def contar_pessoas():
    return Pessoa.select().count()
