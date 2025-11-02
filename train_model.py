"""
Training script for fine-tuning DistilBERT on mental health screening data.
Industry best practices: proper data splits, evaluation metrics, early stopping, model checkpointing.
"""

import os
import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import (
    DistilBertForSequenceClassification,
    DistilBertTokenizer,
    get_linear_schedule_with_warmup,
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report,
)
import pandas as pd
import numpy as np
from tqdm import tqdm
import json
from config import MODEL_DIR, TOKENIZER_NAME


class MentalHealthDataset(Dataset):
    """PyTorch Dataset for mental health text classification."""

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
            padding="max_length",
            truncation=True,
            return_attention_mask=True,
            return_tensors="pt",
        )

        return {
            "input_ids": encoding["input_ids"].flatten(),
            "attention_mask": encoding["attention_mask"].flatten(),
            "labels": torch.tensor(label, dtype=torch.long),
        }


def load_data(data_path):
    """
    Load training data from CSV.
    Expected format: 'text' column for input, 'label' column for binary labels (0=low risk, 1=high risk).

    Args:
        data_path (str): Path to CSV file.

    Returns:
        tuple: (texts, labels) as lists.
    """
    df = pd.read_csv(data_path)

    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError(
            "CSV must contain 'text' and 'label' columns. "
            "Labels should be 0 (low risk) or 1 (high risk)."
        )

    texts = df["text"].tolist()
    labels = df["label"].tolist()

    print(f"Loaded {len(texts)} samples from {data_path}")
    print(f"Label distribution: {pd.Series(labels).value_counts().to_dict()}")

    return texts, labels


