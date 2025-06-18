from enum import Enum
from pathlib import Path
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from statsmodels.iolib.smpickle import load_pickle

class Area(str, Enum):
    D = "D"
    B = "B"
    E = "E"
    C = "C"
    F = "F"
    A = "A"


class Gas(str, Enum):
    Regular = "Regular"
    Diesel = "Diesel"


class VhBrand(str, Enum):
    B1 = "B1"
    B2 = "B2"
    B3 = "B3"
    B4 = "B4"
    B5 = "B5"
    B6 = "B6"
    B10 = "B10"
    B11 = "B11"
    B12 = "B12"
    B13 = "B13"
    B14 = "B14"

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/motor")
async def calculate(power: int,
                    VehAge: int,
                    DrivAge: int,
                    BonusMalus: int,
                    VehGas: Gas,
                    Area: Area,
                    Density: float,
                    VhBrand: VhBrand):
    root = Path(__file__).parent.parent
    frequency = load_pickle(f'models/prod/Frequency.pickle')
    severity = load_pickle(f'models/prod/Severity.pickle')

    single_profile = {'VehPower': [power],
                      'VehAge': [VehAge],
                      'DrivAge': [DrivAge],
                      'BonusMalus': [BonusMalus],
                      'VehGas': [VehGas.name],
                      'Area': [Area.name],
                      'Density': [Density],
                      'VhBrand':[VhBrand.name]}

    single_profile = pd.DataFrame.from_dict(single_profile)
    single_profile['Predicted Frequency'] = frequency.predict(single_profile)
    single_profile['Predicted Severity'] = severity.predict(single_profile)
    single_profile['Predicted Frequency'] = round(single_profile['Predicted Frequency'], 4)
    single_profile['Predicted Severity'] = round(single_profile['Predicted Severity'], 2)
    single_profile['Risk Premium'] = round(single_profile['Predicted Frequency'] * single_profile['Predicted Severity'],
                                           2)
    single_profile = single_profile.to_dict('list')

    return single_profile


#TODO : Create a POST to send data into the policy database once the quote is accepted