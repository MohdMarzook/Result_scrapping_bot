import platform
import subprocess
import shutil
import whisper

# Get the OS name

try:
    model = whisper.load_model("small")
    result = model.transcribe("downloaded_file.mp3",language="en")
except:
    pass

# os_name = platform.system()
# ffmpeg_path = shutil.which('ffmpeg')
# if ffmpeg_path:
#     try:
#         print("checking for ffmpeg is installed or not")
#         result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
#         if result.returncode == 0:
#             print("FFmpeg is installed.")
#         else:
#             print("FFmpeg is installed, but an error occurred while running it.")
#             print(f"Error: {result.stderr}")
#     except Exception as e:
#         print(f"An error occurred while trying to run FFmpeg: {e}")
# else:
#     print("Installing ffmpeg...")
#     if os_name == "Windows":
#         result = subprocess.run(['winget', 'install' ,'FFmpeg (Essentials Build)'], capture_output=True, text=True)
#         if result.returncode == 0:
#             print("ffmpeg is installed")
#         else:
#             print(result.returncode)
#             print(result.stdout)
#     elif os_name == "Linux":
#         subprocess.run(['sudo', 'apt', 'update'], check=True)
#         result = subprocess.run(['sudo', 'apt', 'install', 'ffmpeg', '-y'], check=True)        
#         if result.returncode == 0:
#             print("ffmpeg is installed")
#         else:
#             print(result.returncode)
#             print(result.stdout)
#     elif os_name == "Darwin":
#         result = subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
#         if result.returncode == 0:
#             print("ffmpeg is installed")
#         else:
#             print(result.returncode)
#             print(result.stdout)

