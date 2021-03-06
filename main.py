# kivy.require('1.9.10') # replace with your current kivy version !
# -*- coding: utf-8 -*-
from kivy.uix.gridlayout import GridLayout
import string

from extparams import params
from tincan import (
    RemoteLRS,
    Statement,
    Agent,
    Verb,
    Activity,
    Result,
    Score,
    Extensions,
    LanguageMap,
    ActivityDefinition,
    StateDocument,

)
import uuid
from ressources import lrs_properties



from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.network.urlrequest import UrlRequest
from kivy.uix.spinner import Spinner
import os.path
# from jnius import autoclass, PythonJavaClass, java_method, cast
from kivy.uix.scrollview import ScrollView
from string import ascii_uppercase
try:
    from QRmodule.qr import qrwidget
except:
    qrwidget = None

myparams = params.Extparams()
myparams.build_from_url()
#notation=params.RatingScale()
#notation.__init__(se,type,scale)
# Test du widget ToggleButton
# KIVY_DPI=320 KIVY_METRICS_DENSITY=2 python main.py --size 1280x720


Builder.load_string('''
<myscreen>:
    
    GridLayout:
        cols:1
        rows:5
         # blue color with 50% alpha
        BoxLayout:
            size_hint:('15sp','15sp')
            Label:
                id:labid
                font_size:"15sp"
                text:""
            ToggleButton:
                canvas:
                    Color:
                        rgba: 1,0, 0, 0.5 
                    Rectangle:
                        pos: self.pos
                        size: self.size
                text: 'Déconnexion'
                font_size: '15sp'
                on_press:
                    root.statementsended()
        BoxLayout:
            size_hint:('80sp','80sp')
            id:boxact
            canvas.before:
                Color:
                    rgba: 0, 0.5, 1, 0.7 
                Rectangle:
            # self here refers to the widget i.e FloatLayout
                    pos: self.pos
                    size: self.size
                
            Label:
                id: mylabel
                font_size:'50sp'
                text: "Page d'autoévaluation"
        BoxLayout:
            
            size_hint:('40sp','40sp')
            Spinner:
                id:myspinner
                text:"Sélection d'activités"
                # available values
                values:()
                on_press:root.updateactivities()
                on_text:root.upgradeactivity()
                font_size:'20sp'
        BoxLayout:
            id: blnote
            size_hint:('40sp','40sp')
            Label:
                id: labnote
                text: ''
                font_size:'18sp'
            TextInput:
                id: input
                multiline:False
                font_size: '20sp'
                text:""
                input_type: 'number'
                input_filter: 'int'
                
        BoxLayout:  
            orientation: 'horizontal'                      
            size_hint:('40sp','40sp')
  
            ToggleButton:
                id:actvalidated
                canvas:
                    Color:
                        rgba: 0,0.5, 0, 0.5 
                    Rectangle:
                        pos: self.pos
                        size: self.size
                text: 'Valider'
                font_size: '30sp'
                on_press:
                    root.checkinput()
                    root.manager.transition.direction = 'left'
                    
                state:"down"
        
        
                
<MenuScreen>:
    GridLayout: 
        cols: 1
        rows: 4
        BoxLayout:
            #size: (self.width,self.height)
            size_hint:('80sp','80sp')   
            canvas.before:
                Color:
                    rgba: 0, 0.5, 1, 0.7 
                Rectangle:
            # self here refers to the widget i.e FloatLayout
                    pos: self.pos
                    size: self.size
                    
            Label:
                text: "Bienvenue!"
                
                font_size:'50sp'
       
        BoxLayout:## here is one Box
            size_hint:('50sp','50sp')   
            Label:
                text: 'Identifiant'
                font_size: '18sp'
                
            TextInput:
                id: textid
                text:""
                multiline:False
                font_size: '20sp'   
                
        
        BoxLayout:
            size_hint:('50sp','50sp') ## here is another Box
            canvas.before:
                Color:
                    rgba: 1, 0.,0. ,0.5 
                Rectangle:
            # self here refers to the widget i.e FloatLayout
                    pos: self.pos
                    size: self.size
            Label:
                
                text: 'Mot de passe'
                font_size: '18sp'
                
            TextInput:
                id: textmdp
                multiline:False
                text:""
                password:True
                font_size: '20sp'
                
        BoxLayout:
            size_hint: ('60sp','60sp')
            ToggleButton:
                canvas:
                    Color:
                        rgba: 0,0.5, 0, 0.5 
                    Rectangle:
            # self here refers to the widget i.e FloatLayout
                        pos: self.pos
                        size: self.size
                text: 'Connexion'
                font_size: '30sp'
                on_press:
                    root.checkidandpw()
                
         
            ToggleButton:
                id:buturl
                canvas:
                    Color:
                        rgba: 0.9,0.4,0 , 0.7
                    Rectangle:
            #self here refers to the widget i.e FloatLayout
                        pos: self.pos
                        size: self.size
                text: ''
                 
                font_size: '30sp'
                on_press:
                    root.popupverif()
                    
                    
<QrScreen>:
    fullscreen: True
    name: 'Popups'
    BoxLayout:
        id: bl
                     
<Myalternativepopupbox>:
    GridLayout:
        rows:2
        cols:1
        BoxLayout:
            size_hint:('40sp','40sp')
            id: bl
            Label:
                text: "Ecrivez un lien url valide"
                font_size: '25sp'
        BoxLayout:## here is one Box
            size_hint:('25sp','25sp')
            canvas.before:
                Color:
                    rgba: 1, 0.,0. ,0.5 
                Rectangle:
            # self here refers to the widget i.e FloatLayout
                    pos: self.pos
                    size: self.size
                
            TextInput:
                id: texturl
                text:""
                multiline:False
                font_size: '18sp'
            ToggleButton:
                canvas:
                    Color:
                        rgba: 0,0.5, 0, 0.5 
                    Rectangle:
            # self here refers to the widget i.e FloatLayout
                        pos: self.pos
                        size: self.size
                text: 'Connexion'
                font_size: '30sp'
                on_press:
                    root.checkurl()
            
<Myalternativepopup2>:
    #popup: popup.__self__
    BoxLayout:
        id: blay
        Popup:
            id: popup2
            title : "Bravo vous avez scanné un QR code!"
            Button:
                text : "Revenir à l'écran de connexion"
                id: return_button2

<Coms>:
    GridLayout:
        cols:1
        rows:5
        id:grid
        BoxLayout:
            id: barcom
            size_hint:('15sp','15sp')
            Label:
                id:labcomrecap
                font_size:"15sp"
                text:""
            ToggleButton:
                canvas:
                    Color:
                        rgba: 1,0, 0, 0.5 
                    Rectangle:
                        pos: self.pos
                        size: self.size
                text: 'Déconnexion'
                font_size: '15sp'
                on_press:
                    root.manager.get_screen("activity").statementsended()        
        BoxLayout:
            orientation:'vertical'
            id: changebox
            size_hint:('80sp','80sp')
            
            canvas.before:
                Color:
                    rgba: 0, 0.5, 1, 0.7 
                Rectangle:
            # self here refers to the widget i.e FloatLayout
                    pos: self.pos
                    size: self.size
            Label:
                id: labcom
                text:'Choisissez un commentaire'
                font_size:'50sp'
        BoxLayout:
            
            id: selecom
            size_hint:('40sp','40sp')
            Spinner:
                
                id:myspinner2
                text:"Sélection de commentaires"
                # available values
                values:()
                font_size:'20sp'
                on_press:root.spinner()
                
            ToggleButton:
                canvas:
                    Color:
                        rgba: 0,0.5, 0, 0.5
                    Rectangle:
            # self here refers to the widget i.e FloatLayout
                        pos: self.pos
                        size: self.size
                id:addcom
                
                text:"Ajouter un commentaire"
                font_size:'30sp'
                on_press:root.boxcom()
                state:'normal'
            #root.champlibre()
                
        BoxLayout:
            id: comlib
            size_hint:('50sp','50sp')
            ToggleButton:
                canvas:
                    Color:
                        rgba: 1.0,0,0,0.5
                    Rectangle:
            # self here refers to the widget i.e FloatLayout
                        pos: self.pos
                        size: self.size
                id:champlibre
                text:"Ajouter un champ libre"
                font_size: '18sp'
                on_press:root.createinput()
           
        BoxLayout:
            size_hint: ('60sp','60sp')
            ToggleButton:
                id:valid
                text: 'Valider'
                canvas:
                    Color:
                        rgba: 0,0.5, 0, 0.5 
                    Rectangle:
            # self here refers to the widget i.e FloatLayout
                        pos: self.pos
                        size: self.size
                font_size: '30sp'
                on_press: root.valideco()
                state:'normal'
            
                    
                  
<Logout>:
    GridLayout:
        cols:1
        rows:3
        BoxLayout:
        
            size_hint:('80sp','80sp')
            canvas.before:
                Color:
                    rgba: 0, 0.5, 1, 0.7 
                Rectangle:
            # self here refers to the widget i.e FloatLayout
                    pos: self.pos
                    size: self.size
            Label:
                text:'Confirmer la déconnexion?'
                font_size:'50sp'
        BoxLayout:
            size_hint: ('60sp','60sp')
                    
            ToggleButton:
                canvas:
                    Color:
                        rgba: 0.1,0.5, 0, 0.5 
                    Rectangle:
            # self here refers to the widget i.e FloatLayout
                        pos: self.pos
                        size: self.size
                text: 'RETOUR'
                font_size: '30sp'
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'activity'
                    
            
        BoxLayout:
            size_hint:('60sp','60sp')
            ToggleButton:
                canvas:
                    Color:
                        rgba: 1.0,0.1, 0, 0.5 
                    Rectangle:
            # self here refers to the widget i.e FloatLayout
                        pos: self.pos
                        size: self.size
                text: 'SE DECONNECTER'
                font_size: '30sp'
                on_press: 
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'menu'
              
''')

