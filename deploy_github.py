"""
Deploy to Replicate using GitHub method
"""

import os
import subprocess
import json

def create_git_repo():
    """Initialize git repository and prepare for GitHub"""
    print("🔧 Setting up Git repository...")
    
    try:
        # Initialize git
        subprocess.run(["git", "init"], check=True, capture_output=True)
        print("✅ Git repository initialized")
        
        # Add files
        subprocess.run(["git", "add", "predict.py", "cog.yaml", "requirements.txt"], check=True)
        print("✅ Files added to git")
        
        # Commit
        subprocess.run(["git", "commit", "-m", "Initial ContractBERT deployment"], check=True)
        print("✅ Files committed")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git setup failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Git not found. Please install Git first.")
        return False

def show_github_instructions():
    """Show instructions for GitHub deployment"""
    print("\n📋 GitHub Deployment Instructions:")
    print("=" * 50)
    print("1. Go to https://github.com and create a new repository")
    print("2. Name it: contractbert-replicate")
    print("3. Make it PUBLIC (required for Replicate)")
    print("4. Don't initialize with README")
    print("5. Copy the repository URL")
    print("\n6. Run these commands:")
    print("   git remote add origin https://github.com/YOURUSERNAME/contractbert-replicate.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print("\n7. Go back to Replicate Settings tab")
    print("8. Enter your GitHub URL in the repository field")
    print("9. Click Deploy!")

def main():
    """Main deployment function"""
    print("🚀 ContractBERT GitHub Deployment Setup")
    print("=" * 50)
    
    # Check if git is available
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git not found. Please install Git first:")
        print("   Download from: https://git-scm.com/download/win")
        return
    
    # Set up git repository
    if create_git_repo():
        show_github_instructions()
    else:
        print("\n💡 Alternative: Manual file upload")
        print("1. Create a GitHub repository manually")
        print("2. Upload predict.py, cog.yaml, requirements.txt")
        print("3. Connect to Replicate")

if __name__ == "__main__":
    main()
