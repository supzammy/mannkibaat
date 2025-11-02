"""
Sample data generator for mental health screening model training.
Creates synthetic training data for demonstration purposes.
"""

import pandas as pd
import random


def generate_sample_data(num_samples=1000, output_path="data/training_data.csv"):
    """
    Generate sample mental health screening data for training.
    In production, replace this with real, labeled data.

    Args:
        num_samples (int): Number of samples to generate.
        output_path (str): Path to save the CSV file.
    """
    # Sample texts for different risk levels
    low_risk_texts = [
        "I'm feeling good today and looking forward to the weekend",
        "Had a productive day at work, feeling satisfied",
        "Spent time with friends and family, feeling grateful",
        "I'm excited about my new project",
        "Things are going well, I'm optimistic about the future",
        "I feel motivated and energized",
        "Today was a great day, I'm feeling happy",
        "I'm managing my stress well with exercise",
        "I feel content and at peace",
        "Life has its ups and downs but I'm doing okay",
    ]

    high_risk_texts = [
        "I feel hopeless and don't see a way out",
        "I can't take this anymore, everything feels pointless",
        "I wish I could just disappear",
        "Nobody would miss me if I was gone",
        "I feel completely alone and worthless",
        "I don't want to wake up tomorrow",
        "The pain is too much to bear",
        "I'm having thoughts of ending it all",
        "Life has no meaning anymore",
        "I feel trapped with no escape",
    ]

    medium_risk_texts = [
        "I've been feeling down lately, things are tough",
        "I'm stressed and anxious most of the time",
        "I feel overwhelmed by everything",
        "I'm having trouble sleeping and concentrating",
        "I feel sad more often than not",
        "I'm worried about my mental health",
        "I feel disconnected from people around me",
        "I'm struggling to find motivation",
        "Things don't bring me joy like they used to",
        "I feel exhausted and empty inside",
    ]

    data = []

    # Generate low risk samples (40%)
    for _ in range(int(num_samples * 0.4)):
        text = random.choice(low_risk_texts)
        # Add slight variations
        text = text + random.choice(["", ".", " lately", " recently"])
        data.append({"text": text, "label": 0})

    # Generate high risk samples (30%)
    for _ in range(int(num_samples * 0.3)):
        text = random.choice(high_risk_texts)
        text = text + random.choice(["", ".", " anymore", " constantly"])
        data.append({"text": text, "label": 1})

    # Generate medium risk samples (30%)
    for _ in range(int(num_samples * 0.3)):
        text = random.choice(medium_risk_texts)
        text = text + random.choice(["", ".", " every day", " often"])
        # Medium risk texts mapped to high risk (1) for binary classification
        # Adjust based on your classification strategy
        data.append({"text": text, "label": 1})

    # Shuffle the data
    random.shuffle(data)

    # Create DataFrame and save
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)

    print(f"Generated {len(data)} samples and saved to {output_path}")
    print(f"\nLabel distribution:")
    print(df["label"].value_counts())
    print(f"\nSample data preview:")
    print(df.head(10))


if __name__ == "__main__":
    import os

    os.makedirs("data", exist_ok=True)
    generate_sample_data(num_samples=1000, output_path="data/training_data.csv")
