#!/bin/bash

# 🚀 Morgan Stanley Analytics - GitHub Deployment Script
# This script automates the deployment of your analytics framework to GitHub

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Morgan Stanley Analytics - GitHub Deployment Script${NC}"
echo "=================================================="

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed. Please install Git first.${NC}"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Not in a git repository. Initializing...${NC}"
    git init
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Get repository details
echo -e "${BLUE}Please provide the following information:${NC}"
read -p "GitHub username: " GITHUB_USERNAME
read -p "Repository name (default: morgan-stanley-analytics): " REPO_NAME
REPO_NAME=${REPO_NAME:-morgan-stanley-analytics}

# Update configuration files
echo -e "${YELLOW}Updating configuration files...${NC}"

# Update setup.py
if [ -f "setup.py" ]; then
    sed -i.bak "s|yourusername|$GITHUB_USERNAME|g" setup.py
    echo -e "${GREEN}✅ Updated setup.py${NC}"
fi

# Update README.md
if [ -f "README.md" ]; then
    sed -i.bak "s|yourusername|$GITHUB_USERNAME|g" README.md
    echo -e "${GREEN}✅ Updated README.md${NC}"
fi

# Clean up backup files
rm -f *.bak

# Git operations
echo -e "${YELLOW}Setting up Git repository...${NC}"

# Add all files
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo -e "${YELLOW}⚠️  No changes to commit${NC}"
else
    # Commit changes
    git commit -m "Initial commit: Morgan Stanley Global Markets Analytics Framework

- Portfolio analysis and risk management
- Compliance monitoring and regulatory reporting
- Performance analytics and attribution
- Professional visualization and dashboards
- Database integration and SQL templates
- Morgan Stanley compliance standards"
    echo -e "${GREEN}✅ Initial commit created${NC}"
fi

# Add remote origin
if ! git remote get-url origin &> /dev/null; then
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo -e "${GREEN}✅ Remote origin added${NC}"
else
    echo -e "${YELLOW}⚠️  Remote origin already exists${NC}"
fi

# Push to GitHub
echo -e "${YELLOW}Pushing to GitHub...${NC}"
git push -u origin main

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Go to https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo "2. Verify all files are uploaded correctly"
echo "3. Enable Issues and Discussions in repository settings"
echo "4. Create your first release (v1.0.0)"
echo "5. Share with the community!"
echo ""
echo -e "${GREEN}Your Morgan Stanley Analytics framework is now live on GitHub! 🚀${NC}"

# Optional: Open repository in browser
read -p "Would you like to open the repository in your browser? (y/n): " OPEN_BROWSER
if [[ $OPEN_BROWSER =~ ^[Yy]$ ]]; then
    if command -v open &> /dev/null; then
        open "https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    else
        echo "Please manually open: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    fi
fi
