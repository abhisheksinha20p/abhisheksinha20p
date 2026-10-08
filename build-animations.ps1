# Windows PowerShell helper
# Replace assets/space-shooter.gif with your real contribution-shooter GIF if desired.

Set-Location "$PSScriptRoot/animations"

if (!(Test-Path "node_modules")) {
    npm install
}

npm run build

Write-Host ""
Write-Host "Animation build completed."
Write-Host "Output: animations/dist/"
