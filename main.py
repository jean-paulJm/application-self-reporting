#kivy.require('1.9.10') # replace with your current kivy version !
# -*- coding: utf-8 -*-
from kivy.uix.gridlayout import GridLayout
from extparams import params
from tincan import (
    RemoteLRS,
    Statement,
    Agent,
    Verb,
    Activity,
    Context,
    LanguageMap,
    ActivityDefinition,
    StateDocument,
)
import uuid
from ressources import lrs_properties

#Builder.load_file('/home/upmc/Documents/kivyproject/main.kv')

#class sendStatements(Widget):
 #   RemoteLRS


from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen , SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color

#from jnius import autoclass, PythonJavaClass, java_method, cast
from kivy.uix.scrollview import ScrollView
try:
    from QRmodule.qr import qrwidget
except:
    qrwidget = None


myparams = params.Extparams()
myparams.build_from_url()
# Test du widget ToggleButton
#KIVY_DPI=320 KIVY_METRICS_DENSITY=2 python main.py --size 1280x720



Builder.load_string('''
<myscreen>:
    
    GridLayout:
        cols:1
        rows:5
         # blue color with 50% alpha
       
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
                id: mylabel
                font_size:'50sp'
                text: "Page d'autoévaluation"
        BoxLayout:
            
            size_hint:('40sp','40sp')
            Spinner:
                id:myspinner
                text:"Sélection d'activités"
                # available values
                values:('','')
                
                on_press:root.updateactivities()
                font_size:'20sp'
        BoxLayout:
            
            size_hint:('40sp','40sp')
            Label:
                text: 'Réussite (note sur 20)'
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
            size_hint:('60sp','60sp')
            #ToggleButton:
            #    text: 'Valider'
            #    font_size: '30sp'
            #    on_press:
            #        root.checkinput()
            #        root.upgradeactivity()
                        
  
            ToggleButton:
                canvas:
                    Color:
                        rgba: 0,0.5, 0, 0.5 
                    Rectangle:
            # self here refers to the widget i.e FloatLayout
                        pos: self.pos
                        size: self.size
                text: 'Page suivante'
                font_size: '30sp'
                on_press:
                    root.checkinput()
                    root.manager.transition.direction = 'left'
                    #root.manager.current = 'com'
                

        
                
        
            
<MenuScreen>:
    GridLayout: 
        cols: 1
        rows: 4
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
                text: "Bienvenue!"
                
                font_size:'50sp'
        BoxLayout:## here is one Box
            size_hint:('50sp','50sp')   
            Label:
                text: 'Identifiant'
                font_size: '18sp'
                
            TextInput:
                multiline:False
                font_size: '20sp'   
                
        
        BoxLayout:
            size_hint:('50sp','50sp') ## here is another Box
            Label:
                text: 'Mot de passe'
                font_size: '18sp'
                
            TextInput:
                multiline:False
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
                    root.manager.current= 'qrscr'
                    root.manager.transition.direction = 'left'
                    #root.manager.current = 'activity'
                    
<QrScreen>:
    fullscreen: True
    name: 'Popups'
    BoxLayout:
        id: bl
                     
<Myalternativepopupbox>:
    #popup: popup.__self__
    BoxLayout:
        id: bl
        Popup:
            id: popup
            title : ""
            Button:
                text : "revenir à l'écran de connexion"
                id: return_button
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
        rows:3
        id:grid
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
                canvas:
                    Color:
                        rgba: 0.9,0.1, 0, 0.5 
                    Rectangle:
            # self here refers to the widget i.e FloatLayout
                        pos: self.pos
                        size: self.size
                id:myspinner2
                text:"Sélection de commentaires"
                # available values
                values:('Nul','très amusant','Pas assez de temps','....')
                font_size:'20sp'
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
                on_press:root.createinput()
                state:'normal'
            #root.champlibre()
                
        #BoxLayout:
        #    size_hint:('50sp','50sp')
        #   Label:
        #        text:"Commentaires libres"
        #        font_size: '18sp'
        #    TextInput:
        #        multiline:False
        #        font_size: '20sp'   
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
                #on_press: root.send_statement()
                state:'normal'
            ToggleButton:
                id:deco
                canvas:
                    Color:
                        rgba: 0.9,0.1, 0, 0.5 
                    Rectangle:
            # self here refers to the widget i.e FloatLayout
                        pos: self.pos
                        size: self.size
                
                text: 'Déconnexion'
                font_size: '30sp'
                on_press:root.valideco()
                    
                  
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
                text: 'Retour à la page Activités'
                font_size: '20sp'
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'activity'
                    
            ToggleButton:
                text: 'Retour à la page Commentaires'
                font_size: '20sp'
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'com'
        BoxLayout:
            size_hint:('60sp','60sp')
            ToggleButton:
                canvas:
                    Color:
                        rgba: 0.9,0.1, 0, 0.5 
                    Rectangle:
            # self here refers to the widget i.e FloatLayout
                        pos: self.pos
                        size: self.size
                text: 'Se déconnecter'
                font_size: '20sp'
                on_press: 
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'menu'
#pupqr>:
   # fullscreen:True
    
    #BoxLayout:
        #orientation:'vertical'
        #Popup:
            #id:popup
           # title:'Notation incorrecte!'
            
            #Label:
            #    text:'Veuillez choisir une note entre 0 et 20!'
            #    font_size:'20sp'
            # size = ('500sp', '150sp')
            #ToggleButton:
            #    text:'Ok j\\'ai compris!'
            #    font_size:'20sp'
            #    on_press:popup.dismiss()
            # size = ('480sp', '150sp'
            # box.add_widget(TextInput(text='Hi'))
            
            
            #bout.bind(on_release=popup.dismiss)
            #root.Popup.open()
    
                    
''')
class Myalternativepopup2(BoxLayout):
    pass
