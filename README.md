# ContractBERT on Replicate

This project deploys ContractBERT (or a legal BERT model) on Replicate for contract analysis and legal text processing.

## 🚀 Quick Start

### 1. Deploy to Replicate

1. **Install Replicate CLI**:
   ```bash
   npm install -g @replicate/cli
   ```

2. **Login to Replicate**:
   ```bash
   replicate login
   ```

3. **Deploy the model**:
   ```bash
   replicate deploy
   ```

### 2. Get Your API Token

1. Go to [Replicate Account Settings](https://replicate.com/account/api-tokens)
2. Create a new API token
3. Copy the token for use in your applications

### 3. Use the API

Once deployed, you can use the model via Replicate's API:

```python
import replicate

# Set your API token
replicate.Client(api_token="your_token_here")

# Run the model
output = replicate.run(
    "your-username/contractbert:latest",
    input={
        "text": "This contract agreement is between...",
        "task": "classification"
    }
)
```

## 📁 Project Structure

```
├── Dockerfile          # Container configuration
├── predict.py          # Main prediction script
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── client_example.py  # Example client code
```

## 🔧 Configuration

### Model Selection

The current setup uses `nlpaueb/legal-bert-base-uncased` as the base model. To use a different ContractBERT model:

1. Update the `model_name` in `predict.py`:
   ```python
   model_name = "your-preferred/contractbert-model"
   ```

2. Adjust the `num_labels` parameter based on your model's output classes

### Input Parameters

The API accepts the following parameters:

- `text` (required): The contract text to analyze
- `task` (optional): The type of analysis task (default: "classification")

### Output Format

```json
{
    "predicted_class": 1,
    "confidence": 0.95,
    "class_probabilities": [0.05, 0.95],
    "input_text": "Your input text...",
    "task": "classification"
}
```

## 🛠️ Local Development

### Test Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the prediction script**:
   ```bash
   python predict.py
   ```

3. **Test with curl**:
   ```bash
   curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"text": "This is a sample contract clause.", "task": "classification"}'
   ```

### Environment Variables

- `REPLICATE_API_TOKEN`: Your Replicate API token
- `PORT`: Port for local development (default: 5000)

## 📊 Model Performance

The deployed model provides:
- Text classification for legal documents
- Confidence scores for predictions
- Support for various legal text analysis tasks

## 🔒 Security Notes

- Never commit API tokens to version control
- Use environment variables for sensitive data
- The model runs in a secure containerized environment on Replicate

## 📞 Support

For issues with:
- **Replicate deployment**: Check [Replicate Documentation](https://replicate.com/docs)
- **Model performance**: Verify the model name and parameters in `predict.py`
- **API usage**: See `client_example.py` for usage examples

## 🚀 Next Steps

1. Deploy to Replicate using the CLI
2. Test the API with sample contract text
3. Integrate into your application using the provided client code
4. Monitor usage and performance through Replicate's dashboard
