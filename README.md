# 🛠️ AI Assistant with Tools

An intelligent chat application powered by Groq's LLM that can access various tools to provide accurate, real-time information. Ask about weather, search the web, get Wikipedia summaries, perform calculations, and more!

**Live Demo:** https://chatapptoolagent.streamlit.app/

## ✨ Features

- 🌤️ **Weather** - Get current weather for any location
- 🔍 **Web Search** - Search DuckDuckGo for current information
- 📚 **Wikipedia** - Get detailed summaries of topics
- 🧮 **Calculator** - Perform complex mathematical calculations
- 📅 **Date/Time** - Check current date and time
- 🎲 **Random Facts** - Learn interesting random facts

All tools use free, public APIs with no authentication required.

## 📋 Requirements

- Python 3.8+
- Streamlit
- Groq API key (free from https://console.groq.com)
- Internet connection for API calls

## 🚀 Quick Start

### Local Installation & Setup

#### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ChatAppToolAgent
```

#### 2. Create a Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set Up Groq API Key

Get your free API key from [Groq Console](https://console.groq.com):

**Option A: Using Streamlit Secrets (Recommended)**

Create `.streamlit/secrets.toml` in your project directory:

```toml
GROQ_API_KEY = "your-groq-api-key-here"
```

**Option B: Using Environment Variable**

```bash
export GROQ_API_KEY="your-groq-api-key-here"
```

#### 5. Run the App Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🌐 Deploy on Streamlit Cloud

### Prerequisites

- GitHub account with the repository
- Streamlit account (free at https://streamlit.io)

### Deployment Steps

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create a Streamlit App**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repository
   - Choose the branch (main)
   - Set the main file path to `app.py`

3. **Add Secrets**
   - In your Streamlit Cloud app dashboard, click on "⋮" → "Settings"
   - Go to "Secrets" tab
   - Add your Groq API key:
     ```
     GROQ_API_KEY = "your-groq-api-key"
     ```
   - Save

4. **Deploy**
   - Click "Deploy"
   - Wait for the app to build and launch

Your app will be available at: `https://chatapptoolagent.streamlit.app/`

## 💬 Usage Examples

Try these questions in the chat:

- "What's the weather in Paris?"
- "What day is it today?"
- "Calculate sqrt(144) + 15"
- "Tell me about Albert Einstein"
- "Search for latest AI breakthroughs"
- "Give me a random fact"

## 🔧 How It Works

### Tool System

The app implements a tool-calling system where:

1. **User sends a message** → AI analyzes if tools are needed
2. **AI calls appropriate tools** → Functions execute and return results
3. **AI processes results** → Provides natural language response
4. **User sees the answer** → With tool usage information displayed

### Available Tools

| Tool | Purpose | Requires Auth |
|------|---------|---------------|
| `get_current_weather` | Weather for coordinates | No |
| `search_web` | Web search via DuckDuckGo | No |
| `get_wikipedia_summary` | Wikipedia article summaries | No |
| `calculate` | Mathematical expressions | No |
| `get_current_datetime` | Current date/time | No |
| `get_random_fact` | Random interesting facts | No |

## 🛠️ Troubleshooting

### "GROQ_API_KEY not found"
- Ensure you've set up the API key in `.streamlit/secrets.toml` (local) or Streamlit Secrets (cloud)
- Restart the app after adding the key

### Tools not working
- Check your internet connection
- External APIs might be temporarily down
- Check the tool output for specific error messages

### App runs slowly
- The LLM might be processing a complex request
- External APIs might be responding slowly
- This is normal for first response of the day

## 📦 Project Structure

```
ChatAppToolAgent/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── secrets.toml         # (Local only) API keys
└── README.md                # This file
```

## 🔐 Security

- **No data storage**: All conversations are temporary and cleared when you close the tab
- **Open APIs**: All external APIs used are public and free
- **API key handling**: Never commit `secrets.toml` to GitHub (use Streamlit Secrets instead)
- **Safe evaluation**: Math calculations use a restricted eval context

## 📝 API Documentation

### Groq LLM API
- Free tier available at https://console.groq.com
- Model: `llama-3.1-8b-instant`
- Documentation: https://console.groq.com/docs

### External APIs Used

1. **Open-Meteo Weather API**
   - URL: https://api.open-meteo.com
   - No authentication required

2. **DuckDuckGo Search API**
   - URL: https://api.duckduckgo.com
   - No authentication required

3. **Wikipedia API**
   - URL: https://en.wikipedia.org/api/rest_v1
   - No authentication required

4. **Useless Facts API**
   - URL: https://uselessfacts.jsph.pl
   - No authentication required

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

### Potential Enhancements
- Add more tools (news, stocks, weather alerts)
- Support for multiple languages
- Chat history export
- User preferences and bookmarks

## 📄 License

This project is open source and available for personal and commercial use.

## 🆘 Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Groq API Docs**: https://console.groq.com/docs
- **Issues**: Open a GitHub issue for bugs or feature requests

## 🎯 Future Roadmap

- [ ] Persistent chat history with database
- [ ] Custom tool creation
- [ ] Multi-language support
- [ ] User authentication
- [ ] Advanced analytics

---

**Built with ❤️ using Streamlit and Groq**