class Myalternativepopupbox(BoxLayout):
    pass

class myscreen(Screen):


    def __init__(self,*args, **kwargs):
        super(myscreen, self).__init__(*args, **kwargs)
        self.lrs = RemoteLRS(
            version=lrs_properties.version,
            endpoint=lrs_properties.endpoint,
            username=lrs_properties.username,
            password=lrs_properties.password,
        )

    def upgradeactivity(self):
        i=0
        for k in myparams.activities.keys():

            if self.ids.myspinner.text in k:

                print(myparams.activities.values()[i].values()[1])
                print(myparams.activities.values()[i].values()[0])
                print(self.ids.input.text)
            i = i + 1
    def checkinput(self):
        if self.ids.input.text=="" or int(self.ids.input.text) > 20:
            self.box = BoxLayout(orientation='vertical')
            self.box.add_widget(Label(text='Veuillez choisir une note entre 0 et 20!',font_size='20sp'))
           # size = ('500sp', '150sp')
            yo=ToggleButton(text='Ok j\'ai compris!',font_size='20sp')
            #size = ('480sp', '150sp'
            #box.add_widget(TextInput(text='Hi'))
            self.box.add_widget(yo)
            self.popup = Popup(title='Notation incorrecte!', content=self.box,auto_dismiss=False)
            yo.bind(on_release  =self.popup.dismiss)
            self.popup.open()
        else:
            self.upgradeactivity()
            sm.current="com"



    def updateactivities(self):
        #for k in myparams.activities.iterkeys():
                #lrs_properties.username= myparams.activities.values()[i].values()[1]
                #scale=myparams.activities.values()[i].values()[0]
        self.ids.myspinner.values = myparams.activities.keys()
        #print(myparams.activities.keys())
        self.ids.mylabel.text = "Notez l'activité sélectionnée"
        #if text == '#1':
         #   self.ids.spinner_2.values = ['A', 'B']
        #elif text == '#2':
        #    self.ids.spinner_2.values = ['P', 'Q']
        #else:
        #    self.ids.spinner_2.values = ['Y', 'Z']
    #def deleteactivity(self):
    #    self.ids.lab2.text=self.ids.lab2.text.replace(list[len(list)+1] , " ")
    def send_statement(self):

        actor = Agent(
            name='UserMan_test_2',
            mbox='mailto:tincanpython@tincanapi.com',
        )
        verb = Verb(
            id='http://adlnet.gov/expapi/verbs/experienced',
            display=LanguageMap({'en-US': 'experienced'}),
        )
        object = Activity(
            id='http://tincanapi.com/TinCanPython/Example/0',
            definition=ActivityDefinition(
            name=LanguageMap({'en-US': 'TinCanPython Library'}),
            description=LanguageMap({'en-US': 'Use of, or interaction with, the TinCanPython Library'}),
            ),
        )
        context = Context(
            registration=uuid.uuid4(),
            instructor=Agent(
                name='Lord TinCan',
                mbox='mailto:lordtincan@tincanapi.com',
            ),
            # language='en-US',
        )
        statement = Statement(
            actor=actor,
            verb=verb,
            object=object,
            context=context,
        )
        #self.ids.mylabel.text="Notez l'activité sélectionnée"

        #self.ids.myspinner.text="Les activités"
        #self.ids.myspinner.values = myparams.activities.keys()

        #list+=[self.ids.myspinner.text +' : '+self.ids.input.text + "\n"]
        #self.ids.lab2.text+=self.ids.myspinner.text +' : '+self.ids.input.text + "\n"
        response = self.lrs.save_statement(statement)
        if not response:
            raise ValueError("statement failed to save")

        state_document = StateDocument(
            activity=object,
            agent=actor,
            id='stateDoc',
            content=bytearray('stateDocValue', encoding='utf-8'),
        )
        response = self.lrs.save_state(state_document)

        if not response.success:
            raise ValueError("could not save state document")

