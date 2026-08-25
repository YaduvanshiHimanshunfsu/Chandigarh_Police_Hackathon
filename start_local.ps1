# start_local.ps1 - Run PratiBimb Praman locally (no Docker needed)
$ErrorActionPreference = "Continue"
$ROOT = $PSScriptRoot

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  PratiBimb Praman - Local Startup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Refresh PATH in script environment
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Step 1: Setup .env
$envLocal = Join-Path $ROOT "backend\.env.local"
$envFile  = Join-Path $ROOT "backend\.env"

if (-not (Test-Path $envFile)) {
    if (Test-Path $envLocal) {
        Copy-Item $envLocal $envFile -Force
        Write-Host "[1/4] Created backend\.env from .env.local" -ForegroundColor Green
    }
} else {
    Write-Host "[1/4] backend\.env configured" -ForegroundColor Green
}

# Step 2: Create upload/report directories
$uploads = Join-Path $ROOT "backend\uploads"
$reports = Join-Path $ROOT "backend\reports"
if (-not (Test-Path $uploads)) { New-Item -ItemType Directory -Force -Path $uploads | Out-Null }
if (-not (Test-Path $reports)) { New-Item -ItemType Directory -Force -Path $reports | Out-Null }
Write-Host "[2/4] Upload & report directories ready" -ForegroundColor Green

# Step 3: Check frontend dependencies
$nodeModules = Join-Path $ROOT "frontend\node_modules"
if (-not (Test-Path $nodeModules)) {
    Write-Host "[3/4] Installing frontend dependencies (npm install)..." -ForegroundColor Yellow
    Push-Location (Join-Path $ROOT "frontend")
    npm install
    Pop-Location
} else {
    Write-Host "[3/4] Frontend dependencies already installed" -ForegroundColor Green
}

# Step 4: Launch all services in separate windows
Write-Host "[4/4] Launching services..." -ForegroundColor Green

$backendDir  = Join-Path $ROOT "backend"
$frontendDir = Join-Path $ROOT "frontend"

# FastAPI Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$backendDir'; `$env:PYTHONPATH='.'; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

Start-Sleep -Seconds 2

# Celery Worker
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$backendDir'; `$env:PYTHONPATH='.'; celery -A app.core.celery_app worker --loglevel=info --concurrency=2 --pool=solo"

Start-Sleep -Seconds 2

# Next.js Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$frontendDir'; npm run dev"

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "  All services launched successfully!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Dashboard UI -> http://localhost:3000" -ForegroundColor White
Write-Host "  API Docs     -> http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