# Popup which confirms a QR Code Scan
class Myalternativepopup2(BoxLayout):
    pass

#Screen that appears when the scan of a qr code is impossible
class Myalternativepopupbox(Screen):
    #check if the url entered corresponds to right url
    def checkurl(self):
        if self.ids.texturl.text=="https://api.myjson.com/bins/1aob0f":

            #making the url request by using the function qr_detected
            App._running_app.qr_detected("https://api.myjson.com/bins/1aob0f")
            sm.current = "menu"
            sm.transition.direction = "right"
        else:
            #Popup which shows an error when the url is wrong
            self.boxlab=BoxLayout(orientation="vertical")
            self.popup1 = Popup(title='ERREUR Url', content=self.boxlab, auto_dismiss=False)
            self.yo1 = ToggleButton(text='Retour au menu de connexion', font_size='20sp')
            self.yo2 = ToggleButton(text='Renouveler l\'essai', font_size='20sp')

            self.boxlab.add_widget(Label(text='Url incorrect', font_size='20sp'))
            self.boxlab.add_widget(self.yo1)
            self.boxlab.add_widget(self.yo2)
            self.yo1.bind(on_release=self.returnmenuscreen)
            self.yo2.bind(on_release=self.popup1.dismiss)
            self.popup1.open()
    #return to the menu screen if the url is correct
    def returnmenuscreen(self,hjk):
        sm.current = "menu"
        sm.transition.direction = "right"
        self.popup1.dismiss()


