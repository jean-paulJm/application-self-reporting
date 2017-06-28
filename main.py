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
    Context,
    LanguageMap,
    ActivityDefinition,
    StateDocument,
)
import uuid
from ressources import lrs_properties

# Builder.load_file('/home/upmc/Documents/kivyproject/main.kv')

# class sendStatements(Widget):
#   RemoteLRS


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

# from jnius import autoclass, PythonJavaClass, java_method, cast
from kivy.uix.scrollview import ScrollView

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
        # BoxLayout:
        #     orientation:'horizontal'
        #     size_hint:('40sp','40sp')
        # 
        #     ToggleButton:
        #         canvas:
        #             Color:
        #                 rgba: 1,0, 0, 0.5 
        #             Rectangle:
        #                 pos: self.pos
        #                 size: self.size
        #         text: 'Déconnexion'
        #         font_size: '30sp'
        #         on_press:
        #             root.statementsended()
                   
        
                
        
            
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
                id: textid
                text:""
                multiline:False
                font_size: '20sp'   
                
        
        BoxLayout:
            size_hint:('50sp','50sp') ## here is another Box
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
                canvas:
                    Color:
                        rgba: 0.9,0.4,0 , 0.7
                    Rectangle:
            # self here refers to the widget i.e FloatLayout
                        pos: self.pos
                        size: self.size
                text: 'Scanner un QR code'
                
                font_size: '30sp'
                on_press:
                    root.manager.current= 'qrscr'
                    root.manager.transition.direction = 'left'
                    
                    
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
                #canvas:
                #    Color:
                #        rgba: 0,0.1, 0, 0.5 
                #    Rectangle:
            # self here refers to the widget i.e FloatLayout
                #        pos: self.pos
                #        size: self.size
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
            #TextInput:
            #    multiline:False
            #    font_size: '20sp'   
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
    def __init__(self, *args, **kwargs):
        super(myscreen, self).__init__(*args, **kwargs)
        self.listactivity=[0,0]
        self.letterspinner = Spinner(id="spin", text="les Notes", values=('A', 'B', 'C', 'D'), font_size='20sp')



    def upgradeactivity(self):
        i = 0
        a=1
        self.letterspinner = Spinner(id="spin", text="les Notes", values=('A', 'B', 'C', 'D'), font_size='20sp')
        for k in myparams.activities.keys():

            if 'u''+self.ids.myspinner.text==k:
                #print(myparams.activities.values()[i])
                if myparams.activities.values()[i].type == u'letters':
                    self.ids.labnote.text = "Réussite (en ABCD)"
                    self.ids.blnote.remove_widget(self.ids.blnote.children[0])
                    self.ids.blnote.add_widget(self.letterspinner)
                    a = 2
                    #print(myparams.activities.values()[i].scale)


                else:

                    # self.ids.blnote.add_widget(letterspinner)

                    self.ids.blnote.remove_widget(self.ids.blnote.children[0])

                    self.ids.blnote.add_widget(self.ids.input)

                    self.ids.labnote.text = "Réussite (note sur 20)"

                    #print(myparams.activities.values()[i].scale)

                # print(str(myparams.activities.values()[i].values()[0]))


            i = i + 1


    def checkinput(self):
        if (self.ids.input.text == "" or int(self.ids.input.text) > 20) and (self.ids.blnote.children[0]==self.ids.input):
            self.box = BoxLayout(orientation='vertical')
            self.box.add_widget(Label(text='Veuillez choisir une note entre 0 et 20!', font_size='20sp'))
            # size = ('500sp', '150sp')
            yo = ToggleButton(text='Ok j\'ai compris!', font_size='20sp')
            # size = ('480sp', '150sp'
            # box.add_widget(TextInput(text='Hi'))
            self.a=1
            self.box.add_widget(yo)
            self.popup = Popup(title='Notation incorrecte!', content=self.box, auto_dismiss=False)
            yo.bind(on_release=self.popup.dismiss)
            self.popup.open()
        else:
            if self.ids.blnote.children[0]==self.ids.input and self.ids.myspinner.text in self.ids.myspinner.values:
                print(self.ids.input.text)
                print(self.ids.myspinner.text)
                self.listactivity=[self.ids.myspinner.text,self.ids.input.text]
                sm.current = "com"


                sm.get_screen("com").ids.labcomrecap.text = "Bonjour" + " " + \
                                                myparams.accounts[sm.get_screen("menu").ids.textid.text]["name"] + \
                                                "---" + self.ids.myspinner.text + "---" + self.ids.input.text
                #else:


            if self.letterspinner.text in self.letterspinner.values:
                print(self.letterspinner.text)
                print(self.ids.myspinner.text)
                self.listactivity = [self.ids.myspinner.text, self.letterspinner.text]
                sm.current = "com"
                sm.get_screen("com").ids.labcomrecap.text = "Bonjour" + " " + \
                myparams.accounts[sm.get_screen("menu").ids.textid.text]["name"] + "--- " + self.ids.myspinner.text\
                                                            + "---" + self.letterspinner.text


        # a = []
        # for i in myparams.activities.keys():
        #     print(type(i))
        #     b=i.encode('raw_unicode_escape')
        #     a = a + [b]
        # print(type(b))
        # self.ids.myspinner.values = a
        # print(self.ids.myspinner.values)
    def updateactivities(self):
        #menu=MenuScreen()
        #self.add_widget(menu)
        # if sm.get_screen("com").ids.myspinner2.text=="Sélection de commentaires":
        #     self.ids.labid.text="Bonjour"+" "+myparams.accounts[sm.get_screen("menu").ids.textid.text]["name"]+" "+"Pas de commentaires"
        # else:
        #     self.ids.labid.text = "Bonjour"+" "+myparams.accounts[sm.get_screen("menu").ids.textid.text]["name"]+" "+sm.get_screen("com").ids.myspinner2.text

        #if name.text==self.ids.boxact.children[0].text:
        #    pass

        #else:
        #    self.ids.boxact.add_widget(name)
        self.ids.mylabel.text = "Notez l'activité sélectionnée"
        self.ids.myspinner.values = myparams.activities.keys()
    def statementsended(self):

        if sm.get_screen("com").a!=[2]:
            self.box = BoxLayout(orientation='vertical')
            self.box.add_widget(
                Label(text='Rien n\'a été enregistré,vous allez vous déconnecter sans rien valider', font_size='20sp'))
            # size = ('500sp', '150sp')
            returndeco = ToggleButton(text='Ok, je suis prévenu', font_size='20sp')
            #nextpage = ToggleButton(text='Confirmer la validation', font_size='20sp')
            # size = ('480sp', '150sp'
            # box.add_widget(TextInput(text='Hi'))
            self.box.add_widget(returndeco)
            #self.box.add_widget(nextpage)
            self.popup = Popup(title='Pas d\'enregistrement de vos saisies', content=self.box, auto_dismiss=False)
            returndeco.bind(on_release=self.popup.dismiss)
            #nextpage.bind(on_release=lambda x: self.confirmcom(state))
            self.popup.open()
            sm.transition.direction = 'left'
            sm.current = 'deconnexion'
        else:
            sm.transition.direction = 'left'
            sm.current = 'deconnexion'

class QrScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(QrScreen, self).__init__(*args, **kwargs)

        if qrwidget == None:
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
        # self.add_widget(qrwidget)
        mypop2 = Myalternativepopup2()

        self.add_widget(mypop2)
        bt2 = mypop2.ids.return_button2

        bt2.bind(on_release=self.printsymbols)
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=str(qrwidget.ids.detector.symbols[0].data), font_size='20sp'))
        self.add_widget(box)
        # self.remove_widget(qrwidget)

    def returnmenu(self, data):
        # print("xe tets")
        sm.current = "menu"
        sm.transition.direction = "right"

        App._running_app.qr_detected("https://api.myjson.com/bins/gu4bz")

    def printsymbols(self, data):
        # print(data)
        # self.add_widget(qrwidget)
        # self.testbox = BoxLayout(orientation='vertical')
        # self.testbox.add_widget(Label(text="symbole détecté", font_size='40sp'))
        sm.current = "menu"
        sm.transition.direction = "right"
        # self.add_widget(qrwidget)
        # self.testbox = BoxLayout(orientation='vertical')
        # self.testbox.add_widget(Label(text='Veuillez choisir une note entre 0 et 20!', font_size='40sp'))
        # qrwidget.add_widget(self.testbox)
        print ("ok")
        # self.add_widget(qrwidget)


class MenuScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(MenuScreen, self).__init__(*args, **kwargs)
        self.lrs = RemoteLRS(
            version=lrs_properties.version,
            endpoint=lrs_properties.endpoint,
            username=lrs_properties.username,
            password=lrs_properties.password,
        )

    def checkidandpw(self):
        print (self.ids.textmdp.text)
        print(myparams.__dict__)
        if self.ids.textid.text in myparams.accounts.keys() and self.ids.textmdp.text==myparams.accounts[self.ids.textid.text]["mdp"]:
            sm.transition.direction = 'left'
            sm.current = 'activity'
            sm.get_screen("activity").ids.labid.text="Bonjour"+ "  "+myparams.accounts[self.ids.textid.text]["name"]
            #ok=myscreen()
            #ok.ids.myspinner.values=myparams.activities.keys()
            #print(ok.ids.myspinner.values)
        else:
            self.box = BoxLayout(orientation='vertical')
            self.box.add_widget(Label(text='Veuillez  d\' abord scanner un qr code', font_size='20sp'))
            # size = ('500sp', '150sp')
            yo = ToggleButton(text='Retour au menu de connexion', font_size='20sp')
            # size = ('480sp', '150sp'
            # box.add_widget(TextInput(text='Hi'))
            self.box.add_widget(yo)
            self.popup = Popup(title='Identifiant ou mot de passe incorrect', content=self.box, auto_dismiss=False)
            yo.bind(on_release=self.popup.dismiss)
            self.popup.open()
            print(myparams.activities.keys())
        # def __init__(self,*args, **kwargs):
        #   super(MenuScreen, self).__init__(*args,**kwargs)
        # def identif(self):
        #   self.manager.transition = SlideTransition(direction="left")
        #   self.ids['login'].text = ""
        #   self.ids['password'].text = ""


class Coms(Screen):
    def __init__(self, *args, **kwargs):
        super(Coms, self).__init__(*args, **kwargs)
        self.a=[]
        self.listecom=[]
        self.textinput = TextInput(text=" ", multiline=True, font_size='20sp')
        #if sm.get_screen("activity").ids.blnote.children[0]==sm.get_screen("activity").ids.input:
        #    self.ids.labrecapcom.text="Bonjour"+" "+myparams.accounts[sm.get_screen("menu").ids.textid.text]["name"]+" "+sm.get_screen("activity").ids.myspinner.text+sm.get_screen("activity").ids.input.text
        #else:
        #    self.ids.labrecapcom.text = "Bonjour" + " " + myparams.accounts[sm.get_screen("menu").ids.textid.text][
        #        "name"] + " "+sm.get_screen("activity").ids.myspinner.text + sm.get_screen("activity").letterspinner.text



    def deletebox(self,blhoriz):
        self.ids.changebox.remove_widget(blhoriz)
        if self.ids.changebox.children==[]:         #add the initial title if there is no horizontal boxlayout
            self.ids.changebox.add_widget(self.ids.labcom)


    def boxcom(self):
        #Grid=GridLayout(rows=None,cols=2)
        blhoriz=BoxLayout(orientation="horizontal")
        #blcom = BoxLayout(hint_size_y=None)
        #blerase = BoxLayout(hint_size_y=None)
        if self.ids.labcom in  self.ids.changebox.children:
            self.ids.changebox.remove_widget(self.ids.labcom)
        self.Selectcom = Label(text=self.ids.myspinner2.text, font_size='18sp')
        Erasecom=ToggleButton(text='Supprimer ce commentaire', font_size='20sp')
        Erasecom.bind(on_press=lambda x: self.deletebox(blhoriz))
        blhoriz.add_widget(self.Selectcom)
        blhoriz.add_widget(Erasecom)
        self.ids.changebox.add_widget(blhoriz)
        #Grid.add_widget(blcom)
        #Grid.add_widget(blerase)
    def spinner(self):
        self.ids.myspinner2.values=myparams.commentaries

        # if sm.get_screen("activity").ids.blnote.children[0] == sm.get_screen("activity").ids.input:
        #     self.ids.labcomrecap.text="Bonjour"+" "+myparams.accounts[sm.get_screen("menu").ids.textid.text]["name"]+\
        #                             "---"+sm.get_screen("activity").ids.myspinner.text+"---"+sm.get_screen("activity").ids.input.text
        # else:
        #     self.ids.labcomrecap.text = "Bonjour"+" "+myparams.accounts[sm.get_screen("menu").ids.textid.text][
        #         "name"]+"--- "+sm.get_screen("activity").ids.myspinner.text+"---"+sm.get_screen("activity").letterspinner.text



    def deletecom(self, textinput,erase):

        textinput.text = " "
        self.ids.comlib.remove_widget(textinput)
        self.ids.comlib.remove_widget(erase)
        self.ids.comlib.add_widget(self.ids.champlibre)

    def createinput(self):


        self.ids.comlib.remove_widget(self.ids.champlibre)
        self.ids.comlib.add_widget(self.textinput)
        erase = ToggleButton(text='Supprimer ce champ libre', font_size='20sp')

        erase.bind(on_press=lambda x: self.deletecom(self.textinput,erase))
        self.ids.comlib.add_widget(erase)


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
        com=Coms()
        print (self.textinput.text)
        if self.listecom==["Sélection de commentaires"]:
            del self.listecom[0]
            self.box = BoxLayout(orientation='vertical')
            self.box.add_widget(
                Label(text='Valider sans laisser de commentaires?', font_size='20sp'))
            # size = ('500sp', '150sp')
            returncom = ToggleButton(text='Retour à la page Commentaires', font_size='20sp')
            nextpage = ToggleButton(text='Confirmer la validation', font_size='20sp')
            # size = ('480sp', '150sp'
            # box.add_widget(TextInput(text='Hi'))
            self.box.add_widget(returncom)
            self.box.add_widget(nextpage)
            self.popup = Popup(title='Aucun commentaire saisi', content=self.box, auto_dismiss=False)
            returncom.bind(on_release=self.popup.dismiss)
            nextpage.bind(on_release=lambda x:self.confirmcom(state,com))
            self.popup.open()
        else:
            sm.current="activity"
            sm.transition.direction="right"
            state.send_statement()
            self.a=[2]
            sm.get_screen("activity").ids.labid.text = "Bonjour"+" "+\
                                                           myparams.accounts[sm.get_screen("menu").ids.textid.text][
                                                               "name"]+"---"+str(self.listecom)
        print(self.listecom)

    def confirmcom(self,state,com):
        self.popup.dismiss()
        #state.send_activity()
        #state.send_identity()
        sm.current = "activity"
        sm.transition.direction = "right"
        state.send_statement()
        self.a=[2]
        sm.get_screen("activity").ids.labid.text="Bonjour"+" "+myparams.accounts[sm.get_screen("menu").ids.textid.text]["name"]\
                                                 +" "+"Pas de commentaires"


