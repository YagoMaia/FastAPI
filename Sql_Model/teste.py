from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, select, Session
import json

class Region(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    description : str
    def to_json(self):
        return {'region_description': self.description, 'region_id': self.id}


sql_file_name = "nortwind"
sql_url = f"postgresql://postgres:123@localhost:5432/{sql_file_name}"

engine = create_engine(sql_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#Criando linhas
def create_regions():
    region_1 = Region(id=5, description="East2")
    region_2 = Region(id=6, description="West3")
    region_3 = Region(id=7, description="North4")

    with Session(engine) as session:
        session.add(region_1)
        session.add(region_2)
        session.add(region_3)

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
        j = []
        for r in results:
            j.append(r)
        if len(j) > 0:
            return j[0].to_json()


def teste(id):
    create_db_and_tables()
    select_regions_id(id)
