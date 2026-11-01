from fastapi import FastAPI

from api.routers import auth, facets, games, stats  

app = FastAPI(  
    title="Video Games API",  
    version="0.1.0",  
    description="Query sales and metadata for ~65k video game releases.",  
)

app.include_router(auth.router)
app.include_router(games.router)  
app.include_router(facets.router)  
app.include_router(stats.router)


@app.get("/health", tags=["meta"])  
def health():  
    return {"status": "ok"}  