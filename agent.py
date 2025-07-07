import os
from typing import Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from weather_service import WeatherService
from memory_manager import MemoryManager
from dotenv import load_dotenv

load_dotenv()

class UmbrellaAgent:
    """
    AI Agent that provides umbrella recommendations based on weather data and user history.
    Implements the Observe-Decide-Act loop with memory integration.
    """
    
    def __init__(self):
        """Initialize the UmbrellaAgent with required services."""
        # Initialize services
        self.weather_service = WeatherService()
        self.memory_manager = MemoryManager()
        
        # Initialize LLM
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.3
        )
    
    def run(self, location: str, user_id: str) -> str:
        """
        Main entry point for the agent. Executes the Observe-Decide-Act loop.
        
        Args:
            location: Location to get weather for
            user_id: Unique identifier for the user
            
        Returns:
            Formatted recommendation result
        """
        print(f"🤖 Starting umbrella recommendation for {user_id} in {location}...")
        
        # OBSERVE: Gather weather data and user history
        observations = self.observe(location, user_id)
        
        # DECIDE: Use LLM to make recommendation
        decision = self.decide(observations)
        
        # ACT: Store decision and return result
        result = self.act(decision, user_id)
        
        return result
    
    def observe(self, location: str, user_id: str) -> Dict:
        """
        OBSERVE phase: Gather weather data and user history.
        
        Args:
            location: Location to get weather for
            user_id: User identifier
            
        Returns:
            Dictionary containing observations
        """
        print("📊 OBSERVE: Gathering weather data and user history...")
        
        try:
            # Get weather data
            weather_data = self.weather_service.get_weather(location)
            
            # Get user history
            user_history = self.memory_manager.get_user_history(user_id)
            user_stats = self.memory_manager.get_user_stats(user_id)
            
            observations = {
                'location': location,
                'user_id': user_id,
                'weather': weather_data,
                'history': user_history,
                'stats': user_stats
            }
            
            print(f"   Weather: {weather_data['description']}, {weather_data['rain_probability']}% rain chance")
            print(f"   User history: {user_stats['total_decisions']} past decisions")
            
            return observations
            
        except Exception as e:
            print(f"   Error in observe phase: {str(e)}")
            return {
                'location': location,
                'user_id': user_id,
                'weather': None,
                'history': [],
                'stats': {'total_decisions': 0},
                'error': str(e)
            }
    
    def decide(self, observations: Dict) -> Dict:
        """
        DECIDE phase: Use LLM to analyze observations and make recommendation.
        
        Args:
            observations: Dictionary containing weather and history data
            
        Returns:
            Dictionary containing decision
        """
        print("🧠 DECIDE: Analyzing data and making recommendation...")
        
        try:
            # Handle error case
            if observations.get('error'):
                return {
                    'recommendation': 'NO',
                    'reason': f"Unable to get weather data: {observations['error']}",
                    'confidence': 0.0
                }
            
            # Create prompt for LLM
            prompt = self._create_prompt(observations)
            
            # Get LLM response
            messages = [
                SystemMessage(content="You are a helpful AI assistant that provides umbrella recommendations based on weather data and user history. Always respond with a clear YES or NO recommendation followed by a brief reason."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Parse response
            decision = self._parse_response(response.content, observations)
            
            print(f"   Recommendation: {decision['recommendation']}")
            print(f"   Reason: {decision['reason']}")
            
            return decision
            
        except Exception as e:
            print(f"   Error in decide phase: {str(e)}")
            return {
                'recommendation': 'NO',
                'reason': f"Unable to process decision: {str(e)}",
                'confidence': 0.0
            }
    
    def act(self, decision: Dict, user_id: str) -> str:
        """
        ACT phase: Store decision in memory and return formatted result.
        
        Args:
            decision: Decision dictionary from decide phase
            user_id: User identifier
            
        Returns:
            Formatted result string
        """
        print("💾 ACT: Storing decision and preparing output...")
        
        try:
            # Store decision in memory
            self.memory_manager.store_decision(user_id, decision)
            
            # Get updated stats
            stats = self.memory_manager.get_user_stats(user_id)
            
            # Format output
            result = self._format_output(decision, stats)
            
            print("   Decision stored in memory.")
            
            return result
            
        except Exception as e:
            print(f"   Error in act phase: {str(e)}")
            return f"Error storing decision: {str(e)}"
    
    def _create_prompt(self, observations: Dict) -> str:
        """
        Create prompt for LLM based on observations.
        
        Args:
            observations: Dictionary containing weather and history data
            
        Returns:
            Formatted prompt string
        """
        weather = observations['weather']
        history = observations['history']
        stats = observations['stats']
        
        # Basic weather information
        prompt = f"""Weather Analysis for Umbrella Recommendation:

Location: {weather['location']}
Current Weather: {weather['description']}
Temperature: {weather['temperature']}°C
Rain Probability: {weather['rain_probability']}%
Humidity: {weather['humidity']}%

"""
        
        # Add user history if available
        if stats['total_decisions'] > 0:
            prompt += f"""User History:
- Total past decisions: {stats['total_decisions']}
- Usually takes umbrella: {stats['umbrella_percentage']}% of the time
- Average rain probability in past decisions: {stats['average_rain_probability']}%

Recent decisions:
"""
            for i, h in enumerate(history[:3]):
                prompt += f"- {h.get('decision', 'UNKNOWN')} when rain was {h.get('rain_probability', 0)}% ({h.get('weather_description', 'unknown')})\n"
        else:
            prompt += "User History: No previous decisions (first time user)\n"
        
        prompt += """
Based on the weather conditions and user history, should this user bring an umbrella?

Respond with:
1. [YES] or [NO] 
2. Brief reason (one sentence)

Consider:
- Rain probability > 30% generally suggests umbrella
- User's past patterns and preferences
- Current weather conditions
"""
        
        return prompt
    
    def _parse_response(self, response: str, observations: Dict) -> Dict:
        """
        Parse LLM response into structured decision.
        
        Args:
            response: Raw LLM response
            observations: Original observations for context
            
        Returns:
            Structured decision dictionary
        """
        response = response.strip()
        
        # Extract recommendation
        if '[YES]' in response.upper():
            recommendation = 'YES'
        elif '[NO]' in response.upper():
            recommendation = 'NO'
        else:
            # Fallback logic
            rain_prob = observations['weather']['rain_probability'] if observations['weather'] else 0
            recommendation = 'YES' if rain_prob > 30 else 'NO'
        
        # Extract reason
        lines = response.split('\n')
        reason = response.replace('[YES]', '').replace('[NO]', '').strip()
        
        # Clean up reason
        if len(reason) > 200:
            reason = reason[:200] + "..."
        
        if not reason:
            reason = "Based on current weather conditions."
        
        # Add weather context to decision
        weather_context = {}
        if observations['weather']:
            weather_context = {
                'location': observations['weather']['location'],
                'weather_description': observations['weather']['description'],
                'rain_probability': observations['weather']['rain_probability'],
                'temperature': observations['weather']['temperature']
            }
        
        return {
            'recommendation': recommendation,
            'reason': reason,
            'confidence': 0.8,  # Default confidence
            **weather_context
        }
    
    def _format_output(self, decision: Dict, stats: Dict) -> str:
        """
        Format final output for user.
        
        Args:
            decision: Decision dictionary
            stats: User statistics
            
        Returns:
            Formatted output string
        """
        result = f"""
🌦️  Umbrella Recommendation: [{decision['recommendation']}]

📍 Location: {decision.get('location', 'Unknown')}
🌡️  Weather: {decision.get('weather_description', 'Unknown')} ({decision.get('temperature', 0)}°C)
🌧️  Rain Probability: {decision.get('rain_probability', 0)}%

💭 Reason: {decision['reason']}

📊 Your History:
   - Total decisions: {stats['total_decisions']}
   - Usually take umbrella: {stats['umbrella_percentage']}% of time
   - Average rain probability: {stats['average_rain_probability']}%

{'🌂 Bring an umbrella!' if decision['recommendation'] == 'YES' else '☀️ No umbrella needed!'}
"""
        
        return result.strip()