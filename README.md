# Umbrella Reminder AI Agent

A minimal AI Agent that provides umbrella recommendations based on weather data using Gemini LLM, LangChain framework, and Chroma vector database for memory storage.

## Features

- **Weather Analysis**: Gets current weather from OpenWeatherMap API
- **LLM Decision Making**: Uses Google Gemini to analyze weather data and make recommendations
- **Memory System**: Stores user decisions in Chroma vector database for personalized recommendations
- **Agent Loop**: Implements Observe → Decide → Act pattern with memory integration
- **CLI Interface**: Simple command-line interface for easy usage

## Architecture

```
┌─────────────────┐
│   CLI Input     │
│ (Location +     │
│  User ID)       │
└─────────┬───────┘
          │
┌─────────▼───────┐
│   Agent Loop    │
│ ┌─────────────┐ │
│ │  OBSERVE    │ │ ← Weather API
│ │ Get Weather │ │ ← Chroma Memory
│ │ Load Memory │ │
│ └─────────────┘ │
│ ┌─────────────┐ │
│ │   DECIDE    │ │ ← Gemini LLM  
│ │ Analyze +   │ │
│ │ Consider    │ │
│ │ History     │ │
│ └─────────────┘ │
│ ┌─────────────┐ │
│ │    ACT      │ │ → CLI Output
│ │Show Result +│ │ → Chroma Memory
│ │Save Decision│ │
│ └─────────────┘ │
└─────────────────┘
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd umbrella-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file and add your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   ```

## API Keys Setup

### Google API Key (for Gemini LLM)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

### OpenWeatherMap API Key
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up and get a free API key
3. Add it to your `.env` file

## Usage

### Basic Usage
```bash
python main.py --location "Jakarta" --user-id "john"
```

### Examples
```bash
# First time user
python main.py --location "Jakarta" --user-id "alice"

# Returning user (will show history)
python main.py --location "London" --user-id "bob"

# Different locations
python main.py --location "New York" --user-id "charlie"
```

### Command Line Options
- `--location, -l`: Location to get weather for (required)
- `--user-id, -u`: Unique identifier for the user (required)
- `--verbose, -v`: Enable verbose output showing agent loop steps
- `--help, -h`: Show help message

## Output Example

```
🤖 Umbrella Reminder AI Agent
==================================================
🤖 Starting umbrella recommendation for john in Jakarta...
📊 OBSERVE: Gathering weather data and user history...
   Weather: light rain, 75% rain chance
   User history: 3 past decisions
🧠 DECIDE: Analyzing data and making recommendation...
   Recommendation: YES
   Reason: High rain probability matches your cautious pattern
💾 ACT: Storing decision and preparing output...
   Decision stored in memory.

==================================================
🌦️  Umbrella Recommendation: [YES]

📍 Location: Jakarta
🌡️  Weather: light rain (28°C)
🌧️  Rain Probability: 75%

💭 Reason: High rain probability matches your cautious pattern

📊 Your History:
   - Total decisions: 4
   - Usually take umbrella: 75% of time
   - Average rain probability: 45%

🌂 Bring an umbrella!
```

## How It Works

### 1. OBSERVE Phase
- Fetches current weather data from OpenWeatherMap API
- Retrieves user's decision history from Chroma database
- Calculates user statistics and patterns

### 2. DECIDE Phase
- Sends weather data and user history to Gemini LLM
- LLM analyzes conditions and makes recommendation
- Considers user's past patterns and preferences

### 3. ACT Phase
- Stores the decision in Chroma vector database
- Updates user statistics
- Returns formatted recommendation to user

### Memory Learning
The agent learns from user behavior over time:
- Stores each decision with weather context
- Tracks user patterns (umbrella usage percentage)
- Provides personalized recommendations based on history
- Considers user's risk tolerance and past decisions

## File Structure

```
umbrella-agent/
├── main.py              # CLI entry point
├── agent.py             # Core agent class with Observe-Decide-Act loop
├── weather_service.py   # Weather API integration
├── memory_manager.py    # Chroma database operations
├── requirements.txt     # Dependencies
├── .env.example        # Environment template
├── chroma_db/          # Chroma database storage (auto-created)
└── README.md           # This file
```

## Dependencies

- `langchain`: Framework for LLM applications
- `langchain-google-genai`: Google Gemini integration
- `chromadb`: Vector database for memory storage
- `requests`: HTTP requests for weather API
- `python-dotenv`: Environment variable management

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Make sure your `.env` file exists and contains valid API keys
   - Check that API keys are not expired or rate-limited

2. **Weather API Errors**
   - Verify your OpenWeatherMap API key is active
   - Check if the location name is spelled correctly
   - Ensure internet connection is available

3. **Memory Database Issues**
   - Chroma database is created automatically in `./chroma_db/`
   - If corrupted, delete the `chroma_db` folder and restart

4. **Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

### Error Messages

- `GOOGLE_API_KEY not found`: Add Google API key to `.env` file
- `OPENWEATHER_API_KEY not found`: Add OpenWeatherMap API key to `.env` file
- `Error fetching weather data`: Check internet connection and API key
- `Error storing decision`: Check Chroma database permissions

## Testing

### Manual Testing Scenarios

1. **First Time User**
   ```bash
   python main.py --location "Jakarta" --user-id "test_user_new"
   # Should show: 0 past decisions
   ```

2. **Returning User**
   ```bash
   python main.py --location "Jakarta" --user-id "test_user_new"
   # Should show: 1 past decision
   ```

3. **Pattern Learning**
   ```bash
   # Run multiple times with same user
   python main.py --location "Jakarta" --user-id "test_user_new"
   # Should show increasing decision count and learned patterns
   ```

## Limitations (MVP)

- Single location per run
- Basic user preferences (no explicit settings)
- CLI interface only
- Basic error handling
- Local Chroma database only
- Free API limits only

## Future Enhancements

- Web interface (Streamlit)
- Advanced user preferences storage
- Multiple locations and scheduling
- Real-time weather monitoring
- Advanced analytics and pattern recognition
- Notification scheduling

## License

This project is for educational purposes (Assignment 7).