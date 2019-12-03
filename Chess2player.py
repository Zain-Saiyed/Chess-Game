import pygame, time, chess, copy, threading, sys

pygame.init()
pygame.font.init()
display_width, display_height, piece_size, displayWidth = 600, 600, 75, 1000
gameDisplay = pygame.display.set_mode((displayWidth, display_height))
pygame.display.set_caption('Chess Game')
# rook=5,knight=3,bishop=3,queen=9,king=99999,pawn=1
whitepieces = [pygame.image.load('Chess_image/Chess_tile_rl.png'), pygame.image.load('Chess_image/Chess_tile_nl.png'),
               pygame.image.load('Chess_image/Chess_tile_bl.png'), pygame.image.load('Chess_image/Chess_tile_ql.png'),
               pygame.image.load('Chess_image/Chess_tile_kl.png'), pygame.image.load('Chess_image/Chess_tile_pl.png')]
blackpieces = [pygame.image.load('Chess_image/Chess_tile_rd.png'), pygame.image.load('Chess_image/Chess_tile_nd.png'),
               pygame.image.load('Chess_image/Chess_tile_bd.png'), pygame.image.load('Chess_image/Chess_tile_qd.png'),
               pygame.image.load('Chess_image/Chess_tile_kd.png'), pygame.image.load('Chess_image/Chess_tile_pd.png')]
