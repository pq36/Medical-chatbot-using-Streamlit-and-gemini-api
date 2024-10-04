import streamlit as st
import google.generativeai as genai
import pandas as pd


#hi.csv contains the user details
user_data=pd.read_csv("users.csv")



genai.configure(api_key=YOUR_GOOGLE_GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
model2=genai.GenerativeModel('gemini-pro')
model3=genai.GenerativeModel('gemini-pro')
model4 = genai.GenerativeModel('gemini-pro-vision')
placeholder=st.empty()

ch=model.start_chat(history=[])
responses = []



3create session state for chat history

if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]

def get_ai_response(chat):
    if chat:
        response = ch.send_message(chat,stream=True)
        return response

len=len(st.session_state['chat_history'])



def authenticate_user(username,password,user_data):
    if username in user_data["user_id"].values:
        stored_password = user_data.loc[user_data["user_id"] == username, "passwords"].values[0]

        if password == stored_password:
            st.success("Login successful!")
        else:
            st.error("Incorrect password. Please try again.")
    else:
        st.error("Username not found. Please create a new account.")
        st.write("New to this app?:face_with_rolling_eyes: Create a new  account :smile_cat:")

def create_new_account(new_userid,username, password, user_data,name,email,dob,height,weight,gender,blood):
    if len(password) < 8:
        st.warning("Password must be at least 8 characters long.")
    elif username in user_data["users"].values:
        st.error("Username already exists. Please choose a different username.")
    else:
        val={"user_id": [new_userid],"user_name":[username], "passwords": [password],
             "name":[name],"email":[email], "dob":[dob],"height":[height],"weight":[weight],
             "gender":[gender],"blood":[blood_group]}
        new_account = pd.DataFrame(val)
        user_data = pd.concat([user_data, new_account], ignore_index=True)
        user_data.to_csv("hi.csv", index=False)
        st.success("Account created successfully!")


    
    
def main():
    st.title(":blue[Login]") 
    with st.form(key="login_form"):
        userid=st.text_input("User Id:")
        password=st.text_input("Enter password:",type="password")
        submit_button=st.form_submit_button("Login")
        if submit_button:
            authenticate_user(userid,password,user_data)
    with st.form(key="signup_form"):
        new_userid=st.text_input("Enter new user id")
        name=st.text_input("Enter your name")
        email=st.text_input("Enter your email id")
        new_password = st.text_input("New Password:", type="password")
        dob=st.date_input("Enter your date of birth")
        height=st.number_input("Enter height(in cm):",0,350)
        weight=st.number_input("Enter weight(in kgs):",0,200)
        gender=st.radio("Select gender:",["Male","Female","Other"])
        blood_group=st.selectbox("Select your blood group:",["A+","B+","A-","B-","O+","O-","AB+","AB-"]) 
        create_account_button = st.form_submit_button("create Account")

        if create_account_button:
            create_new_account(new_userid,name,new_password,user_data,name,email,dob,height,weight,gender,blood_group)

if 'name' not in st.session_state:
    st.session_state.name=""
    

with st.sidebar:
    pages_select=st.selectbox("MedInnovate",["chatbot","personalised medicine"])
    if st.session_state.name =="":
        st.info("please login to get personalised precription")
    st.header("chat history")
    for role in st.session_state['chat_history']:
        st.write(f"{role}")
    

