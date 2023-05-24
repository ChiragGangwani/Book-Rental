from fastapi import FastAPI
from . routers import rental_history, user,auth,book,author,genre,review,cart
from fastapi.middleware.cors import CORSMiddleware
from jobs.my_jobs import scheduler

# models.Base.metadata.craleate_all(bind=engine)

origins = ["*"]

app = FastAPI()

scheduler.start()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(book.router)
app.include_router(author.router)
app.include_router(genre.router)
app.include_router(review.router)
app.include_router(cart.router)
app.include_router(rental_history.router)

@app.get('/')
async def test():
    return {"message": "Hello World pushing out to ubuntu"}




    