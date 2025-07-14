from fastapi import FastAPI,UploadFile,File,Depends,HTTPException,status,Request
import database,models
from sqlalchemy.orm import Session
import language_tool_python
import schemas
from typing import List
import markdown
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.post('/upload')
async def upload_md_file(file:UploadFile = File(...),db:Session = Depends(database.get_db)):
    if not file.filename.endswith('.md'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='File should be in .md fomrat')
    note = await file.read()
    note_text = note.decode('utf-8')
    
    existing_file = db.query(models.MarkdownFile).filter(models.MarkdownFile.filename == file.filename).first()
    if existing_file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'File with name {file.filename} already exists')
    new_file = models.MarkdownFile(filename = file.filename,note = note_text)
    db.add(new_file)
    db.commit()
    
    return {'message':f'File with name {file.filename} successfully saved!'}

@app.get('/check-grammar/{id}')
def check_grammar(id:int,db:Session = Depends(database.get_db)):
    note = db.query(models.MarkdownFile).filter(models.MarkdownFile.id == id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'File with id {id} was not found')
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(note.note)
    corrected = language_tool_python.utils.correct(note.note,matches)
    return {
        "filename": note.filename,
        'note':note.note,
        "corrected": corrected
    }

@app.get('/list-files',response_model=List[schemas.FileListResponse])
def get_files(db:Session = Depends(database.get_db)) -> schemas.FileListResponse:
    files = db.query(models.MarkdownFile).all()
    return files


@app.get('/render_html/{id}')
def render_to_html(id:int,db:Session = Depends(database.get_db)):
    note = db.query(models.MarkdownFile).filter(models.MarkdownFile.id == id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Note with id {id} was not found')
    get_markdown = markdown.markdown(note.note)
    return get_markdown

@app.get('/')
def get(request:Request):
    return templates.TemplateResponse('index.md',{'request':request})
    







    
    


