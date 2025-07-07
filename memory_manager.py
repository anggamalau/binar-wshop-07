import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

class MemoryManager:
    """Manager for storing and retrieving user decisions using Chroma database."""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize the memory manager with Chroma database.
        
        Args:
            persist_directory: Directory to store Chroma database
        """
        self.persist_directory = persist_directory
        
        # Initialize Google embeddings
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=api_key
        )
        
        # Initialize Chroma client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Initialize vector store
        self.vector_store = Chroma(
            client=self.client,
            collection_name="umbrella_decisions",
            embedding_function=self.embeddings
        )
    
    def store_decision(self, user_id: str, decision_data: Dict) -> None:
        """
        Store a user's decision in the database.
        
        Args:
            user_id: Unique identifier for the user
            decision_data: Dictionary containing decision information
        """
        try:
            # Create content string for embedding
            content = self._create_content_string(user_id, decision_data)
            
            # Create metadata
            metadata = {
                "user_id": user_id,
                "decision": decision_data.get('recommendation', 'UNKNOWN'),
                "weather_description": decision_data.get('weather_description', ''),
                "rain_probability": decision_data.get('rain_probability', 0.0),
                "temperature": decision_data.get('temperature', 0.0),
                "location": decision_data.get('location', ''),
                "timestamp": datetime.now().isoformat(),
                "reason": decision_data.get('reason', '')
            }
            
            # Store in vector database
            self.vector_store.add_texts(
                texts=[content],
                metadatas=[metadata],
                ids=[f"{user_id}_{datetime.now().timestamp()}"]
            )
            
        except Exception as e:
            print(f"Error storing decision: {str(e)}")
    
    def get_user_history(self, user_id: str, limit: int = 5) -> List[Dict]:
        """
        Get user's decision history from the database.
        
        Args:
            user_id: Unique identifier for the user
            limit: Maximum number of decisions to retrieve
            
        Returns:
            List of decision dictionaries
        """
        try:
            # Search for user's decisions
            results = self.vector_store.similarity_search(
                query=f"User {user_id} umbrella decisions",
                k=limit,
                filter={"user_id": user_id}
            )
            
            # Convert results to list of dictionaries
            history = []
            for result in results:
                if hasattr(result, 'metadata') and result.metadata:
                    history.append({
                        'content': result.page_content,
                        'decision': result.metadata.get('decision'),
                        'weather_description': result.metadata.get('weather_description'),
                        'rain_probability': result.metadata.get('rain_probability'),
                        'temperature': result.metadata.get('temperature'),
                        'location': result.metadata.get('location'),
                        'timestamp': result.metadata.get('timestamp'),
                        'reason': result.metadata.get('reason')
                    })
            
            return history
            
        except Exception as e:
            print(f"Error retrieving user history: {str(e)}")
            return []
    
    def get_user_stats(self, user_id: str) -> Dict:
        """
        Get statistics about user's decisions.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Dictionary containing user statistics
        """
        try:
            history = self.get_user_history(user_id, limit=100)
            
            if not history:
                return {
                    'total_decisions': 0,
                    'umbrella_decisions': 0,
                    'no_umbrella_decisions': 0,
                    'umbrella_percentage': 0.0,
                    'average_rain_probability': 0.0
                }
            
            # Calculate statistics
            total_decisions = len(history)
            umbrella_decisions = sum(1 for h in history if h.get('decision') == 'YES')
            no_umbrella_decisions = total_decisions - umbrella_decisions
            umbrella_percentage = (umbrella_decisions / total_decisions) * 100 if total_decisions > 0 else 0
            
            rain_probabilities = [h.get('rain_probability', 0) for h in history if h.get('rain_probability') is not None]
            average_rain_probability = sum(rain_probabilities) / len(rain_probabilities) if rain_probabilities else 0
            
            return {
                'total_decisions': total_decisions,
                'umbrella_decisions': umbrella_decisions,
                'no_umbrella_decisions': no_umbrella_decisions,
                'umbrella_percentage': round(umbrella_percentage, 1),
                'average_rain_probability': round(average_rain_probability, 1)
            }
            
        except Exception as e:
            print(f"Error calculating user stats: {str(e)}")
            return {
                'total_decisions': 0,
                'umbrella_decisions': 0,
                'no_umbrella_decisions': 0,
                'umbrella_percentage': 0.0,
                'average_rain_probability': 0.0
            }
    
    def _create_content_string(self, user_id: str, decision_data: Dict) -> str:
        """
        Create a content string for embedding storage.
        
        Args:
            user_id: User identifier
            decision_data: Decision information
            
        Returns:
            Content string for embedding
        """
        decision = decision_data.get('recommendation', 'UNKNOWN')
        weather = decision_data.get('weather_description', 'unknown weather')
        rain_prob = decision_data.get('rain_probability', 0)
        location = decision_data.get('location', 'unknown location')
        reason = decision_data.get('reason', 'no reason given')
        
        content = (
            f"User {user_id} decided {decision} for umbrella recommendation "
            f"when weather in {location} was {weather} with {rain_prob}% rain probability. "
            f"Reason: {reason}"
        )
        
        return content