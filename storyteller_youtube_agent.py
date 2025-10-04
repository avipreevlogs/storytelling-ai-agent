import os
import pickle
from googleapiclient.discovery import build
from moviepy.editor import TextClip, concatenate_videoclips

def create_video():
    clip = TextClip("यह एक डेमो कहानी वीडियो है", fontsize=70, color='white', size=(1280,720))
    clip = clip.set_duration(10)
    clip.write_videofile("output.mp4", fps=24)

def upload_video(file):
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)
    youtube = build("youtube", "v3", credentials=creds)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": "Auto Storytelling Video",
            "description": "Generated and uploaded automatically.",
            "tags": ["storytelling","AI","YouTube Automation"]
          },
          "status": {"privacyStatus": "private"}
        },
        media_body=file
    )
    response = request.execute()
    print("✅ Uploaded:", response.get("id"))

if __name__ == "__main__":
    create_video()
    upload_video("output.mp4")
