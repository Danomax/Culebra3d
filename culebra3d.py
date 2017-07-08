from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Line
from kivy.graphics.vertex_instructions import Rectangle
from kivy.clock import Clock
from kivy.uix.label import Label

import random 
from math import atan
from math import atan2, pi

GAME_SPEED = 2

def direction(pos_ini,pos_end):
  '''
  define la direccion dado el angulo formado por las posiciones iniciales y finales
  del movimiento touch. retorna un vector direction
  '''
  diff = pos_end[0] - pos_ini[0],pos_end[1] - pos_ini[1]
  angle = atan2(diff[1],diff[0])
  if angle < (2*pi/8) and angle >= -(1*pi/8):
    direc=[1,0,0]
  elif angle < (5*pi/8) and angle >= (2*pi/8):
    direc=[0,1,0]
  elif angle < (7*pi/8) and angle >= (5*pi/8):
    direc=[0,0,-1]
  elif angle < (-6*pi/8) or angle >= (7*pi/8):
    direc=[-1,0,0]
  elif angle < (-3*pi/8) and angle >= (-6+pi/8):
    direc=[0,-1,0]
  elif angle < (-1*pi/8) and angle >= (-3*pi/8):
    direc=[0,0,1]
  return direc

class TextureDict():
  def __init__(self,**kwargs):
    super(TextureDict,self).__init__(**kwargs)
    self.texture_dict = {}

  def load_chars(self,filename):
    ordn = 0
    for ordn in range(45):
      self.texture_dict[ordn] = Image()
      self.texture_dict[ordn].source = 'atlas://'+filename+'/' + str(ordn)

Textures = TextureDict()
Textures.load_chars('culebra3d_06')

class Grid_Object():
  '''
  cualquier objeto que esetá dentro de la grilla, puede ser SnakePart o Food, u otro (portales, muros, etc)
  '''
  def __init__(self,**kwargs):
    self.pose = []

  def in_grid(self,grid):
    '''
    retorna True si el objeto esta dentro de la grilla
    '''
    if self.pose[0] in range(grid[0]): 
      if self.pose[1] in range(grid[1]): 
        if self.pose[2] in range(grid[2]):
          return True 
    return False

  def same_pose(self,pose):
    '''
    retorna True si la pose es la misma de este objeto
    '''
    if pose[0] == self.pose[0]:
      if pose[1] == self.pose[1]: 
        if pose[2] == self.pose[2]:
          return True 
    return False

