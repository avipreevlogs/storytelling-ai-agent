import os
import pickle
import pyttsx3
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip
from datetime import datetime
import googleapiclient.discovery

def get_youtube_service():
    with open("token.pickle", "rb") as f:
        credentials = pickle.load(f)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    return youtube

def generate_story():
    story = """
    यह कहानी है एक छोटे से गाँव की... 
    जहाँ रात को पेड़ों से अजीब आवाज़ें आती थीं।
    लोग कहते थे वहाँ कोई अनजान शक्ति रहती है।
    लेकिन एक दिन, सच सामने आया और सब हैरान रह गए...
    """
    return story.strip()

def create_voiceover(text, output_audio="voiceover.mp3"):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 0.9)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.save_to_file(text, output_audio)
    engine.runAndWait()
    return output_audio

def create_video_with_audio(story_text, audio_file, output_file="story.mp4"):
    image_path = "background.jpg"
    if not os.path.exists(image_path):
        from PIL import Image
        img = Image.new("RGB", (1280, 720), color=(20, 20, 20))
        img.save(image_path)

    audio_clip = AudioFileClip(audio_file)
    img_clip = ImageClip(image_path).set_duration(audio_clip.duration).set_audio(audio_clip)

    txt_clip = TextClip(story_text, fontsize=40, color='white', font="Arial-Bold", size=(1200, None), method="caption")
    txt_clip = txt_clip.set_position(("center", "bottom")).set_duration(audio_clip.duration)

    final_mix = CompositeVideoClip([img_clip, txt_clip]).set_audio(audio_clip)
    final_mix.write_videofile(output_file, fps=24)
    return output_file

def upload_video(youtube, file_path, title, description, tags=None, category="22", privacy="public"):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or [],
                "categoryId": category
            },
            "status": {
                "privacyStatus": privacy
            }
        },
        media_body=file_path
    )
    response = request.execute()
    print("✅ Uploaded:", response["id"])

if __name__ == "__main__":
    print("🚀 Starting Storytelling Automation...")

    story = generate_story()
    print("📖 Story Generated!")

    audio_file = create_voiceover(story)
    print("🎙 Voiceover Created:", audio_file)

    video_file = create_video_with_audio(story, audio_file)
    print("🎬 Video Created:", video_file)

    youtube = get_youtube_service()
    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    title = f"रहस्यमयी कहानी | Hindi Suspense Story | {today}"
    description = f"""{story}

🔥 रहस्यमयी हिंदी कहानियाँ | Thriller | Suspense | Horror
👉 रोज़ नई कहानी देखने के लिए Subscribe करें!

#HindiStory #Thriller #Suspense #Storytelling #HorrorStories
"""
    tags = ["Hindi Story", "Thriller", "Suspense", "Horror Story", "Storytelling"]

    upload_video(
        youtube,
        video_file,
        title=title,
        description=description,
        tags=tags,
        privacy="public"
    )
