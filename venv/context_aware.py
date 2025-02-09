import os
import openai
import pymongo
from scipy.spatial import distance  # Updated import path
from typing import List, Dict, Tuple
from dotenv import load_dotenv

load_dotenv()

class ContextAwareResponseGenerator:
    def __init__(self):
        """Initialize the response generator with MongoDB connection and OpenAI credentials."""
        self.mongo_uri = os.getenv("MONGO_URI")
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client.Dittoids
        self.collection = self.db.vectordb
        
        # Initialize OpenAI client
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # For a 10-email dataset, we'll consider fewer similar contexts
        self.context_window = 2  # Reduced from 3 to 2 for smaller dataset
        
    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for input text using OpenAI's API."""
        response = openai.Embedding.create(
            input=[text],
            model="text-embedding-ada-002"
        )
        return response['data'][0]['embedding']
    
    def find_similar_contexts(self, query_vector: List[float]) -> List[Dict]:
        """
        Find similar email contexts from MongoDB based on vector similarity.
        Optimized for a small dataset of 10 emails.
        """
        similar_contexts = []
        
        # Fetch all emails from MongoDB (limited to 10)
        all_emails = list(self.collection.find().limit(10))
        
        if not all_emails:
            print("Warning: No emails found in MongoDB. Please run vectorize_emails.py first.")
            return []
            
        # Calculate similarities for all emails
        similarities = []
        for email in all_emails:
            if 'vector' in email:  # Ensure email has vector field
                similarity = 1 - distance.cosine(query_vector, email['vector'])
                similarities.append((similarity, email))
        
        # Sort by similarity and get top matches
        similarities.sort(reverse=True)
        return [doc for _, doc in similarities[:self.context_window]]
    
    def analyze_email_content(self, email_content: str) -> Dict:
        """
        Analyze the content of an email to extract key information.
        This helps in generating more relevant responses.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "Analyze this email content from SP-TBI's perspective."},
                    {"role": "user", "content": email_content}
                ],
                functions=[{
                    "name": "analyze_email",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "main_topic": {"type": "string"},
                            "required_action": {"type": "string"},
                            "priority_level": {
                                "type": "string",
                                "enum": ["low", "medium", "high"]
                            }
                        },
                        "required": ["main_topic", "required_action", "priority_level"]
                    }
                }],
                function_call={"name": "analyze_email"}
            )
            return eval(response.choices[0].message.function_call.arguments)
        except Exception as e:
            print(f"Error in content analysis: {e}")
            return {"main_topic": "unknown", "required_action": "review", "priority_level": "medium"}

    def generate_response(self, new_email_content: str) -> Tuple[str, List[Dict], Dict]:
        """
        Generate a contextually aware response based on the new email content
        and similar historical emails from the 10-email dataset.
        """
        # Generate embedding for new email
        query_vector = self.get_embedding(new_email_content)
        
        # Find similar contexts
        similar_contexts = self.find_similar_contexts(query_vector)
        
        # Analyze email content
        content_analysis = self.analyze_email_content(new_email_content)
        
        # Create a focused context string
        context_str = ""
        for i, context in enumerate(similar_contexts):
            context_str += f"\nRelated Previous Communication {i+1}:\n"
            context_str += f"Subject: {context.get('subject', 'No subject')}\n"
            context_str += f"Content: {context.get('content', 'No content')[:300]}...\n"
        
        # Generate response using GPT-4
        prompt = f"""
        You are assisting at SP-TBI (SP Technology Business Incubator). 
        
        Current Email Content:
        {new_email_content}
        
        Content Analysis:
        Topic: {content_analysis['main_topic']}
        Required Action: {content_analysis['required_action']}
        Priority: {content_analysis['priority_level']}
        
        Previous Related Communications:
        {context_str}
        
        Generate a response that:
        1. Addresses the specific needs identified in the content analysis
        2. Maintains continuity with previous communications
        3. Reflects SP-TBI's supportive and entrepreneurial spirit
        4. Provides clear next steps or actions when needed
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are SP-TBI's AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content, similar_contexts, content_analysis

def main():
    """
    Example usage of the context-aware response generator.
    """
    generator = ContextAwareResponseGenerator()
    
    # Example email to test the system
    test_email = """
    Subject: Follow-up on Mentorship Program
    I recently joined SP-TBI's mentorship program and would like to know more about 
    the upcoming AI/ML workshops. Could you also share any resources from previous 
    sessions that might be helpful for a tech startup in the early stages?
    """
    
    try:
        # Generate response
        response, similar_contexts, analysis = generator.generate_response(test_email)
        
        # Print results
        print("\n=== Email Analysis ===")
        print(f"Main Topic: {analysis['main_topic']}")
        print(f"Required Action: {analysis['required_action']}")
        print(f"Priority Level: {analysis['priority_level']}")
        
        print("\n=== Similar Previous Contexts ===")
        for i, context in enumerate(similar_contexts, 1):
            print(f"\nContext {i}:")
            print(f"Subject: {context.get('subject', 'No subject')}")
            print(f"Content: {context.get('content', 'No content')[:200]}...")
        
        print("\n=== Generated Response ===")
        print(response)
        
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()