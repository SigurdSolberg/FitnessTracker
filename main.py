from gettext import translation
from functools import partial
from msilib.schema import Directory
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import Builder, MDApp, ObjectProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFloatingActionButton, MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.screenmanager import ScreenManager
from Modules import Workout, Set, Exercise, ExerciseSession
ScreenManager   
import pickle
import os

class ShowWorkoutWindow(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        
    def load_workout(self):
        try:
            self.remove_widget(self.session_list)
        except:
            pass
        self.session_list = MDList()
        for exercise, session in self.manager.buffer_workout.workout.items():
            self.session_list.add_widget(OneLineListItem(text = f'{exercise}: {len(session.sets)} sets'))
        self.add_widget(self.session_list)

class ShowExerciseWindow(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)

class HistoryWindow(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.workoutHistoryBtn = MDRectangleFlatButton(text= 'Previous Workouts', pos_hint = {'center_x': 0.5, 'center_y': 0.5}, 
                                                       on_press = self.workout_button)
        self.exercisesHistoryBtn = MDRectangleFlatButton(text= 'Exercises', pos_hint = {'center_x': 0.5, 'center_y': 0.4}, 
                                                       on_press = self.exercises_button)
        self.add_widget(self.workoutHistoryBtn)
        self.add_widget(self.exercisesHistoryBtn)
        
    def workout_button(self, _):
        self.manager.current = 'workout_history'
        self.manager.transition.direction = 'left'
        self.manager.get_screen('workout_history').load_workouts()
        
    def exercises_button(self, _):
        self.manager.current = 'exercises'
        self.manager.transition.direction = 'left'
        self.manager.get_screen('exercises').load_exercises()

class ExercisesWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.load_exercises()
        
    def load_exercises(self):
        try:
            self.remove_widget(self.exercisesList)
        except:
            pass
        self.exercises = [self.load_exercise(name) for name in os.listdir('Data/Exercises/')]
        exercisesList = MDList(pos_hint = {'center_x': 0.5, 'center_y':0.75})
        for i in self.exercises:
            exercisesList.add_widget(OneLineListItem(text = i[0].name))
        self.add_widget(exercisesList)
        
    def load_exercise(self, name):
        with open('Data/Exercises/' + name, 'rb') as outp:
            try: 
                return pickle.load(outp)    
            except:
                return 'Error'
        
class HomeWindow(Screen):
    pass

class WorkoutWindow(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.workout = Workout()
        
        self.workout_list = MDList()
        self.newSessionBtn = MDRectangleFlatButton(text= 'New Exercise', pos_hint= {'center_x': 0.5, 'center_y': 0.5}, 
                              on_press = self.new_session)
        
        self.backBtn = MDRectangleFlatButton(text= 'Back', pos_hint = {'center_x': 0.8, 'center_y': 0.9}, 
                              on_press = self.back)
        
        self.add_widget(self.newSessionBtn)
        self.add_widget(self.backBtn)
        self.add_widget(self.workout_list)
        
    def new_session(self, _):
        self.manager.current = 'exercise_session'
        self.manager.transition.direction = 'left'
         
    def add_session(self):
        exercise_session = self.manager.buffer_session
        if type(exercise_session) == ExerciseSession:
            self.workout.add_exercise(exercise_session)
            self.workout_list.add_widget(OneLineListItem(text = f'{exercise_session.name}: {len(exercise_session.sets)} sets'))
            print('Adding new session to the current workout')
    
    def back(self, _):
        self.manager.current = 'home'
        self.manager.transition.direction = 'right'
        
        if len(self.workout.workout) > 0:
            self.workout.save()
            
        self.clear_widgets()
        self.__init__()
             
    def remove_session(self):
        pass
        
class ExerciseSessionWindow(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.exercise_session = None
        self.exercise_name = None
        
        self.set_list = MDList(pos_hint = {'center_x': 0.5, 'top_y':0.8})
        self.backBtn = MDRectangleFlatButton(text= 'Back', pos_hint = {'center_x': 0.8, 'center_y': 0.7}, on_release = self.back)
        self.addSetBtn = MDRectangleFlatButton(text= 'Add', pos_hint = {'center_x': 0.5, 'center_y': 0.2}, on_release = self.add_set)
        self.name_textField = MDTextField(id= 'exercise_name', hint_text= 'Exercise', pos_hint= {'center_x': 0.5, 'center_y': 0.5}, 
                                          size_hint_x= None, width= 300)
        self.reps_textField = MDTextField(id = 'reps' , hint_text= 'Reps: ', pos_hint= {'center_x': 0.5, 'center_y': 0.4}, 
                                          size_hint_x= None, width= 300)
        self.weight_textField = MDTextField(id= 'weight', hint_text= 'Weight: ', pos_hint= {'center_x': 0.5, 'center_y': 0.3}, 
                                            size_hint_x= None,width= 300)
        
        self.add_widget(self.name_textField)
        self.add_widget(self.reps_textField)
        self.add_widget(self.weight_textField)
        self.add_widget(self.backBtn)
        self.add_widget(self.addSetBtn)
        self.add_widget(self.set_list)
        
    def back(self, _):
        self.manager.current = 'workout'
        self.manager.transition.direction = 'right'
        
        if self.exercise_name != 0:
            self.parent.buffer_session = self.exercise_session
            self.manager.get_screen('workout').add_session()
            self.clear_widgets()
            self.__init__()
                                
    def add_set(self, _):
        
        if self.exercise_name != None:
            if self.reps_textField.text != '':
                    if self.exercise_session == None:
                        self.exercise_session = ExerciseSession(self.exercise_name)
                        
                    new_set = Set(self.reps_textField.text, self.weight_textField.text)
                    self.exercise_session.add_set(new_set)
                    self.set_list.add_widget(OneLineListItem(text = new_set.reps + ' x ' + new_set.weight))
        else:
            if self.name_textField.text != '':
                if self.reps_textField.text != '':
                    if self.exercise_session == None:
                        self.exercise_name = self.name_textField.text
                        self.exercise_session = ExerciseSession(self.name_textField.text)
                        self.remove_widget(self.name_textField)
                        self.add_widget(MDLabel(text = self.exercise_name, pos_hint = {'center_x': 1, 'center_y':0.9}))
                    new_set = Set(self.reps_textField.text, self.weight_textField.text)
                    self.exercise_session.add_set(new_set)
                    self.set_list.add_widget(OneLineListItem(text = new_set.reps + ' x ' + new_set.weight))
            
class WorkoutHistoryWindow(Screen): 
    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.load_workouts()
        print(self.workouts)
    
    
    def load_workouts(self):
        with open('Data/Workouts', 'rb') as outp:
            try:
                self.workouts = pickle.load(outp)
            except:
                self.workouts = []
        try:
            self.remove_widget(self.list)
        except:
            pass
        
        self.list = MDList()
        for i in self.workouts:
            new_list_litem = OneLineListItem(text = i.date, on_release = partial(self.show_workout, i))
            self.list.add_widget(new_list_litem)
        
        self.add_widget(self.list)
        
    def show_workout(self, workout, _):
        self.manager.buffer_workout = workout
        self.manager.current = 'show_workout'
        self.manager.transition.direction = 'left'
        self.manager.get_screen('show_workout').load_workout()
        print('Showing workout: ', workout)
                             
class WindowManager(ScreenManager):
    screen_mngr = ObjectProperty(None)
    buffer_session = []
    buffer_workout = []
    
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