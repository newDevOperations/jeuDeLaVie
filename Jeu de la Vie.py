import numpy as np
import pyautogui as pg
import tkinter as tk

from random import *
from tkinter import *
from tkinter import ttk

class PLANNEUR():
    def __init__(self):
        self.x, self.y = 20, 20
        self.x0, self.y0 = 16,1
        self.preset = ["111",
                       "001",
                       "010"]
       
class MOULIN():
    def __init__(self):
        self.x, self.y = 15, 15
        self.x0, self.y0 = 3,3
        self.preset =["111111011",
                      "111111011",
                      "000000011",
                      "110000011",
                      "110000011",
                      "110000011",
                      "110000000",
                      "110111111",
                      "110111111"]
        
        
class CANON():
    def __init__(self):
        self.x, self.y = 25, 40
        self.x0, self.y0 = 1,2
        self.preset = ["000000000000110000000000000000000000",
                       "000000000001000000000000000000000000",
                       "000000000010000000000000100000000000",
                       "010000000010000000000001100000000000",
                       "110000000010000000000000001100000000",
                       "000000000001000000000000001110000001",
                       "000000000000110000000000001100000011",
                       "000000000000000000000001100000000000",
                       "000000000000000000000000100000000000"]

class VAISSEAU():
     def __init__(self):
         self.x, self.y = 15, 30
         self.x0, self.y0 = 1,1
         self.preset = ["000010",
                        "000001",
                        "010001",
                        "001111",
                        "000000",
                        "000000",
                        "000000",
                        "000000",
                        "000010",
                        "000001",
                        "100001",
                        "011111"]    

class OSCILLATEURS():
    def __init__(self):
        self.x, self.y = 13, 30
        self.x0, self.y0 = 4,3
        self.preset = ["010000000000000000000011",
                       "001100000000100000000011",
                       "110000000001110000001100",
                       "001000000000100000001100"]

class INERTES():
    def __init__(self):
        self.x, self.y = 12, 23
        self.x0, self.y0 = 1,1
        self.preset =["000000000000010000000",
                      "011000010000101000010",
                      "011000101000101000101",
                      "000000010000010000011",
                      "000000000000000000000",
                      "000000000000000000000",
                      "011000001000010000000",
                      "100100010100101000110",
                      "100100100100010100101",
                      "011000011000001000011"]

class LIGNE():
    def __init__(self):
        self.x, self.y = 19, 20
        self.x0, self.y0 = 9,0
        self.preset =["11111111111111111111"]

class DOUBLE_LIGNE():
    def __init__(self):
        self.x, self.y = 20, 20
        self.x0, self.y0 = 9,0
        self.preset =["11111111111111111111",
                      "11111111111111111111"]

class GIANT_DOUBLE_LIGNE():
    def __init__(self):
        self.x, self.y = 50, 75
        self.x0, self.y0 = 23,0
        self.pre_preset=''
        self.preset=[]
        for i in range(self.y):
            self.pre_preset+='1'
        self.preset.append(self.pre_preset)
        self.preset.append(self.pre_preset)



