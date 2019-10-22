import pygame, time, chess,random
from collections import Counter

pygame.init()
pygame.font.init()
display_width, display_height, piece_size ,displayWidth= 600, 600, 75, 1000
gameDisplay = pygame.display.set_mode((displayWidth, display_height))
pygame.display.set_caption('.::Chess Game::.')
gameIcon = pygame.image.load('Chess_image/icon.png')
pygame.display.set_icon(gameIcon)
whitepieces = [pygame.image.load('Chess_image/Chess_tile_rl.png'), pygame.image.load('Chess_image/Chess_tile_nl.png'),
               pygame.image.load('Chess_image/Chess_tile_bl.png'), pygame.image.load('Chess_image/Chess_tile_ql.png'),
               pygame.image.load('Chess_image/Chess_tile_kl.png'), pygame.image.load('Chess_image/Chess_tile_pl.png')]
blackpieces = [pygame.image.load('Chess_image/Chess_tile_rd.png'), pygame.image.load('Chess_image/Chess_tile_nd.png'),
               pygame.image.load('Chess_image/Chess_tile_bd.png'), pygame.image.load('Chess_image/Chess_tile_qd.png'),
               pygame.image.load('Chess_image/Chess_tile_kd.png'), pygame.image.load('Chess_image/Chess_tile_pd.png')]
##choice='negamax'
# Store the piece square tables here so they can be accessed globally by pieceSquareTable() function:
pawn_table = [0, 0, 0, 0, 0, 0, 0, 0,
              50, 50, 50, 50, 50, 50, 50, 50,
              10, 10, 20, 30, 30, 20, 10, 10,
              5, 5, 10, 25, 25, 10, 5, 5,
              0, 0, 0, 20, 20, 0, 0, 0,
              5, -5, -10, 0, 0, -10, -5, 5,
              5, 10, 10, -20, -20, 10, 10, 5,
              0, 0, 0, 0, 0, 0, 0, 0]
knight_table = [-50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20, 0, 0, 0, 0, -20, -40,
                -30, 0, 10, 15, 15, 10, 0, -30,
                -30, 5, 15, 20, 20, 15, 5, -30,
                -30, 0, 15, 20, 20, 15, 0, -30,
                -30, 5, 10, 15, 15, 10, 5, -30,
                -40, -20, 0, 5, 5, 0, -20, -40,
                -50, -90, -30, -30, -30, -30, -90, -50]
bishop_table = [-20, -10, -10, -10, -10, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 5, 5, 10, 10, 5, 5, -10,
                -10, 0, 10, 10, 10, 10, 0, -10,
                -10, 10, 10, 10, 10, 10, 10, -10,
                -10, 5, 0, 0, 0, 0, 5, -10,
                -20, -10, -90, -10, -10, -90, -10, -20]
rook_table = [0, 0, 0, 0, 0, 0, 0, 0,
              5, 10, 10, 10, 10, 10, 10, 5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              0, 0, 0, 5, 5, 0, 0, 0]
queen_table = [-20, -10, -10, -5, -5, -10, -10, -20,
               -10, 0, 0, 0, 0, 0, 0, -10,
               -10, 0, 5, 5, 5, 5, 0, -10,
               -5, 0, 5, 5, 5, 5, 0, -5,
               0, 0, 5, 5, 5, 5, 0, -5,
               -10, 5, 5, 5, 5, 5, 0, -10,
               -10, 0, 5, 0, 0, 0, 0, -10,
               -20, -10, -10, 70, -5, -10, -10, -20]
king_table = [-30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -20, -30, -30, -40, -40, -30, -30, -20,
              -10, -20, -20, -20, -20, -20, -20, -10,
              20, 20, 0, 0, 0, 0, 20, 20,
              20, 30, 10, 0, 0, 10, 30, 20]
king_endgame_table = [-50, -40, -30, -20, -20, -30, -40, -50,
                      -30, -20, -10, 0, 0, -10, -20, -30,
                      -30, -10, 20, 30, 30, 20, -10, -30,
                      -30, -10, 30, 40, 40, 30, -10, -30,
                      -30, -10, 30, 40, 40, 30, -10, -30,
                      -30, -10, 20, 30, 30, 20, -10, -30,
                      -30, -30, 0, 0, 0, 0, -30, -30,
                      -50, -30, -30, -30, -30, -30, -30, -50]
