from fastapi import FastAPI, responses
from core.config import settings
from starlette import status
from db.base import Base
from db.session import engine
from routers import books_routes

# create a database
Base.metadata.create_all(bind=engine)

# # create an app instance
app = FastAPI(title=settings.PROJECT_TITLE)


# set a routing to docs if user access root


@app.get('/', status_code=status.HTTP_200_OK)
async def home():
    return responses.RedirectResponse('/docs')


app.include_router(books_routes.router)