def evaluate_model(model, dataloader, device):
    """
    Evaluate model on validation/test set.

    Args:
        model: The model to evaluate.
        dataloader: DataLoader for evaluation data.
        device: torch device.

    Returns:
        dict: Dictionary containing evaluation metrics.
    """
    model.eval()
    all_preds = []
    all_labels = []
    total_loss = 0

    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Evaluating"):
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            outputs = model(
                input_ids=input_ids, attention_mask=attention_mask, labels=labels
            )

            loss = outputs.loss
            logits = outputs.logits

            total_loss += loss.item()
            preds = torch.argmax(logits, dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_labels.extend(labels.cpu().numpy())

    accuracy = accuracy_score(all_labels, all_preds)
    precision, recall, f1, _ = precision_recall_fscore_support(
        all_labels, all_preds, average="binary"
    )
    conf_matrix = confusion_matrix(all_labels, all_preds)

    metrics = {
        "loss": total_loss / len(dataloader),
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "confusion_matrix": conf_matrix.tolist(),
    }

    return metrics


def train_model(
    train_data_path,
    output_dir=MODEL_DIR,
    epochs=3,
    batch_size=16,
    learning_rate=2e-5,
    max_length=128,
    validation_split=0.2,
    seed=42,
):
    """
    Train DistilBERT for mental health risk classification.

    Args:
        train_data_path (str): Path to training CSV file.
        output_dir (str): Directory to save the fine-tuned model.
        epochs (int): Number of training epochs.
        batch_size (int): Training batch size.
        learning_rate (float): Learning rate for AdamW optimizer.
        max_length (int): Maximum sequence length for tokenization.
        validation_split (float): Fraction of data to use for validation.
        seed (int): Random seed for reproducibility.
    """
    # Set random seeds for reproducibility
    torch.manual_seed(seed)
    np.random.seed(seed)

    # Setup device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load data
    texts, labels = load_data(train_data_path)

    # Train/validation split
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=validation_split, random_state=seed, stratify=labels
    )

    print(f"\nTrain set: {len(train_texts)} samples")
    print(f"Validation set: {len(val_texts)} samples")

    # Load tokenizer and model
    print(f"\nLoading tokenizer: {TOKENIZER_NAME}")
    tokenizer = DistilBertTokenizer.from_pretrained(TOKENIZER_NAME)

    print("Loading DistilBERT model...")
    model = DistilBertForSequenceClassification.from_pretrained(
        TOKENIZER_NAME, num_labels=2
    )
    model.to(device)

    # Create datasets
    train_dataset = MentalHealthDataset(train_texts, train_labels, tokenizer, max_length)
    val_dataset = MentalHealthDataset(val_texts, val_labels, tokenizer, max_length)

    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    # Setup optimizer and scheduler
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    total_steps = len(train_loader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=0, num_training_steps=total_steps
    )

    # Training loop
    print("\n" + "=" * 50)
    print("Starting training...")
    print("=" * 50)

    best_val_f1 = 0
    training_stats = []

    for epoch in range(epochs):
        print(f"\nEpoch {epoch + 1}/{epochs}")
        print("-" * 50)

        # Training phase
        model.train()
        total_train_loss = 0

        for batch in tqdm(train_loader, desc="Training"):
            optimizer.zero_grad()

            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            outputs = model(
                input_ids=input_ids, attention_mask=attention_mask, labels=labels
            )

            loss = outputs.loss
            total_train_loss += loss.item()

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()

        avg_train_loss = total_train_loss / len(train_loader)

        # Validation phase
        val_metrics = evaluate_model(model, val_loader, device)

        print(f"\nTraining Loss: {avg_train_loss:.4f}")
        print(f"Validation Loss: {val_metrics['loss']:.4f}")
        print(f"Validation Accuracy: {val_metrics['accuracy']:.4f}")
        print(f"Validation Precision: {val_metrics['precision']:.4f}")
        print(f"Validation Recall: {val_metrics['recall']:.4f}")
        print(f"Validation F1: {val_metrics['f1']:.4f}")

        # Save best model
        if val_metrics["f1"] > best_val_f1:
            best_val_f1 = val_metrics["f1"]
            print(f"\n✓ New best F1 score: {best_val_f1:.4f}. Saving model...")

            os.makedirs(output_dir, exist_ok=True)
            model.save_pretrained(output_dir)
            tokenizer.save_pretrained(output_dir)

            # Save training metadata
            metadata = {
                "epoch": epoch + 1,
                "best_val_f1": best_val_f1,
                "val_metrics": {
                    k: v for k, v in val_metrics.items() if k != "confusion_matrix"
                },
                "training_params": {
                    "epochs": epochs,
                    "batch_size": batch_size,
                    "learning_rate": learning_rate,
                    "max_length": max_length,
                },
            }

            with open(os.path.join(output_dir, "training_metadata.json"), "w") as f:
                json.dump(metadata, f, indent=2)

        training_stats.append(
            {
                "epoch": epoch + 1,
                "train_loss": avg_train_loss,
                "val_loss": val_metrics["loss"],
                "val_accuracy": val_metrics["accuracy"],
                "val_f1": val_metrics["f1"],
            }
        )

    print("\n" + "=" * 50)
    print("Training completed!")
    print(f"Best validation F1 score: {best_val_f1:.4f}")
    print(f"Model saved to: {output_dir}")
    print("=" * 50)

    return training_stats


if __name__ == "__main__":
    # Example usage
    # Prepare your data in CSV format with 'text' and 'label' columns
    # Labels: 0 = low risk, 1 = high risk

    TRAIN_DATA_PATH = "data/training_data.csv"

    if not os.path.exists(TRAIN_DATA_PATH):
        print(f"Error: Training data not found at {TRAIN_DATA_PATH}")
        print("\nPlease create a CSV file with the following format:")
        print("text,label")
        print('"I feel happy and motivated",0')
        print('"I want to end it all",1')
        print("\nLabels: 0 = low risk, 1 = high risk")
    else:
        training_stats = train_model(
            train_data_path=TRAIN_DATA_PATH,
            epochs=3,
            batch_size=16,
            learning_rate=2e-5,
            max_length=128,
            validation_split=0.2,
        )
