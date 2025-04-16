import json
import datetime
import random # For simple varied responses

# -------------------------------------
# NLU Simulation Functions (Unchanged - Keep as they are)
# -------------------------------------

def get_dialogflow_nlu(text_input, needed_entities=None):
    """Simulates Dialogflow ES NLU."""
    print("... (Simulating Dialogflow NLU call)")
    # Basic intent detection based on keywords
    intent_name = "unknown"
    confidence = 0.5
    params = {}

    text_lower = text_input.lower()

    if any(w in text_lower for w in ["hi", "hello", "hey"]):
        intent_name = "greet"
        confidence = 0.95
    elif any(w in text_lower for w in ["bye", "goodbye", "see ya"]):
        intent_name = "goodbye"
        confidence = 0.95
    elif any(w in text_lower for w in ["book", "appointment", "schedule"]):
        intent_name = "book_appointment"
        confidence = 0.85
    elif any(w in text_lower for w in ["haircut", "coloring", "wash", "tomorrow", "pm", "am", "monday", "tuesday"]):
         intent_name = "provide_details" # Assume providing details if keywords present
         confidence = 0.80

    # Basic entity extraction simulation
    if "haircut" in text_lower or "cut" in text_lower:
        params["service_type"] = "haircut"
    elif "coloring" in text_lower:
        params["service_type"] = "coloring"
    elif "wash" in text_lower or "shampoo" in text_lower:
         params["service_type"] = "wash"

    if "tomorrow" in text_lower:
         # Crude simulation - real system handles dates robustly
         tomorrow_date = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
         params["date"] = f"{tomorrow_date}T00:00:00+00:00" # Example format
    # Add more crude date/time parsing if needed for simulation

    if "pm" in text_lower or "afternoon" in text_lower:
        params["time"] = "T14:00:00+00:00" # Simulate 2 PM
    elif "am" in text_lower or "morning" in text_lower:
        params["time"] = "T10:00:00+00:00" # Simulate 10 AM

    # Simulate prompting if needed (simplified)
    fulfillment_text = "Okay."
    all_required_present = True
    if needed_entities:
        missing = []
        if "service_type" not in params and "service_type" in needed_entities:
            missing.append("service type")
            all_required_present = False
        if "date" not in params and "date" in needed_entities:
             missing.append("date")
             all_required_present = False
        if "time" not in params and "time" in needed_entities:
             missing.append("time")
             all_required_present = False
        if missing:
            fulfillment_text = f"What {', '.join(missing)} would you like?"


    return {
      "queryResult": {
        "queryText": text_input,
        "parameters": params,
        "allRequiredParamsPresent": all_required_present,
        "fulfillmentText": fulfillment_text if intent_name not in ["greet", "goodbye"] else random.choice(["Hi there!", "Hello!"]),
        "intent": {"displayName": intent_name},
        "intentDetectionConfidence": confidence,
        "languageCode": "en"
      }
    }

def get_rasa_nlu(text_input):
    """Simulates Rasa NLU."""
    print("... (Simulating Rasa NLU call)")
    # Very basic simulation - real Rasa is much more sophisticated
    intent_name = "unknown"
    confidence = 0.5
    entities = []
    text_lower = text_input.lower()

    # Crude intent/entity mapping for simulation
    if any(w in text_lower for w in ["hi", "hello", "hey"]):
        intent_name = "greet"
        confidence = 0.95
    elif any(w in text_lower for w in ["bye", "goodbye", "see ya"]):
        intent_name = "goodbye"
        confidence = 0.95
    elif any(w in text_lower for w in ["book", "appointment", "schedule"]):
        intent_name = "book_appointment"
        confidence = 0.85
    elif any(w in text_lower for w in ["haircut", "coloring", "wash", "tomorrow", "pm", "am", "monday", "tuesday"]):
         intent_name = "provide_details" # Assume providing details if keywords present
         confidence = 0.80

    if "haircut" in text_lower: entities.append({"entity": "service_type", "value": "haircut"})
    if "coloring" in text_lower: entities.append({"entity": "service_type", "value": "coloring"})
    if "wash" in text_lower: entities.append({"entity": "service_type", "value": "wash"})
    if "tomorrow" in text_lower: entities.append({"entity": "date", "value": "tomorrow"}) # Raw value
    if "pm" in text_lower: entities.append({"entity": "time", "value": "pm"}) # Raw value
    if "am" in text_lower: entities.append({"entity": "time", "value": "am"}) # Raw value

    return {
        "text": text_input,
        "intent": {"name": intent_name, "confidence": confidence},
        "entities": entities
    }

