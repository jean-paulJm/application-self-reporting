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

myparams = params.Extparams()
myparams.build_from_url()
# Test du widget ToggleButton
#KIVY_DPI=320 KIVY_METRICS_DENSITY=2 python main.py --size 1280x720
Builder.load_string('''
<myscreen>:
    
    GridLayout:
        cols:1
        rows:5
        BoxLayout:
            size_hint:('80sp','80sp')
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
                text: 'Page Commentaires'
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
                text: 'Connexion'
                font_size: '30sp'
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'activity'
<Coms>:
    GridLayout:
        cols:1
        rows:4
        BoxLayout:
            size_hint:('80sp','80sp') 
            Label:
                id: labcom
                text:'Choisissez un commentaire'
                font_size:'50sp'
        BoxLayout:
            size_hint:('40sp','40sp')
            Spinner:
                id:myspinner2
                text:"Sélection de commentaires"
                # available values
                values:('Nul','très amusant','Pas assez de temps','....')
                font_size:'20sp'
        BoxLayout:
            size_hint:('50sp','50sp')
            Label:
                text:"Commentaires libres"
                font_size: '18sp'
            TextInput:
                multiline:False
                font_size: '20sp'   
        BoxLayout:
            size_hint: ('60sp','60sp')
            ToggleButton:
                text: 'Valider'
                font_size: '30sp'
                on_press: root.send_statement()
            ToggleButton:
                text: 'Déconnexion'
                font_size: '30sp'
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'deconnexion'
<Logout>:
    GridLayout:
        cols:1
        rows:3
        BoxLayout:
            size_hint:('80sp','80sp') 
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
                text: 'Se déconnecter'
                font_size: '20sp'
                on_press: 
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'menu'
                    
''')

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
        if int(self.ids.input.text) > 20:
            self.box = BoxLayout(orientation='vertical')
            self.box.add_widget(Label(text='Veuillez choisir une note entre 0 et 20!',font_size='20sp',
                                      size_hint=(None,None),size=('500sp','200sp')))

            yo=ToggleButton(text='Ok j\'ai compris!',font_size='20sp',size_hint=(None,None),size=('480sp','200sp'))

            #box.add_widget(TextInput(text='Hi'))
            self.box.add_widget(yo)
            self.popup = Popup(title='Notation incorrecte!', content=self.box,auto_dismiss=False,
                          size_hint=(None,None),size=('500sp', '500sp'))
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

class MenuScreen(Screen):
        pass
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

class MonAppli(App):
    def build(self):

        return sm

if __name__=="__main__":
    MonAppli().run()