class SnakePart(Grid_Object):
  '''
  Dibuja una parte de la culebra, el source depende de que parte es 
  '''
  def __init__(self,**kwargs):
    super(SnakePart,self).__init__(**kwargs)
    self.next_snake = None
    self.prev_snake = None
    self.texture_index = 0

  def append_snake(self,pose):
    if self.pose == []:
      self.update_pose(pose)
    else:
      if self.next_snake != None:
        self.next_snake.append_snake(pose)
      else:
        self.next_snake = SnakePart()
        self.next_snake.update_pose(pose)
        self.next_snake.prev_snake = self

  def update_pose(self,pose):
    if self.next_snake != None:
      self.next_snake.update_pose(self.pose)
    self.pose = pose

  def update_source(self):
    if self.next_snake == None and self.prev_snake == None:
      return
    elif self.next_snake != None and self.prev_snake == None:
      #Cabeza de la culebra
      diff_next = [pos - next for pos,next in zip(self.pose,self.next_snake.pose)]
      if diff_next == [0,1,0]:
          self.texture_index = 29
      elif diff_next == [0,-1,0]:
          self.texture_index = 28
      elif diff_next == [-1,0,0]:
          self.texture_index = 27
      elif diff_next == [1,0,0]:
          self.texture_index = 26
      elif diff_next == [0,0,-1]:
          self.texture_index = 24
      elif diff_next == [0,0,1]:
          self.texture_index = 25
      self.next_snake.update_source()
    elif self.next_snake == None and self.prev_snake != None:
      #Cola de la culebra
      diff_prev = [prev - pos for pos,prev in zip(self.pose,self.prev_snake.pose)]
      if diff_prev == [0,1,0]:
          self.texture_index = 23
      elif diff_prev == [0,-1,0]:
          self.texture_index = 22
      elif diff_prev == [-1,0,0]:
          self.texture_index = 20
      elif diff_prev == [1,0,0]:
          self.texture_index = 21
      elif diff_prev == [0,0,-1]:
          self.texture_index = 19
      elif diff_prev == [0,0,1]:
          self.texture_index = 18
    elif self.next_snake != None and self.prev_snake != None:
      #cuerpo de la culebra
      diff_next = [self - next for self,next in zip(self.pose,self.next_snake.pose)]
      diff_prev = [prev - pos for pos,prev in zip(self.pose,self.prev_snake.pose)]
      if (diff_prev == [0,1,0] and diff_next == [0,1,0]) or (diff_prev == [0,-1,0] and diff_next == [0,-1,0]) :
        self.texture_index = 34
      elif (diff_prev == [1,0,0] and diff_next == [1,0,0]) or (diff_prev == [-1,0,0] and diff_next == [-1,0,0]) :
        self.texture_index = 33
      elif (diff_prev == [0,0,1] and diff_next == [0,0,1]) or (diff_prev == [0,0,-1] and diff_next == [0,0,-1]) :
        self.texture_index = 32
      # x to z
      elif (diff_prev == [1,0,0] and diff_next == [0,0,-1]) or (diff_prev == [0,0,1] and diff_next == [-1,0,0]) :
        self.texture_index = 16  #35
      elif (diff_prev == [0,0,1] and diff_next == [1,0,0]) or (diff_prev == [-1,0,0] and diff_next == [0,0,-1]) :
        self.texture_index = 43  #36
      elif (diff_prev == [1,0,0] and diff_next == [0,0,1]) or (diff_prev == [0,0,-1] and diff_next == [-1,0,0]) :
        self.texture_index = 17  #37
      elif (diff_prev == [0,0,-1] and diff_next == [1,0,0]) or (diff_prev == [-1,0,0] and diff_next == [0,0,1]) :
        self.texture_index = 15  #38
      #y yo z 
      elif (diff_prev == [0,1,0] and diff_next == [0,0,-1]) or (diff_prev == [0,0,1] and diff_next == [0,-1,0]) :
        self.texture_index = 40
      elif (diff_prev == [0,0,1] and diff_next == [0,1,0]) or (diff_prev == [0,-1,0] and diff_next == [0,0,-1]) :
        self.texture_index = 42
      elif (diff_prev == [0,1,0] and diff_next == [0,0,1]) or (diff_prev == [0,0,-1] and diff_next == [0,-1,0]) :
        self.texture_index = 39
      elif (diff_prev == [0,-1,0] and diff_next == [0,0,1]) or (diff_prev == [0,0,-1] and diff_next == [0,1,0]) :
        self.texture_index = 41
      #x to y
      elif (diff_prev == [1,0,0] and diff_next == [0,1,0]) or (diff_prev == [0,-1,0] and diff_next == [-1,0,0]) :
        self.texture_index = 38 #43
      elif (diff_prev == [1,0,0] and diff_next == [0,-1,0]) or (diff_prev == [0,1,0] and diff_next == [-1,0,0]) :
        self.texture_index = 36 #15
      elif (diff_prev == [0,-1,0] and diff_next == [1,0,0]) or (diff_prev == [-1,0,0] and diff_next == [0,1,0]) :
        self.texture_index = 37 #16
      elif (diff_prev == [0,1,0] and diff_next == [1,0,0]) or (diff_prev == [-1,0,0] and diff_next == [0,-1,0]) :
        self.texture_index = 35 #17
      self.next_snake.update_source()

  def get_poses(self):
    '''
    entrega un [] de las posiciones 
    '''
    if self.next_snake != None:
      result = [self.pose] + self.next_snake.get_poses()
    else:
      result = [self.pose]
    return result

  def get_textures(self):
    '''
    entrega un [] de las texturas 
    '''
    if self.next_snake != None:
      result = [self.texture_index] + self.next_snake.get_textures()
    else:
      result = [self.texture_index]
    return result
    