#grey_image = pygame.image.load('Chess_image/grey.png')
chessBoard = pygame.image.load('Chess_image/chess_board.png')               #1
BoardLayout = [['br1', 'bh1', 'bb1', 'bq', 'bk', 'bb2', 'bh2', 'br2'],      #2
               ['bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'],    #3
               ['0', '0', '0', '0', '0', '0', '0', '0'],                    #4
               ['0', '0', '0', '0', '0', '0', '0', '0'],                    #5
               ['0', '0', '0', '0', '0', '0', '0', '0'],                    #6
               ['0', '0', '0', '0', '0', '0', '0', '0'],                    #7
               ['wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],    #8
               ['wr1', 'wh1', 'wb1', 'wq', 'wk', 'wb2', 'wh2', 'wr2']]      #9
                # a      b     c     d     e     f     g     h

Board_backup = copy.deepcopy(BoardLayout)

wh_checkmate=False
bl_checkmate=False
mate_list_w=[]
mate_list_b=[]
blue,white, black, grey,red,lgreen,lred,green = (0,0,255),(255, 255, 255), (0, 0, 0), (83, 83, 83, 50),(255,0,0),(0,200,0),(200,0,0),(0,255,0)
Exit, intro = False,True
clock = pygame.time.Clock()
smallfont = pygame.font.Font("gameFonts/GeorgiaPro-BlackItalic.ttf", 25)
medfont = pygame.font.Font("gameFonts/GeorgiaPro-BlackItalic.ttf", 50)
largefont = pygame.font.Font("gameFonts/GeorgiaPro-BlackItalic.ttf", 80)
Elargefont = pygame.font.Font("gameFonts/OLDENGL.ttf", 80)
alphabets = { 'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7 }
# draws Chessboard
# Initial printing of Boards and chess pieces
def drawBoard():
    gameDisplay.blit(chessBoard, (0, 0))
    for i in range(0, 8):
        for j in range(0, 8):
            if BoardLayout[i][j] is not '0' and BoardLayout[i][j][0] is 'b':
                if BoardLayout[i][j][1] is 'r':
                    gameDisplay.blit(blackpieces[0], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'h':
                    gameDisplay.blit(blackpieces[1], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'b':
                    gameDisplay.blit(blackpieces[2], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'q':
                    gameDisplay.blit(blackpieces[3], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'k':
                    gameDisplay.blit(blackpieces[4], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'p':
                    gameDisplay.blit(blackpieces[5], (j * piece_size, i * piece_size))
            elif BoardLayout[i][j] is not '0' and BoardLayout[i][j][0] is 'w':
                if BoardLayout[i][j][1] is 'r':
                    gameDisplay.blit(whitepieces[0], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'h':
                    gameDisplay.blit(whitepieces[1], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'b':
                    gameDisplay.blit(whitepieces[2], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'q':
                    gameDisplay.blit(whitepieces[3], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'k':
                    gameDisplay.blit(whitepieces[4], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'p':
                    gameDisplay.blit(whitepieces[5], (j * piece_size, i * piece_size))
            else:
                continue
    pygame.display.update()

class pieces:
    greySurface = []
    # flag_check=is_check()

    def possibleMove(self):
         for gs in self.greySurface:
            s = pygame.Surface((piece_size,piece_size), pygame.SRCALPHA)   
            s.fill((93,93,93,128))                         
            gameDisplay.blit(s,[gs[1]*piece_size,gs[0]*piece_size] )
            pygame.display.update()
##        for gs in self.greySurface:
##            gameDisplay.blit(grey_image,(gs[1] * piece_size, gs[0] * piece_size))
##            pygame.display.update()

    def find_ele(self, value,every=False):
        if every:
            listofLocations = []
            for row in range(8):
                for col in range(8):
                    if BoardLayout[row][col] == value:
                        x = col
                        y = row
                        listofLocations.append((x,y))
            return listofLocations
        else:    
            flag = False
            for i in range(8):  # len(BoardLayout[0])
                for j in range(8):
                    x = BoardLayout[i][j].find(value)
                    if x != -1:
                        flag = True
                        break
                if (flag):   break
            if flag is False:
                return [i + 1, j + 1]
            return [i, j]
    
    def mov_item(self,value):
        self.greySurface=[]
        print(value)
        if value[1] is 'r':
            self.mov_rook(value)
        elif value[1] is 'h':
            self.mov_knight(value)
        elif value[1] is 'b':
            self.mov_bishop(value)
        elif value[1] is 'q':
            self.mov_queen(value)
        elif value[1] is 'k':
            self.mov_king(value)
        elif value[1] is 'p':
            self.mov_pawn(value)
        else:
            print("Haha")

    def mov_pawn(self,value):
        pos = self.find_ele(value,False)
        if value[0] == 'b' and pos[0] == 1 :
            if BoardLayout[pos[0]+1][pos[1]][0] is '0':
                self.greySurface.append([pos[0]+1, pos[1] ])
            if BoardLayout[pos[0]+2][pos[1]][0] is '0' and BoardLayout[pos[0]+1][pos[1]][0] is '0':
                self.greySurface.append([pos[0]+2, pos[1]])
        if value[0] == 'b'  and pos[0]+1 in range(0,8) and pos[1]+1 in range(0,8) and BoardLayout[pos[0]+1][pos[1]+1][0] is not value[0] and BoardLayout[pos[0]+1][pos[1]+1][0] is not '0' :
            self.greySurface.append([pos[0]+1, pos[1] +1])
        if value[0] == 'b' and pos[0]+1 in range(0,8) and pos[1]-1 in range(0,8) and BoardLayout[pos[0]+1][pos[1]-1][0] is not value[0] and BoardLayout[pos[0]+1][pos[1]-1][0] is not '0' :
            self.greySurface.append([pos[0]+1, pos[1] -1])
        if value[0] == 'b'  and pos[0]+1 in range(0,8) and pos[1]-1 in range(0,8) and pos[0] is not 1 and BoardLayout[pos[0]+1][pos[1]][0] is '0':
            self.greySurface.append([pos[0]+1, pos[1] ])
        if value[0] == 'w' and pos[0] == 6 :
            if BoardLayout[pos[0]-1][pos[1]][0] is '0':
                self.greySurface.append([pos[0]-1, pos[1] ])
            if BoardLayout[pos[0]-2][pos[1]][0] is '0' and BoardLayout[pos[0]-1][pos[1]][0] is '0':
                self.greySurface.append([pos[0]-2, pos[1]])
        if value[0] == 'w' and pos[0]-1 in range(0,8) and pos[1]+1 in range(0,8) and BoardLayout[pos[0]-1][pos[1]+1][0] is not value[0] and BoardLayout[pos[0]-1][pos[1]+1][0] is not '0' :
            self.greySurface.append([pos[0]-1, pos[1] +1])
        if value[0] == 'w' and pos[0]-1 in range(0,8) and pos[1]-1 in range(0,8) and BoardLayout[pos[0]-1][pos[1]-1][0] is not value[0] and BoardLayout[pos[0]-1][pos[1]-1][0] is not '0' :
            self.greySurface.append([pos[0]-1, pos[1] -1])
        if value[0] == 'w' and pos[0] is not 1  and pos[0]-1 in range(0,8) and pos[1] in range(0,8) and BoardLayout[pos[0]-1][pos[1]][0] is '0' :
            self.greySurface.append([pos[0]-1, pos[1] ])


    def mov_rook(self, value):
        pos = self.find_ele(value,False)
        temp_add = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for i in range(4):
            t_x = pos[0]
            t_y = pos[1]
            while True:
                t_x = t_x + temp_add[i][0]
                t_y = t_y + temp_add[i][1]
                if t_x in range(0, 8) and t_y in range(0, 8) and BoardLayout[t_x][t_y][0] is not value[0]:
                    if BoardLayout[t_x][t_y][0] is not '0':
                        self.greySurface.append([t_x, t_y])
                        break
                    elif BoardLayout[t_x][t_y][0] is '0':
                        self.greySurface.append([t_x, t_y])
                else:
                    break

    def mov_knight(self, value):
        pos = self.find_ele(value)
        temp_add = [[1, 2], [-1, 2], [-1, -2], [1, -2], [2, -1], [-2, -1], [2, 1], [-2, 1]]
        for i in range(8):
            if pos[0] + temp_add[i][0] in range(0, 8) and pos[1] + temp_add[i][1] in range(0, 8) and \
                    BoardLayout[pos[0] + temp_add[i][0]][pos[1] + temp_add[i][1]][0] is not value[0]:
                self.greySurface.append([pos[0] + temp_add[i][0], pos[1] + temp_add[i][1]])

    def mov_bishop(self, value):
        pos = self.find_ele(value)
        temp_add = [[1, -1], [-1, 1], [1, 1], [-1, -1]]
        for i in range(4):
            t_x = pos[0]
            t_y = pos[1]
            while True:
                t_x = t_x + temp_add[i][0]
                t_y = t_y + temp_add[i][1]
                if t_x in range(0, 8) and t_y in range(0, 8) and BoardLayout[t_x][t_y][0] is not value[0]:
                    if BoardLayout[t_x][t_y][0] is not '0':
                        self.greySurface.append([t_x, t_y])
                        break
                    elif BoardLayout[t_x][t_y][0] is '0':
                        self.greySurface.append([t_x, t_y])

                else:
                    break

    def mov_queen(self, value):
        pos = self.find_ele(value)
        temp_add = [[1, -1], [-1, 1], [1, 1], [-1, -1], [0, 1], [1, 0], [0, -1], [-1, 0]]
        for i in range(8):
            t_x = pos[0]
            t_y = pos[1]
            while True:
                t_x = t_x + temp_add[i][0]
                t_y = t_y + temp_add[i][1]
                if t_x in range(0, 8) and t_y in range(0, 8) and BoardLayout[t_x][t_y][0] is not value[0]:
                    if BoardLayout[t_x][t_y][0] is not '0':
                        self.greySurface.append([t_x, t_y])
                        break
                    elif BoardLayout[t_x][t_y][0] is '0':
                        self.greySurface.append([t_x, t_y])
                else:
                    break

    def mov_king(self, value):
        pos = self.find_ele(value)
        temp_add = [[1, -1], [-1, 1], [1, 1], [-1, -1], [0, 1], [1, 0], [0, -1], [-1, 0]]
        for i in range(8):
            if pos[0] + temp_add[i][0] in range(0, 8) and pos[1] + temp_add[i][1] in range(0, 8) and \
                    BoardLayout[pos[0] + temp_add[i][0]][pos[1] + temp_add[i][1]][0] is not value[0]:
                self.greySurface.append([pos[0] + temp_add[i][0], pos[1] + temp_add[i][1]])
        #add a move where if in that grey square any white can attack then dont move        
                
def quitgame():
     pygame.quit()
     sys.exit()
     
##This is the end of class functions-----------------------------------------------------------------------------------------|         
def text_objects(text,color,size):
    if size=='small':
        textSurface=smallfont.render(text,True,color)
    elif size=='medium':
        textSurface=medfont.render(text,True,color)
    elif size=='large':
        textSurface=largefont.render(text,True,color)
    elif size=='Elarge':
        textSurface=Elargefont.render(text,True,color)
        
    return textSurface,textSurface.get_rect()

def message_to_screen(msg,color,xPos,yPos,y_displace=0,size = "small"):
    textSurface,textRect=text_objects(msg,color,size)
    textRect.center=xPos,yPos+y_displace
    gameDisplay.blit(textSurface,textRect)

#This gets the possible moves checks if check_mate(remove) then prints the possible grey squares
def get_display(mouse,player):
        l=[]
        if mouse[0] < 8 and mouse[1] < 8:
            if BoardLayout[mouse[0]][mouse[1]][0] is 'w' and player is 1:
                p=pieces()
                p.mov_item(BoardLayout[mouse[0]][mouse[1]])
                l=p.greySurface
                if wh_checkmate==True and BoardLayout[mouse[0]][mouse[1]] != 'wk':
                    lw=getlist('w')
                    l=l and lw
                drawBoard()
                p.possibleMove()
                return l
            elif BoardLayout[mouse[0]][mouse[1]][0] is 'b' and player is 2 :
                p=pieces()
                p.mov_item(BoardLayout[mouse[0]][mouse[1]])
                l=p.greySurface
                if bl_checkmate==True and BoardLayout[mouse[0]][mouse[1]] !='bk' :
                    lb=getlist('b')
                    l=l and lb
                drawBoard()
                p.possibleMove()
                return l
            else:
                return l

def getlist(pcs):
    li=[]
    p_temp=pieces()
    if pcs is 'w':
        for i in mate_list_w:
            p_temp.mov_item(i)
            li.append(p_temp.greySurface)
            li.append(p_temp.find_ele(i))
    else:
        for i in mate_list_b:
            p_temp.mov_item(i)
            li.append(p_temp.greySurface)
            li.append(p_temp.find_ele(i))
    return li

#Dispaly button on screen
def button(msg,x,y,breadth,height,lowcol,hicol,action=None):
     mouse = pygame.mouse.get_pos()
     click = pygame.mouse.get_pressed()
     if x + breadth > mouse[0] >x and y+height > mouse[1] > y:
          pygame.draw.rect(gameDisplay, lowcol,(x,y,breadth,height))
          if click[0] == 1 and action !=None:
               action()             
     else:
          pygame.draw.rect(gameDisplay, hicol ,(x,y,breadth,height))
          
##     smallText = pygame.font.Font('GeorgiaPro-BlackItalic.ttf',20)
     textSurf, textRect = text_objects(msg,black,'small')
     ##adding text on button
     textRect.center = ((x+(breadth/2)),(y+(height/2)))
     gameDisplay.blit(textSurf,textRect)
def Continue():
    gameDisplay.fill(white)
    pygame.display.update()
    global intro
    intro = False
def game_intro():
    global intro
    intro = True
    while intro:
        gameDisplay.fill(white)
        message_to_screen(".::CHESS::.",black,(displayWidth/2),(display_height/2),-40,"Elarge")
        message_to_screen("Press S to Start / Press Q to Quit ",blue,(displayWidth/2),(display_height/2),40)
        button("QUIT",680,440,140,50,red,lred,quitgame)
        button("START",180,440,140,50,green,lgreen,Continue)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    Continue()
                if event.key == pygame.K_q:
                    quitgame()
        clock.tick(15)
#Thisis for moving the pieces
def move_pieces(mouse_u,mouse_d):
    global wh_checkmate,bl_checkmate
    swap = BoardLayout[mouse_d[0]][mouse_d[1]]
    print('Moving pieces',swap)
    if BoardLayout[mouse_d[0]][mouse_d[1]][0] == 'w' and BoardLayout[mouse_d[0]][mouse_d[1]] in mate_list_b:
        mate_list_b.remove(BoardLayout[mouse_d[0]][mouse_d[1]])
        if not mate_list_b:
            bl_checkmate=False
    if BoardLayout[mouse_d[0]][mouse_d[1]][0] == 'b' and BoardLayout[mouse_d[0]][mouse_d[1]] in mate_list_w:
        mate_list_w.remove(BoardLayout[mouse_d[0]][mouse_d[1]])
        if not mate_list_w:
            wh_checkmate=False
    #This is for swapping the pieces for movement
    BoardLayout[mouse_d[0]][mouse_d[1]]='0'
    BoardLayout[mouse_u[0]][mouse_u[1]]=swap
##    pcs = AI()
##    pcs.movePiece(swap)
    
#checks the check mate condition!!
def check_mate(mouse_d):
    global wh_checkmate,bl_checkmate
    p=pieces()
    p.mov_item(BoardLayout[mouse_d[0]][mouse_d[1]])
    mate=p.greySurface
    print("HI check mate function")
    print(mate)
    for i in mate:
        if BoardLayout[i[0]][i[1]][0] is not BoardLayout[mouse_d[0]][mouse_d[1]][0] and BoardLayout[i[0]][i[1]][0]\
                is not '0' and BoardLayout[i[0]][i[1]][1] is 'k':
            if BoardLayout[i[0]][i[1]][0] == 'w':
                mate_list_w.append(BoardLayout[mouse_d[0]][mouse_d[1]])
                wh_checkmate=True
                break
            elif BoardLayout[i[0]][i[1]][0]=='b':
                mate_list_b.append(BoardLayout[mouse_d[0]][mouse_d[1]])
                bl_checkmate=True
                break
    print("white")        
    print(mate_list_w)
    print("black")        
    print(mate_list_b)
    
def update_lists():
    global bl_checkmate,wh_checkmate
    temp=pieces()
    for i in mate_list_b:
        if temp.find_ele(i) == [8,8]:
            mate_list_b.remove(i)
            if not mate_list_b:
                bl_checkmate=False
    for i in mate_list_w:
        print(temp.find_ele(i))
        if temp.find_ele(i) == [8,8]:
            mate_list_w.remove(i)
            if not mate_list_w:
                wh_checkmate=False

def game_ex(player):
    ex = True
    while ex:
        gameDisplay.fill(white)
        message_to_screen("GAME  OVER!",black,(displayWidth/2),(display_height/2 - 100),-40,"Elarge")
        message_to_screen(("Player "+str(player)+" Wins!"),red,(displayWidth/2),(display_height/2 - 50),40)
        #message_to_screen(player, red,(displayWidth/2),(display_height/2),80)
        message_to_screen("Press R to play again / Press Q to Exit", blue,(displayWidth/2),(display_height/2)+piece_size-50, 50)
        button("Play Again",80,500,165,50,green,lgreen,restart)
        button("Quit",displayWidth-220,500,140,50,red,lred,quitgame)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    gameDisplay.fill(white)
                    pygame.display.update()
                    global BoardLayout
                    BoardLayout = copy.deepcopy(Board_backup)
                    gameLoop()    
                if event.key == pygame.K_q:
                    quitgame()
        clock.tick(15)
        
def is_king_alive():
    temp=pieces()
    if temp.find_ele('wk') == [8,8]:
        game_ex("Black")
    elif temp.find_ele('bk')==[8,8]:
        game_ex("White")

def restart():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            global BoardLayout
            BoardLayout = copy.deepcopy(Board_backup)            
            gameLoop()
#----------------------------------------------MAIN------------------------------------------
def gameLoop():
    gameDisplay.fill(white)
    drawBoard()
    gameExit=False
    gameover=False
    mouse_d,mouse_u = [-1,-1],[-1,-1]
    player=1
    mouse_up,mouse_down=[0,0],[0,0]    
    message_to_screen("Turn : Player White ", black,(displayWidth-200),(piece_size//2), 0,"small")
    button("QUIT",730,525,140,50,red,lred,quitgame) 
    pygame.display.update()
    while not gameExit:
        press_flag = 0
        press_up_flag = 0
        while gameover:
            gameDisplay.fill(white)
            message_to_screen("Game Over", red,(displayWidth/2),(display_height/2), -50, "large")
            message_to_screen("Press R to play again / Press Q to Exit", black,(displayWidth/2),(display_height/2), 50)            
            pygame.display.update()
            # this case is for check mate so that game is over 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameover = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameover = False
                    if event.key == pygame.K_r:
                        gameLoop()
        button("QUIT",730,525,140,50,red,lred,quitgame) 
        pygame.display.update()               
        #this is to check that if there is a mouse click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit=True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down=pygame.mouse.get_pos()
                press_flag=1                 
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_up = pygame.mouse.get_pos()
                press_up_flag=1
        #check if the mouse click is the chess board region
        if mouse_up[1] < 600 and mouse_up[0] < 600 and mouse_down[1] < 600 and mouse_down[0] < 600:        
            #check the mouse click and its further action 
            if press_flag is 1:
                print('MOuse Button DOwn')
                mouse_d = [int((mouse_down[1]) / 75),int((mouse_down[0]) / 75)]
                print(mouse_d)
                #This prints the possible moves "chess"
    ##            play.possibleMove()
                l = get_display(mouse_d, player)
            if press_up_flag is 1:
                print('MOuse Butotn UP')            
                mouse_u= [int((mouse_up[1]) / 75), int((mouse_up[0]) / 75)]
                print(mouse_u)
                #Mouse up prints the coordinates when the mouse button lifts up
                print(l)
                if mouse_u in l:
                    #If the entered position is in the list then move the element
                    move_pieces(mouse_u,mouse_d)
                    gameDisplay.fill(white)
                    drawBoard()                
                    print(mouse_u)
                    check_mate(mouse_u)
                    update_lists()
                    print(wh_checkmate,bl_checkmate)
                    print(mate_list_w,mate_list_b)
                    is_king_alive() #checks if the kings are alive if no then game is over
                    if player == 1:
                        message_to_screen("Turn : Player Black ", black,(displayWidth-200),(piece_size//2),0, "small")
                        pygame.display.update()
                        player=2
                    else:
                        message_to_screen("Turn : Player White ", black,(displayWidth-200),(piece_size//2), 0,"small")
                        pygame.display.update()
                        player = 1
                else:
                    continue

        clock.tick(10)
def main():
    game_intro()
    gameLoop()

main()
sys.exit()

#--------------------------------------------------------------------------------------------------------------------
##    'br1', 'bh1', 'bb1', 'bq',
##def convert(data):
##    value = ""
##    if data[0] == 'w':
##        if data[1] ==
##class AI:
##    
##    board = chess.Board()
##    legalM = []
##    #N-knight,
##    def possibleMove(self):
##        board = chess.Board()
##        legalM, LegalM = board.legal_moves, []
##        x,y= 0,0
##        print(legalM)
##        for pos in legalM:
##            pos = str(pos)
##            if pos[0] is 'N':   #Knight
##                y = alphabets(pos[1])*piece_size    
##                x = int(pos[2]) * piece_size    
##                LegalM.append([x,y])
##        print(LegalM)         
##    def movePiece(self,piece):
##        if piece
##        board.push_san()
#play = AI()
#-------------------------------------------------------------------------------------------------------------------


