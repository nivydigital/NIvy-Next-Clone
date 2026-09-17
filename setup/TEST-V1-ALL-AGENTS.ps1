# Nivy Next AIOS — V1 agent/workflow verification runner
# This runner verifies the executable V1 revenue-engine API plus discovers agent/workflow
# definitions in the repository. It deliberately does not claim agents are tested when
# no concrete agent definitions are present in the canonical repo.
[CmdletBinding()]
param(
  [switch]$NoDockerStart,
  [switch]$RequireAgentDefinitions
)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Pass($Message) { Write-Host "PASS  $Message" -ForegroundColor Green }
function Warn($Message) { Write-Host "WARN  $Message" -ForegroundColor Yellow }
function Fail($Message) { Write-Host "FAIL  $Message" -ForegroundColor Red; throw $Message }
function Assert-Status($Name, $Expected, $Actual) {
  if ($Actual -ne $Expected) { Fail "$Name expected HTTP $Expected but received HTTP $Actual" }
  Pass "$Name -> HTTP $Actual"
}

if (-not $NoDockerStart) {
  docker compose up -d | Out-Host
}

& "$Root\setup\RUN-ALL-TESTS.ps1" -NoDockerStart

Write-Host "`n=== V1 REVENUE ENGINE EXECUTION TESTS ===" -ForegroundColor Cyan
$base = 'http://localhost:8000'
$stamp = [DateTime]::UtcNow.ToString('yyyyMMddHHmmssfff')
$email = "v1-test-$stamp@example.invalid"
$body = @{ name = 'V1 Automated Test Lead'; email = $email; company = 'Nivy V1 Test'; source = 'v1-agent-test' } | ConvertTo-Json

$create = Invoke-WebRequest -Uri "$base/api/v1/revenue/leads" -Method Post -ContentType 'application/json' -Body $body -UseBasicParsing
Assert-Status 'Revenue lead create' 201 $create.StatusCode
$lead = $create.Content | ConvertFrom-Json
if (-not $lead.id) { Fail 'Revenue lead create did not return an id' }
Pass "Revenue lead created: $($lead.id)"

$qualifyBody = @{ score = 85 } | ConvertTo-Json
$qualify = Invoke-WebRequest -Uri "$base/api/v1/revenue/leads/$($lead.id)/qualify" -Method Post -ContentType 'application/json' -Body $qualifyBody -UseBasicParsing
Assert-Status 'Revenue lead qualify' 200 $qualify.StatusCode
$qualified = $qualify.Content | ConvertFrom-Json
if ($qualified.status -ne 'qualified') { Fail "Lead status after qualification was '$($qualified.status)'" }
Pass 'Revenue lead qualification -> qualified'

$proposal = Invoke-WebRequest -Uri "$base/api/v1/revenue/leads/$($lead.id)/proposal/request" -Method Post -UseBasicParsing
Assert-Status 'Proposal approval request' 200 $proposal.StatusCode
$proposalState = $proposal.Content | ConvertFrom-Json
if ($proposalState.status -ne 'proposal_pending_approval') { Fail "Proposal state was '$($proposalState.status)'" }
Pass 'Proposal approval request -> pending approval'

$approve = Invoke-WebRequest -Uri "$base/api/v1/revenue/leads/$($lead.id)/proposal/approve" -Method Post -UseBasicParsing
Assert-Status 'Proposal approval' 200 $approve.StatusCode
$approved = $approve.Content | ConvertFrom-Json
if ($approved.status -ne 'proposal_approved') { Fail "Proposal approval state was '$($approved.status)'" }
Pass 'Proposal approval -> approved'

$summary = Invoke-WebRequest -Uri "$base/api/v1/revenue/summary" -UseBasicParsing
Assert-Status 'Revenue summary' 200 $summary.StatusCode
Pass 'Revenue summary endpoint responds'

Write-Host "`n=== AGENT / WORKFLOW DISCOVERY ===" -ForegroundColor Cyan
$searchRoots = @('agents','core','business','apps','data','docs') | Where-Object { Test-Path $_ }
$patterns = @('*.agent.*','*agent*.json','*agent*.yaml','*agent*.yml','*agent*.md','*agent*.py','*agent*.ps1','*workflow*.json','*workflow*.yaml','*workflow*.yml','*skill*.md')
$definitions = @()
foreach ($rootPath in $searchRoots) {
  foreach ($pattern in $patterns) {
    $definitions += Get-ChildItem -Path $rootPath -Recurse -File -Filter $pattern -ErrorAction SilentlyContinue
  }
}
$definitions = $definitions | Sort-Object FullName -Unique

$agentDefinitions = $definitions | Where-Object { $_.Name -match '(?i)agent' }
$workflowDefinitions = $definitions | Where-Object { $_.Name -match '(?i)workflow' }
$skillDefinitions = $definitions | Where-Object { $_.Name -match '(?i)skill' }

Write-Host "Discovered agent-definition candidates: $($agentDefinitions.Count)"
Write-Host "Discovered workflow-definition candidates: $($workflowDefinitions.Count)"
Write-Host "Discovered skill-definition candidates: $($skillDefinitions.Count)"

if ($agentDefinitions.Count -eq 0) {
  Warn 'No concrete agent definition files were found in the canonical repository. The executable revenue-engine lifecycle passed, but this run cannot honestly claim that every V1 agent has been tested.'
  if ($RequireAgentDefinitions) { Fail 'RequireAgentDefinitions was set, but no agent definitions were discovered.' }
} else {
  foreach ($file in $agentDefinitions) { Pass "Agent definition discovered: $($file.FullName.Substring($Root.Length + 1))" }
}

Write-Host "`n=== V1 AGENT TEST RESULT ===" -ForegroundColor Cyan
if ($agentDefinitions.Count -gt 0) {
  Write-Host "Executable V1 revenue engine: PASS" -ForegroundColor Green
  Write-Host "Agent definitions discovered: $($agentDefinitions.Count)" -ForegroundColor Green
} else {
  Write-Host 'Executable V1 revenue engine: PASS' -ForegroundColor Green
  Write-Host 'Concrete agent definitions: NOT PRESENT / NOT TESTABLE YET' -ForegroundColor Yellow
}
Write-Host 'Infrastructure smoke tests: PASS (delegated to RUN-ALL-TESTS.ps1)' -ForegroundColor Green
