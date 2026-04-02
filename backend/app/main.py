from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import users, auth, reactivos, nanomateriales, equipamientos, ordenes, dashboard

app = FastAPI(title="Laboratorio Nanomateriales API")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(reactivos.router, prefix="/reactivos", tags=["Reactivos"])
app.include_router(nanomateriales.router, prefix="/nanomateriales", tags=["Nanomateriales"])
app.include_router(equipamientos.router, prefix="/equipamientos", tags=["Equipamientos"])
app.include_router(ordenes.router, prefix="/ordenes", tags=["Ordenes"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}