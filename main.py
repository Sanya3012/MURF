import flet as ft
import requests
import os
import uuid
from murf import Murf
from api_key import API_KEY
# import time

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
    },
      "Alicia" : {
        "voice_id" : "en-US-alicia",
        "moods" :  ['Conversational', 'Angry', 'Calm']
    },
     "Theo" : {
        "voice_id" : "en-UK-theo",
        "moods" :  ['Narration', 'Promo', 'Calm', 'Sad','Angry','Character']
    },
      "Edmund" : {
        "voice_id" : "en-US-edmund",
        "moods" :  ['Conversational','Promo', 'Sports Commentary', 'Sad','Inspirational','NewsCast']
    }
}

#building flet
def main(page: ft.Page):
    page.title="Smart Voice Synthesizer"
    page.padding=40
    page.bgcolor="#1E1E2F"

    #create the ui widgets
    title = ft.Text("Smart Voice Synthesizer", size=42, weight=ft.FontWeight.BOLD,color="#FFD700")

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

    mood_selection = ft.Dropdown(
        label="Choose Mood",
        width=350,
        bgcolor="#2A2A3B",
        color="#ffffff"
    )
    
    def update_moods(e=None):
        selected_voice = voice_selection.value
        mood_selection.options = [
            ft.dropdown.Option(mood) for mood in VOICE_MOODS.get(selected_voice, {}).get("moods", [])
        ]
        mood_selection.value = mood_selection.options[0].text if mood_selection.options else None
        page.update()
        
    voice_selection.on_change = update_moods
    update_moods()
        
    voice_speed = ft.Slider(
        min=-30, max=30, value=0, divisions=10, label="{value}%", active_color="#FFD700"
    )
    
    # Generate AI Voice
    def generate_audio():
        selected_voice = voice_selection.value 
        voice_id = VOICE_MOODS.get(selected_voice, {}).get("voice_id")
        
        if not text_input.value.strip():
            print("ERROR: You need to enter some text.")
            return None
        
        try:
            response = client.text_to_speech.generate(
                format="MP3",
                sample_rate=48000.0,
                channel_type="STEREO",
                text=text_input.value,
                voice_id=voice_id,
                style=mood_selection.value,
                pitch=voice_speed.value
            )
            return response.audio_file if hasattr(response, "audio_file") else None 
        except Exception as e:
            print(f"Error: {e}")
            return None 
        
    def save_and_play(e):
        audio_url = generate_audio()
        if not audio_url:
            print("Error: No audio returned.")
            return 
        
        try:
            response = requests.get(audio_url, stream=True)
            if response.status_code == 200:
                file_path = os.path.abspath("audio.mp3")
                
                # Remove the existing file if it exists
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                        
                print("Audio Saved As:", file_path)
                
                # Play the audio
                page.overlay.clear()
                page.overlay.append(ft.Audio(src="audio.mp3", autoplay=True))
                page.update()
            else:
                print("Failed to download audio.")
        except Exception as e:
            print("ERROR:", e)
    
    # Button to generate voice
    btn_enter = ft.ElevatedButton(
        "Generate Voice",
        bgcolor="#FFD700",
        color="#1E1E2F",
        on_click=save_and_play,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))
    )
  
    # Build a UI Container
    input_container = ft.Container(
        content=ft.Column(
            controls=[ text_input, voice_selection, mood_selection,
                      ft.Text("Adjust Pitch", size=18, weight=ft.FontWeight.BOLD, color="#FF8800"),
                      voice_speed, btn_enter],
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=20,
        border_radius=20,
        bgcolor="#000000",
        shadow=ft.BoxShadow(blur_radius=12, spread_radius=2, color="#FF8800")   
    )
    
    page.add(
        ft.Column(
            controls=[title, input_container],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()

# run the app
if __name__ =="__main__":
    ft.app(target=main, assets_dir=".")
