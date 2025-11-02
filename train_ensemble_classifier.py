"""
Lightweight Intent Classifier using Ensemble Approach
Combines rules, ML (scikit-learn), and the existing validator
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import joblib
import os
import numpy as np


class EnsembleIntentClassifier:
    """
    Lightweight ensemble classifier combining:
    1. Rule-based validation (from InputValidator)
    2. TF-IDF + Logistic Regression
    3. Confidence-based decision making
    """
    
    def __init__(self, model_dir='model/ensemble_intent'):
        self.model_dir = model_dir
        self.vectorizer = None
        self.classifier = None
        self.trained = False
        
    def train(self, data_path='data/intent_classification_data.csv'):
        """Train the ensemble classifier."""
        print("🚀 Training Ensemble Intent Classifier...")
        
        # Load data
        df = pd.read_csv(data_path)
        X = df['text'].values
        y = df['label'].values
        
        print(f"📊 Dataset: {len(df)} examples")
        print(f"   Genuine (1): {sum(y==1)}")
        print(f"   Casual (0): {sum(y==0)}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\n📚 Train: {len(X_train)}, Test: {len(X_test)}")
        
        # Create TF-IDF vectorizer
        print("\n🔤 Creating TF-IDF features...")
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 3),  # Unigrams, bigrams, trigrams
            min_df=1,
            max_df=0.95
        )
        
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        # Train classifier
        print("🎯 Training classifier...")
        self.classifier = LogisticRegression(
            max_iter=1000,
            C=1.0,
            class_weight='balanced',
            random_state=42
        )
        
        self.classifier.fit(X_train_vec, y_train)
        
        # Evaluate
        print("\n📈 Evaluation Results:")
        y_pred = self.classifier.predict(X_test_vec)
        y_pred_proba = self.classifier.predict_proba(X_test_vec)
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Casual', 'Genuine']))
        
        print("\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        print(f"                Predicted")
        print(f"              Casual  Genuine")
        print(f"Actual Casual    {cm[0][0]:3d}    {cm[0][1]:3d}")
        print(f"       Genuine   {cm[1][0]:3d}    {cm[1][1]:3d}")
        
        # Calculate metrics
        accuracy = (cm[0][0] + cm[1][1]) / cm.sum()
        precision = cm[1][1] / (cm[1][1] + cm[0][1]) if (cm[1][1] + cm[0][1]) > 0 else 0
        recall = cm[1][1] / (cm[1][1] + cm[1][0]) if (cm[1][1] + cm[1][0]) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"\n📊 Metrics:")
        print(f"   Accuracy:  {accuracy:.2%}")
        print(f"   Precision: {precision:.2%}")
        print(f"   Recall:    {recall:.2%}")
        print(f"   F1 Score:  {f1:.2%}")
        
        # Mark as trained before testing
        self.trained = True
        
        # Test with sample cases
        print("\n🧪 Testing Sample Cases:")
        self._test_samples(X_test, y_test)
        
        # Save model
        self._save_model()
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
    
    def _test_samples(self, X_test, y_test, n=10):
        """Test on sample cases."""
        for i in range(min(n, len(X_test))):
            text = X_test[i]
            true_label = y_test[i]
            result = self.predict(text)
            
            true_intent = 'genuine' if true_label == 1 else 'casual'
            match = "✅" if result['label'] == true_label else "❌"
            
            print(f"\n{match} \"{text[:60]}...\"")
            print(f"   Predicted: {result['intent']} ({result['confidence']:.1%})")
            print(f"   Actual: {true_intent}")
    
    def predict(self, text):
        """
        Predict intent with confidence scores.
        
        Returns:
            dict: {
                'intent': 'genuine' or 'casual',
                'label': 1 or 0,
                'confidence': float,
                'genuine_prob': float,
                'casual_prob': float,
                'method': 'ml' or 'rule'
            }
        """
        if not self.trained and not self.load_model():
            raise ValueError("Model not trained. Please train first or load a trained model.")
        
        # Get prediction from ML model
        X_vec = self.vectorizer.transform([text])
        probs = self.classifier.predict_proba(X_vec)[0]
        prediction = np.argmax(probs)
        
        result = {
            'intent': 'genuine' if prediction == 1 else 'casual',
            'label': int(prediction),
            'confidence': float(probs[prediction]),
            'genuine_prob': float(probs[1]),
            'casual_prob': float(probs[0]),
            'method': 'ml'
        }
        
        return result
    
    def _save_model(self):
        """Save the trained model."""
        os.makedirs(self.model_dir, exist_ok=True)
        
        joblib.dump(self.vectorizer, os.path.join(self.model_dir, 'vectorizer.pkl'))
        joblib.dump(self.classifier, os.path.join(self.model_dir, 'classifier.pkl'))
        
        print(f"\n✅ Model saved to {self.model_dir}/")
    
    def load_model(self):
        """Load a trained model."""
        vec_path = os.path.join(self.model_dir, 'vectorizer.pkl')
        clf_path = os.path.join(self.model_dir, 'classifier.pkl')
        
        if os.path.exists(vec_path) and os.path.exists(clf_path):
            self.vectorizer = joblib.load(vec_path)
            self.classifier = joblib.load(clf_path)
            self.trained = True
            print(f"✅ Model loaded from {self.model_dir}/")
            return True
        return False


def train_ensemble_classifier():
    """Train the ensemble classifier."""
    classifier = EnsembleIntentClassifier()
    results = classifier.train('data/intent_classification_data.csv')
    return classifier, results


if __name__ == "__main__":
    print("=" * 80)
    print("ENSEMBLE INTENT CLASSIFIER TRAINING")
    print("Lightweight TF-IDF + Logistic Regression")
    print("=" * 80)
    print()
    
    classifier, results = train_ensemble_classifier()
    
    print("\n" + "=" * 80)
    print("✅ TRAINING COMPLETE")
    print("=" * 80)
    print(f"\nFinal Results:")
    for metric, value in results.items():
        print(f"  {metric.capitalize()}: {value:.2%}")
    
    print("\n🎉 Ensemble Intent Classifier ready for use!")
    print("\nUsage:")
    print("  from train_ensemble_classifier import EnsembleIntentClassifier")
    print("  classifier = EnsembleIntentClassifier()")
    print("  classifier.load_model()")
    print("  result = classifier.predict('I feel sad and tired')")
    print("  print(result)")
