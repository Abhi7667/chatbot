# Define chat function
def chat(user_input):
    input_vector = vectorizer.transform([user_input])
    prediction = model.predict(input_vector)[0]
    for intent in data['intents']:
        if intent['tag'] == prediction:
            return random.choice(intent['responses'])

counter = 0

def speak(text):
    """Function to make the chatbot speak in a separate thread."""
    def run_speech():
        #engine.say(text)
        engine.runAndWait()

    # Run the speech in a separate thread
    threading.Thread(target=run_speech).start()

def listen():
    """Function to listen for user speech."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You said: ", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Sorry, the speech service is down.")
            return None

def main():
    global counter
    st.title("Intents of Chatbot using NLP")
    
    # Create a sidebar menu with options
    menu = ["Home", "Conversation History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    # Home Menu
    if choice == "Home":
        st.write("Welcome")
        if not os.path.exists('chat_log.csv'):
            with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['User Input', 'Chatbot Response', 'Timestamp'])
                
        counter += 1
        
        # Option to toggle between text or voice
        input_type = st.radio("Choose input method:", ["Text", "Voice"])
        
        if input_type == "Text":
            # Text input (chat)
            user_input = st.text_input("You:", key=f"user_input_{counter}")
            
            if user_input:
                # Process text input
                user_input_str = str(user_input)
                response = chat(user_input_str)
                st.text_area("Chatbot:", value=response, height=120, max_chars=None, key=f"chatbot_{counter}")
                speak(response)  # Convert the response to speech
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                with open('chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([user_input_str, response, timestamp])
                
                if response.lower() in ['goodbye', 'bye']:
                    st.write("Thank you for chatting with me. Have a great day!")
                    st.stop()

        elif input_type == "Voice":
            # Voice input
            voice_input_button = st.button("Speak")
            if voice_input_button:
                user_input = listen()
                if user_input:
                    st.text(f"You (Voice): {user_input}")
                    response = chat(user_input)
                    st.text_area("Chatbot:", value=response, height=120, max_chars=None, key=f"chatbot_voice_{counter}")
                    speak(response)  # Convert the response to speech
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    with open('chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerow([user_input, response, timestamp])
                    
                    if response.lower() in ['goodbye', 'bye']:
                        st.write("Thank you for chatting with me. Have a great day!")
                        st.stop()

    elif choice == "Conversation History":
        st.header("Conversation History")
        with open('chat_log.csv', 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)
            for row in csv_reader:
                st.text(f"User: {row[0]}")
                st.text(f"Chatbot: {row[1]}")
                st.text(f"Timestamp: {row[2]}")
                st.markdown("------")
                
    elif choice == "About":
        st.subheader("Project Goal:")
        st.write("The aim of this project is to develop a chatbot capable of understanding and responding to user inputs through Natural Language Processing (NLP) techniques, combined with machine learning algorithms for effective interaction.")
        st.subheader("Project Overview:")
        st.write("""
        This project is structured into two main components:
        
        1. NLP & Machine Learning: The chatbot is trained using NLP techniques and the Logistic Regression algorithm on labeled datasets to improve its ability to process and respond to user queries accurately.
        2. Streamlit Interface: Streamlit is utilized to create a user-friendly interface for seamless interaction with the chatbot, enabling users to easily input questions and receive responses in real time.
        """)
        
        st.subheader("Dataset:")
        st.write("The dataset contains intents, patterns, and responses used to train the chatbot, enabling it to accurately understand user queries and provide relevant responses.")

if __name__ == '__main__':
    main()