#Activity screen
class myscreen(Screen):
    def __init__(self, *args, **kwargs):
        super(myscreen, self).__init__(*args, **kwargs)
        #initializing the spinner widget used for letters
        self.letterspinner = Spinner(id="spin", text="les Notes", values=(), font_size='20sp')
        self.ids.labnote.text="Réussite"

    #function called when the text spinner of the activities is modified
    def upgradeactivity(self):
        i = 0

        #research of the correct activity in the dictionary named activities in params.py
        for k in myparams.activities.keys():

            if self.ids.myspinner.text==k.encode("utf-8"):
                #case of a grade in letters
                if myparams.activities.values()[i]["rate"].type == u'letters':
                    self.ids.labnote.text = "Réussite (notation "+\
                                            str(ascii_uppercase[0:myparams.activities.values()[i]["rate"].scale]) + ")"
                    self.ids.blnote.remove_widget(self.ids.blnote.children[0])
                    #activate the letter spinner
                    self.ids.blnote.add_widget(self.letterspinner)

                    #self.rate is the number of letter chosen by the user: if rate=4, there are 4 letters
                    self.rate=myparams.activities.values()[i]["rate"].scale

                    #values of the letters made by the list ascii_uppercase
                    self.letterspinner.values=ascii_uppercase[0:myparams.activities.values()[i]["rate"].scale]
                    self.descr=myparams.activities.values()[i]["description"]

                else:

                    #case of a grade in notes

                    self.ids.blnote.remove_widget(self.ids.blnote.children[0])

                    self.ids.blnote.add_widget(self.ids.input)


                    self.rate = myparams.activities.values()[i]["rate"].scale
                    self.ids.labnote.text = "Réussite (note sur " + str(self.rate)+")"
                    self.descr = myparams.activities.values()[i]["description"]



            i = i + 1

    #function called when we press the button "valider"
    def checkinput(self):
        if self.ids.myspinner.text=="Sélection d'activités":
            self.rate=0
        #case of a note going across the maximum rate
        if (self.ids.input.text == "" or int(self.ids.input.text) > self.rate) and (self.ids.blnote.children[0]==self.ids.input)\
                and self.ids.myspinner.text in self.ids.myspinner.values:
            self.box = BoxLayout(orientation='vertical')
            self.box.add_widget(Label(text='Veuillez choisir une note entre 0 et 20!', font_size='20sp'))

            yo = ToggleButton(text='Ok j\'ai compris!', font_size='20sp')
            nextpage=ToggleButton(text='Ne pas noter cette activité', font_size='20sp')

            self.a=1
            self.box.add_widget(yo)
            self.box.add_widget(nextpage)
            self.popup = Popup(title='Notation incorrecte!', content=self.box, auto_dismiss=False)
            yo.bind(on_release=self.popup.dismiss)
            nextpage.bind(on_release=self.comm)
            self.popup.open()

        elif self.ids.myspinner.text in self.ids.myspinner.values:
            #case of a note entered correctly
            if self.ids.blnote.children[0]==self.ids.input:

                self.listactivity=[self.ids.myspinner.text,self.ids.input.text]
                sm.current = "com"
                sm.get_screen("com").ids.labcomrecap.text = "Bonjour"\
                                                            + " " + \
                    myparams.accounts[sm.get_screen("menu").ids.textid.text]["name"].encode("utf-8") + \
                    "---" + self.ids.myspinner.text + "---" + self.ids.input.text.encode("utf-8")


            #case of a note in letters entered correctly
            elif self.letterspinner.text in self.letterspinner.values:
                print(self.letterspinner.text)

                self.listactivity = [self.ids.myspinner.text, self.letterspinner.text]
                print(type(myparams.accounts[sm.get_screen("menu").ids.textid.text]["name"]))
                print(type(self.ids.myspinner.text))
                print(type(self.letterspinner.text))
                sm.current = "com"
                sm.get_screen("com").ids.labcomrecap.text = "Bonjour" + " " + \
                myparams.accounts[sm.get_screen("menu").ids.textid.text]["name"].encode("utf-8") + "--- " + self.ids.myspinner.text\
                                                         + "---" + self.letterspinner.text
                #case when no activity note is given
            else:
                self.box3 = BoxLayout(orientation='vertical')
                self.box3.add_widget(Label(text='Vous allez validez sans noter votre activité', font_size='20sp'))

                returnact = ToggleButton(text='Retour aux activités', font_size='20sp')
                nextpage2 = ToggleButton(text='Ne pas noter cette activité', font_size='20sp')

                self.box3.add_widget(returnact)
                self.box3.add_widget(nextpage2)
                self.popup = Popup(title='Activité sans notation!', content=self.box3, auto_dismiss=False)
                returnact.bind(on_release=self.popup.dismiss)
                nextpage2.bind(on_release=self.comm)
                self.popup.open()
        #convert the letter graduation into a fraction by 1
        p=len(self.letterspinner.values)
        for a in self.letterspinner.values:
            if self.letterspinner.text == a:
                self.grade = float(p) / float(len(self.letterspinner.values))
            p=p-1
    #called when we want to skip to next page whithout entering a note
    def comm(self,g):
        sm.current="com"
        sm.transition.direction="left"
        self.popup.dismiss()
        sm.get_screen("com").ids.labcomrecap.text = "Bonjour" \
                                                    + " " + \
                                                    myparams.accounts[sm.get_screen("menu").ids.textid.text][
                                                        "name"].encode("utf-8") + \
                                                    "---" + self.ids.myspinner.text + "---non notée"

    #function called when the activity spinner is pressed
    def updateactivities(self):

        self.ids.mylabel.text = "Notez l'activité sélectionnée"
        self.ids.myspinner.values = [v.encode("utf-8") for v in myparams.activities.keys()]


    #function called when we press the sign out button
    def statementsended(self):
        #popup appears if we don't validate at the commentaries page
        if sm.get_screen("com").a!=[2]:
            self.box = BoxLayout(orientation='vertical')
            self.box.add_widget(
                Label(text='Rien n\'a été enregistré,vous allez vous déconnecter sans rien valider', font_size='20sp'))
            returndeco = ToggleButton(text='Ok, je suis prévenu', font_size='20sp')
            self.box.add_widget(returndeco)

            self.popup = Popup(title='Pas d\'enregistrement de vos saisies', content=self.box, auto_dismiss=False)
            returndeco.bind(on_release=self.popup.dismiss)

            self.popup.open()
            sm.transition.direction = 'left'
            sm.current = 'deconnexion'
        else:
            sm.transition.direction = 'left'
            sm.current = 'deconnexion'


