from base64 import encode
import PyPDF2
import camelot
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

  
def text_from_pdf(file_path:str)->str:
    """Esta función recibe la ruta de un archivo pdf y extrae todo el contenido en formato texto

    Args:
        file_path (str): ruta del archivo pdf

    Returns:
        str: contenido del archivo pdf como texto
    """    
    pdf_file = open(file_path, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    text_content = ''
    for i in range(read_pdf.getNumPages()):
        page = read_pdf.getPage(i)
        page_content = page.extractText()
        text_content += str(page_content.encode('utf-8'))
    
    text_content = text_content.replace('\\n', '\n')
    text_content = text_content.replace('\n \n', '\n')
    text_content = text_content.replace("b''", '')
    text_content = text_content.replace("b' \n'", '')
    
    print('se obtiene el contenido del archivo %s como texto' %file_path)
    return text_content
      
def pdf_to_jpg(file_path: str) -> list:
  """recibe la ruta de un archivo pdf, tranforma cada pagina de un archivo en una imagen .jpg, las guarda y devuelve una lista con las rutas donde guardo las imagenes

  Args:
      file_path (str): ruta del archivo .pdf

  Returns:
      list: rutas de las paginas como imagenes .jpg
  """  
  pages = convert_from_path(file_path, 500)
  files = []
  for i,page in enumerate(pages):
    file = file_path.replace('.pdf', '_') + str(i) + '.jpg'
    files.append(file)
    page.save(file, 'JPEG')
  print('se ha guardado el archivo %s como imagenes' %file_path)
  return files     
      
def get_tables(file_path: str) -> list:
  """Esta función recibe la ruta de un archivo pdf y devuelve uan lista de tablas y con cada tabla en formato diccionario

  Args:
      file_path (str): ruta del archivo

  Returns:
      list: lista de diccionarios con el contenido de las tablas
  """    
  tables = camelot.read_pdf(file_path, encode='utf8')
  print('Se extraen las tablas del archivo %s' %file_path)
  return [table.df.to_dict() for table in tables]
  

def text_from_image(file_path: str) -> str:  
  """recibe la ruta de un archivo de tipo imagen y 

  Args:
      file_path (str): _description_

  Returns:
      str: _description_
  """   
  # perform OCR on the processed image
  text_content = pytesseract.image_to_string(Image.open(file_path), lang='spa')
  print('se obtiene el contenido del archivo %s como texto' %file_path)
  return text_content