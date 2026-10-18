param (
    [Parameter(Mandatory=$false)]
    [string]$VideoPath = "demo.mp4",

    [switch]$Color,
    [switch]$Detailed,
    [switch]$NoAudio
)

$cmdArgs = @("ascii_player.py", $VideoPath)
if ($Color) { $cmdArgs += "--color" }
if ($Detailed) { $cmdArgs += "--detailed" }
if ($NoAudio) { $cmdArgs += "--no-audio" }

python @cmdArgs
