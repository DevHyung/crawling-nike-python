# -*- mode: python -*-

block_cipher = None


a = Analysis(['FileScript.py'],
             pathex=['C:\\Users\\������\\Desktop\\nike-scrapping'],
             binaries=[],
             datas=[],
             hiddenimports=['os','shutil'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='FileScript',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='favi.ico')
