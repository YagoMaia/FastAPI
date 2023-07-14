from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, select, Session, or_

class Region(SQLModel, table=True): #None da Tabela
    #None das Colunas
    region_id : Optional[int] = Field(default=None, primary_key=True)
    region_description : str
    def to_json(self):
        return {'region_description': self.region_description, 'region_id': self.region_id}


sql_file_name = "nortwind"
sql_url = f"postgresql://postgres:123@localhost:5432/{sql_file_name}"

engine = create_engine(sql_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#Criando linhas
def create_region(id : int, description : str):
    new_region = Region(region_id=id, region_description=description)
    with Session(engine) as session:
        session.add(new_region)
        session.commit()

#Fazendo Selects

def select_regions():
    with Session(engine) as session:
        statement = select(Region)
        results = session.exec(statement)
        r = []
        for region in results:
            r.append(region)
        if len(r) > 0:
            complet = []
            for x in range(0, len(r)):
                complet.append(r[x].to_json())
            return complet

def select_regions_id(id):
    with Session(engine) as session:
        statement = select(Region).where(Region.region_id == id)
        results = session.exec(statement)
        return results.first()


def teste(id):
    create_db_and_tables()
    select_regions_id(id)
