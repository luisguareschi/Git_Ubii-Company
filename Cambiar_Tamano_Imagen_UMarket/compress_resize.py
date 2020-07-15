import os
from PIL import Image

def compress_resize(file_path, compression_percentage=60):
    # Abrir el archivo y comprimirlo en formato JPG, es necesesario tener el path del archivo
    file_name = os.path.splitext(file_path)[0]
    image = Image.open(file_path)
    new_path = file_name + '_compressed.jpg'
    image.save(new_path, optimize=True, quality=compression_percentage)  # El porcentaje recomendado de compresion es 60, esta por default a ese numero

    # Abrir el archivo nuevo comprimido y crear dos imagenes nuevas, una en tamano mediano (200x200) y otra en tamano pequeno (40x50)
    small_resolution = (200, 200)
    medium_resolution = (40, 50)
    image = Image.open(new_path)
    file_name = os.path.splitext(new_path)[0]
    medium_img = image.resize(medium_resolution, Image.ANTIALIAS)
    small_img = image.resize(small_resolution, Image.ANTIALIAS)
    medium_img.save(file_name+'_medium.jpg', optimize=True, quality=100)
    small_img.save(file_name+'_small.jpg', optimize=True, quality=100)
    small_path = file_name+'_small.jpg'
    medium_path = file_name+'_medium.jpg'
    big_path = new_path
    print('\tArchivo comprimido')

    # Se devuelven las nuevas direcciones de los archivos para que puedan ser usados facilmente
    return big_path, medium_path, small_path

    ''' Se crearan 3 archivos con el siguiente formato:
    1-. 'nombreOriginal_compressed.jpg' (en el tamano original de la imagen)
    2-. 'nombreOriginal_compressed_medium.jpg' (200x200)
    3-. 'nombreOriginal_compressed_small.jpg' (40x50)
    '''

### Main Program ###
folder_path = 'IMAGENES' # Aqui se selecciona la carpeta madre de todas las imagenes que se deseen comprimir
for subdir, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = subdir + os.sep + file
        if file_path.endswith(".jpg") or file_path.endswith('.png'):
            print('Comprimiendo:', file_path)
            compress_resize(file_path)
