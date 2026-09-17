# Nivy Next AIOS v1 — Legacy-compatible Windows installer
# Kept for compatibility. The canonical V1 bootstrap is INSTALL-ALL-WINDOWS.ps1.
[CmdletBinding()]
param(
  [string]$InstallRoot = 'G:\Docker\Nivy\Repository\Nivy-Next-AIOS',
  [string]$DataRoot = 'G:\Docker\Nivy\Data',
  [switch]$SkipPrerequisites,
  [switch]$SkipDockerStart,
  [switch]$SkipTests
)
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
& "$root\setup\INSTALL-ALL-WINDOWS.ps1" `
  -InstallRoot $InstallRoot `
  -DataRoot $DataRoot `
  -SkipPrerequisites:$SkipPrerequisites `
  -SkipDockerStart:$SkipDockerStart `
  -SkipTerraform `
  -SkipAgentTests:$SkipTests `
  -SkipTests:$SkipTests

if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