def get_luis_nlu(text_input):
    """Simulates LUIS NLU."""
    print("... (Simulating LUIS NLU call)")
    # Very basic simulation
    top_intent = "None"
    score = 0.5
    entities = {}
    text_lower = text_input.lower()

    # Crude intent/entity mapping for simulation
    if any(w in text_lower for w in ["hi", "hello", "hey"]):
        top_intent = "Greet"
        score = 0.95
    elif any(w in text_lower for w in ["bye", "goodbye", "see ya"]):
        top_intent = "Goodbye"
        score = 0.95
    elif any(w in text_lower for w in ["book", "appointment", "schedule"]):
        top_intent = "BookAppointment"
        score = 0.85
    elif any(w in text_lower for w in ["haircut", "coloring", "wash", "tomorrow", "pm", "am", "monday", "tuesday"]):
         top_intent = "ProvideDetails" # Assume providing details if keywords present
         score = 0.80

    service_type = None
    if "haircut" in text_lower: service_type = "Haircut"
    if "coloring" in text_lower: service_type = "Coloring"
    if "wash" in text_lower: service_type = "Wash"
    if service_type:
        entities["ServiceType"] = [{"normalizedValue": service_type}] # LUIS structure

    datetime_val = None
    if "tomorrow" in text_lower and "pm" in text_lower:
        # Very crude simulation of datetimeV2 resolution
        tomorrow_date = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
        datetime_val = f"{tomorrow_date}T14:00:00" # Example 2 PM tomorrow
    if datetime_val:
         entities["datetimeV2"] = [{"type": "datetime", "values": [{"timex": datetime_val, "resolution": [{"value": datetime_val}]}]}]

    return {
        "query": text_input,
        "prediction": {
            "topIntent": top_intent,
            "intents": {top_intent: {"score": score}},
            "entities": entities
        }
    }

def get_openai_nlu(text_input):
    """Simulates OpenAI Prompt-based NLU."""
    print("... (Simulating OpenAI NLU call)")
    # Very basic simulation based on keywords
    intent = "unknown"
    entities = {}
    text_lower = text_input.lower()

    if any(w in text_lower for w in ["hi", "hello", "hey"]): intent = "greet"
    elif any(w in text_lower for w in ["bye", "goodbye", "see ya"]): intent = "goodbye"
    elif any(w in text_lower for w in ["book", "appointment", "schedule"]): intent = "book_appointment"
    elif any(w in text_lower for w in ["haircut", "coloring", "wash", "tomorrow", "pm", "am", "monday", "tuesday"]): intent = "provide_details"

    if "haircut" in text_lower: entities["service_type"] = "haircut"
    if "coloring" in text_lower: entities["service_type"] = "coloring"
    if "wash" in text_lower: entities["service_type"] = "wash"
    if "tomorrow" in text_lower: entities["date"] = "tomorrow" # Raw
    if "pm" in text_lower: entities["time"] = "pm" # Raw
    if "am" in text_lower: entities["time"] = "am" # Raw

    # Simulate the JSON structure we would *expect* back from the LLM
    return {
        "intent": intent,
        "entities": entities
    }

# -------------------------------------
# Basic Chatbot Logic
# -------------------------------------

# Store collected information (simple state) - GLOBAL
conversation_context = {
    "service_type": None,
    "date": None,
    "time": None,
    "booking_pending": False # Flag to indicate we are in the booking process
}

def extract_entities_from_dialogflow(df_result):
    """Helper to get entities from the simulated Dialogflow result."""
    params = df_result.get("queryResult", {}).get("parameters", {})
    return {
        "service_type": params.get("service_type"),
        "date": params.get("date"), # Might need further parsing in real life
        "time": params.get("time") # Might need further parsing in real life
    }

