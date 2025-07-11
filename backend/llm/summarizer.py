import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def summarize_reviews(reviews):
    """
    Summarize product reviews using OpenAI's GPT model.
    
    Args:
        reviews (str): String containing product reviews
        
    Returns:
        str: Summarized review or error message
    """
    if not reviews or not reviews.strip():
        return "No reviews provided"
    
    try:
        prompt = f"Summarize the following product reviews and extract key insights:\n{reviews}"
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error summarizing reviews: {str(e)}"

if __name__ == "__main__":
    # Example usage
    reviews = """
    This product is great! Fast shipping.
    Not as described, disappointed.
    Excellent value for the price.
    """
    summary = summarize_reviews(reviews)
    print("Summary:", summary)