import string
import requests
from bs4 import BeautifulSoup
import whisper
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU")
warnings.simplefilter('ignore', InsecureRequestWarning)



green_color = '\033[92m'
red_color = '\033[91m'
warn_color = '\033[93m'
color_end = '\x1b[0m'
def colored_result(result):
    
    if result == "Result":
        return result
    elif result == 'PASS':
        result = f"{green_color}{result}{color_end}"
    elif result[0] == "W":
        result = f"{warn_color}{result}{color_end}"
    elif result == "U" or "RA":
        result = f"{red_color}{result}{color_end}"
    return result

def find_between(s, start, end):
    return s.split(start)[1].split(end)[0]

def transcriber():

    model = whisper.load_model("small")

    result = model.transcribe("downloaded_file.mp3",language="en")

    text = result["text"]
    # print("Extracted text :", text)
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)


    split_text =  text.strip().split()
    cap_text = [i.upper() for i in split_text]
    cap_text = [i.replace(".", "") for i in cap_text]
    num_in_str ={
        'ZERO': "0",
        'ONE': "1",
        'TWO': "2",
        'THREE': "3",
        'FOUR': "4",
        'FIVE': "5",
        'SIX': "6",
        'SEVEN': "7",
        'EIGHT': "8",
        'NINE': "9"
    }
    captcha = ""
    for i in range(0, len(split_text)):
        if cap_text[i] in num_in_str:
            captcha += num_in_str[cap_text[i]]
        if cap_text[i] == "FOR":
            if cap_text[i-1][0] == cap_text[i+1][0]:
                captcha += cap_text[i+1][0]
            elif cap_text[i+1][0] in cap_text[i-1]:
                captcha += cap_text[i+1][0]
        if cap_text[i].isnumeric():
            captcha += cap_text[i]
    # print("Generated captcha :",captcha)
    return captcha

def main(register_no,dob):
    print(register_no, dob)
    print("Fetching result started...")
    s = requests.Session()

    given_data = False
    while True:
        if len(dob) != 10 :
            print("Invalid Register number or Date of birth... ")
            break
         
        url = "http://coe1.annauniv.edu/home/index.php"
        html = s.get(url)

        # getting session token
        soup = BeautifulSoup(html.text, 'html.parser')
        box1, box= soup.find_all("div", {'class': 'box'})
        token = box1.find("input",{'id': "pagetoken"})
        req_token = token["value"]


        # getting captcha audio
        audio = box.find("audio", {"id": "captchademo2"})
        audio = audio.find("source")
        audio_link = audio["src"]
        audio_url = f"https://coe1.annauniv.edu/home/{audio_link}"
        audio_data = s.get(audio_url,verify=False)

        # saving captcha audio
        with open('downloaded_file.mp3', 'wb') as file:
            file.write(audio_data.content)


        # getting captcha

        capcha_string = transcriber()

        
        # # getting captcha image for debugging
        # img = box.find("img", {'class': 'small'})
        # img_link = img["src"].split(",")[-1]
        # img_byte = img_link.encode('utf-8')
        # imgdata = base64.b64decode(img_byte)

        # # saving captcha image
        # with open("current_captcha.png", 'wb') as f:
        #     f.write(imgdata)

        post_url = "http://coe1.annauniv.edu/home/students_corner.php"

        payload = {
            req_token : req_token,
            "register_no" : register_no,
            "dob" : dob,
            "security_code_student": capcha_string,
            "gos": "Login"
        }

        html = s.post(post_url, data=payload)
        try:
            msg = find_between(html.text, "alert(\"", "\");")
            if "Invalid Register number or Date of birth or Profile Not Found ... " in msg:
                print(f"{red_color}{msg}{color_end}")
                break
            else:
                print(f"{warn_color}Invalid captcha, Retrying...{color_end}")
        except:
            print(f"{green_color}Captcha is correct{color_end}")
            given_data = True
            break

    if given_data == False:
        return


    soup = BeautifulSoup(html.text, 'html.parser')
    form = soup.find('form', id='formExamResults')
    req_token = form.find('input')["name"]
                    
    payload = {
        req_token : req_token,
        "ExamResults": "", 
        "univ_reg_no": ""
    }
    html = s.post(post_url, data=payload)

    # print(html.text)
    soup = BeautifulSoup(html.text, 'html.parser')

    tables = soup.find_all('table', id='resulttable')
    name = find_between(html.text,"<td><strong>Name</strong></td>", "</td>").strip()[4:]
    all_results = []

    for table in tables:
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all('th')

            if len(cells) == 4: 
                semester = cells[0].get_text(strip=True)
                subject_code = cells[1].get_text(strip=True)
                grade = cells[2].get_text(strip=True)
                result = cells[3].get_text(strip=True)

                all_results.append({
                    'Semester': semester,
                    'Subject Code': subject_code,
                    'Grade': grade,
                    'Result': result
                })

    # Print the result
    print(f"{warn_color}{name}{color_end}")
    for result in all_results:
        print(f"Semester: {result['Semester']}, Subject Code: {result['Subject Code']}, "
              f"Grade: {result['Grade']}, Result: {colored_result(result['Result'])}")

register_no = input("Enter your register Number : ").strip()
dob = input("Enter your Date of Birth (DD-MM-YYYY) : ").strip()
main(register_no, dob)
input("Press Enter to exit...")
    






