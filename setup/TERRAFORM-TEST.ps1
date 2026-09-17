# Nivy Next AIOS — Terraform infrastructure test runner
[CmdletBinding()]
param(
  [switch]$Apply
)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$TerraformRoot = Join-Path $Root 'terraform'
Set-Location $TerraformRoot

if (-not (Get-Command terraform -ErrorAction SilentlyContinue)) {
  throw 'Terraform is not installed or not on PATH. Run setup/INSTALL-ALL-WINDOWS.ps1 first.'
}

Write-Host 'Terraform version:' -ForegroundColor Cyan
terraform version

Write-Host "`n==> terraform init" -ForegroundColor Cyan
terraform init -input=false

Write-Host "`n==> terraform fmt check" -ForegroundColor Cyan
terraform fmt -check

Write-Host "`n==> terraform validate" -ForegroundColor Cyan
terraform validate

Write-Host "`n==> terraform plan" -ForegroundColor Cyan
terraform plan -input=false -out=aios.tfplan

if ($Apply) {
  Write-Host "`n==> terraform apply" -ForegroundColor Yellow
  terraform apply -input=false -auto-approve aios.tfplan
}

Write-Host "`nTERRAFORM INFRASTRUCTURE CHECKS PASSED" -ForegroundColor Green
if (-not $Apply) {
  Write-Host 'No infrastructure-changing Terraform apply was executed. Use -Apply only when you want Terraform to execute the local runtime test actions.'
}