class QrScreen(Screen):
    def __init__(self,*args, **kwargs):
        super(QrScreen, self).__init__(*args, **kwargs)

        if qrwidget==None:
            mypop = Myalternativepopupbox()
            self.add_widget(mypop)
            print(self.ids.bl.ids)
            but = mypop.ids.return_button
            but.bind(on_release=self.returnmenu)
        else:
            self.add_widget(qrwidget)

            # etape 1 : recup widget ZbarQrcodeDetector (probablement qrwidget.ids.detevtot
            # etape 2 :  widgetdetector.bind(on_symbols=self.printsymbols)

    def create_popup2(self):
        self.add_widget(qrwidget)
        mypop2 = Myalternativepopup2()

        self.add_widget(mypop2)
        bt2 = mypop2.ids.return_button2

        bt2.bind(on_release=self.printsymbols)

        self.remove_widget(qrwidget)

    def returnmenu(self, data):
        print("xe tets")

        sm.current="menu"
        sm.transition.direction="right"
    def printsymbols(self,data):
        #print(data)
        #self.add_widget(qrwidget)
        #self.testbox = BoxLayout(orientation='vertical')
        #self.testbox.add_widget(Label(text="symbole détecté", font_size='40sp'))
        sm.current="menu"
        sm.transition.direction="right"

        #self.add_widget(qrwidget)
        #self.testbox = BoxLayout(orientation='vertical')
        #self.testbox.add_widget(Label(text='Veuillez choisir une note entre 0 et 20!', font_size='40sp'))
        #qrwidget.add_widget(self.testbox)
        print ("ok")
class MenuScreen(Screen):
    def __init__(self,*args, **kwargs):
        super(MenuScreen, self).__init__(*args, **kwargs)
        self.lrs = RemoteLRS(
            version=lrs_properties.version,
            endpoint=lrs_properties.endpoint,
            username=lrs_properties.username,
            password=lrs_properties.password,
        )


        #def __init__(self,*args, **kwargs):
        #   super(MenuScreen, self).__init__(*args,**kwargs)
        #def identif(self):
        #   self.manager.transition = SlideTransition(direction="left")
        #   self.ids['login'].text = ""
        #   self.ids['password'].text = ""
