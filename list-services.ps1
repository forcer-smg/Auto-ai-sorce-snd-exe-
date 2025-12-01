# List All Running Services and Processes
# Run: .\list-services.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "RUNNING SERVICES AND PROCESSES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Python Processes:" -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Select-Object ProcessName, Id, Path | Format-Table -AutoSize

Write-Host ""
Write-Host "Node.js Processes:" -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "node"} | Select-Object ProcessName, Id, Path, MainWindowTitle | Format-Table -AutoSize

Write-Host ""
Write-Host "Flask/App Processes:" -ForegroundColor Yellow
Get-Process | Where-Object {$_.CommandLine -like "*app.py*" -or $_.Path -like "*app.py*"} -ErrorAction SilentlyContinue | Select-Object ProcessName, Id, Path | Format-Table -AutoSize

Write-Host ""
Write-Host "All Services:" -ForegroundColor Yellow
Get-Service | Where-Object {$_.Status -eq "Running"} | Select-Object Name, Status, DisplayName | Format-Table -AutoSize

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DONE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""


