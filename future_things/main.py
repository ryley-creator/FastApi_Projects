from fastapi import FastAPI,Depends,HTTPException, Request,status,Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import models,database,schemas
from database import engine
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post('/create')
def create(request:Request,product_name:str = Form(...),description:str = Form(...),db:Session = Depends(database.get_db)):
    new_product = models.Future(
        product_name = product_name,description = description
    )
    db.add(new_product)
    db.commit()
    products = db.query(models.Future).order_by(models.Future.id.desc()).all()
    db.refresh(new_product)
    return templates.TemplateResponse(request,'index.html',{'products':products})



@app.get('/create_product')
def create(request:Request):
    return templates.TemplateResponse(request,'create.html')
    
@app.get('/')
def get(request:Request,db:Session = Depends(database.get_db)):
    products = db.query(models.Future).all()
    product_name = db.query(models.Future).filter(models.Future.product_name).all()
    description = db.query(models.Future).filter(models.Future.description).all()
    return templates.TemplateResponse(request,'index.html',{'products':products,'name':product_name,'description':description})

@app.post('/update/{id}')
def update(
    id: int,
    product_name: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(database.get_db)
):
    product_p = db.query(models.Future).filter(models.Future.id == id)
    product_o = product_p.first()
    if not product_o:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Product with id {id} was not found')
    product_p.update(
        {"product_name": product_name, "description": description},
        synchronize_session=False
    )
    db.commit()
    return RedirectResponse("/", status_code=302)
    
    
# @app.delete('/delete/{id}')
# def delete(id:int,db:Session = Depends(database.get_db)):
#     product = db.query(models.Future).filter(models.Future.id == id).first()
#     if not product:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Product with is {id} was not found')
#     db.delete(product)
#     db.commit()
#     return {'Product deleted succefully!'}

@app.get('/')
def hello(request:Request):
    return templates.TemplateResponse(request,'index.html')


@app.get('/product/{id}')
def get_by_id(id:int,request:Request,db:Session = Depends(database.get_db)):
    product = db.query(models.Future).filter(models.Future.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Product with id {id} was not found')
    return templates.TemplateResponse(request,'detail.html',{'product':product})


@app.get('/update_product/{id}')
def update_product_page(
    id: int,
    request: Request,
    db: Session = Depends(database.get_db)
):
    product = db.query(models.Future).filter(models.Future.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse('update.html', {'request': request, 'product': product})

@app.get('/delete_product/{id}')
def delete_product_page(
    id: int,
    request: Request,
    db: Session = Depends(database.get_db)
):
    product = db.query(models.Future).filter(models.Future.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return templates.TemplateResponse('delete.html', {'request': request})
