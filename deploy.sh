#!/bin/bash

# Deployment script for Fly.io

echo "🚀 Starting deployment to Fly.io..."

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "❌ flyctl is not installed. Please install it first:"
    echo "   curl -L https://fly.io/install.sh | sh"
    exit 1
fi

# Check if user is logged in
if ! flyctl auth whoami &> /dev/null; then
    echo "❌ You are not logged in to Fly.io. Please run:"
    echo "   flyctl auth login"
    exit 1
fi

echo "✅ flyctl is installed and you are logged in"

# Create the app if it doesn't exist
if ! flyctl apps list | grep -q "autocad-converter"; then
    echo "📱 Creating new Fly.io app..."
    flyctl apps create autocad-converter
else
    echo "✅ App 'autocad-converter' already exists"
fi

# Create volume if it doesn't exist
if ! flyctl volumes list -a autocad-converter | grep -q "autocad_data"; then
    echo "💾 Creating volume for file storage..."
    flyctl volumes create autocad_data --region ord --size 1 -a autocad-converter
else
    echo "✅ Volume 'autocad_data' already exists"
fi

# Deploy the application
echo "🚀 Deploying application..."
flyctl deploy

# Show the deployment status
echo "📊 Deployment status:"
flyctl status -a autocad-converter

echo "🎉 Deployment complete!"
echo "🌐 Your app should be available at: https://autocad-converter.fly.dev"
echo ""
echo "📝 Login credentials:"
echo "   Username: admin"
echo "   Password: password123"
echo ""
echo "🔧 Useful commands:"
echo "   flyctl logs -a autocad-converter     # View logs"
echo "   flyctl ssh console -a autocad-converter  # SSH into the app"
echo "   flyctl status -a autocad-converter   # Check status"
