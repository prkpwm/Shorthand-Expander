$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$PSScriptRoot\Shorthand Expander.lnk")
$Shortcut.TargetPath = "$PSScriptRoot\dist\ShorthandExpander.exe"
$Shortcut.WorkingDirectory = "$PSScriptRoot\dist"
$Shortcut.IconLocation = "$PSScriptRoot\dist\ShorthandExpander.exe,0"
$Shortcut.Description = "Shorthand Expander - Text expansion tool"
$Shortcut.Save()
Write-Host "Shortcut created: Shorthand Expander.lnk" -ForegroundColor Green
