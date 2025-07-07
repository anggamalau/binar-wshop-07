# Product Requirements Document
## Umbrella Reminder AI Agent (Minimum Viable Product)

---

## 1. Executive Summary

### 1.1 Product Overview
A minimal AI Agent that provides umbrella recommendations based on weather data using Gemini LLM, LangChain framework, and basic memory storage.

### 1.2 Scope
**Minimum Viable Product (MVP)** to demonstrate core AI Agent concepts for Assignment 7 with essential functionality only.

### 1.3 Target Users
- Students demonstrating AI Agent architecture
- Assignment evaluators assessing core concepts

---

## 2. Product Goals & Objectives

### 2.1 Primary Goals
- Demonstrate working AI Agent loop (Observe → Decide → Act)
- Show LLM integration with external tools
- Implement basic memory using Chroma vector database
- Prove concept with manageable complexity

### 2.2 Success Metrics
- Agent makes weather-based decisions
- Memory system stores and retrieves basic user data
- Complete agent loop execution with memory integration
- Working demonstration within development timeframe

---

## 3. Functional Requirements (MVP)

### 3.1 Core Features (Must Have)

#### 3.1.1 Weather Analysis
**Priority: P0**
- Get current weather from OpenWeatherMap API
- Extract rain probability
- Basic recommendation logic

**Acceptance Criteria:**
- Fetch weather for hardcoded location (Jakarta)
- Identify if rain probability > 30%
- Return "bring umbrella" or "no umbrella"

#### 3.1.2 LLM Decision Making
**Priority: P0**
- Use Gemini to analyze weather data
- Generate simple recommendation with reasoning
- Parse LLM response

**Acceptance Criteria:**
- Gemini processes weather input
- Returns structured decision
- Basic reasoning included

#### 3.1.3 Basic Memory System
**Priority: P0**
- Store user decisions in Chroma database
- Simple user preference learning
- Remember past recommendations

**Acceptance Criteria:**
- Chroma stores decision history
- Agent retrieves relevant past decisions
- Basic preference adjustment based on history

#### 3.1.4 Agent Loop
**Priority: P0**
- Observe: Get weather data + load memory
- Decide: Use LLM for recommendation with memory context
- Act: Display result + update memory

**Acceptance Criteria:**
- Three-step loop executes with memory integration
- Each step clearly defined
- Basic error handling

#### 3.1.5 Simple Interface
**Priority: P0**
- Command-line interface
- Single location input
- Text output

**Acceptance Criteria:**
- CLI accepts location input
- Displays recommendation clearly
- Shows basic reasoning

### 3.2 Excluded Features (Out of Scope)
- ❌ Complex UI/web interface
- ❌ Advanced user preferences management
- ❌ Real-time weather monitoring
- ❌ Multiple simultaneous users
- ❌ Complex memory analytics
- ❌ Feedback collection UI
- ❌ Notification scheduling

---

## 4. Technical Requirements (MVP)

### 4.1 Minimal Technology Stack
```yaml
LLM: Google Gemini (gemini-1.5-flash)
Framework: LangChain (basic tools + memory)
Memory: Chroma Vector Database (basic setup)
Weather API: OpenWeatherMap API
Interface: Command Line Interface
Language: Python 3.8+
```

### 4.2 Essential Dependencies
```python
# Core dependencies
langchain
langchain-google-genai
chromadb
requests
python-dotenv

# Minimal additional complexity
# No UI libraries
# Basic vector database only
```

### 4.3 Simplified Architecture
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
          │
┌─────────▼───────┐
│ Chroma Database │
│ ┌─────────────┐ │
│ │ User        │ │
│ │ Decisions   │ │
│ │ History     │ │
│ └─────────────┘ │
└─────────────────┘
```

---

## 5. Implementation Specifications (MVP)

### 5.1 Core Classes (Minimal)

#### 5.1.1 Weather Service
```python
class WeatherService:
    def get_weather(self, location: str) -> Dict
    def parse_rain_probability(self, data: Dict) -> float
```

#### 5.1.2 Memory Manager
```python
class MemoryManager:
    def __init__(self, persist_directory: str = "./chroma_db")
    def store_decision(self, user_id: str, decision_data: Dict)
    def get_user_history(self, user_id: str, limit: int = 5) -> List
    def get_user_stats(self, user_id: str) -> Dict
```

#### 5.1.3 Simple Agent
```python
class UmbrellaAgent:
    def __init__(self, llm, weather_service)
    def run(self, location: str) -> str
    # All three steps in one method for simplicity
