# -*- coding: utf-8 -*-

from distutils.core import setup 
import py2exe,sys,os
 
setup(name="Culebra 3D", 
 version="1.0", 
 description="El famoso juego de la culebra en un cubo tridimensional. Fijate en la sombra para alinear la culebra al alimento", 
 author="Daniel Cortes", 
 author_email="sgtdano@gmail.com", 
 url="https://github.com/Danomax/Culebra3d", 
 license="GNU General Public License v3.0", 
 options={"py2exe": {"bundle_files": 3,'compressed': True,
                     "dll_excludes": ['libglib-2.0-0.dll',
					                  'libgstreamer-1.0-0.dll',
									  'libgobject-2.0-0.dll'
					 ]

                    }
         }, 
 windows=[{'script': "culebra3d_py3.py"}],
 zipfile=None,
)