board_mat=[]
chessBoard = pygame.image.load('Chess_image/chess_board.png')

cream,blue, white, black, grey, red, lgreen, lred, green =(255,253,208),(0,0,255),(255, 255, 255),(0, 0, 0),(83, 83, 83, 50),(255,0,0),(70, 255, 70),(255,70,70),(0,255,0)
Exit = False
clock = pygame.time.Clock()
smallfont = pygame.font.Font("gameFonts/calibri.ttf", 25)
##smallfont = pygame.font.Font("GeorgiaPro-BlackItalic.ttf", 25)
medfont = pygame.font.Font("gameFonts/calibri.ttf", 30)
largefont = pygame.font.Font("gameFonts/GeorgiaPro-BlackItalic.ttf", 80)
Elargefont = pygame.font.Font("gameFonts/GOUDOS.ttf", 120)
Mlargefont = pygame.font.Font("gameFonts/calibri.ttf", 80)
board=chess.Board()
def drawBoard():
    global board
    # Display the chessBoard & Borders
    gameDisplay.blit(chessBoard, (0, 0))

    for i in range(0,8):
        for j in range (0,8):
            if chess.Board.piece_at(board, square=(i*8)+j) is not None:
                if chess.Board.piece_at(board, square=(i*8)+j).color is chess.WHITE:
                       if chess.Board.piece_at(board, square=(i*8)+j).piece_type == chess.PAWN:
                           gameDisplay.blit(whitepieces[5],((7-j)*piece_size,i*piece_size))
                       elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.ROOK:
                           gameDisplay.blit(whitepieces[0], ((7-j) * piece_size, i * piece_size))
                       elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.KNIGHT:
                           gameDisplay.blit(whitepieces[1], ((7-j) * piece_size, i * piece_size))
                       elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.BISHOP:
                           gameDisplay.blit(whitepieces[2], ((7-j) * piece_size, i * piece_size))
                       elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.QUEEN:
                           gameDisplay.blit(whitepieces[3], ((7-j) * piece_size, i * piece_size))
                       elif chess.Board.piece_at(board, square=(i*8)+j).piece_type == chess.KING:
                           gameDisplay.blit(whitepieces[4],((7-j)*piece_size,i*piece_size))

                if chess.Board.piece_at(board, square=(i * 8) + j).color is chess.BLACK:

                    if chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.PAWN:

                        gameDisplay.blit(blackpieces[5], ((7-j) * piece_size, i * piece_size))

                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.ROOK:

                        gameDisplay.blit(blackpieces[0], ((7-j) * piece_size, i * piece_size))

                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.KNIGHT:

                        gameDisplay.blit(blackpieces[1], ((7-j) * piece_size, i * piece_size))

                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.BISHOP:

                        gameDisplay.blit(blackpieces[2], ((7-j) * piece_size, i * piece_size))

                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.QUEEN:

                        gameDisplay.blit(blackpieces[3], ((7-j) * piece_size, i * piece_size))

                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.KING:

                        gameDisplay.blit(blackpieces[4], ((7-j) * piece_size, i * piece_size))

    pygame.display.update()

def Draw_Borders(value,colour):
    # Display Borders
    pygame.draw.rect(gameDisplay, colour, [0,0,displayWidth,value])
    pygame.draw.rect(gameDisplay, colour, [0,0,value,display_height])
    pygame.draw.rect(gameDisplay, colour, [0,display_height-value,displayWidth,value])
    pygame.draw.rect(gameDisplay, colour, [displayWidth-value,0,value,display_height])
    pygame.display.update()

def quitgame():
     pygame.quit()
     quit() 

# Function to Print the Value of the current positon Eg. a5,e6 etc
def print_pos(mouse_pointer):
    mouse_pointer[0] = chr(104- mouse_pointer[0])
    mouse_pointer[1]+=1
    pointer = str(mouse_pointer[0]) + str(mouse_pointer[1])
    return pointer

def text_objects(text,color,size):
    if size=='ssmall':
        textSurface=ssmallfont.render(text,True,color)
    elif size=='small':
        textSurface=smallfont.render(text,True,color)
    elif size=='medium':
        textSurface=medfont.render(text,True,color)
    elif size=='large':
        textSurface=largefont.render(text,True,color)
    elif size=='Elarge':
        textSurface=Elargefont.render(text,True,color)
    elif size=='Mlarge':
        textSurface=Mlargefont.render(text,True,color)        
    return textSurface,textSurface.get_rect()