class Food(Grid_Object):
  '''
  Dibuja el alimento 
  '''
  def __init__(self,**kwargs):
    super(Food,self).__init__(**kwargs)
    self.texture_index = 44

  def update_pose(self,pose):
    self.pose = pose

class Score(Label):
  def __init__(self,**kwargs):
    super(Score,self).__init__(**kwargs)
    self.text = 'score:'
    self.size = (600,30)
    #self.pos=(0,0)
    mycolor = [1,1,1,1] # White
    with self.canvas:
      Color(*mycolor)
      Rectangle(pos=(0,0),size=self.size)

  def update(self,text):
    self.text='score:'+str(text)

class BoardGame(Widget):
  #Aqui se dibuja todo el lugar donde se mueve la culebra
  def __init__(self):
    super(BoardGame,self).__init__()
    self.size = (600,600)
    
    self.mylayout = 10
    self.tilewidth,self.tileheight = (50,50)
    self.snake_size = 3
    self.grid = (10,10,10)  #grilla del cubo donde se mueve la culebra
    self.grid_snake = []    #mantiene una matriz que es true en las celdas ocupadas por la culebra
    for i in range(self.grid[0]):
      self.grid_snake.append([])
      for j in range(self.grid[1]):
        self.grid_snake[i].append([])
        for k in range(self.grid[2]):
          self.grid_snake[i][j].append(False)
    self.snake = SnakePart() #objetos de la culebra
    for i in range(self.snake_size):
      [x,y,z] = [int(self.grid[0]/2-i),int(self.grid[1]/2),int(self.grid[2]/2)]
      self.grid_snake[x][y][z] = True
      position = self.get_position([x,y,z])
      self.snake.append_snake([x,y,z])
    self.snake.update_source()
    positions = self.get_positions(self.snake.get_poses())
    textures = self.snake.get_textures()
    for pos,tex in zip(positions,textures):
      self.Draw(alpha=1.0,view_position=pos,texture_index=tex)
    self.food = Food()
    self.food.update_pose(self.new_food_pos())
    view_position = self.get_position(self.food.pose)
    self.Draw(alpha=1.0,view_position=view_position,texture_index=self.food.texture_index)

  def get_position(self,pose):
    '''
    dada la posicion matricial pose calcula la posicion donde debe ir el objeto
    en la pantalla
    '''
    deltax = self.width*0.06*pose[0]
    deltay = self.height*0.06*pose[1]
    deltaz = (self.width*0.012 + self.height*0.012)*pose[2]
    return (deltax+deltaz,deltay+deltaz)

  def get_positions(self,poses):
    '''
    calcula las posiciones de una serie de objetos
    '''
    positions = []
    for pos in poses:
      positions += [self.get_position(pos)]
    return positions

  def new_food_pos(self):
    '''
    retorna nueva posicion para la comida luego de ser devorada
    '''
    #encuentra el numero de espacios libres en la grilla
    empty_spaces = self.grid[0]*self.grid[1]*self.grid[2]
    empty_spaces = empty_spaces - self.snake_size
    print('empty spaces:' + str(empty_spaces))
    #escoge el numero aleatorio entre 1 y empty_spaces
    choose_num = random.randint(1,empty_spaces)
    print('choose num:' + str(choose_num))
    #encuentra el espacio evitando los espacios ocupados por la culebra
    num=0
    for i in range(self.grid[0]):
      for j in range(self.grid[1]):
        for k in range(self.grid[2]):
          if self.grid_snake[i][j][k]==False:
            num+=1
          if num == choose_num:
            return (i,j,k)
    #si no encuentra espacio, se lleno la grilla de culebra, fin del juego!
    return (-1,-1,-1)
      
  def update(self,*ignore):
    self.canvas.clear()
    #Dibujar las partes del cubo que están detrás de los objetos de la grilla
    with self.canvas:
      mycolor = [1,1,1,1] # White
      Color(*mycolor)
      Rectangle(pos=(0,0),size=(self.size))
      mycolor = [0,0,0,1]
      Color(*mycolor)
      Line(points=[1,100,1,600],width=2)
      Line(points=[1,600,500,600],width=2)
      Line(points=[500,100,500,600],width=2)
      Line(points=[1,100,500,100],width=2)
      mycolor = [1,1,0,1] #yellow
      
      
    #actualiza la posicion de la cabeza de acuerdo a la direccion
    if self.parent.direction != [0,0,0]:
      old_head_pose = self.snake.pose
      newpos = [pose+direc for pose,direc in zip(self.snake.pose,self.parent.direction) ]
      #se debe actualizar las posiciones de la culebra y añadir un cuerpo en la cola
      self.snake.update_pose(newpos) 
      #chequear si ha chocado consigo misma
      if self.grid_snake[newpos[0]][newpos[1]][newpos[2]]:
        self.parent.game_over()
        return
      #actualiza la grilla grid_snake con la nueva posicion
      if self.snake.in_grid(self.grid):
        self.grid_snake[newpos[0]][newpos[1]][newpos[2]] = True
      else:
        self.parent.game_over()
      if self.snake.same_pose(self.food.pose):
        #Se come el alimento
        self.score += 100
        self.food.update_pose(self.new_food_pos())
    #actualiza las formas de los cuerpos de la culebra
    self.snake.update_source()
    positions = self.get_positions(self.snake.get_poses())
    textures = self.snake.get_textures()
    for pos,tex in zip(positions,textures):
      #dibuja a la culebra
      self.Draw(alpha=1.0,view_position=pos,texture_index=tex)                
    view_position = self.get_position(self.food.pose)
    self.Draw(alpha=1.0,view_position=view_position,texture_index=self.food.texture_index)

  def Draw(self,alpha,view_position,texture_index):
    with self.canvas:
      position = (view_position[0],self.size[1]-view_position[1])
      mycolor=[1,1,1,alpha]
      Color(*mycolor)
      mytexture = Textures.texture_dict[texture_index].texture
      Rectangle(pos=position,size=(self.tilewidth,self.tileheight),texture=mytexture)

