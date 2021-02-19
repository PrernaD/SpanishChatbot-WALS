# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import pandas as pd
import os

class ActionLanguageSearch(Action):

    def name(self) -> Text:
        return "action_lang_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
        wals_data = pd.read_csv(data_path)
        entities = list(tracker.get_latest_entity_values("language"))

        if len(entities) > 0:
            print("I have an entity")
            query_lang = entities.pop()
            query_lang = query_lang.lower().capitalize()
            print(query_lang)
            
            out_row = wals_data[wals_data["Name"] == query_lang].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                out_text = "El idioma  %s pertenece a la familia %s\n con genus %s\n y tiene código ISO %s" % (out_row["Name"], out_row["Family"], out_row["Genus"], out_row["ISO_codes"])
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "Lo sentimos, no tenemos registros para ese idioma. %s" % query_lang)
        else:
            dispatcher.utter_message(text="lo siento, no pude entender")

        return []

class ActionCountriesLanguageSearch(Action):

    def name(self) -> Text:
        return "action_countries_lang_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "language_country", "country_lang.csv")
        wals_data = pd.read_csv(data_path)
        entities = list(tracker.get_latest_entity_values("language"))
        wals_data['country'] = wals_data['country'].str.lower()
        if len(entities) > 0:
            print("I have an country entity")
            query_lang = entities.pop()
            query_lang = query_lang.lower()
            print(query_lang)
            
            out_row = wals_data[wals_data["country"] == query_lang].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                out_text = "Country %s have these languages %s\n" % (out_row["country"], out_row["language"])
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "Lo sentimos, no tenemos registros para ese idioma. %s" % query_lang)
        else:
            dispatcher.utter_message(text="lo siento, no pude entender")

        return []


class ActionTenseSearch(Action):

    def name(self) -> Text:
        return "action_tense_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "tense_csv", "tense.csv")
        wals_data = pd.read_csv(data_path)
        entities = list(tracker.get_latest_entity_values("language"))
        wals_data['infinitive'] = wals_data['infinitive'].str.lower() 
        if len(entities) > 0:
            print("I have an tense entity")
            query_lang = entities.pop()
            query_lang = query_lang.lower()
            print(query_lang)
            
            out_row = wals_data[wals_data["infinitive"] == query_lang].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                out_text = "Verb %s is of type %s\n" % (out_row["infinitive"], out_row["tense"])
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "Lo sentimos, no tenemos registros para ese idioma. %s" % query_lang)
        else:
            dispatcher.utter_message(text="lo siento, no pude entender")

        return []


class ActionGetPoliteness(Action):

    def name(self) -> Text:
        return "action_polite_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "polite", "pronouns_spanish.xlsm")
        wals_data = pd.read_excel(data_path)
        entities = list(tracker.get_latest_entity_values("language"))
        wals_data['English'] = wals_data['English'].str.lower()
        print(entities)
        if len(entities) > 0:
            print("I have an politeness entity")
            query_lang = entities.pop()
            query_lang = query_lang.lower()
            print(query_lang)
            
            out_row = wals_data[wals_data["English"] == query_lang].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                out_text = "Politeness of english %s in spanish is %s\n" % (out_row["English"], out_row["Spanish"])
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "Lo sentimos, no tenemos registros para ese idioma. %s" % query_lang)
        else:
            dispatcher.utter_message(text="lo siento, no pude entender")

        return []


class ActionLanguageCountriesSearch(Action):

    def name(self) -> Text:
        return "action_lang_countries_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "language_country", "country_lang.csv")
        wals_data = pd.read_csv(data_path)
        entities = list(tracker.get_latest_entity_values("language"))

        print(entities, 'lang_search')
        if len(entities) > 0:
            print("I have an language-country entity")
            query_lang = entities.pop()
            query_lang = query_lang.lower()
            print(query_lang)

            count = 0
            index = []
            for lang in wals_data['language'].values:
                if query_lang in lang.lower().strip().split(','):
                    index.append(count)
                count += 1


            temp = wals_data.iloc[index]


            out_row = temp

            if out_row.shape[0] > 0:
                separator = ', '
                temp = separator.join(list(out_row['country']))
                out_text = "Country %s have these languages %s\n" % (temp, query_lang)
                dispatcher.utter_message(text=out_text)
            else:
                dispatcher.utter_message(text="Lo sentimos, no tenemos registros para ese idioma. %s" % query_lang)
        else:
            dispatcher.utter_message(text="lo siento, no pude entender")

        return []