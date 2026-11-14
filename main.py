from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "FastAPI is a modern Python framework for building APIs quickly and easily.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a powerful programming language, and FastAPI makes backend development even easier.",
        "date_posted": "April 21, 2025",
    },
    {
        "id": 3,
        "author": "John Smith",
        "title": "Learning REST APIs",
        "content": "REST APIs allow different applications to communicate with each other using HTTP methods.",
        "date_posted": "April 22, 2025",
    },
    {
        "id": 4,
        "author": "Alice Johnson",
        "title": "Understanding HTTP Methods",
        "content": "GET, POST, PUT, PATCH, and DELETE are commonly used HTTP methods in backend development.",
        "date_posted": "April 23, 2025",
    },
    {
        "id": 5,
        "author": "David Miller",
        "title": "Why Learn Backend Development",
        "content": "Backend development helps you build the server-side logic, databases, and APIs of modern applications.",
        "date_posted": "April 24, 2025",
    },
]

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/",include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name = "posts")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html",{"posts":posts})


@app.get("/api/posts/{post_id}")
def post_page(request:Request, post_id:int):
    print(posts)
    for post in posts:
        if post.get("id") == post_id:
            title = post.get("title")[:50]
            return templates.TemplateResponse(
                request,
                "post.html",
                {"post":post, "title":title}
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post no found")


@app.get("/api/posts")
def pos():
    return posts


@app.get("/api/posts/{post_id}")
def get_post(post_id:int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post no found")


@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )