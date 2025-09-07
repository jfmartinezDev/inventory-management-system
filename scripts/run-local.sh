#!/bin/bash

# Script to run the application locally

echo "🚀 Starting Inventory Management System..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Stop any running containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start containers
echo "🔨 Building containers..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check health
echo "🏥 Checking service health..."
curl -f http://localhost:8000/health || echo "⚠️ Backend not responding"
curl -f http://localhost || echo "⚠️ Frontend not responding"

echo "✅ Application is running!"
echo "📱 Frontend: http://localhost"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "🔑 Default credentials:"
echo "   Username: admin"
echo "   Password: admin123456"
echo ""
echo "To stop: docker-compose down"
echo "To view logs: docker-compose logs -f"