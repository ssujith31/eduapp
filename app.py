from flask import Flask, render_template,request, session, redirect, url_for, jsonify, Response
from flask_socketio import SocketIO, send, emit
from flask_session import Session
from bs4 import BeautifulSoup
from openai import OpenAI
import os
import threading
import markdown
import pygame
import speech_recognition as sr
#from apiclass import EventHandler
from gtts import gTTS
from pydub import AudioSegment

import logging

r = sr.Recognizer()
"""
from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
    DeepgramClientOptions
)
API_KEY = "f3d4221757432e91e4cb824b3154671490a72abd"
# Set up client configuration
config = DeepgramClientOptions(
    verbose=logging.WARN,  # Change to logging.INFO or logging.DEBUG for more verbose output
    options={"keepalive": "true"}
)
deepgram = DeepgramClient(API_KEY, config)
dg_connection = None

"""

app = Flask(__name__, static_folder='assets',template_folder='templates')

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app)
#app = Flask(__name__)
client = OpenAI(api_key="sk-svcacct-5WprkT-n2Qp7UbWgSw0q8vdtjewYuRKiEMuXdZXvr9bxdT3BlbkFJna96_v8zVptAE0mYwWkJngkJQY-0jL5f99z033SgdKxBQA")

assistant = client.beta.assistants.create(
  name="Math Tutor",
  instructions="You are a personal math tutor. Write and run code to answer math questions.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4",
)

assistant2 = client.beta.assistants.create(
  name="Math Tutor",
  instructions="You are a personal math tutor. Write and run code to answer math questions.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4",
)

thread = client.beta.threads.create()

thread2 = client.beta.threads.create()

t1=""
"""
def initialize_deepgram_connection():
    global dg_connection
    # Initialize Deepgram client and connection
    dg_connection = deepgram.listen.websocket.v("1")

    def on_open(self, open, **kwargs):
        #print(f"\n\n{open}\n\n")
        pass

    def on_message(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if len(transcript) > 0:
            print(f"Question - {result.channel.alternatives[0].transcript}")
            socketio.emit('questionasked',{"question":transcript})
            message = client.beta.threads.messages.create(thread_id=thread2.id,role="user",content=transcript)
            run = client.beta.threads.runs.create_and_poll(thread_id=thread2.id,assistant_id=assistant2.id,instructions="Please address the user as Jane Doe. The user has a premium account.")
            if run.status == 'completed':
                #socketio.emit("voicestart1",{"status":"voice started"})
                messages = client.beta.threads.messages.list(thread_id=thread2.id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                language = 'en'
                print(f"response={response}")
                speech_file_path = "datafiles/welcome.mp3"
                with client.audio.speech.with_streaming_response.create(model="tts-1",voice="alloy",input=response) as  response2:
                    response2.stream_to_file(speech_file_path)
                todisplay=markdown.markdown(response, extensions=['md_in_html'])
                socketio.emit("voicestart1",{"answer":response})
                pygame.mixer.music.load("datafiles/welcome.mp3")
                pygame.mixer.music.play()
                #f1=open("datafiles/transcript.txt")
                #questionasked=f1.read()
                #f1.close()
                #data3={"result":questionasked,"answer":todisplay}
                #emit('displaydetails', data3)
                while True:
                    if pygame.mixer.music.get_busy():
                        #print("Song is not finished")
                        continue
                    else:
                        #print("Song is finshed")
                        break
                socketio.emit('voicecompleted',{"status":"ok"})                
            else:
                print(run.status)
            #socketio.emit('transcription_update', {'transcription': transcript})

    def on_close(self, close, **kwargs):
        #print(f"\n\n{close}\n\n")
        pass

    def on_error(self, error, **kwargs):
        #print(f"\n\n{error}\n\n")
        pass

    dg_connection.on(LiveTranscriptionEvents.Open, on_open)
    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    dg_connection.on(LiveTranscriptionEvents.Close, on_close)
    dg_connection.on(LiveTranscriptionEvents.Error, on_error)

    # Define the options for the live transcription
    options = LiveOptions(model="nova-2", language="en-US")

    if dg_connection.start(options) is False: # THIS CAUSES ERROR
        print("Failed to start connection")
        exit()

@socketio.on('audio_stream')
def handle_audio_stream(data):
    if dg_connection:
        dg_connection.send(data)

@socketio.on('toggle_transcription')
def handle_toggle_transcription(data):
    print("toggle_transcription", data)
    action = data.get("action")
    if action == "start":
        print("Starting Deepgram connection")
        initialize_deepgram_connection()

@socketio.on('connect')
def server_connect():
    print('Client connected')

@socketio.on('restart_deepgram')
def restart_deepgram():
    print('Restarting Deepgram connection')
    initialize_deepgram_connection()

def playvoice(filename1):
    #pygame.mixer.init()
    pygame.mixer.music.load(filename1)
    pygame.mixer.music.play()
"""

pygame.mixer.init()

