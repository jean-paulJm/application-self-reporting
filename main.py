import kivy
#kivy.require('1.9.10') # replace with your current kivy version !

from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
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

# Test du widget ToggleButton

racine = Builder.load_string('''
GridLayout:
    # Disposition des boutons sur une seule ligne
    rows: 1
    #pos_hint: {'center_x':0.5, 'center_y': 0.5}
    #Creation des boutons
    ToggleButton:
        text: 'Choix 1'
        group: 'Choix'
        size_hint: (None,None)
        size: (80,50)
    ToggleButton:
        text: 'Choix 2'
        group: 'Choix'
        size_hint: (None,None)
        size: (80,50)
    ToggleButton:
        text: 'Choix 3'
        group: 'Choix'
        size_hint: (None,None)
        size: (80,50)
''')
class builder(GridLayout):
    


class MonAppli(App):
    def build(self):
        return racine


MonAppli().run()
