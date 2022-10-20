import pickle
from datetime import datetime, date

class Exercise():

    name: str
    pr: float
    pr_goal: float

    def __init__(self, name):
        self.name = name

    def add_exercise_session():
        pass

    def get_history():
        pass

    def save(self):
        file_path = 'Data/' + self.name
        with open(file_path, 'wb') as outp:  # Overwrites any existing file.
            pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)


class ExerciseSession():

    """
        Summarizes all work on one spesific exersice during a workout. Consists of a list of Set. 
    """

    name: str

    def __init__(self, name):
        self.name = name
        self.sets = []

    def add_set(self, set):
        self.sets.append(set)


class Workout():

    """
        Summarizes a workout. Consists of a set of ExerciseSessions, representing all exercises and the effort in each of them.
    """

    def __init__(self):
        self.workout = {}
        self.date = datetime.now().strftime('%B %d, %Y - %H:%M')     #Set date

    def add_exercise(self, session: ExerciseSession):
        self.workout[session.name] = session

    def save(self):
        file_path = 'Data/Workouts'
        workouts = self.load_workouts()
        print(workouts)
        workouts.append(self)
        with open(file_path, 'wb') as outp:  # Overwrites any existing file.
            pickle.dump(workouts, outp, pickle.HIGHEST_PROTOCOL)

    def load_workouts(self):
        with open('Data/Workouts', 'rb') as outp:
            try:
                return pickle.load(outp)
            except:
                return []
class Set():

    """
        Representation of a single set of an exercise. 
    """

    def __init__(self, reps, weight):
        self.reps = reps
        self.weight = 'NO WEIGHT' if weight == '' else weight