"""
def remove_tags(html):
 soup = BeautifulSoup(html, "html.parser")
 for data in soup(['style', 'script']):
  data.decompose()
 return ' '.join(soup.stripped_strings)
"""

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/loginaction', methods=["POST"])
def loginaction():
    if request.method == 'POST':
        data = request.form
        if data['email']=="anandapk90@gmail.com" and data['password']=="123":
            print("success")
            session["name"] = data['email']
            return render_template("profile.html")
        else:
            return render_template("login.html",msg="Invalid Login")

@app.route('/signout')
def signout():
    if not session.get("name"):
        return redirect(url_for('login'))
    else:
        session["name"] = None
        return redirect(url_for('login'))

@app.route('/courses')
def courses():
    if not session.get("name"):
        return redirect(url_for('login'))
    else:
        return render_template("courses.html")

@app.route('/profile')
def profile():
    if not session.get("name"):
        return redirect(url_for('login'))
    else:
        return render_template("profile.html")

@app.route('/basicmathpage')
def basicmathpage():
    if not session.get("name"):
        return redirect(url_for('login'))
    else:
        return render_template("basicmath.html")

@app.route('/stopvoice', methods=['POST'])
def stopvoice():
    if not session.get("name"):
        return redirect(url_for('login'))
    else:
        #t1.stop
        pygame.mixer.music.stop()
        return {"status":"stoppedvoice"}

@app.route('/displaycontent',methods=["POST"])
def displaycontent():
    if not session.get("name"):
        return redirect(url_for('login'))
    else:
        if request.method=="POST":
            data1=request.json
            print(data1)
            if data1['operation']=="add":
                 f = open("contents/addition.txt", "r")
                 content=f.read()
                 content1=markdown.markdown(content)
                 return {"data2":content1,"ops":"Addition"}
            elif data1['operation']=="subtract":
                 f = open("contents/subtraction.txt", "r")
                 content=f.read()
                 content1=markdown.markdown(content)
                 return {"data2":content1,"ops":"Subtraction"}
            elif data1['operation']=="multiply":
                 f = open("contents/multiplication.txt", "r")
                 content=f.read()
                 content1=markdown.markdown(content)
                 return {"data2":content1,"ops":"Multiplication"}
            elif data1['operation']=="divide":
                 f = open("contents/division.txt", "r")
                 content=f.read()
                 content1=markdown.markdown(content)
                 return {"data2":content1,"ops":"Division"}

@app.route('/doubttextmode',methods=["POST"])
def doubttextmode():
    if not session.get("name"):
        return redirect(url_for('login'))
    else:
        if request.method=="POST":
            q1=request.json
            #tosend=q1['question']
            prepend = "Answer should be embedded in html tags. "
            tosend=prepend+q1['question']
            message = client.beta.threads.messages.create(thread_id=thread.id,role="user",content=tosend)
            run = client.beta.threads.runs.create_and_poll(thread_id=thread.id,assistant_id=assistant.id,instructions="Please address the user as Jane Doe. The user has a premium account.")   
            if run.status == 'completed': 
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                #print(messages)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                #language = 'en'
                print(f"response={response}")
                new_str = response.replace('`', '')
                new_str2=new_str.replace('html','',1)
                #output=markdown.markdown(response)
                return {"answer":new_str2}
            else:
                print(run.status)

def ogg2wav(ofn):
    wfn = ofn.replace('.ogg','.wav')
    x = AudioSegment.from_file(ofn)
    x.export(wfn, format='wav')

@app.route("/receive",methods=['post'])
def receive():
    files = request.files
    file = files.get('file')
    print(type(file))
    file.save("audiofiles/test2.ogg")
    ogg2wav("audiofiles/test2.ogg")
    file_audio = sr.AudioFile('audiofiles/test2.wav')
    with file_audio as source:
        audio_text = r.record(source)
    question1=r.recognize_google(audio_text)
    print(question1)
    socketio.emit('questionasked',{"question":question1})
    message = client.beta.threads.messages.create(thread_id=thread2.id,role="user",content=question1)
    run = client.beta.threads.runs.create_and_poll(thread_id=thread2.id,assistant_id=assistant2.id,instructions="Please address the user as Jane Doe. The user has a premium account.")
    if run.status == 'completed':
        #socketio.emit("voicestart1",{"status":"voice started"})
        messages = client.beta.threads.messages.list(thread_id=thread2.id)
        last_message = messages.data[0]
        response = last_message.content[0].text.value
        language = 'en'
        print(f"response={response}")
        speech_file_path = "datafiles/welcome.mp3"
        with client.audio.speech.with_streaming_response.create(model="tts-1",voice="alloy",input=response) as  response2:
            response2.stream_to_file(speech_file_path)
        todisplay=markdown.markdown(response, extensions=['md_in_html'])
        socketio.emit("voicestart1",{"answer":response})
        #pygame.mixer.music.load("datafiles/welcome.mp3")
        #pygame.mixer.music.play()
        #while True:
        #    if pygame.mixer.music.get_busy():
        #        continue
        #    else:
        #        break
        #socketio.emit('voicecompleted',{"status":"ok"})                
    else:
                print(run.status)
    response = "success"
    return response

