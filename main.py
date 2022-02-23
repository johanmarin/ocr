import os
from typing import List
import API.functions as f_api
from fastapi import FastAPI, File, UploadFile

PATH =  os.getcwd().replace('\\', '/')

app = FastAPI()

@app.get('/')
def index():
  return {'Welcome': 'OCR online'}

      
@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
  # in case you need the files saved, once they are uploaded
  resp = {}
  for file in files:
    contents = await file.read()
    filepath =os.path.join(PATH ,file.filename)
    f_api.save_file(filepath, contents)
    resp[file.filename] = f_api.get_content(filepath)
  return resp