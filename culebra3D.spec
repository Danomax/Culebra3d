# -*- mode: python -*-
from kivy.deps import sdl2, glew
block_cipher = None


a = Analysis(['culebra3d_py3.py'],
             pathex=['C:\Users\jacue\OneDrive\Documentos\Proyectos\Python Scripts\kivy\culebra3D'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='culebra3D',
          debug=False,
          strip=False,
          upx=True,
          console=False, 
		  icon='culebra.ico')
coll = COLLECT(exe, Tree('C:\Users\jacue\OneDrive\Documentos\Proyectos\Python Scripts\kivy\culebra3D'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='culebra3D')
