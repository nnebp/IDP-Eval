#!/bin/bash
# Setup script for IDP-Eval project

echo "🚀 Setting up IDP-Eval environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file template..."
    cat > .env << EOF
# Together AI API Configuration
TOGETHER_API_KEY=your_api_key_here
EOF
    echo "✏️  Please edit .env and add your actual Together AI API key"
fi

echo "✅ Setup complete!"
echo ""
echo "To use the project:"
echo "1. Edit .env file with your API key"
echo "2. Activate environment: source venv/bin/activate"
echo "3. Run: python multi_model_query.py"