def run_chatbot():
    """Main chatbot loop."""
    # --- ADD THIS LINE ---
    global conversation_context
    # --- END OF ADDITION ---

    print("Chatbot: Hello! How can I help you book a haircut appointment today?")
    print("Chatbot: (You can type 'quit' to exit)")

    last_bot_response = "" # Keep track of the last response for 'yes' check

    while True:
        user_message = input("You: ")
        if user_message.lower() == 'quit':
            print("Chatbot: Okay, goodbye!")
            break

        # --- NLU Phase (Simulated) ---
        print("\n--- NLU Analysis (Simulated) ---")
        # Decide which entities are currently needed if we are booking
        needed = []
        if conversation_context["booking_pending"]: # Now correctly reads global
             if not conversation_context["service_type"]: needed.append("service_type")
             if not conversation_context["date"]: needed.append("date")
             if not conversation_context["time"]: needed.append("time")

        df_nlu = get_dialogflow_nlu(user_message, needed if needed else None)
        rasa_nlu = get_rasa_nlu(user_message)
        luis_nlu = get_luis_nlu(user_message)
        openai_nlu = get_openai_nlu(user_message)

        # Display simulated NLU results for comparison
        print("\n--- [Dialogflow NLU Result (Simulated)] ---")
        print(json.dumps(df_nlu, indent=2))
        # print("\n--- [Rasa NLU Result (Simulated)] ---")
        # print(json.dumps(rasa_nlu, indent=2))
        # print("\n--- [LUIS NLU Result (Simulated)] ---")
        # print(json.dumps(luis_nlu, indent=2))
        # print("\n--- [OpenAI NLU Result (Simulated)] ---")
        # print(json.dumps(openai_nlu, indent=2))
        print("\n------------------------------------\n")


        # --- Dialogue Management & Response Generation ---
        # Using Dialogflow's simulated result to drive the logic primarily

        intent = df_nlu["queryResult"]["intent"]["displayName"]
        entities = extract_entities_from_dialogflow(df_nlu)

        bot_response = "Chatbot: Sorry, I didn't quite understand that. Can you rephrase?" # Default fallback

        # Handle simple 'yes' confirmation *before* main intent logic if applicable
        if user_message.lower() == 'yes' and "Is that correct?" in last_bot_response:
             bot_response = "Chatbot: Great! Your appointment is confirmed. See you then!"
             # Reset context fully - This assignment now correctly modifies the global
             conversation_context = {"service_type": None, "date": None, "time": None, "booking_pending": False}

        elif intent == "greet":
            bot_response = "Chatbot: " + random.choice(["Hello!", "Hi there!", "Good day!"])
        elif intent == "goodbye":
            bot_response = "Chatbot: " + random.choice(["Goodbye!", "See you later!", "Have a great day!"])
            print(bot_response)
            break # End conversation
        elif intent == "book_appointment" or intent == "provide_details" or conversation_context["booking_pending"]:
            conversation_context["booking_pending"] = True # Enter/stay in booking mode

            # Update context with newly found entities
            if entities.get("service_type") and not conversation_context["service_type"]:
                conversation_context["service_type"] = entities["service_type"]
            if entities.get("date") and not conversation_context["date"]:
                conversation_context["date"] = entities["date"] # Store raw/simulated value
            if entities.get("time") and not conversation_context["time"]:
                 conversation_context["time"] = entities["time"] # Store raw/simulated value

            # Check if all required details are collected
            if conversation_context["service_type"] and conversation_context["date"] and conversation_context["time"]:
                # All details present - Confirm (simulation)
                svc = conversation_context['service_type']
                # Crude extraction - better parsing needed in real bot
                d = conversation_context['date'].split('T')[0] if conversation_context['date'] else 'unknown date'
                t = conversation_context['time'].split('T')[1].split('+')[0][:-3] if conversation_context['time'] else 'unknown time'
                bot_response = f"Chatbot: Okay, I have booked a {svc} for you on {d} at {t}. Is that correct? (Type 'yes' to confirm)"
                # Don't reset context here yet, wait for confirmation
            else:
                # Ask for missing information (using Dialogflow's simulated prompt)
                bot_response = "Chatbot: " + df_nlu["queryResult"]["fulfillmentText"]

        # (Keep the default fallback response if no other condition matched)

        print(bot_response)
        last_bot_response = bot_response # Store the response for the next loop iteration


# --- Main Execution ---
if __name__ == "__main__":
    run_chatbot()