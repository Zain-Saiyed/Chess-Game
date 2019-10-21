from cx_Freeze import setup, Executable

setup(name='Two Player Chess game',
      version='1.0',
      description='Two Player Chess game',
      executables=[Executable("Chess2player.py", base = "Win32GUI")]      
)
