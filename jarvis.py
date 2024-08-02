import pyttsx3
import speech_recognition as sr  
import datetime
import wikipedia  
import webbrowser
import os
import smtplib
import pywhatkit  
import pyautogui  
import requests 
import openai  

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

NEWS_API_KEY = '1234567890abcdef1234567890abcdef'
OPENAI_API_KEY = 'sk-dev-KI0wYAQ8RUk6N9DNPCryT3BlbkFJQVvBpcmZXyP4BqIpd3V1'  

openai.api_key = OPENAI_API_KEY

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Hello Dev sir, I am Jarvis. Please tell me how may I help you")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('devendrarahire20@gmail.com', 'Devendra@20')
        server.sendmail('devendrarahire20@gmail.com', to, content)
        server.close()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def takeScreenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    speak("Screenshot has been taken and saved.")

def calculate(expression):
    try:
        result = eval(expression)
        speak(f"The result is {result}")
        print(f"The result is {result}")
    except Exception as e:
        speak("Sorry, I couldn't calculate that.")
        print(f"Error: {e}")

def getNews():
    try:
        url = f'http://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        news_data = response.json()
        articles = news_data['articles']
        top_articles = articles[:10]
        headlines = [article['title'] for article in top_articles]

        speak("Here are the top 10 news headlines for today:")
        for i, headline in enumerate(headlines, 1):
            speak(f"{i}. {headline}")
            print(f"{i}. {headline}")
    except Exception as e:
        speak("Sorry, I couldn't fetch the news.")
        print(f"Error: {e}")

def answerQuestion(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message['content'].strip()
        speak(answer)
        print(answer)
    except Exception as e:
        speak("Sorry, I couldn't get an answer to your question.")
        print(f"Error: {e}")

def converse():
    context = []
    while True:
        speak("You can ask me anything or say 'exit' to end the conversation.")
        user_input = takeCommand().lower()
        if 'exit' in user_input:
            speak("Ending conversation. Have a nice day!")
            break
        context.append({"role": "user", "content": user_input})
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."}
                ] + context
            )
            answer = response.choices[0].message['content'].strip()
            context.append({"role": "assistant", "content": answer})
            speak(answer)
            print(answer)
        except Exception as e:
            speak("Sorry, I couldn't process that.")
            print(f"Error: {e}")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                if query.strip() == "":
                    speak("Please specify what you want to search on Wikipedia.")
                    continue
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("There are multiple results for this search, please specify.")
                print(e.options)
            except wikipedia.exceptions.PageError:
                speak("I couldn't find any result for your search.")
            except Exception as e:
                speak("Sorry, I couldn't complete the search. Please try again.")
                print(e)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            music_dir = 'D:\\DEVENDRA\\D\\Music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open gmail' in query:
            webbrowser.open("gmail.com")

        elif 'open linkedin' in query:
            webbrowser.open("linkedin.com")

        elif 'open whatsapp' in query:
            webbrowser.open("https://web.whatsapp.com")

        elif 'play song' in query:
            try:
                speak("Which song would you like to hear?")
                song = takeCommand().lower()
                speak(f"Playing {song} on YouTube")
                pywhatkit.playonyt(song)
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to play this song")

        elif 'live match score' in query:
            webbrowser.open("https://www.espncricinfo.com/live-cricket-score")

        elif 'weather' in query:
            webbrowser.open("https://weather.com")

        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "devendrarahire100@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email")

        elif 'take screenshot' in query:
            takeScreenshot()

        elif 'call' in query:
            try:
                speak("To whom should I make the WhatsApp call?")
                contact_name = takeCommand().lower()
                contacts = {
                    "aai": "+918975814123",
                    "dad": "+919423929439"
                }
                if contact_name in contacts:
                    phone_number = contacts[contact_name]
                    current_time = datetime.datetime.now()
                    send_time = (current_time + datetime.timedelta(minutes=2)).strftime("%H:%M")
                    hour, minute = map(int, send_time.split(":"))
                    speak(f"Sending WhatsApp message to {contact_name}")
                    pywhatkit.sendwhatmsg(phone_number, "This is an automated message from Jarvis", hour, minute)
                else:
                    speak("I don't have the contact information for that person.")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send the WhatsApp message")

        elif 'calculate' in query:
            speak("Please tell me the expression to calculate.")
            expression = takeCommand().lower()
            calculate(expression)

        elif 'news' in query:
            getNews()

        elif 'chat gpt' in query:
            speak("What is your question?")
            question = takeCommand()
            answerQuestion(question)

        elif 'conversation' in query:
            converse()

        elif 'stop' in query:
            speak("Goodbye Sir. Have a nice day!")
            break