class JEUDELAVIE(tk.Tk):
    
    def __init__(self,nlig=20,ncol=20):
    
        tk.Tk.__init__(self)
        self.wm_attributes("-topmost",1)
        self.title("Jeu de la Vie") #nom de la fenêtre
        
        self.couleurs = {0:'white',1:'blue'} #couleurs des cases
        self.x, self.y = nlig, ncol #Taille de la grille
        self.min, self.xmax, self.ymax = 15, 150, 225 #Taille mini, maxi de la grille
        
        if self.x>100 or self.y>150: #redimenssionner chaque cases en fonction du nombre de cases
            self.tailleCase = 5
        elif self.x>50 or self.y>75:
            self.tailleCase = 10
        else:
            self.tailleCase = 20
                
        self.flagStop = 0  #Flag passe à 1 pour interrompre le cycle quand l'utilisateur a cliqué sur STOP
        self.flagModif = 1 #Flag passe à 1 quand il a des modifs de cellules depuis le dernier cycle, permet d'arreter automatiquement le cycle si pas de changement
        self.compteur = 0 #Compteur de générations
        self.population = 0 #Compteur de population
        self.tempo=100 #Temps entre chaque génération
        self.matrice=[[0] * self.y for i in range(self.x)] #Création d'une matrice de 0 de dimention x*y
        self.grille={}
               
        self.widgets()        
     
               
    def widgets(self):
       
        #Création de la Grille
        self.widGrille = Canvas(self, width=self.y*self.tailleCase, height=self.x*self.tailleCase, background="ivory")
        self.widGrille.grid(row=0, column=0, rowspan=20)
        self.widGrille.bind("<Button-1>", self.clic_case)
                
        for i in range(self.x):
            for j in range(self.y):
                rect=self.widGrille.create_rectangle(j*self.tailleCase, i*self.tailleCase, (j+1)*self.tailleCase, (i+1)*self.tailleCase, fill=self.couleurs[0], outline="gray")
                self.grille[i,j]=[rect]
        
        #Définition des fonts
        f_bouton = ("Arial", 9, "bold")
                
        #COMPTEUR GENERATION
        tk.Label(self, text="Génération",font=("Arial", 12), fg="black").grid(row=0,column=1, padx = 20, rowspan=2, columnspan=3)
        self.widCompteur = tk.Label(self, text="0",font=("Arial", 12), fg="red")
        self.widCompteur.grid(row=2,column=1, rowspan=2, columnspan=3 )
        
        #BOUTON ACTION
        self.widAction=tk.Button(self, text="GO", width=12, font=f_bouton, relief = RAISED, fg="white", bg="green",command=self.action)
        self.widAction.grid(row=4,column=1, columnspan=3)
        
        #GENERATION MAX
        self.vmaxgen = tk.IntVar()
        self.vmaxgen.set(9999)
        tk.Label(self,text="Max : ",font=("Arial", 8),fg="black").grid(row=5, column=2, sticky=E)
        self.widMaxgen = tk.Entry(self, textvariable=self.vmaxgen,width=4, font=("Arial", 8), fg="black")
        self.widMaxgen.grid(row=5,column=3, sticky=W)
        
        #COMPTEUR POPULATION
        tk.Label(self, text="Population: ",font=("Arial", 8), fg="black").grid(row=6,column=1, padx = 20, rowspan=2, columnspan=2, sticky=E)
        self.widPopulation = tk.Label(self, text='0',font=("Arial", 8), fg="blue")
        self.widPopulation.grid(row=6,column=2, rowspan=2, columnspan=1,sticky=E )
                                        
        #PRESETS
        tk.Label(self, text="Modèles :",font=("Arial", 8), fg="black").grid(row=8,column=1, columnspan=3, sticky=S)
        listeModeles=["Rien (Grille Vide)", "Aléatoire","Planneur","Canon de Planneurs","Moulin", "Vaisseau","Oscillateurs","Ligne","Double Ligne","Double ligne géantes","Formes Inertes"]
        self.widModeles = ttk.Combobox(self, font=("Arial", 9, "bold"), width = 15, values=listeModeles)
        self.widModeles.current(0)
        self.widModeles.grid(row=9,column=1, columnspan=3)
        self.widModeles.bind("<<ComboboxSelected>>", self.change_preset)
             
        #TEMPORISATION
        vtempo = tk.IntVar()
        tk.Label(self, text="Tempo (ms) :",font=("Arial", 10), fg="black").grid(row=10,column=1, columnspan=2, sticky=E)
        self.widTempo=tk.Entry(self, textvariable=vtempo,width=5, font=("Arial", 10), fg="black")
        self.widTempo.grid(row=10,column=3, sticky=W)
        vtempo.set(self.tempo)
  
        #Taille de la grille
        tk.Label(self, text="Grille :",font=("Arial", 10), fg="black").grid(row=12,column=1, columnspan=3)
        tk.Label(self, text="X",font=("Arial", 10), fg="black").grid(row=13,column=2)
        
        vx, vy = tk.IntVar(), tk.IntVar()
        self.widX = tk.Spinbox(self, textvariable=vx, width=4, font=("Arial", 10), fg="black", from_=self.min, to=self.xmax)
        self.widX.grid(row=13,column=1, sticky=E)
        self.widY = tk.Spinbox(self, textvariable=vy, width=4, font=("Arial", 10), fg="black", from_=self.min, to=self.ymax)
        self.widY.grid(row=13,column=3, sticky=W)
        vx.set(self.x)
        vy.set(self.y)
        
        self.widOK=tk.Button(self, text="OK", width=2, font=f_bouton, fg="black", bg="gray",command=self.resize)
        self.widOK.grid(row=14,column=2)
                
        #QUITTER
        tk.Button(self, text="QUIT", width=13, font=f_bouton, fg="black", bg="red",command=self.destroy).grid(row=17,column=1, columnspan=3)
        
        #CHECKBUTTONS REGLE DU JEU
        tk.Label(self, text="Règles du jeu: ", font=("Arial", 12), fg="black").grid(row=0,column=4, columnspan=2)
        tk.Label(self, text="Vie :",           font=("Arial", 12), fg="black").grid(row=2,column=4,sticky=W)
        tk.Label(self, text="Mort :",          font=("Arial", 12), fg="black").grid(row=2,column=5,sticky=E)
        
        self.vlive, self.vdead = {}, {}
        for i in range(1,9):
            self.vlive[i], self.vdead[i] = IntVar(), IntVar()
            tk.Checkbutton(self,  text=i, variable=self.vlive[i], font=("Arial", 8), command=self.modifConditions,  activeforeground='cyan').grid(row=2+i,column=4)
            tk.Checkbutton(self,  text=i, variable=self.vdead[i], font=("Arial", 8), command=self.modifConditions,  activeforeground='cyan').grid(row=2+i,column=5)
        

        self.vlive[3].set(1) #conditions pour qu'une cellule naisse
        self.vdead[2].set(1) #condition pour qu'une cellule reste en vie
        self.vdead[3].set(1) #condition pour qu'une cellule reste en vie
        self.modifConditions() #Initialisation
        
        
    def modifConditions(self):
        self.live, self.dead=[], []
        for i in range(1,9):
            if self.vlive[i].get():
                self.live.append(i)
            if self.vdead[i].get():
                self.dead.append(i)


    def action(self):
         
        if self.widAction['text'] == "GO":
            self.flagStop = 0
            self.widAction['text'] = "STOP"
            self.widAction['bg'] = "RED"
            self.widTempo['state'],self.widX['state'],self.widY['state'],self.widOK['state'],self.widModeles['state'],self.widMaxgen['state'] = DISABLED, DISABLED, DISABLED, DISABLED, DISABLED, DISABLED
            self.cycle()
        else:
            self.flagStop = 1
            self.widAction['text'] = "GO"
            self.widAction['bg'] = "GREEN"
            self.widTempo['state'], self.widX['state'], self.widY['state'], self.widOK['state'], self.widModeles['state'], self.widMaxgen['state'] = NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, NORMAL
                   
        self.tempo=self.widTempo.get()
        
    
    def put_cell(self,x,y,etat): #met à jour la valeur de la cellule et sa couleur en fonction de etat
        self.matrice[x][y]=etat
        self.widGrille.itemconfigure(self.grille[x,y], fill=self.couleurs[etat])
                
    def inv_cell(self,x,y): #inverse la valeur de la cellule 0->1 1->0
        val = self.matrice[x][y]
        val = 0 if val else 1
        self.put_cell(x,y,val)
        
    def raz_matrice(self): #Vider la matrice
        self.raz_compteur()
        for i in range(self.x):
            for j in range(self.y):
                self.put_cell(i,j,0)
        self.calcule_population()
        
    def aleatoire(self):
        self.raz_compteur()
        #self.raz_population()
        for i in range(self.x):
            for j in range(self.y):
                self.put_cell(i,j,randint(0,1))
  
    def maj_graphique(self):
        self.flagModif=0
        for i in range(self.x):
            for j in range(self.y):
                if self.couleurs[self.matrice[i][j]]!=self.widGrille.itemcget(self.grille[i,j], 'fill'):
                    self.flagModif=1               
                    self.put_cell(i,j,self.matrice[i][j])

    def resize(self):
        if pg.confirm(text='Voulez-vous redéfinir la taille de la grille ?', title='Taille de la Grille', buttons=['OK', 'Cancel'])=='OK':
            try:
                x_new, y_new = int(self.widX.get()), int(self.widY.get())
                
            except:
                pg.confirm(text='Les valeurs de la taille de la grille doivent être numériques', title='Erreur de saisie', buttons=['OK'])
                return
            
            if x_new not in range(self.min, self.xmax+1) or y_new not in range(self.min, self.ymax+1): 
                pg.confirm(text='Valeurs en dehors des plages autorisées. Mini=['+str(self.min)+','+str(self.min)+'] Maxi=['+str(self.xmax)+','+str(self.ymax)+']',title='Valeurs en dehors de la plage autorisée', buttons=['OK'])
            else:
                self.destroy()
                jeu=JEUDELAVIE(x_new,y_new)
                jeu.mainloop()  

    def raz_compteur(self): #Remettre le compteur à 0
        self.compteur=0
        self.widCompteur['text'] = "0"
        
    def incremente_compteur(self): #Compteur de génération
        if self.flagModif==1:
            self.compteur+=1
            self.widCompteur['text'] = str(self.compteur)
    
    def calcule_population(self): #Compteur de population
        self.population=np.sum(self.matrice)
        self.widPopulation['text'] = str(self.population)
        
    def clic_case(self,event): #Quand on clique sur une case
        x = int(event.y/self.tailleCase)
        y = int(event.x/self.tailleCase)
        self.inv_cell(x,y)
        self.calcule_population()
              
    def cycle(self):
        if self.flagStop==0 and self.compteur < self.vmaxgen.get() and self.flagModif==1:
            self.matrice=generation(self.matrice,self.live,self.dead)
            self.maj_graphique()
            self.incremente_compteur()
            self.calcule_population()
            self.after(self.tempo,self.cycle)
        else:
            self.action()
            self.flagStop=1
            self.flagModif=1
            
                
    def print_matrice(self):
        for i in range(self.x):
            print (self.matrice[i])
    
    def change_preset(self,event):
        choix=self.widModeles.current()
                
        if choix==0: #Rien (Grille) Vide"
            self.raz_matrice()
        elif choix==1: #Aléatoire
            self.aleatoire()
            self.calcule_population()
        else:
            self.destroy()
            if choix==2:
                motif=PLANNEUR()
            elif choix==3:
                motif=CANON()
            elif choix==4:
                motif=MOULIN()
            elif choix==5:
                motif=VAISSEAU()
            elif choix==6:
                motif=OSCILLATEURS()
            elif choix==7:
                motif=LIGNE()
            elif choix==8:
                motif=DOUBLE_LIGNE()
            elif choix==9:
                motif=GIANT_DOUBLE_LIGNE()
            elif choix==10:
                motif=INERTES()
            
            jeu=JEUDELAVIE(motif.x,motif.y)
            for i in range(len(motif.preset)):
                for j in range(len(motif.preset[0])):
                    jeu.matrice[i+motif.x0][j+motif.y0]=int(motif.preset[i][j])
            jeu.maj_graphique()
            jeu.widModeles.current(choix)
            jeu.calcule_population()
            jeu.mainloop()
        
    