#class making the QR scan process
class QrScreen(Screen):


    def __init__(self, *args, **kwargs):
        super(QrScreen, self).__init__(*args, **kwargs)
        #case when we can't scan a QR code
        if qrwidget == None:
            mypop = Myalternativepopupbox()
            self.add_widget(mypop)



        else:
            #no need to launch the camera if the file exists,already done
            if os.path.exists("mydata.data"):
                self.add_widget(qrwidget)

            else:
                qrwidget.ids.detector.start()
                self.add_widget(qrwidget)




            # etape 1 : recup widget ZbarQrcodeDetector (probablement qrwidget.ids.detevtot
            # etape 2 :  widgetdetector.bind(on_symbols=self.printsymbols)
    #called when a QR code is detected, popup is released
    def create_popup2(self):

        self.mypop2 = Myalternativepopup2()
        self.box = BoxLayout(orientation='vertical')
        self.add_widget(self.mypop2)
        bt2 = self.mypop2.ids.return_button2

        bt2.bind(on_release=self.printsymbols)


        self.add_widget(self.box)


    #the app is going to menuscreen if a QR code is detected
    def printsymbols(self,data):

        sm.current = "menu"
        sm.transition.direction = "right"

        self.remove_widget(self.mypop2)


        self.remove_widget(self.box)





