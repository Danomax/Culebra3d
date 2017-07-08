from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label


from math import atan2, pi

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
  
class MyWidget(Widget):
  def __init__(self):
    super(MyWidget, self).__init__()
    self.labeltext = 'direction:'
    self.label = Label(text=self.labeltext)
    self.add_widget(self.label)

  def on_touch_down(self, touch): 
    self.pos_ini =(touch.x, touch.y)
    #touch.ud['dir'] = pos_ini 
  
  def on_touch_up(self, touch): 
    self.pos_end = (touch.x, touch.y)
    direc = direction(self.pos_ini,self.pos_end)
    self.labeltext = 'direction: (' + str(direc[0]) + ',' + str(direc[1]) + ',' + str(direc[2]) + ')'
    self.label.text = self.labeltext

class DirTestApp(App):
  def build(self):
    game = MyWidget()
    return game

if __name__ == '__main__':
  DirTestApp().run()