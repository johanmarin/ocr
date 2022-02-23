import os 
import json
import pandas as pd
import API.text_extract as tx

def save_file(file_path: str, data: bytes):
  """recibe una ruta y datos y los guarda en un archivo especificado en la ruta

  Args:
      file_path (str): ruta del archivo
      data (bytes): datos a guardar
  """ 
  with open(file_path, 'wb') as f:
      f.write(data)
  print('Se ha guardado el archivo %s' %file_path)

def remove_file(file_path: str):
  """recibe la ruta de un archivo y lo eleimna

  Args:
      file_path (str): ruta del archivo
  """  
  os.remove(file_path)
  print('Se ha eliminado el archivo %s' %file_path)

extentions = {
    'images': ['jpg', 'jpeg', 'png'],
    'pdf': ['pdf'],
    'data': ['csv', 'xlsx', 'txt']
}
    
def get_content(file_path: str) -> dict:
    data = {'text':'',
            'tables': []}
    ext = file_path.split('.')[1]
    
    # Si es un archivo .pdf
    if ext in extentions['pdf']:
        data['text'] += tx.text_from_pdf(file_path)
        
        if data['text'] == '':
            images = tx.pdf_to_jpg(file_path)
            for img_path in images:
                data['text'] += tx.text_from_image(img_path)
                tx.remove_file(img_path)
        
        data['tables'] = tx.get_tables(file_path)
    
    # si es una imagen
    elif ext in extentions['images']:
        data['text'] += tx.text_from_image(file_path)
        
    # si es un archivo de excel
    elif '.xlsx' in file_path:      
        xl = pd.ExcelFile(file_path)        
        for i in xl.sheet_names:
            try: 
                data['tables'].append(json.dumps(pd.read_excel(file_path, i).to_dict()))
            except:
                print('No se logro gargar la hoja %s' %i)
    
    # si es un csv
    elif '.csv' in file_path:
        try: 
            data['tables'].append(json.dumps(pd.read_csv(file_path).to_dict()))
        except:
            f = open(file_path, "r")
            data['text'] = [l.split(',') for l in f.readlines()[0].split('\n')]
            
    # si es un txt
    elif '.txt' in file_path:
        try: 
            data['tables'].append(pd.read_csv(file_path, sep='\t').to_dict())
        except:
            f = open(file_path, "r")
            data['text'] = [l.split('\t') for l in f.readlines()[0].split('\n')]         
 
    remove_file(file_path)
    
    return data