# Menu screen, sign in menu
class MenuScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(MenuScreen, self).__init__(*args, **kwargs)

        #modifying text we can't scan a QR code
        if qrwidget==None:
            self.ids.buturl.text="Entrez un url"
        else:
            self.ids.buturl.text = "Scannez un qr code"

    #check if id and password are correct and correspond to our elements in the dic called accounts in params.py
    def checkidandpw(self):
        print (self.ids.textmdp.text)
        print(myparams.__dict__)
        self.box = BoxLayout(orientation='vertical')
        self.popup = Popup(title='Identifiant ou mot de passe incorrect', content=self.box, auto_dismiss=False)
        self.yo = ToggleButton(text='Retour au menu de connexion', font_size='20sp')

        if self.ids.textid.text in myparams.accounts.keys() and self.ids.textmdp.text == \
                myparams.accounts[self.ids.textid.text]["mdp"]:
            sm.transition.direction = 'left'
            sm.current = 'activity'
            sm.get_screen("activity").ids.labid.text = "Bonjour" + "  " + myparams.accounts[self.ids.textid.text][
                "name"]
        else:

            self.box.add_widget(Label(text='Erreur dans la saisie de l\'identifiant ou mot de passe', font_size='20sp'))
            self.box.add_widget(self.yo)

            self.yo.bind(on_release=self.popup.dismiss)
            self.popup.open()

    #verify if a QR is already scanned and registered
    def popupverif(self):
        if os.path.exists("mydata.data"):
            self.b = BoxLayout(orientation='vertical')
            self.pop = Popup(title='Un QR code est déjà enregistré', content=self.b, auto_dismiss=False)
            self.yo = ToggleButton(text='Retour au menu de connexion', font_size='20sp')
            if qrwidget==None:
                self.yo1=ToggleButton(text='Je veux enregistrer un lien url', font_size='20sp')
            else:
                self.yo1 = ToggleButton(text='Je veux scanner un QR code', font_size='20sp')
            self.b.add_widget(
                    Label(text='Un QR code déjà enregistré, êtes vous sûr d\'en enregistrer un nouveau?', font_size='20sp'))
            self.b.add_widget(self.yo)
            self.b.add_widget(self.yo1)
            self.yo.bind(on_release=self.pop.dismiss)
            self.yo1.bind(on_release=self.gotoqrscr)
            self.pop.open()
        else:
            if qrwidget == None:
                sm.current="qrscr"
                sm.transition.direction="left"
            else:
                sm.current = "qrscr"
                sm.transition.direction = "left"
                qrwidget.ids.detector.start()

    #function called when we want to scan an other QR code
    def gotoqrscr(self,t):
        if qrwidget == None:
            sm.current = "qrscr"
            sm.transition.direction = "left"
        else:
            qrwidget.ids.detector.start()
            sm.current = "qrscr"
            sm.transition.direction = "left"

        self.pop.dismiss()



