"""
Two-Stage Intent Classification Model
Stage 1: Genuine Mental Health Content vs Casual/Gibberish
Stage 2: Depression Assessment (only if Stage 1 = genuine)
"""

import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import os


class IntentDataset(Dataset):
    """Custom dataset for intent classification."""
    
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }


class IntentClassifier:
    """Two-stage classification system for intent detection."""
    
    def __init__(self, model_path='model/intent_classifier'):
        self.model_path = model_path
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
    def train(self, data_path='data/intent_classification_data.csv', epochs=3, batch_size=16):
        """Train the intent classifier."""
        print("🚀 Starting Intent Classifier Training...")
        print(f"Device: {self.device}")
        
        # Load data
        df = pd.read_csv(data_path)
        print(f"\n📊 Loaded {len(df)} examples")
        print(f"   Genuine (1): {len(df[df['label'] == 1])}")
        print(f"   Casual (0): {len(df[df['label'] == 0])}")
        
        # Split data
        train_texts, val_texts, train_labels, val_labels = train_test_split(
            df['text'].values,
            df['label'].values,
            test_size=0.2,
            random_state=42,
            stratify=df['label'].values
        )
        
        print(f"\n📚 Train: {len(train_texts)}, Validation: {len(val_texts)}")
        
        # Create datasets
        train_dataset = IntentDataset(train_texts, train_labels, self.tokenizer)
        val_dataset = IntentDataset(val_texts, val_labels, self.tokenizer)
        
        # Initialize model
        self.model = DistilBertForSequenceClassification.from_pretrained(
            'distilbert-base-uncased',
            num_labels=2
        )
        self.model.to(self.device)
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir='./results_intent',
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            warmup_steps=100,
            weight_decay=0.01,
            logging_dir='./logs_intent',
            logging_steps=10,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
        )
        
        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            compute_metrics=self.compute_metrics
        )
        
        # Train
        print("\n🎯 Training model...")
        trainer.train()
        
        # Evaluate
        print("\n📈 Evaluating model...")
        eval_results = trainer.evaluate()
        print(f"\nValidation Results:")
        for key, value in eval_results.items():
            print(f"  {key}: {value:.4f}")
        
        # Test predictions
        print("\n🧪 Testing predictions...")
        self.test_predictions(val_texts[:10], val_labels[:10])
        
        # Save model
        os.makedirs(self.model_path, exist_ok=True)
        self.model.save_pretrained(self.model_path)
        self.tokenizer.save_pretrained(self.model_path)
        print(f"\n✅ Model saved to {self.model_path}")
        
        return eval_results
    
    def compute_metrics(self, pred):
        """Compute evaluation metrics."""
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)
        precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
        acc = accuracy_score(labels, preds)
        cm = confusion_matrix(labels, preds)
        
        return {
            'accuracy': acc,
            'f1': f1,
            'precision': precision,
            'recall': recall,
        }
    
    def load_model(self):
        """Load trained model."""
        if os.path.exists(self.model_path):
            self.model = DistilBertForSequenceClassification.from_pretrained(self.model_path)
            self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_path)
            self.model.to(self.device)
            self.model.eval()
            print(f"✅ Intent classifier loaded from {self.model_path}")
            return True
        return False
    
    def predict(self, text):
        """
        Predict intent: genuine (1) or casual (0).
        
        Returns:
            dict: {
                'intent': 'genuine' or 'casual',
                'label': 1 or 0,
                'confidence': float,
                'genuine_prob': float,
                'casual_prob': float
            }
        """
        if self.model is None:
            if not self.load_model():
                raise ValueError("Model not trained or loaded")
        
        self.model.eval()
        
        # Tokenize
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=128,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)
        
        # Predict
        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=1).cpu().numpy()[0]
            prediction = np.argmax(probs)
        
        return {
            'intent': 'genuine' if prediction == 1 else 'casual',
            'label': int(prediction),
            'confidence': float(probs[prediction]),
            'genuine_prob': float(probs[1]),
            'casual_prob': float(probs[0])
        }
    
    def test_predictions(self, texts, true_labels):
        """Test predictions on sample data."""
        print("\nSample Predictions:")
        print("-" * 80)
        
        for text, true_label in zip(texts, true_labels):
            result = self.predict(text)
            true_intent = 'genuine' if true_label == 1 else 'casual'
            match = "✅" if result['label'] == true_label else "❌"
            
            print(f"{match} Text: {text[:60]}...")
            print(f"   Predicted: {result['intent']} ({result['confidence']:.2%})")
            print(f"   Actual: {true_intent}")
            print()


def train_intent_classifier():
    """Main training function."""
    classifier = IntentClassifier()
    results = classifier.train(
        data_path='data/intent_classification_data.csv',
        epochs=4,
        batch_size=16
    )
    return classifier, results


if __name__ == "__main__":
    print("=" * 80)
    print("INTENT CLASSIFICATION MODEL TRAINING")
    print("Stage 1: Genuine Mental Health vs Casual Text")
    print("=" * 80)
    print()
    
    classifier, results = train_intent_classifier()
    
    print("\n" + "=" * 80)
    print("✅ TRAINING COMPLETE")
    print("=" * 80)
    print("\nTest the model:")
    print('  from train_intent_classifier import IntentClassifier')
    print('  classifier = IntentClassifier()')
    print('  classifier.load_model()')
    print('  result = classifier.predict("I feel sad and hopeless")')
    print('  print(result)')
