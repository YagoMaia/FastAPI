from fastapi import FastAPI #Importando a função FastAPI
from enum import Enum #Importando a função Enum

app = FastAPI() #Criando o ponto de interação da API

@app.get("/") #Endpoint "/" com o path do tipo get
def root(): #Definindo a função do path
    return {"mensage": "Hello World"} #retorno da função que será mostrado no path "/"

@app.get("/items/{items_id}") #path /items/items_id(que seria um número)
def read_item(items_id : int): #parametro da função
    return {"Item Id" : items_id} #retorno

@app.get("/users/me") #Metódo específico definido antes do metódo geral
def read_user_me():
    return {"User id":"The curent user"} #Por conta disso ao inves de de retornar User id : me retorna o que está dentro da função

@app.get("/users/{user_id}") #Metódo generalizado
def read_user(user_id : str):
    return {"User id" : user_id}

#Dado um mesmo caminho, a função definida primeiramente se sobressai

@app.get("/users") 
def read_users():
    return ["Yago", "Maia"]

@app.get("/users")
def read_users_2():
    return ["Rene", "Veloso"]

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
def get_model(model_name : ModelName):
    if model_name is ModelName.alexnet: #comparando se o model_name é igual ao ModelName.alexnet que seria o valor de alexnet
        return {"Model Name" : model_name, "mensage" : "Someone"}
    if model_name.value == "resnet": #Mesmo tipo de comparação, mas comparando o valor 
        return {"Model Name" : model_name, "mensage" : "Anyway"}
    return {"Model Name" : model_name, "mensage" : "Nothing"}

#Tem como usar um caminho como parâmetro

@app.get("/files/{file_path:path}")
def read_file(file_path : str):
    return {"Path" : file_path}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
def read_items2(skip: int = 0, limit : int = 10):
    return fake_items_db[skip: skip + limit]

#Parametros Opcionais

@app.get("/teste/{teste_id}")
def read_teste(teste_id : str, q : str | None = None, short : bool = False):
    teste = {"Teste Id" : teste_id}
    if q:
        teste.update({"Q" : q })
    if not short:
        teste.update({"Description" : "This is an amazing item that has a long description"})
    return teste

@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(
    user_id : int,
    item_id : str,
    q : str | None = None,
    short : bool = False
):
    item = {"Item Id" : item_id, "Onwer Id" : user_id}
    if q:
        item.update({"Q" : q })
    if not short:
        item.update({"Description" : "This is an amazing item that has a long description"})
    return item