def generation(matr,lLive,lDead):
    n0,p0=len(matr), len(matr[0])
    nv_matr=np.copy(matr) #matrice après la génération
    
    for x in range(n0): #parcourir chaque éléments de la matrice
        for y in range(p0):
            viv=0 #nbr de cellule vivante autour de la case
            carre=[]
            mini_1,mini_2= -1,-1
            maxi_1,maxi_2= 2,2
            if x==0: # déterminer où commencer le carré autour du centre (si dans un coin, on commence par 0)
                mini_1+=1
            elif x==n0-1: 
                maxi_1-=1
            if y==0:
                mini_2+=1
            elif y==p0-1:
                maxi_2-=1
                
            for m in range(mini_1,maxi_1): #ajouter dans une liste tous les nombres autour de la case
                for p in range(mini_2,maxi_2):
                    carre.append(matr[x+m][y+p])  
            if matr[x][y]==1: #pour une case noire
                viv=sum(carre)-1 #nbr de cellule vivante autour du centre (on ne comptabilise pas le centre)
                if viv not in lDead: #conditions pour qu'une cellule meurt
                    nv_matr[x][y]=0
            else: #pour une case blanche
                viv=sum(carre)      
                if viv in lLive: #condition pour naissance d'une cellule
                    nv_matr[x][y]=1
    matr=np.copy(nv_matr)
    return matr


jeu=JEUDELAVIE()
jeu.mainloop()