#Screen of commentaries
class Coms(Screen):
    def __init__(self, *args, **kwargs):
        super(Coms, self).__init__(*args, **kwargs)
        #initializing listecom, list which will contain all the coms
        self.a=[]
        self.listecom=[]
        #textinput of the freecoms
        self.textinput = TextInput(text=" ", multiline=True, font_size='20sp')


    #case when we want to delete the box appeared when adding a com
    def deletebox(self,blhoriz):
        self.ids.changebox.remove_widget(blhoriz)
        if self.ids.changebox.children==[]:         #add the initial title if there is no horizontal boxlayout
            self.ids.changebox.add_widget(self.ids.labcom)

    #create a new box in the top of the screen, containing a spinner com
    def boxcom(self):

        blhoriz=BoxLayout(orientation="horizontal")

        if self.ids.labcom in  self.ids.changebox.children:
            self.ids.changebox.remove_widget(self.ids.labcom)
        self.Selectcom = Label(text=self.ids.myspinner2.text, font_size='18sp')
        Erasecom=ToggleButton(text='Supprimer ce commentaire', font_size='20sp')
        Erasecom.bind(on_press=lambda x: self.deletebox(blhoriz))
        blhoriz.add_widget(self.Selectcom)
        blhoriz.add_widget(Erasecom)
        self.ids.changebox.add_widget(blhoriz)

    #function called when the com spinner is pressed
    def spinner(self):
        self.ids.myspinner2.values=[v.encode("utf-8") for v in myparams.commentaries]

    #create a new box in the top of the screen, containing a free com written in the textinput
    def inputcom(self):
        blhoriz2 = BoxLayout(orientation="horizontal")

        if self.ids.labcom in self.ids.changebox.children:
            self.ids.changebox.remove_widget(self.ids.labcom)
        self.Selectcom = Label(text=self.textinput.text.encode("utf-8"), font_size='18sp')
        Erasecom = ToggleButton(text='Supprimer ce commentaire', font_size='20sp')
        Erasecom.bind(on_press=lambda x: self.deletebox(blhoriz2))
        blhoriz2.add_widget(self.Selectcom)
        blhoriz2.add_widget(Erasecom)
        self.ids.changebox.add_widget(blhoriz2)
        self.textinput.text=" "

    #replace boxes to add the textinput for freecoms
    def createinput(self):


        self.ids.comlib.remove_widget(self.ids.champlibre)
        self.ids.comlib.add_widget(self.textinput)
        addcominput = ToggleButton(text='Ajouter un autre commentaire libre', font_size='20sp')

        addcominput.bind(on_press=lambda x: self.inputcom())
        self.ids.comlib.add_widget(addcominput)

    #function called when the button "valider" is pressed, statements are sended
    def valideco(self):
        state=Autostatement()
        self.listecom=[]
        for box in self.ids.changebox.children:
            try:
                if box.children[1].text in self.listecom:
                    pass
                else:
                    self.listecom.append(box.children[1].text)
            except:
                pass
        if self.ids.myspinner2.text in self.listecom:
            pass
        else:
            self.listecom.append(self.ids.myspinner2.text)

        if self.textinput.text!=" ":
            self.listecom.append(self.textinput.text.encode("utf-8"))

        #initializing popup when a validation is made succesfully
        self.bvalid = BoxLayout(orientation="vertical")
        self.returnact = ToggleButton(text='Retour', font_size='20sp')
        self.pops = Popup(title='Bravo, vos données ont bien été envoyées', content=self.bvalid, auto_dismiss=False)
        self.returnact.bind(on_release=self.validate)

        if self.listecom[0]==["Sélection de commentaires"]:
            del self.listecom[0]

        if self.listecom==["Sélection de commentaires"]:
            del self.listecom[0]
            self.box = BoxLayout(orientation='vertical')
            self.box.add_widget(
                Label(text='Valider sans laisser de commentaires?', font_size='20sp'))

            returncom = ToggleButton(text='Retour à la page Commentaires', font_size='20sp')
            nextpage = ToggleButton(text='Confirmer la validation', font_size='20sp')

            self.box.add_widget(returncom)
            self.box.add_widget(nextpage)
            self.popup = Popup(title='Aucun commentaire saisi', content=self.box, auto_dismiss=False)
            returncom.bind(on_release=self.popup.dismiss)
            nextpage.bind(on_release=lambda x:self.confirmcom(state))
            self.popup.open()
        else:
            try:
                state.send_statement()
            except:
                #case when the statements are not send due to a default of connexion
                self.boxerr = BoxLayout(orientation="vertical")
                self.errpop = Popup(title='ERREUR Url', content=self.boxlab, auto_dismiss=False)
                self.returntocom = ToggleButton(text='Retour à la page commentaires', font_size='20sp')
                self.boxerr.add_widget\
                    (Label(text='Veuillez vous connecter à un réseau sans fil avant de lancer l\'application', font_size='20sp'))
                self.boxerr.add_widget(self.returntocom)

                self.returntocom.bind(on_release=self.errpop.dismiss)
                self.errpop.open()
            self.a=[2]

            self.bvalid.add_widget(self.returnact)

            self.pops.open()

            sm.get_screen("activity").ids.labid.text = "Bonjour"+" "+\
                                                           myparams.accounts[sm.get_screen("menu").ids.textid.text][
                                                            "name"].encode("utf-8")+"---"+str(self.listecom)
    #return to activity if the validation is a success
    def validate(self,uyf):
        self.pops.dismiss()

        sm.current = "activity"
        sm.transition.direction = "right"

    #case when there is no coms entered, popup released
    def confirmcom(self,state):
        self.popup.dismiss()
        self.bvalid.add_widget(self.returnact)
        self.pops.open()
        try:
            state.send_statement()
        except:
            # case when the statements are not sent due to a default of connexion
            self.boxerr = BoxLayout(orientation="vertical")
            self.errpop = Popup(title='ERREUR Url', content=self.boxlab, auto_dismiss=False)
            self.returntocom = ToggleButton(text='Retour à la page commentaires', font_size='20sp')
            self.boxerr.add_widget \
                (Label(text='Veuillez vous connecter à un réseau sans fil avant de lancer l\'application',
                       font_size='20sp'))
            self.boxerr.add_widget(self.returntocom)

            self.returntocom.bind(on_release=self.errpop.dismiss)
            self.errpop.open()


        self.listecom = ["No commentaries"]

        self.a=[2]
        sm.get_screen("activity").ids.labid.text="Bonjour"+" "\
                                                 +myparams.accounts[sm.get_screen("menu").ids.textid.text]["name"].encode("utf-8")\
                                                 +" "+"---Pas de commentaires"

