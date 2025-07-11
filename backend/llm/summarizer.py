import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def summarize_reviews(reviews):
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    if not reviews or not reviews.strip():
        return "No reviews to summarize."
    
    try:
        prompt = f"Summarize the following product reviews:\n{reviews}"
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except openai.AuthenticationError:
        raise ValueError("Invalid OpenAI API key")
    except openai.RateLimitError:
        raise ValueError("OpenAI API rate limit exceeded")
    except Exception as e:
        raise ValueError(f"OpenAI API error: {str(e)}")

if __name__ == "__main__":
    # Example usage
    reviews = """
    This product is great! Fast shipping.
    Not as described, disappointed.
    Excellent value for the price.
    """
    summary = summarize_reviews(reviews)
    print("Summary:", summary)