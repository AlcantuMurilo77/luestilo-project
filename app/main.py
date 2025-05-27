
from fastapi import FastAPI , Depends

from app.network.oauth import oauth2_scheme
from app.routers import auth, client, product, order

app = FastAPI()

app.include_router(auth.router)

app.include_router(client.router, dependencies=[Depends(oauth2_scheme)])
app.include_router(product.router, dependencies=[Depends(oauth2_scheme)])
app.include_router(order.router, dependencies=[Depends(oauth2_scheme)])


@app.get("/ping")
def ping():
    return {"message": "pong"}

