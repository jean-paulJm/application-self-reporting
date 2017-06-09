#kivy.require('1.9.10') # replace with your current kivy version !
from kivy.uix.gridlayout import GridLayout
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

'''class draw(BoxLayout):
    def build(self):
        city = BoxLayout(orientation='vertical')
        cities = ('Bruxelles', 'Gent', 'Namur')
        self.title = ('Tableau de bord')
        city.add_widget(Label(text='Exercices'))
        city.add_widget(Spinner(values=cities))
        return c

class MainApp(App):

    def build(self):
        game=draw()

        game.build

        return city

if __name__ == '__main__':
    MainApp().run()
'''
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.label import Label

# Test du widget ToggleButton

Builder.load_string('''
<myscreen>:
    # Disposition des boutons sur une seule ligne
    rows: 1
    pos_hint: {'x':0.0, 'y': 0.0}
    #Creation des boutons
    ToggleButton:
        text: 'Choix 1'
        group: 'Choix'
        size_hint: (None,None)
        on_press:root.send_statement()
        size: (80,50)
    ToggleButton:
        text: 'Choix 2'
        group: 'Choix'
        size_hint: (None,None)
        size: (80,50)
        #on_press: root.send_statement()
    ToggleButton:
        text: 'Choix 3'
        group: 'Choix'
        size_hint: (None,None)
        size: (80,50)
        #on_press:root.send_statement()
    Label:
        id: mylabel
        font_size:15
        pos_hint: {'y': 0.1, 'x': 0.4}
        text: ""
    
''')

class myscreen(GridLayout):
    def __init__(self,*args, **kwargs):
        super(myscreen, self).__init__(*args, **kwargs)
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
        #self.label = Label(text="Saving the Statements")
        #self.ToggleButton(text="Saving the Statements")
        self.ids.mylabel.text="Bienvenue dans l'activite numero 2"

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








class MonAppli(App):
    def build(self):
        ms = myscreen()
        return ms

if __name__=="__main__":
    MonAppli().run()
