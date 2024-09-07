from datetime import timedelta
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from schemas import UserCreate, ItemCreate, ItemUpdate
from crud import create_user, get_user, create_item, get_items, get_item, update_item, delete_item
from auth import authenticate_user, create_access_token, get_current_user
from database import get_db
from sqlalchemy.orm import Session
from models import User
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()

# Landing page (authentication optional)
@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "current_user": current_user})

# Signup
@router.get("/signup", response_class=HTMLResponse)
async def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
async def signup(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    user_data = UserCreate(
        username=form.get("username"),
        email=form.get("email"),
        password=form.get("password")
    )
    if get_user(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    create_user(db, user_data)
    return RedirectResponse(url="/login", status_code=303)

# Login
@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    user = authenticate_user(db, username, password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    
    # Return the token in a JSON response (the frontend should store it in localStorage)
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"})

# Logout
@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=303)
    # You should also clear the session or token here if applicable.
    return response

# List items (authentication not required)
@router.get("/items", response_class=HTMLResponse)
async def list_items(request: Request, db: Session = Depends(get_db)):
    items = get_items(db)
    return templates.TemplateResponse("item_list.html", {"request": request, "items": items})

# Create item form (authentication required)
@router.get("/items/create", response_class=HTMLResponse)
async def create_item_form(request: Request, current_user: User = Depends(get_current_user)):
    if current_user is None:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("create_item.html", {"request": request})

# Create item (authentication required)
@router.post("/items/create")
async def create_item_view(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    form = await request.form()
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    
    item_data = ItemCreate(
        name=form.get("name"),
        description=form.get("description"),
        price=float(form.get("price"))
    )
    create_item(db, item_data)
    return RedirectResponse(url='/items', status_code=303)

# Update item form (authentication required)
@router.get("/items/update/{item_id}", response_class=HTMLResponse)
async def update_item_form(request: Request, item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse("update_item.html", {"request": request, "item": item})

# Update item (authentication required)
@router.post("/items/update/{item_id}")
async def update_item_view(request: Request, item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    form = await request.form()
    item_data = ItemUpdate(
        name=form.get("name"),
        description=form.get("description"),
        price=float(form.get("price"))
    )
    item = update_item(db, item_id, item_data)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return RedirectResponse(url="/items", status_code=303)

# Delete item (authentication required)
@router.post("/items/delete/{item_id}")
async def delete_item_view(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = delete_item(db, item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return RedirectResponse(url="/items", status_code=303)
