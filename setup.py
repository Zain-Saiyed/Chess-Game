from cx_Freeze import setup, Executable

## Two Player
##setup(name='Two Player Chess game',
##      version='1.0',
##      description='Two Player Chess game',
##      executables=[Executable("Chess2player.py", base = "Win32GUI", icon='Chess_image/exe_icon.ico')]      
##)

## AI
setup(name='AI Chess game',
      version='1.0',
      description='AI Chess game',
      executables=[Executable(script="AIChess.py", base = "Win32GUI", icon='Chess_image/exe_icon.ico')]      
)
