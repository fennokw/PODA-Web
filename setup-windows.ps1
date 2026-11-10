[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

function Run-Checked {
    param([string]$Executable, [string[]]$Arguments)
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Executable exited with code $LASTEXITCODE." }
}

$Requirements = Join-Path $PSScriptRoot 'requirements.txt'
$RuntimeParent = $PSScriptRoot
$Runtime = Join-Path $RuntimeParent '.venv'
$Python = Join-Path $Runtime 'Scripts\python.exe'
$Version = (Get-FileHash -Algorithm SHA256 -LiteralPath $Requirements).Hash
$Ready = Join-Path $Runtime '.requirements-sha256'
[IO.Directory]::CreateDirectory($RuntimeParent) | Out-Null
$Lock = [IO.File]::Open((Join-Path $RuntimeParent '.setup.lock'), 'OpenOrCreate', 'ReadWrite', 'None')
try {
    if ((Test-Path -LiteralPath $Ready -PathType Leaf) -and (Test-Path -LiteralPath $Python -PathType Leaf) -and ([IO.File]::ReadAllText($Ready) -eq $Version)) {
        Write-Host 'PODA runtime is ready. Run Start-PODA.cmd to launch PODA Web.'
        exit 0
    }
    $Launcher = Get-Command py.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $Launcher) { throw 'Install 64-bit Python 3.12 from python.org with the Python Launcher option enabled, then run Setup PODA again.' }

    Run-Checked $Launcher.Source @('-3.12', '-I', '-c', 'import sysconfig; assert sysconfig.get_platform() == ''win-amd64'', ''PODA requires x64 Python''')
    if (Test-Path -LiteralPath $Ready) { Remove-Item -LiteralPath $Ready }
    Run-Checked $Launcher.Source @('-3.12', '-I', '-m', 'venv', $Runtime)
    Run-Checked $Python @('-I', '-m', 'pip', 'install', '--only-binary=:all:', '--disable-pip-version-check', '-r', $Requirements)
    Run-Checked $Python @('-I', '-c', 'import fastapi, uvicorn, win32cred, pythoncom, open3d; from sqlcipher3 import dbapi2; from zoneinfo import ZoneInfo; assert dbapi2.connect('':memory:'').execute(''PRAGMA cipher_version'').fetchone(); ZoneInfo(''America/New_York'')')
    Run-Checked $Python @('-m', 'poda_app.runtime.llama_install')
    [IO.File]::WriteAllText($Ready, $Version)
    Write-Host 'PODA runtime is ready. Run Start-PODA.cmd to launch PODA Web.'
}
finally {
    $Lock.Dispose()
}