@app.route("/mp3")
def streamwav():
    if not session.get("name"):
        return redirect(url_for('login'))
    else:
        def generate():
            with open("datafiles/welcome.mp3", "rb") as fwav:
                data = fwav.read(1024)
                while data:
                    yield data
                    data = fwav.read(1024)
        return Response(generate(), mimetype="audio/x-mp3")

"""
@socketio.on('voiceaction')
def handle_message(data):
    if not session.get("name"):
        return redirect(url_for('login'))
    else:
        #if request.method=="POST":
        transcript = open('datafiles/transcript.txt', 'w')
        #transcript.write("Answer should be embedded in html tags.")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                transcript.write(r.recognize_google(audio))
            except Exception as e:
                pass
            with open("datafiles/recorded.wav", "wb") as f:
                f.write(audio.get_wav_data())
                f.close()
        transcript.close()
        f = open("datafiles/transcript.txt", "r")
        message = client.beta.threads.messages.create(thread_id=thread2.id,role="user",content=f.read())
        run = client.beta.threads.runs.create_and_poll(thread_id=thread2.id,assistant_id=assistant2.id,instructions="Please address the user as Jane Doe. The user has a premium account.")
        if run.status == 'completed': 
            messages = client.beta.threads.messages.list(thread_id=thread2.id)
            last_message = messages.data[0]
            response = last_message.content[0].text.value
            language = 'en'
            print(f"response={response}")
            speech_file_path = "datafiles/welcome.mp3"
            
            #resp9 = client.audio.speech.create(model="tts-1",voice="alloy",input=response)
            #resp9.stream_to_file(speech_file_path)

            with client.audio.speech.with_streaming_response.create(model="tts-1",voice="alloy",input=response) as  response2:
                response2.stream_to_file(speech_file_path)

            todisplay=markdown.markdown(response, extensions=['md_in_html'])
            #resp=remove_tags(response)
            #newresp=resp.replace('*','')
            #n1=newresp.replace('\\','')
            #n2=n1.replace('(','')
            #n3=n2.replace(')','')
            #myobj = gTTS(text=n3, lang=language, slow=False)
            #myobj.save("datafiles/welcome.mp3")
            #pygame.mixer.init()
            pygame.mixer.music.load("datafiles/welcome.mp3")
            pygame.mixer.music.play()
            f1=open("datafiles/transcript.txt")
            questionasked=f1.read()
            f1.close()
            data3={"result":questionasked,"answer":todisplay}
            emit('displaydetails', data3)
            #t1 = threading.Thread(target=playvoice, args=("datafiles/welcome.mp3",))
            #t1.start()
            while True:
                if pygame.mixer.music.get_busy():
                    #print("Song is not finished")
                    continue
                else:
                    #print("Song is finshed")
                    break
            emit('voicecompleted',{"status":"ok"})                
        else:
            print(run.status)
        #f1=open("datafiles/transcript.txt")
        #questionasked=f1.read()
        #f1.close()
        #return {"result":questionasked,"answer":todisplay}

"""
"""
@app.route('/startconvert', methods=['POST'])
def startconvert():
    transcript = open('transcript.txt', 'w')
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        #print("Please say something to start recording the lecture ")
        audio = r.listen(source)
        #print("Recognizing Now .... ")
        try:
           #print("You have said \n" + r.recognize_google(audio))
            transcript.write(r.recognize_google(audio))
            #print("Audio Recorded Successfully \n ")
        except Exception as e:
            #print("Error :  " + str(e))
            pass

        with open("recorded.wav", "wb") as f:
            f.write(audio.get_wav_data())
            f.close()
    
    transcript.close()
    f = open("transcript.txt", "r")
    #print(f.read())
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f.read()
    )
    with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account.",
    event_handler=EventHandler(),
    ) as stream:
        stream.until_done()
    print("\n\n")
    return {"filename":"recorded.wav"}

@app.route('/startconvert2', methods=['POST'])
def startconvert2():
    transcript = open('transcript.txt', 'w')
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        #print("Please say something to start recording the lecture ")
        audio = r.listen(source)
        #print("Recognizing Now .... ")
        try:
           #print("You have said \n" + r.recognize_google(audio))
            transcript.write(r.recognize_google(audio))
            #print("Audio Recorded Successfully \n ")
        except Exception as e:
            #print("Error :  " + str(e))
            pass

        with open("recorded.wav", "wb") as f:
            f.write(audio.get_wav_data())
            f.close()
    
    transcript.close()
    f = open("transcript.txt", "r")
    #print(f.read())
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f.read()
    )
    #print(f"message - {message}")
    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account."
    )
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        #print(messages)
        last_message = messages.data[0]
        response = last_message.content[0].text.value
        language = 'en'
        print(f"response={response}")
        myobj = gTTS(text=response, lang=language, slow=False)
        myobj.save("welcome.mp3")
        #os.system("start welcome.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("welcome.mp3")
        pygame.mixer.music.play()
    else:
        print(run.status)
    return {"filename":"recorded.wav"}

#@socketio.on('hello')
#def handle_message(data):
#    print('received message: ' + data)
"""

if __name__ == '__main__':

    socketio.run(app)

