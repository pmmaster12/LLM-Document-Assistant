from .server import app


def main():
    import uvicorn

    uvicorn.run(app=app, host="0.0.00.0", port =8000)
    
    
    
main()
