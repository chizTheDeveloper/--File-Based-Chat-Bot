Chima Chat Bot
Chima Chat Bot is a Streamlit application that allows users to upload PDF or TXT documents and interact with a chatbot powered by conversational AI. The chatbot provides responses to user prompts/questions based on the content of the uploaded documents.

Setup and Installation
Clone the repository:
bash
Copy code
git clone <repository_url>
Install the required Python packages:
Copy code
pip install -r requirements.txt
Run the Streamlit app:
arduino
Copy code
streamlit run app.py
Usage
API Key Configuration
Before running the application, you need to obtain an API key from OpenAI and configure it in the application. Follow these steps:

Sign up for an account on OpenAI.
Generate an API key from your OpenAI account settings.
Add the API key to the application:
Launch the application.
Enter your API key in the provided input field in the sidebar.
Click on the "Submit" button.
Uploading Documents
Upload PDF or TXT documents containing the content you want the chatbot to process.
The documents will be used to provide context for generating responses to user prompts/questions.
Interacting with the Chatbot
Once the documents are uploaded and the API key is configured, you can interact with the chatbot.
Enter your questions/prompts in the provided input field.
The chatbot will generate responses based on the content of the uploaded documents and display them in the chat interface.
About
This project utilizes Streamlit for the web application framework, PyPDF2 for PDF file processing, and OpenAI's GPT-3 model for conversational AI capabilities.
