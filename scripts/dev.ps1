# PowerShell script for development without Docker
# Run from project root: .\scripts\dev.ps1

param(
    [Parameter(Mandatory=$false)]
    [string]$Component = "all"  # all, backend, frontend
)

Write-Host "🚀 Starting Development Environment..." -ForegroundColor Green

function Start-Backend {
    Write-Host "`n🔧 Starting Backend..." -ForegroundColor Cyan
    
    # Check if PostgreSQL is running
    try {
        psql -U postgres -c "SELECT 1" | Out-Null
        Write-Host "✅ PostgreSQL is running" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ PostgreSQL is not running. Starting it..." -ForegroundColor Yellow
        # Try to start PostgreSQL service
        Start-Service postgresql-x64-14 -ErrorAction SilentlyContinue
    }
    
    # Start backend in new terminal
    Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
        cd backend
        Write-Host 'Activating Python virtual environment...' -ForegroundColor Yellow
        .\venv\Scripts\Activate
        Write-Host 'Starting FastAPI server...' -ForegroundColor Green
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"@
    
    Write-Host "✅ Backend starting on http://localhost:8000" -ForegroundColor Green
}

function Start-Frontend {
    Write-Host "`n🎨 Starting Frontend..." -ForegroundColor Cyan
    
    # Start frontend in new terminal
    Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
        cd frontend
        Write-Host 'Starting React development server...' -ForegroundColor Green
        npm run dev
"@
    
    Write-Host "✅ Frontend starting on http://localhost:5173" -ForegroundColor Green
}

# Main execution
switch ($Component) {
    "backend" {
        Start-Backend
    }
    "frontend" {
        Start-Frontend
    }
    "all" {
        Start-Backend
        Start-Sleep -Seconds 3
        Start-Frontend
        
        Write-Host "`n✅ Development environment is starting!" -ForegroundColor Green
        Write-Host "`n📱 Access points:" -ForegroundColor Yellow
        Write-Host "   Frontend: http://localhost:5173" -ForegroundColor White
        Write-Host "   Backend API: http://localhost:8000" -ForegroundColor White
        Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
        Write-Host "`n🔑 Default credentials:" -ForegroundColor Yellow
        Write-Host "   Username: admin" -ForegroundColor White
        Write-Host "   Password: admin123456" -ForegroundColor White
        Write-Host "`n⚠️ Each component is running in its own terminal window" -ForegroundColor Yellow
    }
    default {
        Write-Host "Invalid component. Use: all, backend, or frontend" -ForegroundColor Red
    }
}