def message_to_screen(msg,color,xPos,yPos,y_displace=0,size = "small"):
    textSurface,textRect=text_objects(msg,color,size)
    textRect.center=xPos,yPos+y_displace
    gameDisplay.blit(textSurface,textRect)
    
#Dispaly button on screen
def button(msg,x,y,breadth,height,lowcol,hicol,action=None):
     mouse = pygame.mouse.get_pos()
     click = pygame.mouse.get_pressed()
     if x + breadth > mouse[0] >x and y+height > mouse[1] > y:
        #   pygame.draw.rect(gameDisplay, lowcol,(x,y,breadth,height))
          round_rect(gameDisplay,x,y,breadth,height,lowcol)

          if click[0] == 1 and action !=None:
              for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        action()             
     else:
        #   pygame.draw.rect(gameDisplay, hicol ,(x,y,breadth,height))
            round_rect(gameDisplay,x,y,breadth,height,hicol)

     smallText = pygame.font.Font('gameFonts/calibri.ttf',20)
     textSurf, textRect = text_objects(msg,black,'small')
     ##adding text on button
     textRect.center = ((x+(breadth/2)),(y+(height/2)))
     gameDisplay.blit(textSurf,textRect)
     
def round_rect(gameDisplay,x,y,length,breadth,color,radius = 10 ):
    xpos = int(x + radius)
    ypos = int(y + radius)
    
    ##  Body rectangle
    pygame.draw.rect(gameDisplay, color, [xpos,ypos,length-radius*2,breadth-radius*2])
    ##  Round corners
    pygame.draw.circle(gameDisplay, color, [xpos,ypos],radius )
    pygame.draw.circle(gameDisplay, color, [xpos,ypos+breadth-2*radius],radius )
    pygame.draw.circle(gameDisplay, color, [xpos+length-2*radius,ypos],radius )
    pygame.draw.circle(gameDisplay, color, [xpos+length-2*radius,ypos+breadth-2*radius],radius )
    ##  Rectangle strips
    pygame.draw.rect(gameDisplay, color, [xpos,ypos-radius,length-radius*2,radius])
    pygame.draw.rect(gameDisplay, color, [xpos-radius,ypos,radius,breadth-radius*2])
    pygame.draw.rect(gameDisplay, color, [xpos+length-2*radius,ypos,radius,breadth-radius*2])
    pygame.draw.rect(gameDisplay, color, [xpos,ypos+breadth-2*radius,length-radius*2,radius])

    pygame.display.update()



def Continue():
    gameDisplay.fill(cream)
    pygame.display.update()
    global intro
##    global choice
##    choice = choose_option()
    intro = False
    
############################################################################################################
def undo():
    global board
    pygame.draw.rect(gameDisplay, cream, (600,75,400,450))
    try:
        board.pop()
        board.pop()        
        pygame.display.update()
        message_to_screen(("Moves undone!"),black,(displayWidth)-200,(display_height/2-50),40,'small')           
    except IndexError as error:
##        pygame.draw.rect(gameDisplay, cream, (600,75,400,450))
        pygame.display.update()
        message_to_screen(("Please play moves to UNDO"),red,(displayWidth)-200,(display_height/2-50),40,'medium')
    return 1

def restart():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            global BoardLayout
            BoardLayout = Board_backup
            gameLoop()
            
def convert_board_matrix():
    global board_mat
    board_mat=[]
    for i in range(0,8):
        for j in range(0,8):
            if chess.Board.piece_at(board, square=(i*8)+j) is not None:
                if chess.Board.piece_at(board, square=(i*8)+j).color is chess.WHITE:
                       if chess.Board.piece_at(board, square=(i*8)+j).piece_type == chess.PAWN:
                           board_mat.append(chess.PAWN)
                       elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.ROOK:
                           board_mat.append(chess.ROOK)
                       elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.KNIGHT:
                           board_mat.append(chess.KNIGHT)
                       elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.BISHOP:
                           board_mat.append(chess.BISHOP)
                       elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.QUEEN:
                           board_mat.append(chess.QUEEN)
                       elif chess.Board.piece_at(board, square=(i*8)+j).piece_type == chess.KING:
                           board_mat.append(chess.KING)

                elif chess.Board.piece_at(board, square=(i * 8) + j).color is chess.BLACK:
                    if chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.PAWN:
                        board_mat.append(-chess.PAWN)
                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.ROOK:
                        board_mat.append(-chess.ROOK)
                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.KNIGHT:
                        board_mat.append(-chess.KNIGHT)
                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.BISHOP:
                        board_mat.append(-chess.BISHOP)
                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.QUEEN:
                        board_mat.append(-chess.QUEEN)
                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.KING:
                        board_mat.append(-chess.KING)
            else:
                board_mat.append(0)


