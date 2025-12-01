# Force Close Auto_Punch IDE
# Run: .\force-close.ps1

Write-Host ""
Write-Host "Force closing all Auto_Punch IDE processes..." -ForegroundColor Yellow
Write-Host ""

# Find all related processes
$allProcesses = Get-Process | Where-Object {
    $_.ProcessName -like "*Auto_Punch*" -or 
    $_.ProcessName -like "*AutoPunch*" -or
    $_.ProcessName -like "*autopunch*" -or
    $_.MainWindowTitle -like "*Auto_Punch*" -or
    $_.Path -like "*Auto_Punch*" -or
    ($_.ProcessName -eq "electron" -and $_.Path -like "*Auto_Punch*")
}

if ($allProcesses) {
    Write-Host "Found $($allProcesses.Count) process(es):" -ForegroundColor Cyan
    $allProcesses | ForEach-Object {
        Write-Host "  Closing: $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor Gray
        taskkill /F /PID $_.Id >nul 2>&1
    }
    Start-Sleep -Seconds 2
    Write-Host ""
    Write-Host "All processes closed!" -ForegroundColor Green
} else {
    Write-Host "No Auto_Punch IDE processes found." -ForegroundColor Gray
}

Write-Host ""


