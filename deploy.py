"""
Deployment script for ContractBERT on Replicate
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    # Check if replicate CLI is installed
    try:
        result = subprocess.run(["replicate", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Replicate CLI is installed")
        else:
            print("❌ Replicate CLI not found")
            return False
    except FileNotFoundError:
        print("❌ Replicate CLI not found")
        print("Install it with: npm install -g @replicate/cli")
        return False
    
    # Check if Docker is available
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is available")
        else:
            print("❌ Docker not found")
            return False
    except FileNotFoundError:
        print("❌ Docker not found")
        print("Please install Docker to build the container")
        return False
    
    return True

def check_api_token():
    """Check if API token is set"""
    token = os.environ.get("REPLICATE_API_TOKEN")
    if token:
        print("✅ REPLICATE_API_TOKEN is set")
        return True
    else:
        print("❌ REPLICATE_API_TOKEN not set")
        print("Please set your API token:")
        print("export REPLICATE_API_TOKEN=your_token_here")
        return False

def build_and_deploy():
    """Build and deploy the model to Replicate"""
    print("\n🚀 Building and deploying to Replicate...")
    
    try:
        # Deploy using replicate CLI
        result = subprocess.run(
            ["replicate", "deploy"],
            cwd=Path.cwd(),
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Deployment successful!")
            print(result.stdout)
            
            # Try to extract model name from output
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if 'your-username' in line or 'model' in line.lower():
                    print(f"📝 Model URL: {line.strip()}")
                    break
                    
        else:
            print("❌ Deployment failed!")
            print("Error:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during deployment: {e}")
        return False
    
    return True

def create_env_file():
    """Create a .env file template"""
    env_content = """# Replicate API Configuration
REPLICATE_API_TOKEN=your_token_here

# Optional: Model configuration
MODEL_NAME=your-username/contractbert:latest
"""
    
    with open(".env.example", "w") as f:
        f.write(env_content)
    
    print("📝 Created .env.example file")
    print("Copy it to .env and fill in your actual values")

def main():
    """Main deployment function"""
    print("🚀 ContractBERT Replicate Deployment")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements not met. Please install missing tools.")
        return
    
    # Check API token
    if not check_api_token():
        print("\n❌ API token not set. Please set REPLICATE_API_TOKEN.")
        return
    
    # Create environment file template
    create_env_file()
    
    # Build and deploy
    if build_and_deploy():
        print("\n🎉 Deployment completed successfully!")
        print("\n📝 Next steps:")
        print("1. Note your model URL from the output above")
        print("2. Update client_example.py with your model name")
        print("3. Test the API using the client example")
        print("4. Integrate into your application")
    else:
        print("\n❌ Deployment failed. Check the error messages above.")

if __name__ == "__main__":
    main()