#log out screen
class Logout(Screen):
    pass

#screen widget
sm = ScreenManager(transition=SlideTransition())

#the first screen is different if the url or qr code is registered or not
if os.path.exists("mydata.data"):
    sm.add_widget(MenuScreen(name='menu'))
    sm.add_widget(QrScreen(name='qrscr'))
    sm.add_widget(myscreen(name='activity'))
    sm.add_widget(Coms(name='com'))
    sm.add_widget(Logout(name='deconnexion'))

else:

    sm.add_widget(QrScreen(name='qrscr'))
    sm.add_widget(MenuScreen(name='menu'))
    sm.add_widget(myscreen(name='activity'))
    sm.add_widget(Coms(name='com'))
    sm.add_widget(Logout(name='deconnexion'))


#class sending the statements to an endpoint written in our dictionary in params.py
class Autostatement():
    def __init__(self):
        self.actor_name = myparams.accounts[sm.get_screen("menu").ids.textid.text]["name"].encode("utf-8")
        self.activity_name=sm.get_screen("activity").ids.myspinner.text
        #case when the graduation is a correct note
        if (sm.get_screen("activity").ids.blnote.children[0]==sm.get_screen("activity").ids.input)\
                and sm.get_screen("activity").ids.input.text.encode("utf-8")!="" \
                and int(sm.get_screen("activity").ids.input.text.encode("utf-8"))<sm.get_screen("activity").rate:
            self.activity_note=sm.get_screen("activity").ids.input.text.encode("utf-8")
            self.ratescale = sm.get_screen("activity").rate
            self.min=0
        #case of a grade in letters
        elif sm.get_screen("activity").letterspinner.text in sm.get_screen("activity").letterspinner.values:
            self.activity_note=sm.get_screen("activity").grade
            self.ratescale=1
            self.min=0.25
        #otherwise no notes
        else:
            self.activity_note=None
            self.ratescale=None
            self.min=None

        #reaffect the lrs properties in self.lrs
        lrs_properties.endpoint=myparams.lrsdict.values()[0]["endpoint"]

        lrs_properties.password=myparams.lrsdict.values()[0]["password"]
        lrs_properties.username=myparams.lrsdict.keys()[0]
        lrs_properties.version=myparams.lrsdict.values()[0]["version"]
        self.lrs = RemoteLRS(
            version=lrs_properties.version,
            endpoint=lrs_properties.endpoint,
            username=lrs_properties.username,
            password=lrs_properties.password,
        )

    #function which send a statement containing actor, verb ,object,result
    def send_statement(self):

        actor = Agent(
            name=self.actor_name,
            mbox='mailto:'+self.actor_name+'@hotmail.fr',
        )
        verb = Verb(
            id='http://adlnet.gov/expapi/verbs/experienced',
            display=LanguageMap({'en-US': 'completed'}),
        )
        object = Activity(
            id='http://tincanapi.com/TinCanPython/Example/0',
            definition=ActivityDefinition(
                name=LanguageMap({'fr-FR': self.activity_name}),
                description=LanguageMap({'fr-FR':str(sm.get_screen("activity").descr)}),
                #= self.activity_note,
            ),

        )
        dico={}
        comment=""
        #list containing all the coms registered by the user
        self.comlist = sm.get_screen("com").listecom
        for com in self.comlist:
            comment+=com

        #determine if there is a need to send the result statement
        if self.activity_note==None and comment=="No commentaries":
            print("ok ca passe")
            statement = Statement(
                actor=actor,
                verb=verb,
                object=object,

            )
        #case when only coms are entered, no score needed in result
        elif self.activity_note==None:
            dico["http://www.tincan.com/extensions/commentaries"] = str(self.comlist)
            result = Result(
                extensions=Extensions(dico
                                      ),
            )
            statement = Statement(
                actor=actor,
                verb=verb,
                object=object,
                result=result,
            )

        # case when only notes are entered, no extensions needed
        elif comment=="No commentaries":
            result = Result(
                score=Score(
                    raw=self.activity_note,
                    min=self.min,
                    max=self.ratescale,
                ),

            )
            statement = Statement(
                actor=actor,
                verb=verb,
                object=object,
                result=result,
            )
        else:

            dico["http://www.tincan.com/extensions/commentaries"]=str(self.comlist)
            result = Result(
                score=Score(
                    raw=self.activity_note,
                    min=self.min,
                    max=self.ratescale,
                ),
                extensions= Extensions(dico
                ),
            )
            statement = Statement(
            actor=actor,
            verb=verb,
            object=object,
            result=result,
            )



        response = self.lrs.save_statement(statement)

        print (statement.to_json())
        if not response:
            self.blay = BoxLayout(orientation='vertical')
            self.blay.add_widget(
                Label(text='Erreur de connexion, veuillez vérifiez votre connexion sans fil', font_size='20sp'))
            # size = ('500sp', '150sp')
            returncom = ToggleButton(text='Retour au menu principal', font_size='20sp')

            self.blay.add_widget(returncom)
            #self.blay.add_widget(nextpage)
            self.popup3 = Popup(title='Données non envoyées!', content=self.blay, auto_dismiss=False)
            returncom.bind(on_release=self.returnidmenu)

            self.popup.open()

    def returnidmenu(self):

        sm.current="menu"
        sm.transition.direction="right"
        self.popup3.dismiss()

class CarnetdeBord(App):


    def build(self):

        return sm
    #function called when a qr code is scanned
    def qr_det(self):
        qrwidget.ids.detector.stop()
        sm.get_screen("qrscr").create_popup2()

    #function when the returnmenu button is pressed in th qr screen
    def menureturn(self):
        qrwidget.ids.detector.stop()
        sm.current="menu"
        sm.transition.direction="right"

    #called to make an urlrequest
    def qr_detected(self, url):
        myparams.build_from_url2(url)



if __name__ == "__main__":
    CarnetdeBord().run()
