# Nivy Next AIOS — local smoke/integration test runner
[CmdletBinding()]
param([switch]$NoDockerStart)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Assert-Url($Name, $Url) {
  try {
    $r = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 15
    if ($r.StatusCode -ge 200 -and $r.StatusCode -lt 500) { Write-Host "PASS  $Name -> $($r.StatusCode)" -ForegroundColor Green }
    else { throw "HTTP $($r.StatusCode)" }
  } catch { throw "FAIL  $Name -> $Url : $($_.Exception.Message)" }
}

if (-not $NoDockerStart) {
  docker compose up -d | Out-Host
}

Write-Host 'Checking container state...'
$services = @('nivy-backend','nivy-frontend','nivy-postgres','nivy-redis','nivy-qdrant','nivy-minio','nivy-ollama','nivy-n8n','nivy-reacher')
$running = docker ps --format '{{.Names}}'
foreach ($s in $services) {
  if ($running -contains $s) { Write-Host "PASS  container $s" -ForegroundColor Green }
  else { throw "FAIL  container $s is not running" }
}

Assert-Url 'Backend health' 'http://localhost:8000/health'
Assert-Url 'Backend system' 'http://localhost:8000/api/v1/system'
Assert-Url 'Frontend' 'http://localhost:3000'
Assert-Url 'n8n' 'http://localhost:5678'
Assert-Url 'Qdrant' 'http://localhost:6333'
Assert-Url 'MinIO console' 'http://localhost:9001'
Assert-Url 'Ollama' 'http://localhost:11434/api/tags'

Write-Host "`nALL LOCAL AIOS V1 SMOKE TESTS PASSED" -ForegroundColor Green
