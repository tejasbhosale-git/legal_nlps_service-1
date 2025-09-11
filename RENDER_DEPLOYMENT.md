# ContractBERT Render Deployment Guide

## 🚀 Deploy to Render (Much Easier than Replicate!)

### Step 1: Create New GitHub Repository
1. Go to [GitHub.com](https://github.com) and create a new repository
2. Name it: `contractbert-render`
3. Make it **PUBLIC**
4. Don't initialize with README

### Step 2: Push Your Code
```bash
git remote add origin https://github.com/YOURUSERNAME/contractbert-render.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Render
1. Go to [Render.com](https://render.com)
2. Sign up/Login with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository: `contractbert-render`
5. Configure:
   - **Name**: `contractbert-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python predict.py`
   - **Plan**: `Starter` (Free)

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Get your API URL: `https://your-app-name.onrender.com`

### Step 5: Test Your API
```python
import requests

# Test your deployed API
response = requests.post(
    "https://your-app-name.onrender.com/predict",
    json={
        "text": "This contract is between Company A and Company B.",
        "task": "classification"
    }
)

print(response.json())
```

## 🎯 Benefits of Render over Replicate:
- ✅ **Easier deployment** - No complex Cog setup
- ✅ **Free tier available** - No cost for testing
- ✅ **Simple Flask API** - Standard REST endpoints
- ✅ **GitHub integration** - Automatic deployments
- ✅ **Better for APIs** - Designed for web services

## 📁 Files Ready for Render:
- ✅ `predict.py` - Flask API with ContractBERT
- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render configuration
- ✅ `test_render_api.py` - Test script

**Ready to deploy!** 🚀
