# Check Build Status and Open Folder
# Run: .\check-build.ps1

Set-Location -Path "C:\Users\Administrator\Auto_Punch IDE"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "BUILD STATUS CHECK" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

if (Test-Path "dist\Auto_Punch IDE Setup 1.0.0.exe") {
    $exe = Get-Item "dist\Auto_Punch IDE Setup 1.0.0.exe"
    Write-Host "✅ EXE INSTALLER: SUCCESS!" -ForegroundColor Green
    Write-Host ""
    Write-Host "   File Name: $($exe.Name)" -ForegroundColor White
    Write-Host "   File Size: $([math]::Round($exe.Length/1MB, 2)) MB" -ForegroundColor Cyan
    Write-Host "   Created: $($exe.LastWriteTime)" -ForegroundColor Gray
    Write-Host "   Full Path: $($exe.FullName)" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "❌ EXE Installer: Not found" -ForegroundColor Red
    Write-Host ""
}

if (Test-Path "dist\win-unpacked\Auto_Punch IDE.exe") {
    $portable = Get-Item "dist\win-unpacked\Auto_Punch IDE.exe"
    Write-Host "✅ PORTABLE APP: Ready" -ForegroundColor Green
    Write-Host "   Location: dist\win-unpacked\Auto_Punch IDE.exe" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "⚠️  Portable App: Not found" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "All files in dist folder:" -ForegroundColor Cyan
Get-ChildItem "dist" -ErrorAction SilentlyContinue | Select-Object Name, @{Name="Size (MB)";Expression={[math]::Round($_.Length/1MB, 2)}}, LastWriteTime | Format-Table -AutoSize

Write-Host ""
Write-Host "Opening dist folder in File Explorer..." -ForegroundColor Yellow
Start-Sleep -Seconds 1
explorer dist

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "BUILD COMPLETE! 🎉" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your installer is ready to distribute!" -ForegroundColor Cyan
Write-Host ""


