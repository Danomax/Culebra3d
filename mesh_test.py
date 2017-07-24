#mesh Test

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Line, Rectangle, Mesh
from kivy.clock import Clock
from kivy.properties import ListProperty, ObjectProperty, NumericProperty


class MyWidget(Widget):
  def __init__(self):
    super(MyWidget, self).__init__()
    self.mesh_texture = ObjectProperty()
    self.mesh_texture = CoreImage('circulo de angulos.png').texture 
    self.mesh_points = ListProperty([])
    self.mesh_points = points = [0,0,self.width, self.height, 0,0,1,1]
    with self.canvas:
      self.mesh = Mesh(vertices = self.mesh_points,indices = range(len(self.mesh_points) // 4),texture=self.mesh_texture,mode='points')
    
  def on_touch_down(self, touch): 
    x,y =(touch.x, touch.y)
    self.mesh_points.extend([x,y,0,0])
    self.mesh.indices = range(len(self.mesh_points) // 4)

class Mesh_testApp(App):
  def build(self):
    widg = MyWidget()
    Window.size = widg.size
    return widg

if __name__ == "__main__":
  Mesh_testApp().run()