class Game(Widget):
  def __init__(self):
    super(Game, self).__init__()
     
    self.direction = [0,0,0]
    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
    self.score = Score()
    self.score.pos = (0,0)
    self.add_widget(self.score)
    self.scorevalue = 0
    
    self.board = BoardGame()
    self.add_widget(self.board)
    self.size = self.board.size[0],self.score.size[1]+self.board.size[1]
    Clock.schedule_interval(self.board.update, 1.0/GAME_SPEED)
    Clock.schedule_interval(self.update, 1.0/GAME_SPEED)

  def update(self,*ignore):    
    debug_text = ''
    positions = self.board.snake.get_poses()
    for pos in positions:
      debug_text += str(pos)+','
    diff_next = [self - next for self,next in zip(positions[1],positions[2])]
    diff_prev = [prev - pos for pos,prev in zip(positions[1],positions[0])]

    debug_text += '\n diff prev:' + str(diff_prev) + ', diff next:' + str(diff_next) 
    self.score.update(debug_text)


  def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard = None

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'd' and self.direction != [-1,0,0]:
      self.direction = [1,0,0] 
    elif keycode[1] == 'a' and self.direction != [1,0,0]:
      self.direction = [-1,0,0]
    elif keycode[1] == 'w' and self.direction != [0,1,0]:
      self.direction = [0,-1,0]
    elif keycode[1] == 'x' and self.direction != [0,-1,0]:
      self.direction = [0,1,0]
    elif keycode[1] == 'q' and self.direction != [0,0,1]:
      self.direction = [0,0,-1]
    elif keycode[1] == 'c' and self.direction != [0,0,-1]:
      self.direction = [0,0,1]
    return True

  def on_touch_down(self, touch): 
    self.pos_ini =(touch.x, touch.y)
    #touch.ud['dir'] = pos_ini 
  
  def on_touch_up(self, touch): 
    self.pos_end = (touch.x, touch.y)
    direc = direction(self.pos_ini,self.pos_end)
    if [dir+dire for dir,dire in zip(direc,self.direction)]!= [0,0,0]:
      self.direction = direc 

  def game_over(self):
    self.clear_widgets()
    Clock.unschedule(self.board.update)
    Clock.unschedule(self.update)
    self.__init__()


class Culebra3DApp(App):
  def build(self):
    game = Game()
    Window.size = game.size
    return game

if __name__ == "__main__":
  Culebra3DApp().run()