def recognize_and_speak(target_language='en', max_duration=10):
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

    with sr.Microphone() as source:
        st.write("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=max_duration)
        except sr.WaitTimeoutError:
            st.write("Speech recognition timed out. Maximum duration reached.")
            return

    try:
        text = recognizer.recognize_google(audio)
        st.write(f"You said: {text}")

        translated_text = translate_text(text, target_language)
        st.write(f"Translated Text: {translated_text}")

        # Speak the translated text
        speak(translated_text)

    except sr.UnknownValueError:
        st.write("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")


    


def main():
    st.title(":blue[Login]") 
    with st.form(key="login_form"):
        userid=st.text_input("User Id:")
        password=st.text_input("Enter password:",type="password")
        submit_button=st.form_submit_button("Login")
        if submit_button:
            authenticate_user(userid,password,user_data)
    with st.form(key="signup_form"):
        new_userid=st.text_input("Enter new user id")
        name=st.text_input("Enter your name")
        email=st.text_input("Enter your email id")
        new_password = st.text_input("New Password:", type="password")
        dob=st.date_input("Enter your date of birth")
        height=st.number_input("Enter height(in cm):",0,350)
        weight=st.number_input("Enter weight(in kgs):",0,200)
        gender=st.radio("Select gender:",["Male","Female","Other"])
        blood_group=st.selectbox("Select your blood group:",["A+","B+","A-","B-","O+","O-","AB+","AB-"]) 
        create_account_button = st.form_submit_button("create Account")


        if create_account_button:
            create_new_account(new_userid,name, new_password, user_data,name,email,dob,height,weight,gender,blood_group)
        id=userid
        st.session_state.name=userid
        return
    
def get_gemini_response(input,image):
    if input!="" and image!="":
       response = model4.generate_content([input,image])
    if input!="" and image=="":
       response = model.generate_content(image)
    if len(response.candidates) == 1 and len(response.candidates[0].content.parts) == 1:
        text_response = response.candidates[0].content.parts[0].text
        return text_response
    else:
        complex_response = " ".join(part.text for part in response.parts)
        st.write(complex_response)


def chat_page(chat):
    st.title(":green[MEDINNOVATE AI CHATBOT]:dizzy:")
    with st.chat_message("assistant"):
        st.write("Hi friend:wave:,Ask any querries related to health")
    if chat:
        st.session_state.chat_history.append(chat)
        with st.chat_message("user"):
            st.write(chat)
        with st.chat_message("assistant"):
            response= model.generate_content(chat)
            st.write(response.text)

    
       
def med():
    st.title("Personalised Medicine")
    st.info("Please answer all questions as possible to get more accurate response")
    symptom = st.text_input("Write the symptom of the disease")
    days = st.text_input("From how many days?")
    other_symptoms = st.text_input("What are the other symptoms")
    oth=st.text_input("if you have any other disease?(To confirm the sideeffects)")
    if symptom:
        q=model2.generate_content(f"based on the given data generate the question in 1 line to know predict the disease ,the question is in the other symptoms is there or not form ,symptom={symptom},number of days={days},other symptoms={other_symptoms}")
        answer=st.text_input(q.text)

        prompt = f"Predict the disease with symptoms: {symptom}, and the number of days the disease is: {days}, and other symptoms: {other_symptoms},{q}:{answer},and other disease:{oth},also generate remedies for it,tablets for it and dosage according to the details mentioned ,just generate in 1 line in tabular form,and drug response prediction in other below box,,then leave the 3 lines gap and generate then the tablet or medicine to the predicted disease along with composition note that other disease:{oth},the medicine do not give the side effect for the other disease,cost and dosage according to age "
            
        response = model2.generate_content(prompt)
        st.write(response.text)

def home():
    st.title("MEDICAL CHATBOT")
    st.image("img.jpeg")
    #st.title("Personal info")
    user_row = user_data[user_data['name'] == id]

    if not user_row.empty:
        # Access the "user_id" for the specified name
        user_id = user_row['user_id'].values[0]
        st.write(f"Name: {id}, User ID: {user_id}")

def predictor():
    st.title("Medicine info")
    p=st.text_input("Enter the name of the medicine")
    if p:
        prompt=f"for the medicine: {p} ,generate the composition of the given medicine and cost in rupees of the given medicine,dosage according to age,disadvantage of consuming more dosage,alternative home remidies,all in tabular form"
        response = model3.generate_content(prompt)
        st.write(response.text)


if pages_select=="Login":
    with placeholder:
        with st.container():
            id=main()





elif pages_select=="personalised medicine":
    with placeholder:
        with st.container():
            if st.session_state.name=="":
                main()
            elif st.session_state!="":
                med()
                
elif pages_select=="Drug response predictor":
    with placeholder:
        with st.container():
            predictor()


else:
    
    chat=st.chat_input("say something")
    
    with placeholder:
        with st.container():
            chat_page(chat)           


