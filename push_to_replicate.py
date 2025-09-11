"""
Push model directly to Replicate using Python
"""

import os
import subprocess
import sys

def try_cog_push():
    """Try to push using cog command"""
    print("🚀 Attempting to push to Replicate...")
    
    try:
        # Try to run cog push
        result = subprocess.run([
            "python", "-m", "cog", "push", "r8.im/tejasbhosale-git/legal-nlp-pipeline"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("✅ Successfully pushed to Replicate!")
            print(result.stdout)
            return True
        else:
            print("❌ Cog push failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_files():
    """Check if required files exist"""
    required_files = ["predict.py", "cog.yaml", "requirements.txt"]
    
    print("🔍 Checking required files...")
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            return False
    
    return True

def main():
    """Main function"""
    print("🚀 ContractBERT Replicate Push")
    print("=" * 50)
    
    # Check files
    if not check_files():
        print("❌ Missing required files. Cannot proceed.")
        return
    
    # Try cog push
    if try_cog_push():
        print("\n🎉 Model pushed successfully!")
        print("⏳ Wait 5-10 minutes for deployment to complete")
        print("🧪 Then test with: python final_test.py")
    else:
        print("\n💡 Alternative solutions:")
        print("1. Check Replicate Settings tab for manual deploy button")
        print("2. Try creating a new model on Replicate")
        print("3. Contact Replicate support")

if __name__ == "__main__":
    main()