class Logout(Screen):
    pass


sm = ScreenManager(transition=SlideTransition())
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(myscreen(name='activity'))
sm.add_widget(Coms(name='com'))
sm.add_widget(Logout(name='deconnexion'))
sm.add_widget(QrScreen(name='qrscr'))

class Autostatement():
    def __init__(self, *args, **kwargs):
       # super(Autostatement, self).__init__(*args, **kwargs)
        self.actor_name = None
        #self.actor_mbox= None
        self.activity_name=None
        self.activity_note=None

        self.lrs = RemoteLRS(
            version=lrs_properties.version,
            endpoint=lrs_properties.endpoint,
            username=lrs_properties.username,
            password=lrs_properties.password,
        )
    # def send_identity(self):
    #     menu=MenuScreen()
    #     self.actor_name=menu.ids.textid.text
    #     #self.actor_mbox='mailto: namefirstname@tincanapi.com'
    #     #self.lrs.password=menu.ids.textmdp.text
    #     self.send_statement()
    # def send_activity(self):
    #     actscreen=myscreen()
    #     self.activity_name=actscreen.listactivity[0]
    #     self.activity_note=actscreen.listactivity[1]
    #     self.send_statement()

    def send_statement(self):

        actor = Agent(
            name=self.actor_name ,
            mbox='mailto: tincanpython@tincanapi.com',
        )
        verb = Verb(
            id='http://adlnet.gov/expapi/verbs/experienced',
            display=LanguageMap({'fr-FR': 'experimenté'}),
        )
        object = Activity(
            id='http://tincanapi.com/TinCanPython/Example/0',
            definition=ActivityDefinition(
                name=LanguageMap({'fr-FR': 'ok ca marche'}),
                description=LanguageMap({'en-US': 'Use of, or interaction with, the TinCanPython Library'}),
                #= self.activity_note,
            ),
        )
        statement = Statement(
            actor=actor,
            verb=verb,
            object=object,
        )
        #print(object.definition.name)
        # self.ids.mylabel.text="Notez l'activité sélectionnée"

        # self.ids.myspinner.text="Les activités"
        # self.ids.myspinner.values = myparams.activities.keys()
        # self.ids.lab2.text = myparams.activities.keys()[1]
        response = self.lrs.save_statement(statement)
        if not response:

            raise ValueError("statement failed to save")


class MonAppli(App):
    # qrscreen = None

    def build(self):
        return sm
    def qr_det(self):

        #sm.get_screen("qrscr").create_popup2()
        #sm.get_screen("qrscr").remove_widget(qrwidget)
        sm.current="menu"
        sm.transition.direction="right"
    def qr_detected(self, url):
        myparams.build_from_url2(url)
        #self.qr_detected("https://api.myjson.com/bins/gu4bz")
        # self.add_widget(box)

        # self.req = UrlRequest(qrwidget.ids.detector.Qrcode.data, studentsdata)


        # sm.current="menu"
        # sm.transition.direction="right"


if __name__ == "__main__":
    MonAppli().run()