```

### 5.2 Basic Chroma Integration
```python
import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings import GoogleGenerativeAIEmbeddings

# Simple Chroma setup
client = chromadb.PersistentClient(path="./chroma_db")
vector_store = Chroma(
    client=client,
    collection_name="umbrella_decisions",
    embedding_function=GoogleGenerativeAIEmbeddings(model="text-embedding-004")
)

# Basic operations
def store_decision(user_id: str, weather: str, decision: str):
    content = f"User {user_id} decided {decision} when weather was {weather}"
    metadata = {"user_id": user_id, "decision": decision, "timestamp": datetime.now()}
    vector_store.add_texts([content], [metadata])

def get_user_history(user_id: str, limit: int = 3):
    return vector_store.similarity_search(
        query=f"User {user_id} decisions",
        k=limit,
        filter={"user_id": user_id}
    )
```

### 5.3 Enhanced LangChain Integration
```python
# Single weather tool
@tool
def get_weather_data(location: str) -> str:
    """Get current weather for location"""
    return weather_service.get_weather(location)

# Simple prompt
PROMPT = """
Weather: {weather_data}
Should user bring umbrella? Answer with [YES] or [NO] and brief reason.
"""
```

### 5.4 Enhanced Data Structures
```python
# Input
{
    "location": str,     # e.g., "Jakarta"
    "user_id": str      # e.g., "user123"
}

# Memory Data (Chroma)
{
    "content": str,      # "User decided YES when weather was rainy"
    "metadata": {
        "user_id": str,
        "decision": str,  # "YES" or "NO"
        "weather": str,
        "timestamp": datetime
    }
}

# Output  
{
    "recommendation": str,  # "YES" or "NO"
    "reason": str,         # Brief explanation with history context
    "past_decisions": int   # Count of previous decisions
}
```

---

## 6. User Stories (MVP)

### 6.1 Primary User Story
```
As a user
I want to input my location and user ID
So that I get personalized umbrella recommendations based on my history

Acceptance Criteria:
- Enter city name and user ID via CLI
- Receive clear YES/NO recommendation  
- See reasoning that considers my past decisions
- View count of my previous decisions
```

### 6.2 Memory Learning Story
```
As a returning user
I want the agent to remember my past decisions
So that recommendations become more personalized over time

Acceptance Criteria:
- Agent stores my decisions in Chroma database
- Retrieves my history for context
- Recommendations consider my patterns
- Memory persists across sessions
```

### 6.3 Technical Demo Story
### 6.3 Technical Demo Story
```
As an evaluator
I want to see the agent loop with memory integration
So that I can verify AI Agent concepts with persistence

Acceptance Criteria:
- Observe step fetches weather + loads user memory
- Decide step uses LLM with memory context
- Act step produces output + updates memory
- Memory demonstrates learning over multiple runs
```

---

## 7. Setup & Usage (MVP)

### 7.1 Installation
```bash
# Clone repository
git clone <repo>
cd umbrella-agent

# Install minimal dependencies
pip install langchain langchain-google-genai requests python-dotenv

# Setup environment
cp .env.example .env
# Add GOOGLE_API_KEY and OPENWEATHER_API_KEY
```

### 7.2 Usage
```bash
# CLI usage with memory
python main.py --location "Jakarta" --user-id "john"

# Output example:
# Loading user history... (2 past decisions found)
# Weather: 65% chance of rain, cloudy
# Past pattern: You usually take umbrella when rain > 50%
# Recommendation: [YES] Bring an umbrella
# Reason: High rain probability matches your cautious pattern
# Decision saved to memory.

# Subsequent runs show learning:
python main.py --location "Jakarta" --user-id "john"
# (now shows 3 past decisions)
```

---

## 8. File Structure (MVP)
```
umbrella-agent/
├── main.py              # CLI entry point with user ID support
├── agent.py             # Core agent class with memory integration
├── weather_service.py   # Weather API integration
├── memory_manager.py    # Chroma database operations
├── requirements.txt     # Dependencies including chromadb
├── .env.example        # Environment template
├── chroma_db/          # Chroma database storage (auto-created)
└── README.md           # Usage instructions with memory examples
```

---

## 9. Example Implementation

### 9.1 Main Script
```python
# main.py
import argparse
from agent import UmbrellaAgent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--location", required=True)
    parser.add_argument("--user-id", required=True)
    args = parser.parse_args()
    
    agent = UmbrellaAgent()
    result = agent.run(args.location, args.user_id)
    print(result)

