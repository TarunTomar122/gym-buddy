# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker, FormValidationAction, logger
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from datetime import datetime

import requests
import json
import os

from actions.workout import mainFunction


class ClearSlotValues(Action):

    def name(self) -> Text:
        return "action_clear_slot_values"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [AllSlotsReset()]


class StartWorkoutAction(Action):
    def name(self) -> Text:
        return "action_start_workout"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        reps = tracker.get_slot("reps")
        exercise = tracker.get_slot("exercise")

        print("values", reps, exercise)

        # os.system("python workout.py %s %s", reps, exercise)
        mainFunction(reps, exercise)

        dispatcher.utter_message(text="ok, let's start!")

        return []


class StartWorkoutValidation(FormValidationAction):

    def name(self) -> Text:
        return "validate_start_workout_form"

    def validate_reps(self, value, dispatcher, tracker, domain):

        return {"reps": value}

    def validate_exercise(self, value, dispatcher, tracker, domain):

        return {"exercise": value}
