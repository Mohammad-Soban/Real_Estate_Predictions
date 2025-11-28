# Run Property Analysis with Ollama
# This script makes Ollama available and runs your analysis

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Property Analysis with LOCAL AI" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

# Add Ollama to PATH for this session
$env:PATH += ";$env:LOCALAPPDATA\Programs\Ollama"

# Verify Ollama is available
Write-Host "Checking Ollama..." -ForegroundColor White
try {
    $version = & ollama --version 2>&1
    Write-Host "✅ $version" -ForegroundColor Green
    
    Write-Host "`nInstalled Models:" -ForegroundColor White
    & ollama list
    
    Write-Host "`n🏠 Starting analysis with LOCAL AI..." -ForegroundColor Green
    Write-Host "   - No internet needed" -ForegroundColor Gray
    Write-Host "   - 100% private" -ForegroundColor Gray
    Write-Host "   - Unlimited usage`n" -ForegroundColor Gray
    
    # Run the analysis
    python main_phase2.py
    
} catch {
    Write-Host "❌ Ollama not found!" -ForegroundColor Red
    Write-Host "`nUsing full path instead..." -ForegroundColor Yellow
    
    $ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
    if (Test-Path $ollamaPath) {
        Write-Host "✅ Ollama found at: $ollamaPath" -ForegroundColor Green
        python main_phase2.py
    } else {
        Write-Host "❌ Ollama not installed. Please download from: https://ollama.ai/" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Analysis Complete!" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan
