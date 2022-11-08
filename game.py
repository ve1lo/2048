
from tkinter import *
from matplotlib.pyplot import fill
import numpy as np
import random
import os.path


if os.path.exists("Best_score.txt") == False:
    with open("Best_score.txt", 'w') as file:
        file.write('0')
        




root = Tk() 
c = Canvas(root, width=600, height=600, bg='white')
c.pack()
size=120
x1 = 60
y1 = 60

score = 0
pole = np.zeros((4,4), dtype=int)

dict_digits = {
    2:{'color_block':'#eee4da','color_font':'#776e65','font':'Verdana 40 bold'},
    4:{'color_block':'#eee1c9','color_font':'#776e65','font':'Verdana 40 bold'},
    8:{'color_block':'#f3b27a','color_font':'#f9f6f2','font':'Verdana 40 bold'},
    16:{'color_block':'#f69664','color_font':'#f9f6f2','font':'Verdana 38 bold'},
    32:{'color_block':'#f77c5f','color_font':'#f9f6f2','font':'Verdana 38 bold'},
    64:{'color_block':'#f75f3b','color_font':'#f9f6f2','font':'Verdana 35 bold'},
    128:{'color_block':'#edd073','color_font':'#f9f6f2','font':'Verdana 35 bold'},
    256:{'color_block':'#edcc62','color_font':'#f9f6f2','font':'Verdana 35 bold'},
    512:{'color_block':'#edc950','color_font':'#f9f6f2','font':'Verdana 35 bold'},
    1024:{'color_block':'#edc53f','color_font':'#f9f6f2','font':'Verdana 30 bold'},
    2048:{'color_block':'#ffcf40','color_font':'#f9f6f2','font':'Verdana 30 bold'},
    4096:{'color_block':'#CC0000','color_font':'#f9f6f2','font':'Verdana 30 bold'},
    8192:{'color_block':'#990000','color_font':'#f9f6f2','font':'Verdana 30 bold'},
    16384:{'color_block':'#FF66FF','color_font':'#f9f6f2','font':'Verdana 25 bold'},
    32768:{'color_block':'#FF33FF','color_font':'#f9f6f2','font':'Verdana 25 bold'},
    65536:{'color_block':'#FF00FF','color_font':'#f9f6f2','font':'Verdana 25 bold'},    
}

def zero():
    c.delete('best_score')
    c.delete('score')
    for i in range(4):
        for j in range(4):
            pole[i][j] = 0


def menu():
    
    global best_score
    with open("Best_score.txt", 'r') as file:
        best_score = file.read()
    c.delete('all')
    c.create_rectangle(0,0,600,600,fill='grey', tags='menubg')

    c.create_rectangle(200,250,400,300,fill='white', tags='startbutton')
    c.create_text(300,275,text='Start', font='Verdana 20', anchor='center', tags='startbutton')
    
    c.create_rectangle(200,330,400,380,fill='white', tags='aibutton')
    c.create_text(300,355,text='AI', font='Verdana 20', anchor='center',tags='aibutton')
    
    c.tag_bind('startbutton','<Button-1>',startgame)
    
def startgame(event):
    c.delete('all')
    c.create_text(100,30,text='Score:', font='Verdana 16', justify='left')
    c.create_text(400,30,text='Best:',  font='Verdana 16', justify='left')
    c.create_text(430,30,text = best_score,font='Verdana 20',anchor='w', tags='best_score')
   
    for i in range(4):
        for j in range(4):
            c.create_rectangle(x1+size*j,y1+size*i,x1+size*(j+1),y1+size*(i+1), fill ='#cdc1b4',tags='blocks', outline='black')
    global pole
    global score
    score = 0
    pole = np.zeros((4,4), dtype=int)
    generatestart(2)
      

def gencolor():
    global pole
    n = 2
    for i in range(4):
        for j in range(4):
            pole[i][j] = n
            n = n*2
    print(pole)

def render():
    global best_score
    c.delete('digit')
    c.delete('score')
    c.delete('colored_blocks')
    for i in range(4):
        for j in range(4):
            if pole[j][i] != 0:               
                    c.create_rectangle(x1+size*i,y1+size*j,x1+size*(i+1),y1+size*(j+1), fill=dict_digits[pole[j][i]]['color_block'],tags='colored_blocks')                
                    c.create_text(size*(i+1),size*(j+1),text=pole[j][i], font=dict_digits[pole[j][i]]['font'], fill=dict_digits[pole[j][i]]['color_font'], tags='digit')
    c.create_text(135,30,text = score,font='Verdana 20',anchor='w', tags='score')
    if get_current_state(pole) == 'LOST':
        if int(best_score) < int(score):
            with open("2048/Best_score.txt", 'w') as file:
                file.write(str(score))
        c.create_rectangle(0,0,600,600, fill='grey')
        c.create_text(300,300,text='LOST')
        c.after(1000,menu)
        zero()
        
        


def generatestart(n):
    
    while np.count_nonzero(pole)<n:
        x = random.randint(0,3)
        y = random.randint(0,3)
        dr = 2*random.randint(0,9)
        if dr == 0:
            d = 4
        else:
            d = 2
        if pole[x][y] == 0:
            pole[x][y] = d   
        render()

def generatedig():
        gen = 0
        zerocount = 0
        for i in range(4):
            for j in range(4):
                if pole[i][j]==0:
                    zerocount+=1
        while gen==0 and zerocount > 0:
            x = random.randint(0,3)
            y = random.randint(0,3)
            if pole[x][y] == 0:
                dr = 2*random.randint(0,9)
                if dr == 0:
                    d = 4
                else:
                    d = 2
                if pole[x][y] == 0:
                    pole[x][y] = d  
                print(x,y,d)
                gen = gen+1

