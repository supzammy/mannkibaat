"""
Training Data for Intent Classification: Mental Health vs Casual Text
Dataset for two-stage classification system
"""

import pandas as pd
import json

# Label: 1 = Genuine Mental Health Content, 0 = Casual/Gibberish

TRAINING_DATA = [
    # ===== GENUINE MENTAL HEALTH CONTENT (Label: 1) =====
    # Depression symptoms
    {"text": "I've been feeling exhausted and hopeless for weeks now", "label": 1, "category": "depression"},
    {"text": "My sleep has been terrible and I can't focus at work anymore", "label": 1, "category": "depression"},
    {"text": "I feel empty and don't enjoy anything that used to make me happy", "label": 1, "category": "depression"},
    {"text": "Constant sadness and loss of appetite for the past month", "label": 1, "category": "depression"},
    {"text": "I feel worthless and like a burden to everyone around me", "label": 1, "category": "depression"},
    {"text": "Everything feels pointless and I have no motivation to do anything", "label": 1, "category": "depression"},
    {"text": "I can't stop crying and feel overwhelmed by sadness", "label": 1, "category": "depression"},
    {"text": "No energy, no interest in life, just want to sleep all day", "label": 1, "category": "depression"},
    {"text": "I feel disconnected from everything and everyone", "label": 1, "category": "depression"},
    {"text": "My mood is consistently low and I struggle to get out of bed", "label": 1, "category": "depression"},
    
    # Anxiety symptoms
    {"text": "Constant anxiety and racing thoughts keep me awake at night", "label": 1, "category": "anxiety"},
    {"text": "I feel nervous and worried about everything all the time", "label": 1, "category": "anxiety"},
    {"text": "My heart races and I feel like I can't breathe when I think about work", "label": 1, "category": "anxiety"},
    {"text": "Overwhelming panic attacks that come out of nowhere", "label": 1, "category": "anxiety"},
    {"text": "I'm constantly on edge and can't relax even when I try", "label": 1, "category": "anxiety"},
    {"text": "Fear and worry dominate my thoughts every single day", "label": 1, "category": "anxiety"},
    {"text": "Physical tension, trembling, and constant nervousness", "label": 1, "category": "anxiety"},
    {"text": "I avoid social situations because of intense anxiety", "label": 1, "category": "anxiety"},
    {"text": "Restless and unable to calm my mind despite trying meditation", "label": 1, "category": "anxiety"},
    {"text": "Intrusive anxious thoughts that I can't control or stop", "label": 1, "category": "anxiety"},
    
    # Mixed symptoms
    {"text": "I'm struggling with both depression and anxiety lately", "label": 1, "category": "mixed"},
    {"text": "Feeling tired, sad, and worried all at the same time", "label": 1, "category": "mixed"},
    {"text": "My mental health has declined significantly over the past months", "label": 1, "category": "mixed"},
    {"text": "I experience mood swings, anxiety attacks, and deep sadness", "label": 1, "category": "mixed"},
    {"text": "Cannot concentrate, feel hopeless, and constantly stressed", "label": 1, "category": "mixed"},
    
    # Physical symptoms
    {"text": "I have no appetite and have lost significant weight recently", "label": 1, "category": "physical"},
    {"text": "Chronic insomnia and fatigue affecting my daily functioning", "label": 1, "category": "physical"},
    {"text": "Headaches, body aches, and extreme tiredness every day", "label": 1, "category": "physical"},
    {"text": "Sleep disturbances and loss of energy for basic tasks", "label": 1, "category": "physical"},
    {"text": "Physical exhaustion combined with emotional numbness", "label": 1, "category": "physical"},
    
    # Suicidal ideation (severe)
    {"text": "I've been having thoughts about ending my life", "label": 1, "category": "severe"},
    {"text": "Feel like the world would be better without me", "label": 1, "category": "severe"},
    {"text": "Life feels unbearable and I don't see a way forward", "label": 1, "category": "severe"},
    {"text": "Constant thoughts of self-harm and giving up on everything", "label": 1, "category": "severe"},
    
    # Specific mental health concerns
    {"text": "I think I might be experiencing clinical depression", "label": 1, "category": "seeking_help"},
    {"text": "My mental state has deteriorated and I need professional help", "label": 1, "category": "seeking_help"},
    {"text": "I'm concerned about my mental health and emotional wellbeing", "label": 1, "category": "seeking_help"},
    {"text": "Experiencing symptoms of a mental health disorder", "label": 1, "category": "seeking_help"},
    
    # Detailed descriptions
    {"text": "For the past three weeks I've felt sad every single day with no energy to do basic things like showering or eating", "label": 1, "category": "detailed"},
    {"text": "My anxiety has gotten so bad that I can't leave my house anymore and I feel trapped", "label": 1, "category": "detailed"},
    {"text": "I used to love painting and spending time with friends but now nothing brings me joy and I isolate myself", "label": 1, "category": "detailed"},
    {"text": "Every morning I wake up with a heavy feeling in my chest and dread facing another day of feeling this way", "label": 1, "category": "detailed"},
    {"text": "I cry unexpectedly throughout the day and struggle to explain why I feel so broken inside", "label": 1, "category": "detailed"},
    {"text": "My concentration is gone, I can't remember things, and my work performance has suffered terribly", "label": 1, "category": "detailed"},
    {"text": "I feel like I'm drowning in negative thoughts and can't find a way to feel normal again", "label": 1, "category": "detailed"},
    {"text": "The guilt and shame I feel about everything is overwhelming and I can't shake these feelings", "label": 1, "category": "detailed"},
    {"text": "I'm emotionally numb, can't connect with loved ones, and feel completely alone even in a crowd", "label": 1, "category": "detailed"},
    {"text": "Sleep is either impossible or all I do, my eating habits are irregular, and I have zero motivation", "label": 1, "category": "detailed"},
    
    # Indian English variations
    {"text": "I'm feeling very much depressed and tension is too much", "label": 1, "category": "indian_english"},
    {"text": "My mind is not working properly and I feel very sad all the time", "label": 1, "category": "indian_english"},
    {"text": "I am having too much stress and cannot cope with daily life", "label": 1, "category": "indian_english"},
    
    # Edge cases - clinical/medical language (ADD MORE OF THESE)
    {"text": "I think I might be experiencing clinical depression", "label": 1, "category": "clinical"},
    {"text": "Experiencing symptoms of major depressive disorder", "label": 1, "category": "clinical"},
    {"text": "I believe I have generalized anxiety disorder", "label": 1, "category": "clinical"},
    {"text": "Showing signs of persistent depressive mood", "label": 1, "category": "clinical"},
    {"text": "I may be suffering from a mental health condition", "label": 1, "category": "clinical"},
    {"text": "Concerned about possible psychiatric symptoms", "label": 1, "category": "clinical"},
    {"text": "I might need psychological evaluation and treatment", "label": 1, "category": "clinical"},
    {"text": "Experiencing clinical levels of anxiety and stress", "label": 1, "category": "clinical"},
    
    # "Everything/anything/nothing" in genuine context
    {"text": "worried about everything constantly and can't relax", "label": 1, "category": "everything_genuine"},
    {"text": "feeling anxious about everything in my life", "label": 1, "category": "everything_genuine"},
    {"text": "everything feels overwhelming and too much to handle", "label": 1, "category": "everything_genuine"},
    {"text": "I worry about everything all day long", "label": 1, "category": "everything_genuine"},
    {"text": "nothing makes me happy anymore and I feel empty", "label": 1, "category": "everything_genuine"},
    {"text": "nothing interests me and life feels meaningless", "label": 1, "category": "everything_genuine"},
    {"text": "I can't enjoy anything anymore, nothing brings pleasure", "label": 1, "category": "everything_genuine"},
    {"text": "anything triggers my anxiety and panic", "label": 1, "category": "everything_genuine"},
    
    # Stress and burnout
    {"text": "Completely burned out from work and life demands", "label": 1, "category": "stress"},
    {"text": "Overwhelming stress that I can't manage anymore", "label": 1, "category": "stress"},
    {"text": "Work stress combined with personal issues breaking me down", "label": 1, "category": "stress"},
    {"text": "Chronic stress affecting my physical and mental health", "label": 1, "category": "stress"},
    {"text": "Under extreme pressure and feeling like I'm breaking", "label": 1, "category": "stress"},
    {"text": "Stress levels are unbearable and affecting everything", "label": 1, "category": "stress"},
    
    # Relationship and social issues
    {"text": "Feeling isolated and lonely with no one to talk to", "label": 1, "category": "social"},
    {"text": "My relationships are falling apart and I feel alone", "label": 1, "category": "social"},
    {"text": "Social anxiety prevents me from connecting with people", "label": 1, "category": "social"},
    {"text": "I've withdrawn from all my friends and family", "label": 1, "category": "social"},
    {"text": "Loneliness is crushing me and I can't reach out", "label": 1, "category": "social"},
    
    # Trauma and PTSD-like symptoms
    {"text": "Haunted by past traumatic experiences daily", "label": 1, "category": "trauma"},
    {"text": "Flashbacks and nightmares affecting my daily life", "label": 1, "category": "trauma"},
    {"text": "Can't stop thinking about traumatic events from my past", "label": 1, "category": "trauma"},
    {"text": "Triggered by certain situations that remind me of trauma", "label": 1, "category": "trauma"},
    
    # Self-esteem and self-image
    {"text": "I hate myself and think I'm worthless", "label": 1, "category": "self_esteem"},
    {"text": "My self-confidence is completely destroyed", "label": 1, "category": "self_esteem"},
    {"text": "I feel inadequate and like a failure at everything", "label": 1, "category": "self_esteem"},
    {"text": "No self-worth and constant negative self-talk", "label": 1, "category": "self_esteem"},
    
    # Substance and coping mechanisms
    {"text": "Using alcohol to cope with my depression", "label": 1, "category": "substance"},
    {"text": "Unhealthy coping mechanisms are taking over my life", "label": 1, "category": "substance"},
    {"text": "Self-medicating to deal with anxiety and pain", "label": 1, "category": "substance"},
    
    # Work and academic struggles
    {"text": "Can't focus on work due to depression and anxiety", "label": 1, "category": "work"},
    {"text": "My academic performance has crashed due to mental health", "label": 1, "category": "work"},
    {"text": "Unable to function at work because of constant sadness", "label": 1, "category": "work"},
    {"text": "Career is suffering because I can't concentrate or care", "label": 1, "category": "work"},
    
    # More Indian context
    {"text": "Family pressure and expectations causing severe stress", "label": 1, "category": "indian_context"},
    {"text": "Struggling with arranged marriage pressure and depression", "label": 1, "category": "indian_context"},
    {"text": "Career expectations from parents making me anxious and sad", "label": 1, "category": "indian_context"},
    {"text": "Feeling trapped by family obligations and cultural expectations", "label": 1, "category": "indian_context"},
    
    # ===== CASUAL/GIBBERISH/NON-DESCRIPTIVE CONTENT (Label: 0) =====
    # Direct casual phrases
    {"text": "bro what should i tell you", "label": 0, "category": "casual_english"},
    {"text": "lol idk what to write here", "label": 0, "category": "casual_english"},
    {"text": "nothing much just chilling", "label": 0, "category": "casual_english"},
    {"text": "hey just testing this app out", "label": 0, "category": "casual_english"},
    {"text": "hello world testing testing", "label": 0, "category": "casual_english"},
    {"text": "sup bro how does this work", "label": 0, "category": "casual_english"},
    {"text": "lmao this is funny af", "label": 0, "category": "casual_english"},
    {"text": "idk man dunno what to say", "label": 0, "category": "casual_english"},
    {"text": "random text here just checking", "label": 0, "category": "casual_english"},
    {"text": "yo what's good with you", "label": 0, "category": "casual_english"},
    
    # Indian casual
    {"text": "yaar kya bolu samajh nahi aa raha", "label": 0, "category": "casual_hindi"},
    {"text": "bhai pata nahi kya likhun", "label": 0, "category": "casual_hindi"},
    {"text": "kuch nahi bas timepass kar raha", "label": 0, "category": "casual_hindi"},
    {"text": "arre yaar kaise batau", "label": 0, "category": "casual_hindi"},
    {"text": "bhai demo hai kya ye", "label": 0, "category": "casual_hindi"},
    
    # Questions without feeling description
    {"text": "what should i write in this box", "label": 0, "category": "question"},
    {"text": "how does this mental health test work", "label": 0, "category": "question"},
    {"text": "can you tell me what to enter here", "label": 0, "category": "question"},
    {"text": "what am i supposed to tell you exactly", "label": 0, "category": "question"},
    {"text": "is this for real or just a demo", "label": 0, "category": "question"},
    {"text": "what information do you need from me", "label": 0, "category": "question"},
    {"text": "how accurate is this assessment tool", "label": 0, "category": "question"},
    
    # Very short non-descriptive
    {"text": "i'm okay", "label": 0, "category": "too_short"},
    {"text": "nothing wrong", "label": 0, "category": "too_short"},
    {"text": "fine thanks", "label": 0, "category": "too_short"},
    {"text": "all good", "label": 0, "category": "too_short"},
    {"text": "not bad", "label": 0, "category": "too_short"},
    
    # Neutral content without feelings
    {"text": "today i went to work and came back home", "label": 0, "category": "neutral"},
    {"text": "i had lunch with my friends at a restaurant", "label": 0, "category": "neutral"},
    {"text": "the weather is nice today and sunny", "label": 0, "category": "neutral"},
    {"text": "i watched a movie last night with family", "label": 0, "category": "neutral"},
    {"text": "my schedule for tomorrow is quite busy", "label": 0, "category": "neutral"},
    
    # Gibberish
    {"text": "asdfgh jklqwerty zxcvbn", "label": 0, "category": "gibberish"},
    {"text": "dnksdnksdds md skdnsk", "label": 0, "category": "gibberish"},
    {"text": "aaaaaaa bbbbbbb cccccc", "label": 0, "category": "gibberish"},
    {"text": "qwerty uiop asdfgh jkl", "label": 0, "category": "gibberish"},
    {"text": "xyzabc defghi jklmno", "label": 0, "category": "gibberish"},
    
    # Testing/demo phrases
    {"text": "just trying out this tool", "label": 0, "category": "testing"},
    {"text": "let me see how this works", "label": 0, "category": "testing"},
    {"text": "checking if the app is functional", "label": 0, "category": "testing"},
    {"text": "this is a test message to see results", "label": 0, "category": "testing"},
    
    # Greetings
    {"text": "hello how are you doing", "label": 0, "category": "greeting"},
    {"text": "hi there good morning", "label": 0, "category": "greeting"},
    {"text": "hey what's up buddy", "label": 0, "category": "greeting"},
    
    # Confused/uncertain responses
    {"text": "i don't know what you want me to say", "label": 0, "category": "confused"},
    {"text": "not sure what information to provide", "label": 0, "category": "confused"},
    {"text": "what kind of response are you expecting", "label": 0, "category": "confused"},
    
    # More casual variations
    {"text": "yo bro just hanging out here", "label": 0, "category": "casual_english"},
    {"text": "lol this is cool lemme try", "label": 0, "category": "casual_english"},
    {"text": "nah man i'm good no worries", "label": 0, "category": "casual_english"},
    {"text": "dude what's this about anyway", "label": 0, "category": "casual_english"},
    {"text": "haha nice app you got here", "label": 0, "category": "casual_english"},
    {"text": "meh whatever doesn't matter", "label": 0, "category": "casual_english"},
    {"text": "bruh moment lmao wtf", "label": 0, "category": "casual_english"},
    {"text": "ayy lmao that's crazy bro", "label": 0, "category": "casual_english"},
    {"text": "yeah yeah sure thing mate", "label": 0, "category": "casual_english"},
    {"text": "nahh fam i'm chilling rn", "label": 0, "category": "casual_english"},
    
    # More Hindi/Hinglish casual
    {"text": "arre bhai chalta hai yaar", "label": 0, "category": "casual_hindi"},
    {"text": "kya scene hai boss", "label": 0, "category": "casual_hindi"},
    {"text": "theek hai yaar sab theek", "label": 0, "category": "casual_hindi"},
    {"text": "bas bhai normal hi hai", "label": 0, "category": "casual_hindi"},
    {"text": "kuch special nahi yaar", "label": 0, "category": "casual_hindi"},
    {"text": "chal theek hai bhai", "label": 0, "category": "casual_hindi"},
    {"text": "dekh lete hain kya hota hai", "label": 0, "category": "casual_hindi"},
    {"text": "pata nahi yaar bas aise hi", "label": 0, "category": "casual_hindi"},
    {"text": "achha theek hai samajh gaya", "label": 0, "category": "casual_hindi"},
    {"text": "haan bhai sab mast hai", "label": 0, "category": "casual_hindi"},
    
    # More gibberish patterns
    {"text": "kjsdhfkjsdhf dskjfhsd ksjdhf", "label": 0, "category": "gibberish"},
    {"text": "mnbvcxz lkjhgfdsa poiuytrewq", "label": 0, "category": "gibberish"},
    {"text": "zzzzzzz xxxxxxx ccccccc", "label": 0, "category": "gibberish"},
    {"text": "qazwsxedc rfvtgbyhn", "label": 0, "category": "gibberish"},
    {"text": "plokmijn uhbygvtfc", "label": 0, "category": "gibberish"},
    {"text": "sdkjnfskdjnf skdnfksd", "label": 0, "category": "gibberish"},
    {"text": "mxnzmxcn zxmcnzxmc", "label": 0, "category": "gibberish"},
    {"text": "qwertyuiop asdfghjkl", "label": 0, "category": "gibberish"},
    {"text": "hhhhh jjjjj kkkkk lllll", "label": 0, "category": "gibberish"},
    {"text": "abcdefgh ijklmnop qrstuv", "label": 0, "category": "gibberish"},
    
    # More questions/meta
    {"text": "what happens if i click submit", "label": 0, "category": "question"},
    {"text": "how long does this test take", "label": 0, "category": "question"},
    {"text": "who made this application", "label": 0, "category": "question"},
    {"text": "is my data secure and private", "label": 0, "category": "question"},
    {"text": "will i get results immediately", "label": 0, "category": "question"},
    {"text": "can i retake this assessment", "label": 0, "category": "question"},
    {"text": "what do you do with my responses", "label": 0, "category": "question"},
    {"text": "how does the algorithm work exactly", "label": 0, "category": "question"},
    
    # More short non-descriptive
    {"text": "meh okay", "label": 0, "category": "too_short"},
    {"text": "yeah sure", "label": 0, "category": "too_short"},
    {"text": "nope nah", "label": 0, "category": "too_short"},
    {"text": "k thx", "label": 0, "category": "too_short"},
    {"text": "cool beans", "label": 0, "category": "too_short"},
    {"text": "alright then", "label": 0, "category": "too_short"},
    {"text": "got it", "label": 0, "category": "too_short"},
    {"text": "sounds good", "label": 0, "category": "too_short"},
    
    # More neutral/factual statements
    {"text": "i work in software development", "label": 0, "category": "neutral"},
    {"text": "my favorite color is blue", "label": 0, "category": "neutral"},
    {"text": "i live in mumbai with my family", "label": 0, "category": "neutral"},
    {"text": "completed my engineering degree last year", "label": 0, "category": "neutral"},
    {"text": "i enjoy playing cricket on weekends", "label": 0, "category": "neutral"},
    {"text": "currently working from home", "label": 0, "category": "neutral"},
    {"text": "my name is john and i'm 25", "label": 0, "category": "neutral"},
    {"text": "planning to visit goa next month", "label": 0, "category": "neutral"},
    
    # More testing/demo phrases
    {"text": "demo mode activated let's see", "label": 0, "category": "testing"},
    {"text": "test test one two three", "label": 0, "category": "testing"},
    {"text": "sample input for testing purposes", "label": 0, "category": "testing"},
    {"text": "trial run to check functionality", "label": 0, "category": "testing"},
    {"text": "experiment with this feature", "label": 0, "category": "testing"},
    
    # More greetings/pleasantries
    {"text": "good evening hope you're well", "label": 0, "category": "greeting"},
    {"text": "namaste how may i help you", "label": 0, "category": "greeting"},
    {"text": "hi hello testing this out", "label": 0, "category": "greeting"},
    {"text": "hey there nice to meet you", "label": 0, "category": "greeting"},
    {"text": "greetings and salutations friend", "label": 0, "category": "greeting"},
    
    # Sarcastic/dismissive (casual)
    {"text": "oh great another mental health thing", "label": 0, "category": "sarcastic"},
    {"text": "sure this will solve all my problems", "label": 0, "category": "sarcastic"},
    {"text": "yeah right like this actually works", "label": 0, "category": "sarcastic"},
    {"text": "wow such helpful much therapy", "label": 0, "category": "sarcastic"},
    
    # Spam-like patterns
    {"text": "click here for more information now", "label": 0, "category": "spam"},
    {"text": "visit our website for best deals", "label": 0, "category": "spam"},
    {"text": "subscribe and hit the bell icon", "label": 0, "category": "spam"},
]


def save_training_data():
    """Save training data in multiple formats."""
    
    # Convert to DataFrame
    df = pd.DataFrame(TRAINING_DATA)
    
    # Save as CSV
    df.to_csv('data/intent_classification_data.csv', index=False)
    print(f"✅ Saved {len(df)} examples to data/intent_classification_data.csv")
    
    # Save as JSON
    with open('data/intent_classification_data.json', 'w', encoding='utf-8') as f:
        json.dump(TRAINING_DATA, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved to data/intent_classification_data.json")
    
    # Print statistics
    print("\n📊 Dataset Statistics:")
    print(f"Total examples: {len(df)}")
    print(f"Genuine mental health (1): {len(df[df['label'] == 1])}")
    print(f"Casual/gibberish (0): {len(df[df['label'] == 0])}")
    print(f"\nCategories breakdown:")
    print(df.groupby(['label', 'category']).size())
    
    return df


if __name__ == "__main__":
    df = save_training_data()
    print("\n✅ Training data created successfully!")
    print("\nSample genuine examples:")
    print(df[df['label'] == 1].head(3)['text'].values)
    print("\nSample casual examples:")
    print(df[df['label'] == 0].head(3)['text'].values)
