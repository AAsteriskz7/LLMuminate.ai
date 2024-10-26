import spacy

# Load the pre-trained spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_facts(text):
    # Process the text with spaCy NLP pipeline
    doc = nlp(text)
    
    # Extract named entities and their labels
    facts = []
    for ent in doc.ents:
        facts.append((ent.text, ent.label_))
    
    return facts

if __name__ == "__main__":
    # Sample text
    text = """If you have a bloody nose, here are the steps you should follow:

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

    # Extract and print facts
    facts = extract_facts(text)
    for fact in facts:
        print(f"Entity: {fact[0]}, Type: {fact[1]}")
