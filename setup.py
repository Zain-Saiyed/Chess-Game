from cx_Freeze import setup, Executable
import sys

if sys.platform == "win32":
    base = "Win32GUI"

## Two Player
    
setup(name='Two Player Chess game',
      version='1.0',
      description='Two Player Chess game',
      options = {
          'build_exe':{
              "include_files":["gameFonts/","Chess_image/"]
            }
          },
      executables=[
          Executable("Chess2player.py",
                     base = base,
                     icon='Chess_image/exe_icon.ico',
                     shortcutName='Two Player Chess',
                     targetName='Chess2P.exe')]      
)

## AI
    
##setup(name='AI Chess game',
##      version='1.0',
##      description='AI Chess game',
##      options = {
##          'build_exe':{
##              "include_files":["gameFonts/","Chess_image/"]
##            }
##          },
##      executables=[Executable(script="AIChess.py", base = base, icon='Chess_image/exe_icon.ico')]      
##)

    
