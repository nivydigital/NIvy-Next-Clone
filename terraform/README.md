# Terraform PC Infrastructure Test Package

## ⚡ QUICK START

| Item | Action |
|---|---|
| Purpose | Validate the local AIOS runtime contract with Terraform + Docker smoke tests |
| Start | Run `setup/INSTALL-ALL-WINDOWS.ps1` |
| Terraform checks | `terraform init` → `terraform fmt -check` → `terraform validate` → `terraform plan` |
| Runtime test | Terraform apply can execute the existing smoke-test runner |
| Default behavior | Non-destructive validation/plan; no Terraform apply |
| Full local execution | `setup/TERRAFORM-TEST.ps1 -Apply` |

## What Terraform does

Terraform is the infrastructure-test/orchestration layer for the PC runtime. Docker Compose remains the canonical service definition. The Terraform module does not recreate the application stack or replace Compose.

The module validates its configuration and, when `-Apply` is explicitly selected, executes the repository's existing smoke-test runner against the already-started local Docker stack.

## Commands

From the repository root:

```powershell
.\setup\TERRAFORM-TEST.ps1
```

For validation plus execution of the local smoke-test command through Terraform:

```powershell
.\setup\TERRAFORM-TEST.ps1 -Apply
```

The `-Apply` mode is intentionally explicit because Terraform provisioners execute commands during apply.

## Scope

This package verifies the infrastructure/runtime layer. Passing it does **not** mean every agent, skill, workflow, business process, integration or production deployment is complete.
