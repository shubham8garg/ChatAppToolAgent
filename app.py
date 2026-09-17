import streamlit as st
from groq import Groq
import json
import requests
from datetime import datetime
import math

# Page config
st.set_page_config(page_title="AI Assistant with Tools", page_icon="🛠️")
st.title("🛠️ AI Assistant with Tools")
st.caption("I can search the web, check weather, do calculations, and more!")

# Initialize Groq client
@st.cache_resource
def get_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_groq_client()

# =============================================================================
# TOOL DEFINITIONS (Free APIs - No Keys Required!)
# =============================================================================

def get_current_weather(latitude: float, longitude: float) -> str:
    """Get current weather using Open-Meteo API (free, no key needed)"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weathercode,windspeed_10m,relative_humidity_2m"
        response = requests.get(url, timeout=10)
        data = response.json()
        current = data["current"]
        
        # Weather code descriptions
        weather_codes = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Foggy", 48: "Depositing rime fog", 51: "Light drizzle",
            53: "Moderate drizzle", 55: "Dense drizzle", 61: "Slight rain",
            63: "Moderate rain", 65: "Heavy rain", 71: "Slight snow",
            73: "Moderate snow", 75: "Heavy snow", 80: "Slight rain showers",
            81: "Moderate rain showers", 82: "Violent rain showers",
            95: "Thunderstorm", 96: "Thunderstorm with slight hail"
        }
        
        weather_desc = weather_codes.get(current["weathercode"], "Unknown")
        
        return json.dumps({
            "temperature": f"{current['temperature_2m']}°C",
            "condition": weather_desc,
            "humidity": f"{current['relative_humidity_2m']}%",
            "wind_speed": f"{current['windspeed_10m']} km/h"
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

def search_web(query: str) -> str:
    """Search web using DuckDuckGo Instant Answer API (free, no key needed)"""
    try:
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json", "no_html": 1}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        results = []
        
        # Abstract (main answer)
        if data.get("Abstract"):
            results.append({
                "type": "answer",
                "text": data["Abstract"],
                "source": data.get("AbstractSource", "")
            })
        
        # Related topics
        for topic in data.get("RelatedTopics", [])[:3]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append({
                    "type": "related",
                    "text": topic["Text"][:200]
                })
        
        if not results:
            return json.dumps({"message": "No instant results. Try a more specific query."})
        
        return json.dumps(results)
    except Exception as e:
        return json.dumps({"error": str(e)})

def get_wikipedia_summary(topic: str) -> str:
    """Get Wikipedia summary (free, no key needed)"""
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 404:
            return json.dumps({"error": "Topic not found on Wikipedia"})
        
        data = response.json()
        return json.dumps({
            "title": data.get("title", ""),
            "summary": data.get("extract", ""),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page", "")
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

def calculate(expression: str) -> str:
    """Safely evaluate mathematical expressions"""
    try:
        # Safe math functions
        safe_dict = {
            "abs": abs, "round": round,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "sqrt": math.sqrt, "pow": pow, "log": math.log,
            "log10": math.log10, "pi": math.pi, "e": math.e,
            "floor": math.floor, "ceil": math.ceil
        }
        
        # Clean expression
        expression = expression.replace("^", "**")
        
        # Evaluate safely
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return json.dumps({"expression": expression, "result": result})
    except Exception as e:
        return json.dumps({"error": f"Could not calculate: {str(e)}"})

def get_current_datetime(timezone: str = "UTC") -> str:
    """Get current date and time"""
    now = datetime.now()
    return json.dumps({
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A"),
        "timezone": timezone
    })

def get_random_fact(language: str = "en") -> str:
    """Get a random fact (free API)"""
    try:
        response = requests.get(f"https://uselessfacts.jsph.pl/random.json?language={language}", timeout=10)
        data = response.json()
        return json.dumps({"fact": data.get("text", "No fact available")})
    except Exception as e:
        return json.dumps({"error": str(e)})

# =============================================================================
# TOOL SCHEMAS (For LLM)
# =============================================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather for a location using coordinates. Use this when users ask about weather.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "Latitude of the location (e.g., 40.7128 for New York)"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "Longitude of the location (e.g., -74.0060 for New York)"
                    }
                },
                "required": ["latitude", "longitude"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for current information. Use this for questions about recent events, facts, or general knowledge.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_wikipedia_summary",
            "description": "Get a Wikipedia summary for a topic. Use this for detailed information about people, places, concepts, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to search (use underscores for spaces, e.g., 'Albert_Einstein')"
                    }
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations. Supports basic arithmetic, trigonometry, logarithms, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 2', 'sqrt(16)', 'sin(3.14159/2)')"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get the current date and time. Use this when users ask about today's date or current time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone (default: UTC)",
                        "default": "UTC"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_random_fact",
            "description": "Get a random interesting fact. Use this when users want to learn something random or are bored.",
            "parameters": {
                "type": "object",
                "properties": {
                    "language": {
                        "type": "string",
                        "description": "Language for the fact (default: en for English)",
                        "default": "en"
                    }
                },
                "required": []
            }
        }
    }
]

# Map function names to actual functions
tool_functions = {
    "get_current_weather": get_current_weather,
    "search_web": search_web,
    "get_wikipedia_summary": get_wikipedia_summary,
    "calculate": calculate,
    "get_current_datetime": get_current_datetime,
    "get_random_fact": get_random_fact
}

# =============================================================================
# CHAT LOGIC
# =============================================================================

def process_tool_calls(response_message, messages_for_api):
    """Process tool calls and get final response"""
    tool_calls = response_message.tool_calls
    
    # Add assistant message with tool calls
    messages_for_api.append({
        "role": "assistant",
        "tool_calls": [
            {
                "id": tc.id,
                "type": "function",
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments
                }
            } for tc in tool_calls
        ]
    })
    
    tool_results = []
    
    # Execute each tool call
    for tool_call in tool_calls:
        function_name = tool_call.function.name

        # Parse arguments safely - handle empty or None arguments
        try:
            function_args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
        except (json.JSONDecodeError, TypeError):
            function_args = {}

        # Show tool usage in UI
        st.info(f"🔧 Using tool: **{function_name}**\n\nArgs: `{function_args}`")

        # Execute the function
        if function_name in tool_functions:
            result = tool_functions[function_name](**function_args)
        else:
            result = json.dumps({"error": f"Unknown function: {function_name}"})
        
        tool_results.append({
            "name": function_name,
            "result": result
        })
        
        # Add tool result to messages
        messages_for_api.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })
    
    # Get final response with tool results
    final_response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages_for_api,
        tools=tools,
        tool_choice="auto",
        max_tokens=1024
    )
    
    return final_response.choices[0].message, tool_results

# =============================================================================
# STREAMLIT UI
# =============================================================================

# Sidebar
with st.sidebar:
    st.header("🛠️ Available Tools")
    st.markdown("""
    - 🌤️ **Weather** - Get current weather
    - 🔍 **Web Search** - Search DuckDuckGo
    - 📚 **Wikipedia** - Get summaries
    - 🧮 **Calculator** - Math calculations
    - 📅 **Date/Time** - Current date/time
    - 🎲 **Random Fact** - Learn something new
    """)
    
    st.divider()
    
    st.markdown("### Example Questions")
    st.markdown("""
    - *What's the weather in Paris?*
    - *Calculate sqrt(144) + 15*
    - *Tell me about Albert Einstein*
    - *What day is it today?*
    - *Give me a random fact*
    """)
    
    st.divider()
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Prepare messages for API
                messages_for_api = [
                    {
                        "role": "system",
                        "content": """You are a helpful assistant with access to tools. 
Use tools when appropriate to provide accurate, up-to-date information.
For weather, use these common coordinates:
- New York: 40.7128, -74.0060
- London: 51.5074, -0.1278
- Paris: 48.8566, 2.3522
- Tokyo: 35.6762, 139.6503
- Sydney: -33.8688, 151.2093
Always explain what you found from the tools in a natural way."""
                    },
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ]
                
                # Initial API call with tools
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=messages_for_api,
                    tools=tools,
                    tool_choice="auto",
                    max_tokens=1024
                )
                
                response_message = response.choices[0].message
                
                # Check if model wants to use tools
                if response_message.tool_calls:
                    response_message, tool_results = process_tool_calls(
                        response_message, 
                        messages_for_api
                    )
                
                # Display final response
                assistant_message = response_message.content
                st.markdown(assistant_message)
                
                # Add to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
