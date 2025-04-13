import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from openai import OpenAI, APIStatusError
from pydantic import BaseModel

app = FastAPI()

app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def serve_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
async def handle_chat(request: ChatRequest):
    query = request.query
    try:
        print(f"Received query: {query}")

        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": query}]
            )
            print(f"OpenAI response: {response}")
        except APIStatusError as e:
            print(f"OpenAI API error: {e}")

        bot_response = response.choices[0].message["content"]
        print(f"Bot response: {bot_response}")

        parameters = extract_parameters(bot_response)
        print(f"Extracted parameters: {parameters}")

        visualization_data = generate_visualization_data(parameters)
        print("Response sent to frontend:", {"message": bot_response, "visualization": visualization_data})

        return JSONResponse(content={"message": bot_response, "visualization": visualization_data})
    except Exception as e:
        import traceback
        print("Exception occurred:")
        traceback.print_exc()
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"})

def extract_parameters(bot_response: str):
    return {}

def generate_visualization_data(parameters: dict):
    try:
        df = pd.read_csv("Financial-Analytics-data.csv", sep=",")

        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": f"Error generating visualization data: {str(e)}"}