# AI Blog Generator

🚀 **AI-Powered Blog Generator & Translator** – A Streamlit web app that generates blogs using AI and translates them into different languages. Users can input a topic and target language, and the app will create an English blog and translate it. Markdown downloads are available for both versions.

## 🔥 Features
- **AI-Powered Blog Generation** using `gemini-1.5-flash`
- **Automatic Translation** to multiple languages
- **Simple & Clean UI** built with Streamlit
- **Download Blogs** in Markdown format

## 🛠️ Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/Nishaad27/ai-blog-generator.git
   cd ai-blog-generator
   ```
2. **Create a virtual environment** (optional but recommended)
   ```sh
   python -m venv myvenv
   source myvenv/bin/activate  # On Windows use `myvenv\Scripts\activate`
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up environment variables**
   - Create a `.env` file and add your API keys (if required)

## 🚀 Usage
Run the Streamlit app:
```sh
streamlit run app.py
```

## 📂 Project Structure
```
├── blog_automation.py      # Handles blog generation
├── blog_translate.py       # Handles blog translation
├── main.py                 # Manages backend logic & flow integration
├── app.py                  # Streamlit UI & app execution
├── requirements.txt        # Python dependencies
├── .gitignore              # Ignored files/folders (myvenv, __pycache__, .env)
└── README.md               # Project documentation
```

## ⚠️ License
This project does not currently have a license.

## 🤝 Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

## 📬 Contact
For any queries or discussions, reach out via GitHub Issues.

---
🌍 **AI-driven content creation made easy!**

