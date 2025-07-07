#!/usr/bin/env python3
"""
Umbrella Reminder AI Agent - CLI Interface
Main entry point for the AI agent that provides umbrella recommendations.
"""

import argparse
import sys
from agent import UmbrellaAgent

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="AI Agent that provides umbrella recommendations based on weather data and user history",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --location "Jakarta" --user-id "john"
  python main.py --location "London" --user-id "alice"
  python main.py --location "New York" --user-id "bob"

Requirements:
  - Set GOOGLE_API_KEY in .env file
  - Set OPENWEATHER_API_KEY in .env file
        """
    )
    
    parser.add_argument(
        "--location",
        "-l",
        required=True,
        help="Location to get weather for (e.g., 'Jakarta', 'London', 'New York')"
    )
    
    parser.add_argument(
        "--user-id",
        "-u",
        required=True,
        help="Unique identifier for the user (e.g., 'john', 'alice', 'user123')"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output showing agent loop steps"
    )
    
    args = parser.parse_args()
    
    try:
        print("🤖 Umbrella Reminder AI Agent")
        print("=" * 50)
        
        # Initialize and run agent
        agent = UmbrellaAgent()
        result = agent.run(args.location, args.user_id)
        
        print("\n" + "=" * 50)
        print(result)
        
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure you have created a .env file with your API keys")
        print("2. Check that your API keys are valid")
        print("3. Ensure you have internet connection")
        print("4. Install required dependencies: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()