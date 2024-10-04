# Medical Chatbot using Streamlit and Gemini API

This project is a **Medical Chatbot** built using **Streamlit** and **Gemini API**. It allows users to interact with a chatbot for health-related queries, manage personalized medicine recommendations, and predict drug responses.

## Features

- **User Authentication**: Login and Sign-up for users to access personalized services.
- **Chatbot**: A conversational chatbot for health-related queries powered by Google Gemini API.
- **Personalized Medicine**: Get personalized medicine recommendations based on symptoms and user data.
- **Drug Response Predictor**: Predict the composition, cost, dosage, and side effects of medicines.

## Technologies Used

- **Streamlit**: For building the web interface.
- **Google Gemini API**: For generating AI-based responses.
- **Pandas**: For handling user data stored in a CSV file.
- **Speech Recognition**: For voice interaction.
- **Text-to-Speech (pyttsx3)**: For converting responses into speech.

## How to Clone and Set Up

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/Medical-chatbot-using-Streamlit-and-Gemini-API.git
    cd Medical-chatbot-using-Streamlit-and-Gemini-API
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory of the project and add your **Google Gemini API** key:
    ```bash
    GOOGLE_GEMINI_API_KEY="your_google_gemini_api_key"
    ```

4. Create a `users.csv` file with the following structure to store user details:
    ```csv
    user_id,user_name,passwords,name,email,dob,height,weight,gender,blood
    1,john_doe,password123,John Doe,john@example.com,1990-01-01,180,75,Male,O+
    ```

5. Run the application using Streamlit:
    ```bash
    streamlit run app.py
    ```

## Setting Up the Google Gemini API

To interact with the chatbot, you need to configure the **Google Gemini API**:

1. [Create a Google Cloud account](https://cloud.google.com).
2. Enable the **Gemini API** in your project.
3. Generate an API key and copy it to the `.env` file as described above.

## Application Workflow

### User Authentication
- **Login**: Users can log in by providing a username and password.
- **Sign-up**: New users can create an account by providing details like name, email, password, and personal medical information.

### Chatbot Page
- Users can interact with a health chatbot.
- The chatbot assists with health-related queries, providing information based on the user's symptoms.

### Personalized Medicine
- Users can input symptoms, and the AI will predict possible diseases and provide medicine recommendations in a structured format.

### Drug Response Predictor
- Provides information about the composition, cost, and side effects of the entered medicine name. It also suggests home remedies as alternatives.

## Code Structure

```python
import streamlit as st
import google.generativeai as genai
import pandas as pd

# Load user data
user_data = pd.read_csv("users.csv")

# Configure Google Gemini API
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

# Chat model
model = genai.GenerativeModel('gemini-pro')


```
