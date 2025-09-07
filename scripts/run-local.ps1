# PowerShell script to run the application locally on Windows
# Run from project root: .\scripts\run-local.ps1

Write-Host "🚀 Starting Inventory Management System..." -ForegroundColor Green

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop and try again." -ForegroundColor Red
    exit 1
}

# Stop any running containers
Write-Host "🛑 Stopping existing containers..." -ForegroundColor Yellow
docker-compose down

# Build and start containers
Write-Host "🔨 Building containers..." -ForegroundColor Cyan
docker-compose build

Write-Host "🚀 Starting services..." -ForegroundColor Cyan
docker-compose up -d

# Wait for services to be ready
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check health
Write-Host "🏥 Checking service health..." -ForegroundColor Cyan

# Check backend
try {
    $backendResponse = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "✅ Backend is running: $($backendResponse.status)" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Backend not responding yet" -ForegroundColor Yellow
}

# Check frontend
try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost" -Method Head
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend is running" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ Frontend not responding yet" -ForegroundColor Yellow
}

Write-Host "`n✅ Application is running!" -ForegroundColor Green
Write-Host "📱 Frontend: http://localhost" -ForegroundColor White
Write-Host "🔧 Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "`n🔑 Default credentials:" -ForegroundColor Yellow
Write-Host "   Username: admin" -ForegroundColor White
Write-Host "   Password: admin123456" -ForegroundColor White
Write-Host "`nCommands:" -ForegroundColor Cyan
Write-Host "  Stop: docker-compose down" -ForegroundColor White
Write-Host "  Logs: docker-compose logs -f" -ForegroundColor White
Write-Host "  Status: docker-compose ps" -ForegroundColor White