Jarvis Weather & Assistant Application 🌤️🤖

This project is a Python-based virtual assistant named Jarvis, equipped with advanced features such as weather updates, voice recognition, text-to-speech capabilities, and interaction with OpenAI's GPT. Jarvis can help users with tasks like checking weather forecasts, opening websites, and chatting with AI.
Features ✨

    Weather Updates:
        Current, weekly, and hourly forecasts for any city.
        Details include temperature, condition, wind speed, humidity, air quality, and rain probability.

    Voice Assistant:
        Responds to user commands via voice.
        Greets based on the time of day (Morning, Afternoon, Evening).
        Can listen and respond to user queries.

    Browser Interaction:
        Opens popular websites like Chrome, Firefox, Safari, Edge, and YouTube.

    Chat with AI:
        Interact with OpenAI's GPT model for conversations or queries.

    Code Interaction:
        Opens Visual Studio Code for programming tasks.

Setup Instructions 🛠️
Prerequisites

Ensure the following are installed on your system:

    Python 3.8 or higher
    Required Python packages (see below)
    Microphone for voice commands

Installation

    Clone this repository: https://github.com/haseeb676-sir7/JarvisWeather.git

git clone https://github.com/your-username/jarvis-weather-assistant.git
cd jarvis-weather-assistant

Install dependencies:

pip install -r requirements.txt

Required packages include:

    requests
    pyttsx3
    speechrecognition
    openai

Set up your API keys:

    Replace placeholders in the code with your actual OpenAI API key and Weather API key.

Run the application:

    python h1.py

Usage 🧑‍💻

    Launch the application:
        Follow voice instructions from Jarvis.
        Say commands such as "weather update", "open browser", "chat", or "exit."

    Weather Updates:
        Provide the city name when prompted.
        Select between current, weekly, or hourly forecasts.

    Browser Commands:
        Say the browser name (e.g., "Chrome") to open it.

    Exit:
        Say "exit" to terminate the program.

File Overview 📂

    h1.py: Contains the main application code.
    hello.txt: Stores website links and references used by Jarvis.

Security ⚠️

This project contains sensitive information such as API keys in the source code. Ensure to:

    Use .env files to securely store API keys.
    Avoid sharing your keys publicly.

Future Enhancements 🚀

    Add more browser options.
    Integrate AI models for enhanced weather predictions.
    Create a GUI for easier interaction.
