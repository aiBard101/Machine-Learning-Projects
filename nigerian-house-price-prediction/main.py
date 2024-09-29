from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
import json
from predict import predict

app = FastAPI()

# Mount the "static" directory for serving CSS/JS files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up the Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# Serve the index.html as the root route
@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Allow CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('models/state_town_dict.json', 'r') as json_file:
    towns_dict = json.load(json_file)


with open('models/house_title.json', 'r') as f:
    house_types = json.load(f)  

# States endpoint
@app.get("/states")
def get_states():
    return {"states": list(towns_dict.keys())}

# Towns by state endpoint
@app.get("/towns/{state}")
def get_towns(state: str):
    towns = towns_dict.get(state, [])
    return {"towns": towns}

# House types endpoint
@app.get("/house-types")
def get_house_types():
    return {"house_types": house_types}

# Dummy prediction logic
class HouseDetails(BaseModel):
    bedrooms: int
    bathrooms: int
    toilets: int
    parking_space: int
    house_type: str
    town: str
    state: str

@app.post("/predict")
def predict_price(details: HouseDetails):
    print(details.bedrooms, details.bathrooms, details.toilets, details.parking_space, details.house_type, details.state, details.town)
    predicted_price = predict(details.bedrooms, details.bathrooms, details.toilets, details.parking_space, details.house_type, details.state, details.town)
    formatted_price = "{:,.2f}".format(predicted_price)
    return {"predicted_price": formatted_price}
    
