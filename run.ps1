param (
    [Parameter(Mandatory=$false)]
    [string]$VideoPath = "",

    [switch]$Mono,
    [switch]$Detailed,
    [switch]$NoAudio
)

$cmdArgs = @("ascii_player.py")
if ($VideoPath -ne "") { $cmdArgs += $VideoPath }
if ($Mono) { $cmdArgs += "--mono" }
if ($Detailed) { $cmdArgs += "--detailed" }
if ($NoAudio) { $cmdArgs += "--no-audio" }

python @cmdArgs
