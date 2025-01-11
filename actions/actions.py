# actions/actions.py
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionSaveIngredient(Action):
    def name(self) -> Text:
        return "action_save_ingredient"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extraer entidades
        ingrediente = tracker.get_slot("ingrediente") or ""
        marca = tracker.get_slot("marca") or ""
        cantidad = tracker.get_slot("number") or ""
        unidad = tracker.get_slot("unidad") or ""
        precio = tracker.get_slot("amount-of-money") or ""

        # Validar que los datos no estén vacíos
        if not ingrediente or not cantidad or not precio:
            dispatcher.utter_message(text="Faltan algunos datos del ingrediente. Por favor, ingresalos correctamente.")
            return []

        # Crear el payload para enviar a Django
        payload = {
            "nombre": ingrediente,
            "marca": marca,
            "cantidad": cantidad,
            "unidad": unidad,
            "precio": precio
        }

        # Ajusta la URL según tu API en PythonAnywhere
        django_url = "https://cynthiavillagra.pythonanywhere.com/api/chatbot/"

        # Realizar la solicitud POST
        try:
            response = requests.post(django_url, json=payload)

            if response.status_code == 201:
                dispatcher.utter_message(text="Ingrediente guardado exitosamente en Django (PythonAnywhere).")
            else:
                dispatcher.utter_message(
                    text=f"Ocurrió un error al guardar el ingrediente. Respuesta [{response.status_code}]: {response.text}"
                )

        except Exception as e:
            dispatcher.utter_message(text=f"Error de conexión al guardar ingrediente: {str(e)}")

        return []
