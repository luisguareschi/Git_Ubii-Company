import os
from PIL import Image

def compress_resize(file_path, compression_percentage=60):
    # Abrir el archivo y comprimirlo en formato JPG, es necesesario tener el path del archivo
    # Compresion de la imagen
    file_name = os.path.splitext(file_path)[0]
    image = Image.open(file_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    new_path = file_name + '_c.jpg'
    print(new_path)
    image.save(new_path, optimize=True, quality=compression_percentage)  # El porcentaje recomendado de compresion es 60, esta por default a ese numero
    image.close()
    os.remove(file_path)
    if os.path.exists(file_name+'.jpg'):
        os.remove(file_name+'.jpg')
    os.rename(new_path, file_name+'.jpg')
    new_path = file_name+'.jpg'

    # Abrir el archivo nuevo comprimido y crear dos imagenes nuevas, una en tamano mediano (200x200) y otra en tamano pequeno (40x50)
    # Cambiar el tamano de la imagen
    small_resolution = (50, 50)
    medium_resolution = (212, 212)
    big_resolution = (600, 600)
    banner_resolution = (1920, 200)
    image = Image.open(new_path)
    width, height = image.size
    if width/height < 2:
        file_name = os.path.splitext(new_path)[0]
        medium_img = image.resize(medium_resolution, Image.ANTIALIAS)
        small_img = image.resize(small_resolution, Image.ANTIALIAS)
        image = image.resize(big_resolution, Image.ANTIALIAS)
        image.save(new_path, optimize=True, quality=100)
        medium_img.save(file_name+'_medium.jpg', optimize=True, quality=100)
        small_img.save(file_name+'_small.jpg', optimize=True, quality=100)
        # small_path = file_name+'_small.jpg'
        # medium_path = file_name+'_medium.jpg'
        # big_path = new_path
    else:
        image = image.resize(banner_resolution, Image.ANTIALIAS)
        image.save(new_path, optimize=True, quality=100)
        # banner_path = new_path
    print('-->Archivo comprimido')

### Main Program ###
folder_path = 'IMAGENES' # Aqui se selecciona la carpeta madre de todas las imagenes que se deseen comprimir
# Este loop va a ejecutar el metodo con todos los archivos dentro de la caperta que tengan la terminacion jpg o png
for subdir, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = subdir + os.sep + file
        if file_path.endswith(".jpg") or file_path.endswith('.png'):
            print('Comprimiendo:', file_path)
            compress_resize(file_path)

''' Se crearan los siguientes archivos con el siguiente formato:
----------------SI ES UNA IMAGEN DE PRODUCTO---------------------
1-. 'nombreOriginal.jpg' (600x600)
2-. 'nombreOriginal_medium.jpg' (200x200)
3-. 'nombreOriginal_small.jpg' (40x50)
-----------------SI ES UNA IMAGEN DE BANNER----------------------
1-. 'nombreOriginal.jpg' (1920x200)
'''

