#!/bin/bash

echo "🐳 Testing Dockerized Scrabble App"
echo "=================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✅ Docker is running"

# Build and start containers
echo "🔨 Building and starting containers..."
docker-compose up --build -d

# Wait for containers to be ready
echo "⏳ Waiting for containers to start..."
sleep 10

# Test backend health
echo "🏥 Testing backend health..."
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
fi

# Test frontend
echo "🌐 Testing frontend..."
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend is not accessible"
fi

echo ""
echo "🎉 Setup complete!"
echo "📱 Open http://localhost:3000 in your browser"
echo "🔧 Backend API available at http://localhost:5000"
echo ""
echo "To stop: docker-compose down"
echo "To view logs: docker-compose logs"