def possible_moves(pos):
    l=list(board.legal_moves);
    li=[]
    promotion_flag =0
    for i in range(0,8):
        for j in range(0,8):
            p=print_pos([i,j])
            s=pos+p
            if chess.Move.from_uci(s) in board.legal_moves:
                li.append(p)
            for k in [ s + 'q', s + 'r', s + 'b', s + 'n']:
                if chess.Move.from_uci(k) in board.legal_moves:
                    promotion_flag=1
                    li.append(p)

    return li,promotion_flag

def display_possible_moves(pos):
    lis,flag=possible_moves(pos)
    drawBoard()
    for i in lis:
        s = pygame.Surface((piece_size,piece_size), pygame.SRCALPHA)   
        s.fill((93,93,93,128))                         
        gameDisplay.blit(s,[((104-ord(i[0])) * piece_size), ((ord(i[1])-49) * piece_size)] )
        pygame.display.update()
##    pygame.display.update()
    return lis,flag

def ra_chess():
    lis = list(board.legal_moves)
    try:
        r = random.choice(lis)
    except:
        print("Chess over")
        game_ex(True)
    board.push(r)

def lookfor(i):
    li=[]
    for temp in range(0,len(board_mat)):
        if board_mat[temp] is i:
            li.append(temp)
    return li

def doubledPawns(col):
    listofpawns=lookfor(col*chess.PAWN)
    listofp=[x%8 for x in listofpawns]
    c=Counter(listofp)
    l=[]
    for i in range(0,len(listofp)):
        l.append(c[i]-1)
    if len(l) is 0:
        return 0
    return max(l)

def blockedPawns(col):
    listofpawns = lookfor(col * chess.PAWN)
    listofpawnsopp = lookfor(-1*col * chess.PAWN)
    blocked=0
    for i in listofpawns:
        for j in listofpawnsopp:
            if i%8 is j%8:
                if col is 1:
                    if int(i/8) is int(j/8)+1:
                        blocked+=1
                else:
                    if int(i/8) is int(j/8)-1:
                        blocked+=1
    return blocked

def isolatedPawns(col):
    lisofpawns=lookfor(col*chess.PAWN)
    isolated=0

    for i in lisofpawns:
        count = 0
        for j in [1,-1,-9,-8,-7,7,8,9]:
            if i+j in range(0,64) and board_mat[i+j] is 0:
                count+=1
        if count is 8:
            isolated +=1
    return isolated

def pieceSquareTable(matrix,gamephase):
    score=0
    for i in range(0,64):
        if abs(matrix[i]) is chess.PAWN:
            score+=matrix[i]*pawn_table[i]
        elif abs(matrix[i]) is chess.ROOK:
            score+=matrix[i]*rook_table[i]
        elif abs(matrix[i]) is chess.BISHOP:
            score+=matrix[i]*bishop_table[i]
        elif abs(matrix[i]) is chess.KNIGHT:
            score+=matrix[i]*knight_table[i]
        elif abs(matrix[i]) is chess.QUEEN:
            score+=matrix[i]*queen_table[i]
        elif abs(matrix[i]) is chess.KING:
            if gamephase is 'opening':
                score+=matrix[i]*king_table[i]
            elif gamephase is 'ending':
                score+=matrix[i]*king_endgame_table[i]
    return score

def eval_board(i):
    convert_board_matrix()
    c=Counter(board_mat)
    Qw = c[chess.QUEEN]
    Qb = c[-chess.QUEEN]
    Rw = c[chess.ROOK]
    Rb = c[-chess.ROOK]
    Bw = c[chess.BISHOP]
    Bb = c[-chess.BISHOP]
    Nw = c[chess.KNIGHT]
    Nb = c[-chess.KNIGHT]
    Pw = c[chess.PAWN]
    Pb = c[-chess.PAWN]
    #print("Printing values",Qw,Qb,Rw,Rb,Bw,Bb,Nw,Nb,Pw,Pb)
    whiteMaterial = 9 * Qw + 5 * Rw + 3 * Nw + 3 * Bw + 1 * Pw
    blackMaterial = 9 * Qb + 5 * Rb + 3 * Nb + 3 * Bb + 1 * Pb
    numofmoves = board.fullmove_number
    gamephase = 'opening'
    if numofmoves > 40 or (whiteMaterial < 14 and blackMaterial < 14):
        gamephase = 'ending'
    Dw = doubledPawns(1)
    Db = doubledPawns(-1)
    Sw = blockedPawns(1)
    Sb = blockedPawns(-1)
    Iw = isolatedPawns(1)
    Ib = isolatedPawns(-1)
    evaluation1 = 900 * (Qw - Qb) + 500 * (Rw - Rb) + 330 * (Bw - Bb) + 320 * (Nw - Nb) + 100 * (Pw - Pb) + -30\
                  *(Dw - Db + Sw - Sb +Iw - Ib)
    cap,cas=0,0
    if board.is_capture(i):
        cap=50
    if board.is_castling(i):
        cas=500
    evaluation2 = pieceSquareTable(board_mat, gamephase)
    eval_value = evaluation1 + evaluation2+cap+cas
    # Return it:
    #print("evaluation: " + str(eval_value))
    return eval_value

def generate_minmax_leaf(mat,val):
    if val is 1:
        p = []
        for x in range(0, len(mat)):
            p.append(mat[x][1])
        p = [x for x in range(0, len(p)) if p[x] == max(p)]
        p = random.choice(p)
    elif val is -1:
        p = []
        for x in range(0, len(mat)):
            p.append(mat[x][1])
        p = [x for x in range(0, len(p)) if p[x] == min(p)]
        p = random.choice(p)
    return p

def generate_minmax_above(mat,val):
    if val is 1:
        i = []
        for x in range(0, len(mat)):
            i.append(mat[x][1][1])
        i = [x for x in range(0, len(i)) if i[x] == max(i)]
        i = random.choice(i)

    else:
        i = []
        for x in range(0, len(mat)):
            i.append(mat[x][1][1])
        i = [x for x in range(0, len(i)) if i[x] == min(i)]
        i = random.choice(i)

    mat = [mat[i][0],mat[i][1][1]]
    return mat

def negamax(val,depth,k,k1):
        l=list(board.legal_moves)
        if len(l) is not 0:
            k=[]
            for i in l:
                board.push(i)
                l1=list(board.legal_moves)
                if len(l1) is 0:
                    t=eval_board(i)
                    board.pop()
                    return [i,t]
                else:
                    k1=[]
                    for j in l1:
                        board.push(j)
                        l2=list(board.legal_moves)
                        if len(l2) is 0:
                            t=eval_board(j)
                            board.pop()
                            return [i,t]
                        else:
                            k2=[]
                            for z in l2:
                                board.push(z)
                                k2.append([z,eval_board(z)])
                                board.pop()
                            p2=generate_minmax_leaf(k2,val)
                            k1.append([j,k2[p2]])
                        board.pop()
                    pk=generate_minmax_above(k1,(-1*val))
                    k.append([i,pk])
                board.pop()
            k=generate_minmax_above(k,val)
            return k
        else:
            return []

def Negamax(val,depth):
    start = int(time.clock())
    p=negamax(val,depth,[],[])
    lapse = int(time.clock())-start
    if len(p) is 0:
        game_ex(not board.turn)
    else:
        board.push(p[0])
        print("\n\n",p)
    return lapse

def ai(val,depth):
    #ra_chess()
##    global choice
    choice = 'negamax'
    if choice == 'negamax':
        message_to_screen('AI is calculating best move...',black,(displayWidth-200),(display_height/2), 0,"medium")
        message_to_screen("Pls. wait!",red,(displayWidth-200),(display_height/2)+30, 0,"small")
        pygame.display.update()
        lapse = Negamax(val,depth)
        return lapse
    else:
        global board
        moves=list(board.legal_moves)
        if len(moves)!=0:
            mov=random.choice(moves)
            board.push(mov)
        else:
            end_game()
        return -1
        
