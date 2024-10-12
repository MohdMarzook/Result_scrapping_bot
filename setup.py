import platform
import subprocess
import shutil
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU")
warnings.simplefilter('ignore', InsecureRequestWarning)

def install_dependences():
    print("Installing dependences from requirements.txt")
    command = subprocess.run(["pip", "install", '-r', "requirements.txt"])
    import whisper
    try:
        model = whisper.load_model("small")
        model.transcribe("downloaded_file.mp3",language="en")
    except:
        pass

    os_name = platform.system()
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        try:
            print("checking for ffmpeg is installed or not")
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            if result.returncode == 0:
                print("FFmpeg is installed.")
            else:
                print("FFmpeg is installed, but an error occurred while running it.")
                print(f"Error: {result.stderr}")
        except Exception as e:
            print(f"An error occurred while trying to run FFmpeg: {e}")
    else:
        print("Installing ffmpeg...")
        if os_name == "Windows":
            result = subprocess.run(['winget', 'install' ,'FFmpeg (Essentials Build)'], capture_output=True, text=True)
            if result.returncode == 0:
                print("ffmpeg is installed")
            else:
                print(result.returncode)
                print(result.stdout)
        elif os_name == "Linux":
            subprocess.run(['sudo', 'apt', 'update'], check=True)
            result = subprocess.run(['sudo', 'apt', 'install', 'ffmpeg', '-y'], check=True)        
            if result.returncode == 0:
                print("ffmpeg is installed")
            else:
                print(result.returncode)
                print(result.stdout)
        elif os_name == "Darwin":
            result = subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
            if result.returncode == 0:
                print("ffmpeg is installed")
            else:
                print(result.returncode)
                print(result.stdout)

install_dependences()

