import pandas as pd
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def serve_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
async def handle_form(search: str = Form(...)):
    try:
        df = pd.read_csv("Financial-Analytics-data.csv", sep=",")
    except Exception as e:
        return {"message": f"Error reading CSV file: {str(e)}"}

    data_json = df.to_dict(orient="records")

    search_tokens = search.lower().split()

    filtered_data = [
        row for row in data_json
        if any(token in str(row).lower() for token in search_tokens)
    ]

    if not filtered_data:
        return JSONResponse(content={"message": "No matching data found", "data": []})

    return JSONResponse(content={"message": "Filtered Data", "data": filtered_data})