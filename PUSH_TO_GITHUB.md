# Push to GitHub Guide

## Quick Commands

```bash
# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Shorthand Expander with modern UI"

# Push to GitHub (if repository already exists)
git push origin main

# Or if it's the first push
git branch -M main
git remote add origin https://github.com/yourusername/shorthand-expander.git
git push -u origin main
```

## Step by Step

### 1. Stage all changes
```bash
git add .
```

### 2. Commit with message
```bash
git commit -m "Add Shorthand Expander application

- Modern VS Code-inspired UI with sidebar layout
- Real-time text expansion functionality
- Add/Edit/Delete shortcuts through GUI
- Statistics tracking
- Fullscreen mode support
- Build scripts for creating executable
- Comprehensive documentation"
```

### 3. Create GitHub repository
1. Go to https://github.com/new
2. Create a new repository named `shorthand-expander`
3. Don't initialize with README (we already have one)

### 4. Push to GitHub
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/shorthand-expander.git
git push -u origin main
```

## What will be pushed

✅ Source code (Python files)
✅ UI files and styles
✅ Build scripts
✅ Documentation (README, BUILD_INSTRUCTIONS)
✅ Requirements files
✅ Icon file

❌ Build artifacts (dist/, build/)
❌ Python cache (__pycache__)
❌ Executables (.exe)
❌ Shortcuts (.lnk)
❌ IDE files (.vscode/)

## After pushing

Your repository will be ready with:
- Complete source code
- Build instructions
- Professional README
- Proper .gitignore

Users can:
- Clone and run from source
- Build their own executable
- Contribute to the project
