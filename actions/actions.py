import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List

class ActionSaveIngredient(Action):
    def name(self) -> Text:
        return "action_save_ingredient"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ingrediente = tracker.get_slot("ingrediente")
        marca = tracker.get_slot("marca")
        number = tracker.get_slot("number")
        unidad = tracker.get_slot("unidad")
        amount = tracker.get_slot("amount-of-money")

        # Ajusta según tu lógica de parseo o validación
        # para evitar resultados extraños como 500000000000.07

        payload = {
            "ingrediente": ingrediente,
            "marca": marca,
            "cantidad": number,
            "unidad": unidad,
            "precio": amount
        }

        try:
            # EJEMPLO: Llamada a Django
            response = requests.post("http://localhost:8000/api/chatbot/ingrediente", json=payload)
            response.raise_for_status()

            # Respuesta exitosa
            dispatcher.utter_message(text="El ingrediente se guardó correctamente.")
        except requests.exceptions.RequestException as e:
            # Captura error
            dispatcher.utter_message(
                text=f"Ocurrió un error al guardar el ingrediente. {str(e)}"
            )

        return []
