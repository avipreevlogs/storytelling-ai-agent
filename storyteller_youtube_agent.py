import os
import sys
import subprocess
import shutil
import logging
from pathlib import Path
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Optional: Load env vars
# from dotenv import load_dotenv
# load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Initialize OpenAI LLM for the agent
llm = OpenAI(temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY", "MISSING_KEY"))

def detect_ffmpeg():
    """Tool: Detect FFmpeg."""
    ffmpeg_path = Path("ffmpeg.exe")
    if ffmpeg_path.exists():
        return str(ffmpeg_path)
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg
    raise FileNotFoundError("FFmpeg not found.")

def generate_hindi_story(prompt):
    """Tool: Generate suspense-thriller Hindi story with outputs."""
    if os.getenv("OPENAI_API_KEY") == "MISSING_KEY":
        return "Error: OpenAI API key not set."
    
    full_prompt = f"""
    {prompt}
    Generate a new suspense-thriller Hindi story in Three-Act Structure with emotions (fear, thrill, etc.).
    Include: Story, YouTube Title, Description, Hashtags, CTA.
    """
    chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(full_prompt))
    return chain.run({})

def add_background_music(video_path, music_path, output_path):
    """Tool: Add music to video using FFmpeg."""
    ffmpeg_path = detect_ffmpeg()
    if not Path(video_path).exists() or not Path(music_path).exists():
        return f"Error: Files not found - {video_path} or {music_path}."
    
    cmd = [ffmpeg_path, "-i", video_path, "-i", music_path, "-c:v", "copy", "-c:a", "aac", "-shortest", output_path]
    try:
        subprocess.run(cmd, check=True)
        return f"Video with music created: {output_path}"
    except subprocess.CalledProcessError as e:
        return f"FFmpeg error: {e}"

def upload_to_youtube(video_path):
    """Tool: Upload to YouTube (placeholder)."""
    if os.getenv("CLIENT_SECRET_JSON") == "MISSING_SECRET":
        return "Error: Google Client Secret not set."
    # Placeholder: Implement with google-api-python-client
    return f"Uploaded {video_path} to YouTube (placeholder)."

# Define tools for the agent
tools = [
    Tool(name="DetectFFmpeg", func=detect_ffmpeg, description="Detect FFmpeg executable."),
    Tool(name="GenerateStory", func=generate_hindi_story, description="Generate a suspense-thriller Hindi story with YouTube outputs."),
    Tool(name="AddMusic", func=add_background_music, description="Add background music to a video."),
    Tool(name="UploadYouTube", func=upload_to_youtube, description="Upload video to YouTube."),
]

# Initialize the agent
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

def main():
    logging.info("=== AI Storytelling Agent ===")
    logging.info("Agent is ready. Type commands like 'Generate a new story' or 'Process video with music'.")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            logging.info("Agent shutting down.")
            break
        
        try:
            response = agent.run(user_input)
            print(f"Agent: {response}")
        except Exception as e:
            logging.error(f"Agent error: {e}")

if __name__ == "__main__":
    main()
