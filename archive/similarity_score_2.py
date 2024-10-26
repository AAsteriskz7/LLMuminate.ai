import spacy
from transformers import pipeline

# Load spaCy model for Named Entity Recognition
nlp = spacy.load("en_core_web_md")

# Load a pre-trained NLI model (using a transformer model from Hugging Face)
nli_model = pipeline("text-classification", model="roberta-large-mnli")

### 1. Named Entity Extraction (Facts)
def extract_facts(text):
    """
    Extract named entities (facts) from the text using spaCy.
    """
    doc = nlp(text)
    facts = {ent.text for ent in doc.ents if ent.label_ in {"PERSON", "ORG", "GPE", "DATE", "TIME", "MONEY", "QUANTITY", "PERCENT"}}
    return facts

### 2. Compare Facts Using NLI
def compare_facts_with_nli(fact1, fact2):
    """
    Compare two facts using the NLI model to determine if they entail or contradict each other.
    """
    result = nli_model(f"{fact1} entails {fact2}")
    
    # Extract the label (entailment, contradiction, or neutral)
    label = result[0]['label']
    
    return label

### 3. Fact Matching Score Using NLI (and print the facts)
def fact_matching_nli(response, article):
    """
    Use an NLI model to compare the factual consistency between the response and article.
    Also, print out the extracted facts.
    """
    response_facts = extract_facts(response)
    article_facts = extract_facts(article)

    print("\nAI Response Facts:", response_facts)
    print("Article Facts:", article_facts)

    matched_facts = 0
    total_facts = len(response_facts)
    
    # Compare each fact in the response with each fact in the article
    for response_fact in response_facts:
        for article_fact in article_facts:
            # Use NLI to check if the facts are semantically consistent (entailment)
            result = compare_facts_with_nli(response_fact, article_fact)
            if result == "ENTAILMENT":
                print(f"Match Found: '{response_fact}' entails '{article_fact}'")
                matched_facts += 1
                break  # If we find one matching fact, we move to the next fact in the response

    if total_facts == 0:
        return 0  # Avoid division by zero

    return matched_facts / total_facts

### 4. Combine AI-Based Semantic Similarity and NLI-Based Fact Comparison
def combined_similarity_score_nli(response, article):
    """
    Combines AI-based semantic similarity with NLI-based fact comparison for a holistic evaluation.
    """
    # Step 1: Use NLI for fact consistency
    fact_score = fact_matching_nli(response, article)
    
    # Step 2: Print the fact comparison result
    print(f"Fact-Matching (NLI) Score: {fact_score:.2f}")
    
    return fact_score

### Example Usage
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

final_score = combined_similarity_score_nli(ai_response, article_text)
print(f"Final Combined Score (Fact Comparison with NLI): {final_score:.2f}")