import flet as ft
import requests
import os
from murf import Murf
from api_key import API_KEY
import time

#api client
client =Murf(api_key=API_KEY)


voices=client.text_to_speech.get_voices()

# for voice in voices:
#     print(f"Voice ID: {voice.voice_id}, Name: {voice.display_name}, Moods: {voice.available_styles}")


#voice setting
VOICE_MOODS ={
    "Miles" :{
        "voice_id" : "en-US-miles",
        "moods": ['Conversational', 'Promo', 'Sports Commentary', 'Narration', 'Newscast', 'Sad', 'Angry', 'Calm', 'Terrified', 'Inspirational', 'Pirate', 'Customer Support Agent']
    },
    "Shane" : {
        "voice_id" : "en-AU-shane",
        "moods": ['Conversational','Narration']
    },
    "Natalie" : {
        "voice_id" : "en-US-natalie",
        "moods": ['Promo', 'Narration', 'Newscast Formal', 'Meditative', 'Sad', 'Angry', 'Conversational', 'Newscast Casual', 'Furious', 'Sorrowful', 'Terrified', 'Inspirational']
    }
}
