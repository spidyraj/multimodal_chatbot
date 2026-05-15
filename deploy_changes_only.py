#!/usr/bin/env python3
"""
Deploy only the changed files to avoid full rebuild
"""
import os
import shutil
from pathlib import Path

def create_deployment_package():
    """Create a package with only changed files"""
    
    print("🚀 Creating deployment package with only changed files...")
    
    # Create deployment directory
    deploy_dir = Path("deployment_changes")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # Files that were changed
    changed_files = {
        # Backend changes
        "backend/schemas/youtube_schema.py": "schemas/youtube_schema.py",
        "backend/services/youtube_service.py": "services/youtube_service.py", 
        "backend/api/routes/youtube.py": "api/routes/youtube.py",
        
        # Frontend changes
        "frontend/src/services/api.js": "frontend/src/services/api.js",
        "frontend/src/pages/Chat.jsx": "frontend/src/pages/Chat.jsx",
    }
    
    print("\n📁 Copying changed files:")
    
    for source, dest in changed_files.items():
        source_path = Path(source)
        dest_path = deploy_dir / dest
        
        if source_path.exists():
            # Create destination directory if needed
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy the file
            shutil.copy2(source_path, dest_path)
            print(f"  ✅ {source} -> {dest}")
        else:
            print(f"  ❌ {source} not found")
    
    # Create deployment instructions
    instructions = """
# 🚀 DEPLOYMENT INSTRUCTIONS

## 📋 CHANGED FILES TO DEPLOY:

### Backend Changes:
1. schemas/youtube_schema.py - Added video_id field to fix schema mismatch
2. services/youtube_service.py - Enhanced with better error handling and video title support
3. api/routes/youtube.py - Updated to pass video_title in response

### Frontend Changes:
4. frontend/src/services/api.js - Added sendMessageWithFile for chat file upload
5. frontend/src/pages/Chat.jsx - Enhanced with PDF upload directly in chat

## 🛠️ DEPLOYMENT STEPS:

### Option 1: Direct File Replacement (Recommended)
1. Copy backend files to Railway backend service
2. Copy frontend files to Railway frontend service
3. Restart services

### Option 2: Docker Rebuild (if needed)
1. Copy these files to your backend directory
2. Copy frontend files to your frontend directory  
3. Run: docker build -t multimodal-backend .
4. Run: docker build -t multimodal-frontend .
5. Push and deploy

## 🎯 WHAT'S FIXED:

### YouTube Summarizer:
- ✅ Schema mismatch fixed (video_id field added)
- ✅ Better error handling with specific messages
- ✅ Multi-language transcript support
- ✅ Video title retrieval added
- ✅ Enhanced logging for debugging

### Chat File Upload:
- ✅ PDF upload directly in chat interface
- ✅ Drag & drop support
- ✅ File preview and removal
- ✅ Integration with existing chat API

## 🧪 TESTING:
After deployment, test:
1. YouTube summarization with videos that have captions
2. PDF upload in chat section
3. File removal functionality
4. Error handling for invalid URLs/files

"""
    
    with open(deploy_dir / "README.md", "w") as f:
        f.write(instructions)
    
    print(f"\n✅ Deployment package created in: {deploy_dir}")
    print(f"📄 Instructions saved: {deploy_dir}/README.md")
    
    # Show what's in the package
    print("\n📦 Package contents:")
    for file_path in deploy_dir.rglob("*"):
        if file_path.is_file():
            rel_path = file_path.relative_to(deploy_dir)
            size = file_path.stat().st_size
            print(f"  📄 {rel_path} ({size} bytes)")
    
    return deploy_dir

def show_file_changes():
    """Show what exactly was changed in each file"""
    
    print("\n" + "="*60)
    print("📝 DETAILED CHANGES MADE")
    print("="*60)
    
    changes = {
        "backend/schemas/youtube_schema.py": [
            "Added video_id field to YouTubeResponse",
            "Fixed schema mismatch with route"
        ],
        "backend/services/youtube_service.py": [
            "Added get_video_title() function",
            "Enhanced get_transcript() with multi-language support",
            "Improved error messages and logging",
            "Better transcript validation and processing"
        ],
        "backend/api/routes/youtube.py": [
            "Updated to pass video_title in response",
            "Enhanced logging with video_id"
        ],
        "frontend/src/services/api.js": [
            "Added sendMessageWithFile() function",
            "Support for FormData with file uploads"
        ],
        "frontend/src/pages/Chat.jsx": [
            "Added file upload state management",
            "Drag & drop functionality",
            "File preview and removal",
            "Enhanced message display with file info",
            "Updated handleSubmit to support files"
        ]
    }
    
    for file_path, change_list in changes.items():
        print(f"\n📁 {file_path}:")
        for change in change_list:
            print(f"  ✅ {change}")

def main():
    print("🚀 TARGETED DEPLOYMENT PACKAGE CREATOR")
    print("Multimodal AI - Changed Files Only")
    
    show_file_changes()
    deploy_dir = create_deployment_package()
    
    print("\n" + "="*60)
    print("🎯 NEXT STEPS")
    print("="*60)
    print(f"1. Copy files from {deploy_dir} to your deployment")
    print("2. Deploy only the changed files (not entire backend)")
    print("3. Test YouTube summarizer and chat file upload")
    print("4. Monitor logs for any issues")
    
    print("\n💡 This approach avoids rebuilding the entire Docker image!")

if __name__ == "__main__":
    main()
