from fastapi import FastAPI
from . routers import rental_history, user,auth,book,author,genre,review,cart
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.craleate_all(bind=engine)

origins = ["*"]

app = FastAPI()

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

# while True:
#     try:
#         conn=psycopg2.connect(host='localhost',database='bookRental',user='postgres',password='postgres',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database connected successfully")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("Error = ", error)
#         time.sleep(2)



    