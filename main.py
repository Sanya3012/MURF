import flet as ft
import requests
import os
from murf import Murf
from api_key import API_KEY
import time

# creating api client
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

#building flet
def main(page: ft.Page):
    page.title="AI FriendZone"
    page.padding=40
    page.bgcolor="#1E1E2F"

    #create the ui widgets
    title = ft.Text("AI FriendZone", size=42, weight=ft.FontWeight.BOLD,color="#FFD700")

    text_input=ft.TextField(
        label="ENTER SOME TEXT HERE...",
        width=350,
        bgcolor="#2A2A3B",
        color="#ffffff",
        border_radius=15,
        border_color="#FFD700"
    )
    voice_selection = ft.Dropdown(
        label="Choose Voice",
        options=[ft.dropdown.Option(voice) for voice in VOICE_MOODS.keys()],
        width=350,
        bgcolor="#2A2A3B",
        color="#ffffff",
        value="Miles"
    )





# run the app
if __name__ =="__main__":
    ft.app(target=main, assets_dir=".")
