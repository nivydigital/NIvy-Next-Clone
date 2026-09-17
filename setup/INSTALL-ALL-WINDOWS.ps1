# Nivy Next AIOS — Complete Windows V1 Bootstrap
# Default layout keeps the Nivy repository + persistent application data on G:\Docker\Nivy.
# Docker Desktop itself may still keep its own engine/WSL image on its configured system drive.
[CmdletBinding()]
param(
  [string]$InstallRoot = 'G:\Docker\Nivy\Nivy-Next-AIOS',
  [string]$DataRoot = 'G:\Docker\Nivy\Data',
  [string]$LogRoot = 'G:\Docker\Nivy\Logs',
  [switch]$SkipPrerequisites,
  [switch]$SkipDockerStart,
  [switch]$SkipTerraform,
  [switch]$SkipTests,
  [switch]$SkipAgentTests
)
$ErrorActionPreference = 'Stop'

function Step($Message) { Write-Host "`n=== $Message ===" -ForegroundColor Cyan }
function Require-Command($Name) {
  if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) { throw "$Name is required but was not found on PATH." }
}
function Ensure-Directory($Path) {
  if (-not (Test-Path -LiteralPath $Path)) { New-Item -ItemType Directory -Path $Path -Force | Out-Null }
}
function Refresh-Path {
  $machine = [Environment]::GetEnvironmentVariable('Path','Machine')
  $user = [Environment]::GetEnvironmentVariable('Path','User')
  if ($machine -or $user) { $env:Path = "$machine;$user" }
}
function Invoke-Native($File, [string[]]$Arguments) {
  Write-Host "> $File $($Arguments -join ' ')" -ForegroundColor DarkGray
  & $File @Arguments
  if ($LASTEXITCODE -ne 0) { throw "$File failed with exit code $LASTEXITCODE." }
}
function Install-Or-Continue($PackageId, $CommandName) {
  if (Get-Command $CommandName -ErrorAction SilentlyContinue) {
    Write-Host "PASS  $CommandName is already available." -ForegroundColor Green
    return
  }

  Write-Host "> winget install --id $PackageId -e --accept-source-agreements --accept-package-agreements" -ForegroundColor DarkGray
  & winget install --id $PackageId -e --accept-source-agreements --accept-package-agreements
  $code = $LASTEXITCODE
  Refresh-Path

  # winget returns a non-zero code when the package is already installed and
  # there is no newer version. That is a successful/idempotent state for us.
  if ($code -ne 0) {
    Write-Warning "winget returned exit code $code for $PackageId. Checking whether $CommandName is now available..."
    Refresh-Path
    if (-not (Get-Command $CommandName -ErrorAction SilentlyContinue)) {
      throw "winget failed for $PackageId with exit code $code and $CommandName is still unavailable on PATH."
    }
  }
}

Step 'Preparing G: drive layout'
Ensure-Directory $InstallRoot
Ensure-Directory $DataRoot
Ensure-Directory $LogRoot
foreach ($dir in @('postgres','qdrant','minio','ollama','n8n')) { Ensure-Directory (Join-Path $DataRoot $dir) }

Step 'Installing/checking prerequisites'
if (-not $SkipPrerequisites) {
  if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    throw 'winget is required for automatic prerequisite installation. Install/enable App Installer, then rerun this script.'
  }

  Install-Or-Continue 'Git.Git' 'git'
  Install-Or-Continue 'Docker.DockerDesktop' 'docker'
  if (-not $SkipTerraform) {
    Install-Or-Continue 'Hashicorp.Terraform' 'terraform'
  }
}

Require-Command git
if (-not $SkipDockerStart) { Require-Command docker }
if (-not $SkipTerraform) { Require-Command terraform }

