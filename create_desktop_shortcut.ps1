$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Video to ASCII Player.lnk"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $ScriptDir) {
    $ScriptDir = "C:\Users\Admin\.gemini\antigravity\scratch\ascii_player"
}

$PythonDir = Split-Path (Get-Command python).Source
$PythonwExe = Join-Path $PythonDir "pythonw.exe"
if (-not (Test-Path $PythonwExe)) {
    $PythonwExe = (Get-Command python).Source
}

$TargetScript = Join-Path $ScriptDir "gui_launcher.py"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $PythonwExe
$Shortcut.Arguments = "`"$TargetScript`""
$Shortcut.WorkingDirectory = $ScriptDir
$Shortcut.Description = "Phát video bằng ký tự ASCII trên PowerShell"

# Icon máy chiếu / phim ảnh từ thư viện Windows
$Shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll,115"
$Shortcut.Save()

Write-Host "[+] Đã tạo biểu tượng 'Video to ASCII Player' thành công trên màn hình Desktop!" -ForegroundColor Green
Write-Host "    Đường dẫn: $ShortcutPath" -ForegroundColor Cyan
