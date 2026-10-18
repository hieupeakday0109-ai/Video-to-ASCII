$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Video to ASCII Player.lnk"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $ScriptDir) {
    $ScriptDir = (Get-Location).Path
}

$PythonDir = Split-Path (Get-Command python).Source
$PythonwExe = Join-Path $PythonDir "pythonw.exe"
if (-not (Test-Path $PythonwExe)) {
    $PythonwExe = (Get-Command python).Source
}

$TargetScript = Join-Path $ScriptDir "gui_launcher.py"
$IconFile = Join-Path $ScriptDir "icon.ico"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $PythonwExe
$Shortcut.Arguments = "`"$TargetScript`""
$Shortcut.WorkingDirectory = $ScriptDir
$Shortcut.Description = "Phát video bằng ký tự ASCII trên PowerShell"

if (Test-Path $IconFile) {
    $Shortcut.IconLocation = "$IconFile,0"
} else {
    $Shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll,115"
}

$Shortcut.Save()

Write-Host "[+] Đã tạo biểu tượng 'Video to ASCII Player' thành công trên màn hình Desktop!" -ForegroundColor Green
Write-Host "    Đường dẫn: $ShortcutPath" -ForegroundColor Cyan
