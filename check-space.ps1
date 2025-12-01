# Check Disk Space
# Run: .\check-space.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DISK SPACE CHECK" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$drive = Get-PSDrive C
$freeGB = [math]::Round($drive.Free/1GB, 2)
$usedGB = [math]::Round($drive.Used/1GB, 2)
$totalGB = [math]::Round(($drive.Free + $drive.Used)/1GB, 2)

Write-Host "Drive C: Status" -ForegroundColor Yellow
Write-Host "  Total: $totalGB GB" -ForegroundColor White
Write-Host "  Used:  $usedGB GB" -ForegroundColor Gray
Write-Host "  Free:  $freeGB GB" -ForegroundColor Cyan
Write-Host ""

$percentFree = [math]::Round(($drive.Free / ($drive.Free + $drive.Used)) * 100, 1)
Write-Host "  Free: $percentFree%" -ForegroundColor $(if ($percentFree -lt 10) { "Red" } elseif ($percentFree -lt 20) { "Yellow" } else { "Green" })
Write-Host ""

Write-Host "Requirements:" -ForegroundColor Yellow
Write-Host "  EXE Installer: ~500 MB free (recommended)" -ForegroundColor Gray
Write-Host "  MSI Installer: ~2 GB free (recommended)" -ForegroundColor Gray
Write-Host "  Build process: ~3 GB free (safe)" -ForegroundColor Gray
Write-Host ""

if ($freeGB -lt 0.5) {
    Write-Host "  ERROR: Less than 500 MB free!" -ForegroundColor Red
    Write-Host "  Cannot build installer. Free up space first." -ForegroundColor Red
} elseif ($freeGB -lt 2) {
    Write-Host "  WARNING: Less than 2 GB free" -ForegroundColor Yellow
    Write-Host "  EXE installer should work, MSI may fail" -ForegroundColor Yellow
    Write-Host "  Recommended: Free up space or use EXE installer" -ForegroundColor Yellow
} else {
    Write-Host "  OK: Sufficient space for both EXE and MSI installers" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""


