from fastapi import FastAPI, Path, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class LoginDTO(BaseModel):
    login: str
    password: str

class RegisterDTO(BaseModel):
    login: str
    password: str
    pass_comp: str

class DB_User(BaseModel):
    login: str
    password: str


# @app.get("/")
# def home():
#     return {"Data": "Testing"}

# @app.get("/about")
# def about():
#     return {"Data":"About"}

# inventory = {}

# @app.get("/get-item/{item_id}")
# def get_item(item_id: int = Path(None, description="The ID of item to look", gt=0)):
#     return inventory[item_id]

# @app.get("/get-by-name/{item_id}")
# def get_item(name: Optional[str] = None):
#     for item_id in inventory:
#         if inventory[item_id].name == name:
#             return inventory[item_id]
#     return {"Data":"Not found"}

# @app.post("/create-item/{item_id}")
# def create_item(item_id: int, item: Item):
#     if item_id in inventory:
#         return{"Error":"Item ID exist"}

#     inventory[item_id] = item
#     return inventory[item_id]

@app.post("/register")
def register(Register: RegisterDTO):
    return 0

@app.post("/login")
def login(Login: LoginDTO):
    DB_Login = "DB Login"
    if(LoginDTO.login != DB_User.login):
        raise HTTPException(status_code=400, detail="Incorrect login")
    if(LoginDTO.password != DB_User.password):
        raise HTTPException(status_code=400, detail="Incorrect password")