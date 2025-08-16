"""
Simple web test to isolate the issue.
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Simple Test")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    return {"status": "working"}

if __name__ == "__main__":
    print("🚀 Starting Simple Web Test...")
    print("📱 Open your browser and go to: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
