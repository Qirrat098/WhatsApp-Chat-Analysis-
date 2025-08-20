WhatsApp Chat Analyzer

A Streamlit web app to analyze WhatsApp chat data and generate insightful visualizations, including message statistics, activity timelines, word clouds, and emoji analysis.

Features

Top Statistics: Total messages, words, media, and links shared.

Timeline Analysis: Monthly and daily message trends.

Activity Map: Most active days, months, and weekly activity heatmap.

Busiest Users: Identifies the most active participants in group chats.

Word Cloud: Visual representation of most common words.

Emoji Analysis: Displays frequently used emojis with charts.

Demo


Replace screenshot.png with your actual screenshot.

Installation

Clone the repository:

git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer


Create a virtual environment:

python -m venv .venv


Activate the environment:

Windows: .venv\Scripts\activate

Mac/Linux: source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Usage

Run the Streamlit app:

streamlit run app.py


Upload your WhatsApp .txt chat file.

Select a user or Overall for group-level analysis.

Explore stats, visualizations, and insights.

File Structure
whatsapp-chat-analyzer/
│
├─ app.py              # Main Streamlit application
├─ preprocessor.py     # Data cleaning and preprocessing
├─ helper.py           # Helper functions for analysis & visualization
├─ requirements.txt    # Python dependencies
├─ README.md           # Project documentation
└─ .venv/              # Virtual environment (optional)

Dependencies

Python 3.8+

Streamlit

pandas

matplotlib

seaborn

wordcloud

emoji

regex

Contributing

Contributions are welcome! Please open an issue or submit a pull request.
