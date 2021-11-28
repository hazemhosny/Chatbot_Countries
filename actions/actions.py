from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

import requests

# get country database through GET method API
response = requests.get('https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCountries')
# check for errors in connection
if response.status_code != 200:
    raise RuntimeError("Something bad happened, Please check the server.")
country_db_json = response.json()
country_db = country_db_json['body']

def get_capital(country_name):
    """ get capital given the country name through POST method API """
    url = 'https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCapital'
    data_ = {"country": country_name}
    r = requests.post(url=url, json=data_)
    # check for errors in connection
    if response.status_code != 200:
        raise RuntimeError("Something bad happened, Please check the server.")
    data = r.json()
    success = data['success']
    body = data['body']
    return success, body

def get_population(country_name):
    """ get population given the country name through POST method API """
    url = 'https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getPopulation'
    data_ = {"country": country_name}
    r = requests.post(url=url, json=data_)
    # check for errors in connection
    if response.status_code != 200:
        raise RuntimeError("Something bad happened, Please check the server.")
    data = r.json()
    success = data['success']
    body = data['body']
    return success, body

class ValidateCountryForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_country_form"
    
    def validate_country(self, slot_value: Text, dispatcher: CollectingDispatcher,
                         tracker: Tracker, domain: DomainDict,) -> Dict[Text, Any]:
        """ Validate country name value """
        
        # preprocess all words except USA to handle unexpected text
        if slot_value != 'USA':
            slot_value = slot_value.capitalize()
        # validate slot to be in the country databsae    
        if slot_value not in country_db:
            msg = f"please enter a valid country, here is a list of valid countries\n{country_db}"
            dispatcher.utter_message(text=msg)
            return {"country": None}
        # confirm country is available, and add to slot 
        dispatcher.utter_message(text=f"OK! You want to know about {slot_value}.")
        return {"country": slot_value}

class ActionDisplayCountries(Action):

    def name(self) -> Text:
        return "action_display_countries"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """ Display all valid countries """
        msg = f"here is a list of valid countries\n{country_db}"
        dispatcher.utter_message(text=msg)
        return [SlotSet("country", None)]

class ActionInformCapital(Action):

    def name(self) -> Text:
        return "action_inform_capital_pop"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_country = tracker.get_slot("country")
        # check that slot is not None
        if not current_country:
            msg = f"I didn't get it. Here is a list of valid countries.\n{country_db}"
            dispatcher.utter_message(text=msg)
            return []
        # preprocess all words except USA to handle unexpected text
        if current_country != 'USA':
            current_country = current_country.capitalize()
        # get latest intent to perform different functions
        current_intent = tracker.latest_message['intent'].get('name')

        if current_intent == 'request_capital':
            success, body = get_capital(current_country)
            # check if the slot 'country' within the valid countries
            if not success:
                msg = f"{body} Make sure you spelled it correctly.\n{country_db}"
                dispatcher.utter_message(text=msg)
                return []
            # get and utter the capital of country
            capital = body['capital']
            msg = f"{capital} is the capital of {current_country}."
            dispatcher.utter_message(text=msg)
            return []
        
        elif current_intent == 'request_population':
            success, body = get_population(current_country)
            # check if the slot 'country' within the valid countries
            if not success:
                msg = f"{body} Make sure you spelled it correctly.\n{country_db}"
                dispatcher.utter_message(text=msg)
                return []
            # get and utter the population of country
            population = body['population']
            msg = f"There is {population} in {current_country}."
            dispatcher.utter_message(text=msg)
            return []

        elif current_intent == 'inform_country_only':
            """ In case given country only, utter both capital and population """
            success, body_cap = get_capital(current_country)
            # check if the slot 'country' within the valid countries
            if not success:
                msg = f"{body_cap} Make sure you spelled it correctly.\n{country_db}."
                dispatcher.utter_message(text=msg)
                return []
        
            capital = body_cap['capital']   # get the capital of country
            _, body_pop = get_population(current_country)   # get the population of country
            population = body_pop['population']
            # utter the capital and population of country
            msg = f"{capital} is the capital of {current_country} with a population of {population}."
            dispatcher.utter_message(text=msg)
            return []
            