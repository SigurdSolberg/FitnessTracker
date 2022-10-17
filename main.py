from kivy.uix.floatlayout import FloatLayout
from kivymd.app import Builder, MDApp, ObjectProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFloatingActionButton, MDRectangleFlatButton
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.screenmanager import ScreenManager
ScreenManager   
import pickle
import os

class HistoryWindow(Screen):
    pass

class ExercisesWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.exercises = [self.load_exercise(name) for name in os.listdir('Data/Exercises')]
        
        list = MDList()
        for i in self.exercises:
            list.add_widget(OneLineListItem(text = i.name))
        
        list.add_widget(OneLineListItem(text = 'Pushups'))
        list.add_widget(OneLineListItem(text = 'Pullups'))
            
        self.add_widget(list)
        
    def load_exercise(self, name):
        with open('Data/' + name, 'rb') as outp:
            return pickle.load(outp)    

class HomeWindow(Screen):
    pass

class WorkoutWindow(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        
class ExerciseSession(Screen):
    pass

class WorkoutHistoryWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.workouts = self.load_workouts()
        
        list = MDList()
        for i in self.workouts:
            list.add_widget(OneLineListItem(text = i.date))
        
        list.add_widget(OneLineListItem(text = 'Pushups'))
        list.add_widget(OneLineListItem(text = 'Pullups'))
            
        self.add_widget(list)
    
        
    def load_workouts(self):
        with open('Data/Workouts', 'rb') as outp:
            try:
                return pickle.load(outp)
            except:
                return []

class WindowManager(ScreenManager):
    screen_mngr = ObjectProperty(None)
    

class App(MDApp):

    def build(self, name = 'FitnessTracker'):
        #self.theme_cls.theme_style = 'Dark'
        return Builder.load_file('Screens.kv')
        
    def start_btn(self, obj):
        print('You pressed the Start-button')
        self.build('hello')
        pass
    
    def history_btn(self, obj):
        print('You pressed the Workout History-button')
        pass