from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime

class ActionTellTime(Action):
    def name(self) -> Text:
        return "action_hora"

    async def run(self, 
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #current_time = datetime.now().strftime("%H:%M")
        #hora = f"La hora actual es {current_time}"
        print("No lo sé")
        hora="No lo sé"
        dispatcher.utter_custom_message(text=hora)

        return []