if __name__ == "__main__":
    main()
```

### 9.2 Core Agent with Memory
```python
# agent.py
class UmbrellaAgent:
    def __init__(self):
        self.weather_service = WeatherService()
        self.memory_manager = MemoryManager()
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    
    def run(self, location: str, user_id: str) -> str:
        # OBSERVE
        observations = self.observe(location, user_id)
        
        # DECIDE  
        decision = self.decide(observations)
        
        # ACT
        result = self.act(decision, user_id)
        return result
    
    def observe(self, location: str, user_id: str) -> Dict:
        weather_data = self.weather_service.get_weather(location)
        user_history = self.memory_manager.get_user_history(user_id)
        return {"weather": weather_data, "history": user_history, "user_id": user_id}
    
    def decide(self, observations: Dict) -> Dict:
        prompt = self.create_prompt(observations)
        response = self.llm.invoke(prompt)
        return self.parse_response(response)
    
    def act(self, decision: Dict, user_id: str) -> str:
        # Store decision in memory
        self.memory_manager.store_decision(user_id, decision)
        
        # Return formatted result
        return self.format_output(decision)
```

---

## 10. Testing (MVP)

### 10.1 Manual Testing with Memory
```python
# Test scenarios with memory progression
test_scenarios = [
    # First run - no history
    {"location": "Jakarta", "user_id": "test_user", "expected": "basic decision"},
    
    # Second run - should show 1 past decision
    {"location": "Jakarta", "user_id": "test_user", "expected": "decision with history context"},
    
    # Third run - should show learning pattern
    {"location": "Jakarta", "user_id": "test_user", "expected": "personalized decision"},
]

# Memory verification tests
test_memory = [
    {"action": "store_decision", "verify": "decision stored in Chroma"},
    {"action": "retrieve_history", "verify": "past decisions returned"},
    {"action": "user_stats", "verify": "correct decision count"}
]

# Run manually:
# python main.py --location "Jakarta" --user-id "test_user"
# Verify: Shows 0 past decisions first time
# python main.py --location "Jakarta" --user-id "test_user"  
# Verify: Shows 1 past decision second time
```

---

## 11. Constraints (MVP)

### 11.1 Deliberate Limitations
- Single location per run
- Basic user preferences (no explicit settings)
- Simple decision patterns only
- CLI interface only
- Basic error handling
- Hardcoded thresholds (30% rain)
- Local Chroma database only

### 11.2 Technical Constraints  
- Free API limits only
- Local execution only
- Basic Chroma database setup
- Minimal dependencies (5 packages)
- Simple embedding model only

---

## 12. Success Criteria (MVP)

### 12.1 Functional Success
✅ Agent fetches real weather data  
✅ LLM makes intelligent decisions  
✅ Clear agent loop demonstration  
✅ Working CLI interface  
✅ Chroma stores and retrieves user decisions
✅ Memory influences future recommendations
✅ User patterns emerge over multiple runs  

### 12.2 Educational Success
✅ Demonstrates Observe → Decide → Act pattern  
✅ Shows LLM tool integration  
✅ Proves AI agent concept  
✅ Demonstrates basic memory/learning
✅ Shows vector database integration with LangChain
✅ Completable within assignment timeframe  

---

## 13. Future Enhancements (Post-MVP)
- Web interface (Streamlit)
- Advanced user preferences storage  
- Complex memory analytics and patterns
- Multiple locations and scheduling
- Advanced weather analysis
- Notification scheduling
- User preference learning algorithms
- Social features and sharing

---

## 14. Risk Mitigation (MVP)

### 14.1 Simplified Risk Profile
| Risk | Mitigation |
|------|------------|
| API failures | Basic error messages |
| LLM parsing errors | Simple fallback logic |
| Chroma database issues | Basic error handling, auto-create db |
| Complex requirements | Strict MVP scope with basic memory only |

### 14.2 Development Risk
- **Scope creep**: Stick to basic memory features only
- **Over-engineering**: Use simplest Chroma setup possible
- **Time constraints**: Focus on core demonstration with simple learning
- **Memory complexity**: Limit to basic storage and retrieval patterns

---

**Document Version:** 2.1 (MVP with Memory)  
**Last Updated:** July 2025  
**Status:** MVP Specification with Basic Memory Integration  
**Scope:** Minimum viable demonstration of AI Agent concepts with Chroma vector database