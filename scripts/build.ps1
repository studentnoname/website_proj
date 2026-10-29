param([switch]$InstallDependencies)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding
$OutputEncoding = [Console]::OutputEncoding
. (Join-Path $PSScriptRoot 'windows-env.ps1')
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $projectRoot
try {
    foreach ($tool in @('python', 'hugo', 'go', 'node', 'npm')) {
        if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
            throw "Required tool is missing: $tool. See README.md."
        }
    }
    if ($InstallDependencies) {
        python .github/pages_build.py --dependencies
        if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
    }
    python .github/pages_build.py --build
    if ($LASTEXITCODE -ne 0) { throw 'Hugo build failed.' }
} finally {
    Pop-Location
}