def get_current_state(pole):
    for i in range(4):
        for j in range(4):
            if(pole[i][j]== 0):
                return 'GAME NOT OVER'
    for i in range(3):
        for j in range(3):
            if(pole[i][j]== pole[i + 1][j] or pole[i][j]== pole[i][j + 1]):
                return 'GAME NOT OVER'
    for j in range(3):
        if(pole[3][j]== pole[3][j + 1]):
            return 'GAME NOT OVER'
    for i in range(3):
        if(pole[i][3]== pole[i + 1][3]):
            return 'GAME NOT OVER'
    return 'LOST'            

        

def leftmove(event):
    print(event.keysym)
    oldpole = pole.copy()
    global score
    for i in range(4):
        counter = 0
        for j in range(4):
            if pole[i][j]!=0:
                for d in range(j-1,-1,-1):          
                    if pole[i][d] == 0:
                        pole[i][d] = pole[i][d+1]
                        pole[i][d+1] = 0
                    if pole[i][0] == pole[i][1] and pole[i][2] == pole[i][3] and pole[i][0]!=0 and pole[i][2]!=0 and counter<1:
                        pole[i][0] = pole[i][0]*2
                        pole[i][1] = pole[i][2]*2
                        pole[i][2] = 0
                        pole[i][3] = 0
                        counter += 1
                        score = score + pole[i][0] + pole[i][1]
                    if pole[i][d] == pole[i][d+1] and counter == 0:
                        pole[i][d] = pole[i][d]*2
                        pole[i][d+1] = 0
                        counter +=1
                        score += pole[i][d]
    if np.array_equal(oldpole,pole) == False:
        generatedig()
    print(get_current_state(pole))                      
    render()
    print(pole)                   
    

def rightmove(event):
    print(event.keysym)
    oldpole = pole.copy()
    global score
    for i in range(4):
        counter = 0
        for j in range(2,-1,-1):
            if pole[i][j]!=0: 
                for d in range(j+1,4,1):          
                    if pole[i][d] == 0:
                        pole[i][d] = pole[i][d-1]
                        pole[i][d-1] = 0
                    if pole[i][0] == pole[i][1] and pole[i][2] == pole[i][3] and pole[i][0]!=0 and pole[i][2]!=0 and counter<1:
                        pole[i][3] = pole[i][2]*2
                        pole[i][2] = pole[i][0]*2
                        pole[i][1] = 0
                        pole[i][0] = 0
                        counter += 1
                        score = score + pole[i][3] + pole[i][2]
                    if pole[i][d] == pole[i][d-1] and counter == 0:
                        pole[i][d] = pole[i][d-1]*2
                        pole[i][d-1] = 0
                        counter +=1
                        score += pole[i][d]
    if np.array_equal(oldpole,pole) == False:
        generatedig()
    print(get_current_state(pole))                                           
    render()                        
    print(pole)                   
    

def upmove(event):
    print(event.keysym)
    oldpole = pole.copy()
    global score
    for i in range(4):
        counter = 0
        for j in range(4):
            if pole[j][i]!=0:
                for d in range(j-1,-1,-1):          
                    if pole[d][i] == 0:
                        pole[d][i] = pole[d+1][i]
                        pole[d+1][i] = 0
                    if pole[0][i] == pole[1][i] and pole[2][i] == pole[3][i] and pole[0][i]!=0 and pole[2][i]!=0 and counter<1:
                        pole[0][i] = pole[0][i]*2
                        pole[1][i] = pole[2][i]*2
                        pole[2][i] = 0
                        pole[3][i] = 0
                        counter += 1
                        score = score + pole[0][i]+ pole[1][i]
                    if pole[d][i] == pole[d+1][i] and counter == 0:
                        pole[d][i] = pole[d][i]*2
                        pole[d+1][i] = 0
                        counter +=1
                        score += pole[d][i]
    if np.array_equal(oldpole,pole) == False:
        generatedig()                     
    print(get_current_state(pole))
    render()                    
    print(pole)                   
    
    

def downmove(event):
    print(event.keysym)
    oldpole = pole.copy()
    global score
    for i in range(4):
        counter = 0
        for j in range(2,-1,-1):
            if pole[j][i]!=0: 
                for d in range(j+1,4,1):          
                    if pole[d][i] == 0:
                        pole[d][i] = pole[d-1][i]
                        pole[d-1][i] = 0
                    if pole[0][i] == pole[1][i] and pole[2][i] == pole[3][i] and pole[0][i]!=0 and pole[2][i]!=0 and counter<1:
                        pole[3][i] = pole[2][i]*2
                        pole[2][i] = pole[0][i]*2
                        pole[1][i] = 0
                        pole[0][i] = 0
                        counter += 1
                        score = score + pole[3][i] + pole[2][i]
                    if pole[d][i] == pole[d-1][i] and counter == 0:
                        pole[d][i] = pole[d-1][i]*2
                        pole[d-1][i] = 0
                        counter +=1
                        score += pole[d][i]
    if np.array_equal(oldpole,pole) == False:
        generatedig()                     
    print(get_current_state(pole))
    render()                        
    print(pole)                                        
    


root.bind('<Left>', leftmove)
root.bind('<Right>', rightmove)
root.bind('<Up>', upmove)
root.bind('<Down>', downmove)




menu()
print(pole)
root.mainloop()
