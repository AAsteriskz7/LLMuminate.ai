import anthropic
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()


client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key = os.getenv("ANTHROPIC_API_KEY")
)

# Replace placeholders like {{AI_RESPONSE}} with real values,
# because the SDK does not support variables.
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "You are a fact-checking AI assistant tasked with determining the similarity between an AI-generated response and relevant quotes from scholarly articles. Your goal is to assess the credibility of the AI response based on its alignment with the scholarly sources.\n\nFirst, you will be given the AI-generated response:\n\n<ai_response>\n{{AI_RESPONSE}}\n</ai_response>\n\nNext, you will be provided with relevant quotes from scholarly articles:\n\n<article_quotes>\n{{ARTICLE_QUOTES}}\n</article_quotes>\n\nTo analyze the similarity between the AI response and the article quotes, follow these steps:\n\n1. Carefully read both the AI response and the article quotes.\n2. Identify key claims, facts, or statements in the AI response.\n3. Compare these key elements to the information provided in the article quotes.\n4. Look for:\n   a. Direct matches or very similar statements\n   b. Supporting evidence for claims made in the AI response\n   c. Contradictions or discrepancies between the AI response and scholarly quotes\n   d. Important information from the scholarly quotes that is missing from the AI response\n\n5. Provide your reasoning for the similarity assessment. Consider the following:\n   - How well does the AI response align with the scholarly information?\n   - Does the AI response accurately represent the scholarly consensus?\n   - Are there any potential misinterpretations or oversimplifications in the AI response?\n   - Don't subtract points for omissions or unsupported claims in the AI response, only if there         are clear discrepancies with the sources.\n\n\nWrite your reasoning inside <reasoning> tags.\n\n6. Based on your analysis, assign a similarity score from 0 to 100, where:\n   0 = No similarity or completely contradictory\n   50 = Moderate similarity with some discrepancies\n   100 = Perfect alignment with scholarly sources\n\nConsider both the quantity and quality of matching information when assigning the score. In your reasoning, you should elaborate on why you subtracted points. As for how many points you should subtract for every discrepancy, make it very specific and case-by-case based on how different the two are.\n\nProvide your final similarity score inside <similarity_score> tags.\n\nYour complete response should be structured as follows:\n\n<reasoning>\n[Your detailed reasoning for the similarity assessment]\n</reasoning>\n\n<similarity_score>\n[Your similarity score between 0 and 100]\n</similarity_score>"
                }
            ]
        }
    ]
)
print(message.content)