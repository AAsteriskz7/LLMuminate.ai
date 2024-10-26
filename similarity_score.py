import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load spaCy's pre-trained language model
nlp = spacy.load("en_core_web_md")

# Example data: AI response and article content
ai_response = """If you have a bloody nose, here are the steps you should follow:

Stay calm: Nosebleeds are usually not serious and can be easily managed.

Sit upright: Sitting up helps reduce blood pressure in the veins of your nose, which can help to stop the bleeding. Avoid lying down, as this can cause you to swallow blood.

Lean forward slightly: This prevents blood from running down your throat, which could cause nausea or choking.

Pinch your nose: Use your thumb and index finger to firmly pinch the soft part of your nose, just below the bony bridge. Keep this pressure for about 10-15 minutes without checking if the bleeding has stopped, as this could interfere with clot formation.

Breathe through your mouth: While pinching your nose, continue to breathe through your mouth to stay relaxed.

Apply a cold compress: Placing a cold pack or a cloth-wrapped ice pack on the bridge of your nose can help constrict the blood vessels and stop the bleeding.

Avoid blowing your nose: After the bleeding stops, try not to blow your nose for several hours to avoid dislodging the clot.

When to seek medical attention:
If the nosebleed lasts more than 20 minutes.
If it occurs after an injury to the head or face.
If you have frequent or heavy nosebleeds.
If you're on blood-thinning medication or have a known bleeding disorder.
Let me know if you need more information or have any concerns about managing nosebleeds!"""

article_text = """On sitting upright and leaning forward:
"Sit up straight and tip your head slightly forward. This will help prevent blood from running down the back of your throat." - WebMD, First Aid

On pinching the nose:
"Pinch the soft part of your nose just below the bony ridge. Hold it firmly for about 10 minutes. Don't let go to check if the bleeding has stopped during this time." - WebMD, First Aid

On breathing through mouth:
"Breathe through your mouth while you're doing this." - WebMD, First Aid

On post-bleeding care:
"Once the bleeding stops, don't bend down, strain, blow, or pick your nose for a few days." - WebMD, First Aid

On when to seek medical attention:
"Get emergency care if:
- Bleeding doesn't stop after two attempts of applying pressure for 10 minutes each
- The bleeding is rapid or the blood loss is large
- You're having difficulty breathing
- You've had recent surgery on your nose
- You've had a recent injury to your head or nose
- You're taking blood thinners or have a blood disorder" - WebMD, First Aid"""

# Mock credibility score (0 to 1 scale) for the article source
source_credibility = 0.8  # Example: a peer-reviewed journal with good reputation

### 1. Keyword Overlap Calculation
def keyword_overlap_score(response, article):
    response_doc = nlp(response)
    article_doc = nlp(article)

    response_keywords = {token.lemma_ for token in response_doc if token.is_alpha and not token.is_stop}
    article_keywords = {token.lemma_ for token in article_doc if token.is_alpha and not token.is_stop}

    # Print keywords from both the response and the article
    print("AI Response Keywords:", response_keywords)
    print("Article Keywords:", article_keywords)

    overlap = response_keywords.intersection(article_keywords)
    if len(response_keywords) == 0:
        return 0
    return len(overlap) / len(response_keywords)

### 2. Semantic Similarity Calculation
def semantic_similarity_score(response, article):
    response_doc = nlp(response).vector
    article_doc = nlp(article).vector

    # Cosine similarity between the response and article vectors
    similarity = cosine_similarity([response_doc], [article_doc])[0][0]
    return similarity

### 3. Fact Matching Calculation
def fact_matching_score(response, article):
    # Process the texts with spaCy to extract entities using NER
    response_doc = nlp(response)
    article_doc = nlp(article)
    
    # Extract named entities (NER) from both the AI response and the article
    response_facts = extract_facts(response_doc)
    article_facts = extract_facts(article_doc)

    # Print facts from both the response and the article
    print("AI Response Facts:", response_facts)
    print("Article Facts:", article_facts)

    # Convert to sets for comparison
    matched_facts = response_facts.intersection(article_facts)

    # If there are no facts in the response, return 0 to avoid division by zero
    if len(response_facts) == 0:
        return 0

    # Return the ratio of matched facts to total facts in the response
    return len(matched_facts) / len(response_facts)

def extract_facts(doc):
    """
    Extracts key factual entities such as numbers, percentages, diseases, technologies, etc.
    """
    facts = set()

    for ent in doc.ents:
        # Include only certain types of entities
        if ent.label_ in {"PERCENT", "MONEY", "DATE", "TIME", "QUANTITY", "ORDINAL", "CARDINAL"}:
            facts.add(ent.text)
        elif ent.label_ in {"ORG", "PERSON", "GPE", "LOC"}:
            facts.add(ent.text)

    # Lemmatize and normalize fact extraction (optional, for matching variations)
    lemmatized_facts = {token.lemma_ for token in doc if token.is_alpha and not token.is_stop}

    # Merge lemmatized important facts with the NER extracted facts
    return facts.union(lemmatized_facts)

### Final Match Score Calculation
def final_match_score(response, article, source_credibility):
    keyword_score = keyword_overlap_score(response, article)
    semantic_score = semantic_similarity_score(response, article)
    fact_score = fact_matching_score(response, article)

    # Weights for each factor (you can adjust these)
    weights = {
        'keyword': 0.1,
        'semantic': 0.3,
        'fact': 0.6,
    }

    # Final weighted score
    final_score = (
        weights['keyword'] * keyword_score +
        weights['semantic'] * semantic_score +
        weights['fact'] * fact_score
    )

    print(f"Keyword Score: {keyword_score:.2f}")
    print(f"Semantic Score: {semantic_score:.2f}")
    print(f"Fact Score: {fact_score:.2f}")

    return final_score

### Example Usage
final_score = final_match_score(ai_response, article_text, source_credibility)

print(f"Final Match Score: {final_score:.2f}")