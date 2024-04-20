import uvicorn
import pickleball_ai
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()
favicon_path = 'favicon.ico'

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

@app.get('/pickleball-query')
def pickleball_query(input_text: str = "What is pickleball?"):
    response_text = pickleball_ai.rag_chain_function(input_text)
    return {"response": response_text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)