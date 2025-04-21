from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
import httpx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any frontend, or specify ["http://localhost:5500"] if you want
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConversionRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float

class ConversionResponse(BaseModel):
    converted_amount: float

API_KEY = "7XgndZ1z026z6kmIVcT34bxrdHFuiTGG"
HEADERS = {"apikey": API_KEY}

@app.post("/convert", response_model=ConversionResponse)
async def convert_currency(request: ConversionRequest):
    from_curr = request.from_currency.upper()
    to_curr = request.to_currency.upper()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.apilayer.com/exchangerates_data/convert",
            headers=HEADERS,
            params={"from": from_curr, "to": to_curr, "amount": request.amount}
        )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch conversion rates.")

    data = response.json()
    if not data.get("success"):
        raise HTTPException(status_code=400, detail="Invalid conversion request.")

    converted_amount = data.get("result")

    return ConversionResponse(converted_amount=round(converted_amount, 2))


@app.get("/symbols")
async def get_symbols():
    url = "https://api.apilayer.com/exchangerates_data/symbols"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail="Failed to fetch symbols")


@app.get("/")
def read_root():
    return {"message": "Currency Converter (Live Rates)"}