def get_promotion():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'q'
                elif event.key == pygame.K_2:
                    return 'b'
                elif event.key == pygame.K_3:
                    return 'n'
                elif event.key == pygame.K_4:
                    return 'r'
                else:
                    return 'q'
def end_game():
    while True:
        gameDisplay.fill(cream)
        message_to_screen("Player Black Wins!", black,(displayWidth/2),(display_height/2)-100, 50)
        message_to_screen("Checkmate: Black King", black,(displayWidth/2),(display_height/2)-50, 50)
        message_to_screen("Press R to restart!", red ,(displayWidth/2),(display_height/2), 50)
        button("QUIT",(displayWidth/2)-50,(display_height/2)+200,140,50,red,lred,quitgame)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                gameover = False
                quitgame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    global board
                    newBoard = chess.Board()
                    board = newBoard

                    board.clear_stack()
                    gameLoop()
                    
def paused():
    while True:
        gameDisplay.fill(cream)
        Draw_Borders(4,black)
        message_to_screen(".::",black,(displayWidth/2)-200,(display_height/2)-23,-40,"Elarge")
        message_to_screen("PAUSED",black,(displayWidth/2),(display_height/2),-40,"Mlarge")
        message_to_screen("::.",black,(displayWidth/2)+200,(display_height/2)-23,-40,"Elarge")
        message_to_screen("Press R to Resume / Press Q to Quit / Press X to Restart Game",blue,(displayWidth/2),(display_height/2),40)
        button("QUIT",(displayWidth/2)-50,(display_height/2)+200,100,50,red,lred,quitgame)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    gameDisplay.fill(cream)
                    drawBoard()
                    message_to_screen("Turn : Player White ", black,(displayWidth-200),(piece_size//2), 0,"small")
                    pygame.display.update()
                    return
                if event.key == pygame.K_x:
                    global board
                    newBoard = chess.Board()
                    board = newBoard
                    print("HI")
                    board.clear_stack()
                    gameLoop()

                if event.key == pygame.K_q:
                    quitgame()
        clock.tick(10)
        

##def choose_option():
##    global choice
##    while True:
##        gameDisplay.fill(white)
##        message_to_screen(".::",black,(displayWidth/2)-150,(display_height/2)-23,-40,"Elarge")
##        message_to_screen("CHOOSE FROM FOLLOWING",black,(displayWidth/2),(display_height/2),-40,"large")
##        message_to_screen("::.",black,(displayWidth/2)+150,(display_height/2)-23,-40,"Elarge")
##        message_to_screen("Press A to play with AI-3 / Press R to play with Random moves",blue,(displayWidth/2),(display_height/2),40)
##        button("RANDOM",680,440,140,50,red,lred,quitgame)
##        button("AI - 3",180,440,140,50,green,lgreen,Continue)
##        pygame.display.update()
##        for event in pygame.event.get():
##            if event.type == pygame.QUIT:
##                pygame.quit()
##                quit()
##            if event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_a:
##                    choice = 'negamax'
##                if event.key == pygame.K_r:
##                    choice = 'random'
##                if event.key == pygame.K_q:
##                    pygame.quit()
##                    quit()
##        return choice
        
def game_intro():
    global intro
##    global choice
    intro = True    
    while intro:
        gameDisplay.fill(cream)
        # Draw_Borders(4,black)
        message_to_screen(".::",black,(displayWidth/2)-150,(display_height/2)-23,-40,"Elarge")
        message_to_screen("CHESS",black,(displayWidth/2),(display_height/2),-40,"Mlarge")
        message_to_screen("::.",black,(displayWidth/2)+150,(display_height/2)-23,-40,"Elarge")
        message_to_screen("Press S to Start / Press Q to Quit ",blue,(displayWidth/2),(display_height/2),40)
        button("QUIT",680,440,140,50,red,lred,quitgame)
        button("START",180,440,140,50,green,lgreen,Continue)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
##                    choice = choose_option()
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(10)

def game_ex(player):
    ex = True
    if player == 1: player='white'
    else: player='black'
    while ex:
        gameDisplay.fill(cream)
        Draw_Borders(4,lgreen)
        message_to_screen("GAME  OVER!",black,(displayWidth/2),(display_height/2 - 100),-40,"Elarge")
        message_to_screen(("Player "+player+" Wins!"),red,(displayWidth/2),(display_height/2 - 50),40)
        #message_to_screen(player, red,(displayWidth/2),(display_height/2),80)
        message_to_screen("Press R to play again / Press Q to Exit", blue,(displayWidth/2),(display_height/2)+piece_size-50, 50)
        button("Play Again",80,500,165,50,green,lgreen,restart)
        button("Quit",displayWidth-220,500,140,50,red,lred,quitgame)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    board.clear()
                    board.clear_stack()
                    gameLoop()
        clock.tick(15)

        
#######################MAIN
def gameLoop():
    gameDisplay.fill(cream)
    drawBoard()
    global board
    gameExit = False
    gameover = False
    mouse_d, mouse_u, mouse_up, mouse_down = [-1, -1], [-1, -1], [0,0], [0,0]
    global player
    message_to_screen("Turn : Player White ", black,(displayWidth-200),(piece_size//2), 0,"small")
    button("QUIT",730,525,140,50,red,lred,quitgame)
    pygame.display.update()
    while not gameExit:
        press_flag = 0
        press_up_flag = 0
        while gameover:
            gameDisplay.fill(cream)
            message_to_screen("Game Over", red,(displayWidth/2),(display_height/2), -50, "large")
            message_to_screen("", red,(displayWidth/2),(display_height/2), -50, "large")
            message_to_screen("Press R to play again / Press Q to Exit", black,(displayWidth/2),(display_height/2), 50)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameover = False
                    quitgame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameover = False
                    if event.key == pygame.K_r:
                        global board
                        newBoard = chess.Board()
                        board = newBoard
                        gameLoop()
                        
        button("QUIT",730,525,140,50,red,lred,quitgame) 
        pygame.display.update()
        if board.turn is chess.WHITE:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        und = undo()
                        mouse_down=mouse_up=[1,1]
                        press_flag = press_up_flag = 1
                        if und == 1:    break
                    if event.key == pygame.K_p:
                        paused()
                    if event.key == pygame.K_q:
                        quitgame()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = pygame.mouse.get_pos()
                    press_flag = 1
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_up = pygame.mouse.get_pos()
                    press_up_flag = 1
                    
            if mouse_up[1] < 600 and mouse_up[0] < 600 and mouse_down[1] < 600 and mouse_down[0] < 600:
                if press_flag is 1:
                    #print('Mouse Button DOwn')
                    mouse_d = print_pos([int((mouse_down[0]) / 75), int((mouse_down[1]) / 75)])
                    #print(mouse_d)
                    l,k=display_possible_moves(mouse_d)
                if press_up_flag is 1:
                    #print('MOuse Butotn UP')
                    mouse_u =print_pos([int((mouse_up[0]) / 75), int((mouse_up[1]) / 75)])
                    #print(mouse_u)
                    if mouse_u in l and k is 0 :
                        board.push(chess.Move.from_uci(mouse_d+mouse_u))
                        gameDisplay.fill(cream)
                        drawBoard()
                        message_to_screen("Turn : AI Black ", black,(displayWidth-200),(piece_size//2),0, "medium")
                        pygame.display.update()
                    elif mouse_u in l and k is 1:
                        ch=get_promotion()
                        board.push(chess.Move.from_uci(mouse_d + mouse_u+ch))
                        gameDisplay.fill(cream)
                        drawBoard()
                        message_to_screen("Turn : AI Black ", black,(displayWidth-200),(piece_size//2),0, "medium")
                        pygame.display.update()
        elif board.turn is chess.BLACK:
            if list(board.legal_moves) is not None:                
                lapse = ai(-1,1)
                gameDisplay.fill(cream)
                if lapse != -1:
                    lapse = str(lapse)+" sec"
                    message_to_screen('Time elapsed to search:',black,(displayWidth-200),(display_height/2), 0,"medium")
                    message_to_screen(lapse,red,(displayWidth-200),(display_height/2)+30, 0,"small")
                    pygame.display.update()
                drawBoard()
                message_to_screen("Turn : Player White ", black,(displayWidth-200),(piece_size//2), 0,"medium")
                pygame.display.update()
            if board.is_checkmate() is  True :
                end_game()
                print("Checkmate!")
        clock.tick(10)

def main():
    game_intro()
    gameLoop()

main()






