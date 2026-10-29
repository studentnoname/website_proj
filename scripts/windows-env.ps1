# Session-local tool paths; does not modify the user's global PATH.
$projectRoot = Split-Path -Parent $PSScriptRoot
$toolDirectories = @(
    (Join-Path $projectRoot '.local/tools/hugo'),
    (Join-Path $projectRoot '.local/tools/go/bin'),
    (Join-Path $projectRoot '.local/tools/dart-sass')
)
$env:PATH = ($toolDirectories -join [IO.Path]::PathSeparator) + [IO.Path]::PathSeparator + $env:PATH
