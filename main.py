from fastapi import FastAPI, Query, Path, Body, Cookie, Form, Depends, APIRouter, BackgroundTasks
from enum import Enum 
from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated, Any
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from Sql_Model.db import select_regions_id as select_id, select_regions
from fastapi.testclient import TestClient

app = FastAPI() #Criando o ponto de interação da API

@app.get("/") #Endpoint "/" com o path do tipo get
def root(): #Definindo a função do path
    return {"mensage": "Hello World"} #retorno da função que será mostrado no path "/"

@app.get("/items/{items_id}", tags=["item"]) #path /items/items_id(que seria um número)
def read_item(items_id : int): #parametro da função
    return {"Item Id" : items_id} #retorno

@app.get("/users/me", tags=["user"]) #Metódo específico definido antes do metódo geral
def read_user_me():
    return {"User id":"The curent user"} #Por conta disso ao inves de de retornar User id : me retorna o que está dentro da função

@app.get("/users/{user_id}", tags=["user"]) #Metódo generalizado
def read_user(user_id : str):
    return {"User id" : user_id}

#Dado um mesmo caminho, a função definida primeiramente se sobressai

@app.get("/users/") 
def read_users():
    return ["Yago", "Maia"]

@app.get("/users/", deprecated=True)
def read_users_2():
    return ["Rene", "Veloso"]

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}", tags=["user"])
def get_model(model_name : ModelName):
    if model_name is ModelName.alexnet: #comparando se o model_name é igual ao ModelName.alexnet que seria o valor de alexnet
        return {"Model Name" : model_name, "mensage" : "Someone"}
    if model_name.value == "resnet": #Mesmo tipo de comparação, mas comparando o valor 
        return {"Model Name" : model_name, "mensage" : "Anyway"}
    return {"Model Name" : model_name, "mensage" : "Nothing"}

#Tem como usar um caminho como parâmetro

@app.get("/files/{file_path:path}", tags=["path"])
def read_file(file_path : str):
    return {"Path" : file_path}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/", tags=["item"])
def read_items2(skip: int = 0, limit : int = 10):
    return fake_items_db[skip: skip + limit]

#Parametros Opcionais

@app.get("/teste/{teste_id}", tags=["item"])
def read_teste(teste_id : str, q : str | None = None, short : bool = False):
    teste = {"Teste Id" : teste_id}
    if q:
        teste.update({"Q" : q })
    if not short:
        teste.update({"Description" : "This is an amazing item that has a long description"})
    return teste

@app.get("/users/{user_id}/items/{item_id}", tags=["user", "item"])
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

#Request Body -> envia os dados para os cliente pela API
#Ao invés de get usa-se Post

class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None = None

@app.post("/items/", 
            tags=["item"],
            summary="Create an item",
            description="""
Create an item with all the information:

- **name**: each item must have a name
- **description**: a long description
- **price**: required
- **tax**: if the item doesn't have tax, you can omit this
- **tags**: a set of unique tag strings for this item
    """
        )
def create_item(item:Item):
    item_dict = item.model_dump() #dict está obsoleto
    if item.tax:
        price_with_tax = item.tax + item.price
        item_dict.update({"Price with Tax" : price_with_tax})
    return item

@app.put("/items/{item_id}", tags=["item"]) #Put junção do get com post
def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}

#Additional validation
#Só tem como usar o query com o Annotated? -> Não, fica melhor usar com o Annotated

@app.get("/query/", tags=["query"])
def read_query(q : Annotated[str | None, Query(max_length=50, min_length=3)] = None): #Restrição de tamanho -> Máximo de 50
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#Annotated ge(greater or equal), le(less or equal) gt(greater than), lt(less than) funciona para float também

@app.get("/path/{item_id}", tags=["path"])
def read_item4(
    item_id : Annotated[int, Path(title="The id of the item to get", ge=5)],
    q : Annotated[str | None, Query(alias="item-query")] = None,
    size : Annotated[float, Query(ge=0, lt=10)] = None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q" : q})
    return results

class User(BaseModel):
    username : str
    full_name :str | None = None

@app.put("/put/", tags=["item"]) 
def update_item(
    item_id : int, 
    item : Annotated[Item, Body(embed=False)], 
    user: User,
    importance : Annotated[int, Body()] #Body funciona semelhante ao Query e ao Path em questão dos parametros
):
    results = {"item_id" : item_id, "item" : item, "user" : user}
    return results

class Field(BaseModel): #Field funciona da mesma forma que o Path, Query e Body
    name : str
    description : str | None = Field(
        default = None, title = "the description of the item", max_length = 300
    )
    price : float
    tax : float | None = None

class Image(BaseModel):
    url : HttpUrl #Validador de URL
    name : str

class Sale(BaseModel): #Field funciona da mesma forma que o Path, Query e Body
    name : str
    description : str | None = None
    price : float
    tax : float | None = None
    tags: list[str] = []
    image : Image | None = None
    images : list[Image] | None = None

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Sale]

@app.post("/offers/", tags=["item"])
def create_offer(offer:Offer) -> Offer:
    return offer

#Dentro das funções Body, Query, Field é possível colocar o parametro example

#Pode atribuir tipos de dados mais complexos, como datatime e entre outros

#Cookie Parameters

@app.get("/cookie/", tags=["cookies"])
def read_cookie(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

class UserIn(BaseModel):
    username: str
    password: str 
    email: str
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: str
    full_name: str | None = None

#Extra Models -> Exemplo:
#Modelo de Entrada, Modelo de Saída e Modelo para o Banco

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: str
    full_name: str | None = None

def fake_password_hasher(raw_password : str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password) #Quando se coloca **em um dicionário extrai todos os campos como parametro
    """"
    Exemplo:
    UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
    )
    """
    print("User saved! ..not really")
    return user_in_db

@app.post("/db/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

"""Para melhorar o funcionamento da API usa-se um modelo base e passa o campo adiconal
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str

"""

@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]): #Mexendo com Formulários
    return {"username": username}

def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/dep1/")
def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/dep2/")
def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

#Security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/security/", tags=["security"])
def read_security(token :Annotated[str, Depends(oauth2_scheme)]):
    return {"token" : token}

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@app.get("/security/me", tags=["security"])
def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

#SqlModel

@app.get("/database/{region_id}", tags=["db"])
def read_data_base(region_id : int):
    regions = {"Teste" : "Teste"}
    return select_id(region_id)

@app.get("/database/region/", tags=["db"])
def read_table():
    return select_regions()

"""router = APIRouter(
prefix = "/router",
tags = ["router"],
) Já deixa prefixado

@router.get("/router/", tags=["router"])
def read_user():
    return [{"username": "Rick"}, {"username": "Morty"}]"""


#Background Task's

def write_notification(email : str, mensage = ""):
    with open("log.txt", mode = "w") as email_file:
        content = f"Notification for {email} : {mensage}"
        email_file.write(content)

@app.post("/send-notification/{email}", tags = ["Back"])
def send_notification(email : str, background_taks : BackgroundTasks):
    background_taks.add_task(write_notification, email, mensage = "Some Notifcation")
    return {"mensage" : "Notification sent in the background"}