class Coms(Screen):
    def __init__(self,*args, **kwargs):
        super(Coms, self).__init__(*args, **kwargs)
        self.lrs = RemoteLRS(
            version=lrs_properties.version,
            endpoint=lrs_properties.endpoint,
            username=lrs_properties.username,
            password=lrs_properties.password,
        )

    #def champlibre(self):
        #self.box2 = BoxLayout(orientation='vertical')
     #   champ = ToggleButton(text='Ajouter un commentaire', font_size='20sp')
        # size = ('480sp', '150sp'
        # box.add_widget(TextInput(text='Hi'))
        #self.box2.add_widget(champ)
        #if self.ids..on_press==root.champlibre():
        #    print(ok)
        #else:
        #    self.ids.selecom.add_widget(champ)
    def deletecom(self,textinput):

        textinput.text=""




    def createinput(self):
        #root = ScrollView(bar_pos_y="right", bar_width="10sp", bar_margin="1sp", scroll_type=["bars"])

        textinput = TextInput(text='', multiline=True, font_size='20sp')
        text=self.ids.labcom
        erase = ToggleButton(text='Supprimer ce commentaire', font_size='20sp')
        erase.bind(on_press=lambda x: self.deletecom(textinput))
        self.ids.valid.bind(on_press=lambda x:self.retake(textinput))
        box=BoxLayout()
        Grid=GridLayout(cols=2,rows=None,size_hint_y='80sp')
        if self.ids.addcom.state=='down':
            self.ids.changebox.remove_widget(text)

         #   root.add_widget(Grid)
        #Grid.add_widget(box)
        #box.add_widget(Grid)
        self.ids.changebox.add_widget(Grid)
        Grid.add_widget(box)
        box.add_widget(textinput)
        box.add_widget(erase)
        #Grid.add_widget(erase)
        self.ids.addcom.state='down'

        #root.add_widget(erase)
        #textinput.add_widget(s)
    def retake(self,textinput):
        self.ids.valid.state='down'

        print (textinput.text)

    def valideco(self):

        if self.ids.valid.state == 'down' and self.ids.myspinner2.text in self.ids.myspinner2.values:
            print(self.ids.myspinner2.text)
            sm.transition.direction = 'left'
            sm.current = 'deconnexion'
        else:
            self.box2 = BoxLayout(orientation='vertical')
            self.box2.add_widget(Label(text='Veuillez validez avant de vous déconnecter', font_size='20sp'))
            # size = ('500sp', '150sp')
            yo = ToggleButton(text='Ok j\'ai compris!', font_size='20sp')
            # size = ('480sp', '150sp'
            # box.add_widget(TextInput(text='Hi'))
            self.box2.add_widget(yo)
            self.popup = Popup(title='Non validation de vos commentaires', content=self.box2, auto_dismiss=False)
            yo.bind(on_release=self.popup.dismiss)

            self.popup.open()
        self.ids.valid.state = "normal"


    def send_statement(self):

        actor = Agent(
            name='UserMan_test_2',
            mbox='mailto:tincanpython@tincanapi.com',
        )
        verb = Verb(
            id='http://adlnet.gov/expapi/verbs/experienced',
            display=LanguageMap({'en-US': 'experienced'}),
        )
        object = Activity(
            id='http://tincanapi.com/TinCanPython/Example/0',
            definition=ActivityDefinition(
                name=LanguageMap({'en-US': 'TinCanPython Library'}),
                description=LanguageMap({'en-US': 'Use of, or interaction with, the TinCanPython Library'}),
            ),
        )
        context = Context(
            registration=uuid.uuid4(),
            instructor=Agent(
                name='Lord TinCan',
                mbox='mailto:lordtincan@tincanapi.com',
            ),
            # language='en-US',
        )
        statement = Statement(
            actor=actor,
            verb=verb,
            object=object,
            context=context,
        )


        # self.ids.mylabel.text="Notez l'activité sélectionnée"

        # self.ids.myspinner.text="Les activités"
        # self.ids.myspinner.values = myparams.activities.keys()
        #self.ids.lab2.text = myparams.activities.keys()[1]
        response = self.lrs.save_statement(statement)
        if not response:
            raise ValueError("statement failed to save")

        state_document = StateDocument(
            activity=object,
            agent=actor,
            id='stateDoc',
            content=bytearray('stateDocValue', encoding='utf-8'),
        )
        response = self.lrs.save_state(state_document)

        if not response.success:
            raise ValueError("could not save state document")
class Logout(Screen):
        pass

sm = ScreenManager(transition=SlideTransition())
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(myscreen(name='activity'))
sm.add_widget(Coms(name='com'))
sm.add_widget(Logout(name='deconnexion'))
sm.add_widget(QrScreen(name='qrscr'))
class MonAppli(App):
    #qrscreen = None
    def build(self):

        return sm

    def qr_detected(self):
        #qrscreen=QrScreen()
        #qrscreen.create_popup2(MonAppli.s)
        #self.qrscreen.get_screen("qrscr").create_popup2()
        sm.get_screen("qrscr").create_popup2()
        #sm.current="menu"
        #sm.transition.direction="right"



if __name__=="__main__":
    MonAppli().run()
