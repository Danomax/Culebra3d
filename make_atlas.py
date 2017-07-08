
'''
make Atlas. Define un nuevo archivo atlas dada la imagen, las dimensiones y el numero de 
sprites en forma matricial
'''

def write_atlas(file_path, text):
  '''
  Write the atlas file.
  '''
  with open(file_path,"w",encoding="utf8") as current_file:
    current_file.write(text)

def make_atlas(imagefile, width, height, rows,cols):
  sprite_width = int(width / cols)
  sprite_height = int(height / rows)
  text = '{ \n'
  text += '  "' + imagefile + '": {\n'
  for row in range(rows):
    for col in range(cols):
      text += '    "' + str(col+(row*cols)) + '": [' + str(col*sprite_width + 1) + ',' + str(row*sprite_height + 1) + ',' + str(sprite_width) + ',' + str(sprite_height) + '], \n' 
  text += "  } \n}"
  
  filename = imagefile[:-4] + ".atlas"
  write_atlas(filename,text)
  
make_atlas('culebra3d_05.png',750,150,3,15)