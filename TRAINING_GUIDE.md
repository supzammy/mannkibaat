# Training Guide for MannKiBaat Mental Health Screening Model

## Overview
This guide explains how to train the DistilBERT model for mental health risk assessment.

## Prerequisites
- Python 3.12+
- CUDA-compatible GPU (recommended) or CPU
- Training data in CSV format

## Training Data Format

Create a CSV file with two columns:
- `text`: The input text (user's mental health description)
- `label`: Binary label (0 = low risk, 1 = high/medium risk)

Example:
```csv
text,label
"I feel happy and motivated",0
"I feel hopeless and alone",1
"I'm stressed but managing",1
```

## Steps to Train the Model

### 1. Generate Sample Data (Optional)
If you don't have real training data yet, generate sample data:

```bash
python generate_sample_data.py
```

This creates `data/training_data.csv` with 1000 synthetic samples.

**⚠️ Important**: Replace with real, ethically-sourced, labeled data for production use.

### 2. Prepare Your Training Data
Place your CSV file at `data/training_data.csv` or modify the path in `train_model.py`.

### 3. Run Training

```bash
python train_model.py
```

Training parameters (can be modified in `train_model.py`):
- **Epochs**: 3 (default)
- **Batch Size**: 16
- **Learning Rate**: 2e-5
- **Max Sequence Length**: 128
- **Validation Split**: 20%

### 4. Monitor Training
The script will display:
- Training loss per epoch
- Validation metrics (accuracy, precision, recall, F1)
- Best model checkpoint saves automatically

### 5. Training Output
After training, the following will be saved to `model/fine_tuned_model/`:
- `pytorch_model.bin` - Model weights
- `config.json` - Model configuration
- `tokenizer_config.json` - Tokenizer settings
- `vocab.txt` - Vocabulary
- `training_metadata.json` - Training metrics and parameters

## Training Time Estimates
- **CPU**: 30-60 minutes for 1000 samples (3 epochs)
- **GPU (CUDA)**: 5-10 minutes for 1000 samples (3 epochs)

## Best Practices

### Data Quality
1. **Balanced Dataset**: Aim for balanced representation of risk levels
2. **Data Size**: Minimum 500-1000 samples, ideally 5000+ for production
3. **Data Privacy**: Ensure all data is anonymized and ethically sourced
4. **Label Quality**: Use expert mental health professionals for labeling

### Model Evaluation
- **F1 Score**: Primary metric (balances precision and recall)
- **Recall**: Critical for mental health (don't miss high-risk cases)
- **Precision**: Important to avoid false alarms

### Production Deployment
1. Achieve validation F1 > 0.85 before production use
2. Test on held-out test set
3. Implement human review for high-risk predictions
4. Regular model retraining with new data
5. Monitor model performance in production

## Ethical Considerations

⚠️ **Critical**: This model is a screening tool, NOT a diagnostic tool.
- Always include human mental health professionals in the workflow
- Provide crisis helpline information with all predictions
- Ensure user privacy and data protection
- Regular audits for bias and fairness
- Clear disclaimers about limitations

## Customization

### Adjust Hyperparameters
Edit `train_model.py` to modify:
```python
training_stats = train_model(
    train_data_path=TRAIN_DATA_PATH,
    epochs=5,              # Increase for better performance
    batch_size=32,         # Increase if you have more GPU memory
    learning_rate=3e-5,    # Tune based on validation performance
    max_length=256,        # Increase for longer texts
    validation_split=0.2,
)
```

### Multi-class Classification
To classify into Low/Medium/High risk:
1. Update labels in data (0=Low, 1=Medium, 2=High)
2. Modify `num_labels=3` in `train_model.py`
3. Update `config.py` thresholds accordingly

## Troubleshooting

### Out of Memory (OOM)
- Reduce batch_size to 8 or 4
- Reduce max_length to 64 or 128
- Use gradient accumulation

### Poor Performance
- Increase training data size
- Increase epochs (5-10)
- Adjust learning rate
- Check data quality and balance
- Use stratified validation split

### Model Not Loading
- Check `model/fine_tuned_model/` contains all required files
- Verify file permissions
- Check PyTorch/Transformers version compatibility

## Next Steps

After successful training:
1. Evaluate on test set: Create `evaluate_model.py` script
2. Test the Streamlit app: `streamlit run app.py`
3. Monitor predictions and collect feedback
4. Plan for regular model updates

## Support

For issues or questions:
1. Check error messages and logs
2. Verify data format matches requirements
3. Ensure all dependencies are installed
4. Review training metrics for anomalies