Step "Preparing repository at $InstallRoot"
$parent = Split-Path -Parent $InstallRoot
Ensure-Directory $parent
if (Test-Path (Join-Path $InstallRoot '.git')) {
  Invoke-Native 'git' @('-C',$InstallRoot,'fetch','--all','--prune')
  Invoke-Native 'git' @('-C',$InstallRoot,'checkout','main')
  Invoke-Native 'git' @('-C',$InstallRoot,'pull','--ff-only','origin','main')
} elseif (Test-Path $InstallRoot) {
  $items = @(Get-ChildItem -LiteralPath $InstallRoot -Force -ErrorAction SilentlyContinue)
  if ($items.Count -gt 0) { throw "$InstallRoot exists but is not a Git repository. Choose another InstallRoot or remove/rename that folder." }
  Invoke-Native 'git' @('clone','https://github.com/nivyindia/Nivy-Next-AIOS.git',$InstallRoot)
} else {
  Invoke-Native 'git' @('clone','https://github.com/nivyindia/Nivy-Next-AIOS.git',$InstallRoot)
}

Set-Location $InstallRoot

Step 'Writing local .env with G: persistent data paths'
if (-not (Test-Path '.env') -and (Test-Path '.env.example')) { Copy-Item '.env.example' '.env' }
$envPath = Join-Path $InstallRoot '.env'
$envText = if (Test-Path $envPath) { Get-Content -LiteralPath $envPath -Raw } else { '' }
$pathMap = @{
  'NIVY_POSTGRES_DATA' = (Join-Path $DataRoot 'postgres').Replace('\','/')
  'NIVY_QDRANT_DATA'   = (Join-Path $DataRoot 'qdrant').Replace('\','/')
  'NIVY_MINIO_DATA'    = (Join-Path $DataRoot 'minio').Replace('\','/')
  'NIVY_OLLAMA_DATA'   = (Join-Path $DataRoot 'ollama').Replace('\','/')
  'NIVY_N8N_DATA'      = (Join-Path $DataRoot 'n8n').Replace('\','/')
}
foreach ($name in $pathMap.Keys) {
  $line = "$name=$($pathMap[$name])"
  if ($envText -match "(?m)^$name=.*$") {
    $escaped = [regex]::Escape($line).Replace('\=','=')
    $envText = [regex]::Replace($envText, "(?m)^$name=.*$", $escaped)
  } else {
    $envText = $envText.TrimEnd() + "`r`n$line`r`n"
  }
}
Set-Content -LiteralPath $envPath -Value $envText -Encoding UTF8

if (-not $SkipDockerStart) {
  Step 'Starting complete Docker runtime with G: persistent storage'
  Invoke-Native 'docker' @('compose','config')
  Invoke-Native 'docker' @('compose','pull')
  Invoke-Native 'docker' @('compose','build')
  Invoke-Native 'docker' @('compose','up','-d')
}

if (-not $SkipTerraform) {
  Step 'Running Terraform infrastructure validation and plan'
  & "$InstallRoot\setup\TERRAFORM-TEST.ps1"
  if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) { throw "Terraform validation failed with exit code $LASTEXITCODE." }
}

if (-not $SkipTests) {
  Step 'Running infrastructure/application smoke tests'
  & "$InstallRoot\setup\RUN-ALL-TESTS.ps1" -NoDockerStart
  if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) { throw "Smoke tests failed with exit code $LASTEXITCODE." }
}

if (-not $SkipAgentTests) {
  Step 'Running V1 agent/workflow discovery and executable tests'
  & "$InstallRoot\setup\TEST-V1-ALL-AGENTS.ps1" -NoDockerStart
  if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) { throw "V1 agent verification failed with exit code $LASTEXITCODE." }
}

Write-Host "`n=== NIVY NEXT AIOS V1 G: INSTALLATION FINISHED ===" -ForegroundColor Green
Write-Host "Repository: $InstallRoot"
Write-Host "Data:       $DataRoot"
Write-Host "Logs:       $LogRoot"
Write-Host 'Frontend:   http://localhost:3000'
Write-Host 'Backend:    http://localhost:8000/health'
Write-Host 'n8n:        http://localhost:5678'
Write-Host 'Qdrant:     http://localhost:6333'
Write-Host 'MinIO:      http://localhost:9001'
Write-Host 'Ollama:     http://localhost:11434'
Write-Host 'Reacher:    http://localhost:8080'
Write-Host 'Agent test: setup\TEST-V1-ALL-AGENTS.ps1'
Write-Host 'Note: Docker Desktop engine/WSL storage is controlled separately by Docker Desktop.'
