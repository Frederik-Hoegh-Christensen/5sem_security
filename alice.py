# your_fastapi_script.py
from fastapi import FastAPI
import uvicorn
import httpx

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World"}

@app.get("/request")
async def send_request():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8001/")
        return {"response_from_api2": response.text}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
