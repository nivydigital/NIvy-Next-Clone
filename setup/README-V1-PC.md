# Nivy Next AIOS V1 — Windows G: Install, Runtime & Full V1 Testing

## ⚡ ONE-CLICK INSTALL

The canonical Windows V1 layout now defaults to:

```text
G:\Docker\Nivy\
├── Repository\Nivy-Next-AIOS\   # Git repository / source
├── Data\
│   ├── postgres\
│   ├── qdrant\
│   ├── minio\
│   ├── ollama\
│   └── n8n\
└── Logs\
```

From the cloned repository, double-click:

**`INSTALL-NIVY-V1.bat`**

It creates the G: layout, checks/installs prerequisites, clones/updates the repository, writes the local `.env`, binds persistent Docker application data to G:, starts the runtime, runs Terraform validation/plan, runs infrastructure smoke tests, and then runs the V1 revenue/agent verification runner.

### PowerShell equivalent

```powershell
Set-ExecutionPolicy -Scope Process Bypass
& .\setup\INSTALL-ALL-WINDOWS.ps1 -InstallRoot 'G:\Docker\Nivy\Repository\Nivy-Next-AIOS' -DataRoot 'G:\Docker\Nivy\Data' -LogRoot 'G:\Docker\Nivy\Logs'
```

### Direct remote bootstrap

```powershell
Set-ExecutionPolicy -Scope Process Bypass
irm https://raw.githubusercontent.com/nivyindia/Nivy-Next-AIOS/main/setup/INSTALL-ALL-WINDOWS.ps1 | iex
```

The remote command now uses the G: defaults built into the script. You can override them with explicit parameters when running the downloaded script locally.

## 🧪 FULL V1 TEST

After installation, double-click:

**`TEST-NIVY-V1.bat`**

Or run:

```powershell
& 'G:\Docker\Nivy\Repository\Nivy-Next-AIOS\setup\TEST-V1-ALL-AGENTS.ps1'
```

The full runner executes:

1. Container/runtime checks.
2. Backend, frontend, n8n, Qdrant, MinIO and Ollama endpoint checks.
3. V1 revenue-engine lifecycle: create lead → qualify → request proposal approval → approve proposal → summary.
4. Repository discovery for concrete agent, workflow and skill definitions.
5. An explicit warning when concrete agent definitions are absent, so infrastructure success is never presented as proof that all agents passed.

To make absence of concrete agent definitions a hard failure:

```powershell
& 'G:\Docker\Nivy\Repository\Nivy-Next-AIOS\setup\TEST-V1-ALL-AGENTS.ps1' -RequireAgentDefinitions
```

### Current canonical-repository limitation

The `agents/` directory currently contains only `.gitkeep`; therefore there are **no concrete agent definition files in that directory to execute**. The V1 revenue engine is executable and is tested by the runner, but the repository cannot honestly report that every named V1 agent has passed until those agent definitions are present in the canonical repository.

## Terraform

```powershell
cd 'G:\Docker\Nivy\Repository\Nivy-Next-AIOS'
.\setup\TERRAFORM-TEST.ps1
```

Explicit apply:

```powershell
.\setup\TERRAFORM-TEST.ps1 -Apply
```

## Run infrastructure smoke tests only

```powershell
& 'G:\Docker\Nivy\Repository\Nivy-Next-AIOS\setup\RUN-ALL-TESTS.ps1'
```

## Runtime control

```powershell
cd 'G:\Docker\Nivy\Repository\Nivy-Next-AIOS'
docker compose stop
docker compose start
```

Rebuild:

```powershell
docker compose up -d --build
& .\setup\TEST-V1-ALL-AGENTS.ps1 -NoDockerStart
```

## Main local URLs

| Component | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend health | http://localhost:8000/health |
| Backend system | http://localhost:8000/api/v1/system |
| n8n | http://localhost:5678 |
| Qdrant | http://localhost:6333 |
| MinIO console | http://localhost:9001 |
| Ollama | http://localhost:11434 |
| Reacher | http://localhost:8080 |

## Storage policy

The Compose runtime uses configurable host bind mounts for PostgreSQL, Qdrant, MinIO, Ollama and n8n. The G: installer sets these to `G:\Docker\Nivy\Data\<service>` and writes the corresponding paths into `.env`.

This keeps Nivy's repository and persistent application data on G:. **Docker Desktop's own application files, WSL2 distribution and engine disk image are separate from the Compose bind mounts and remain controlled by Docker Desktop's storage configuration.** Therefore this package does not falsely claim that every byte belonging to Docker Desktop is moved to G:.

## Security

- Never commit real API keys/passwords.
- Keep secrets in the local `.env`.
- Change development placeholder credentials before any non-local deployment.
- The V1 test suite is an executable validation gate, not a production-readiness certification.

## Package files

- `INSTALL-NIVY-V1.bat` — one-click G: installation.
- `TEST-NIVY-V1.bat` — one-click V1 test.
- `setup/INSTALL-ALL-WINDOWS.ps1` — parameterized installer.
- `setup/TEST-V1-ALL-AGENTS.ps1` — V1 revenue + agent/workflow/skill verification.
- `setup/RUN-ALL-TESTS.ps1` — infrastructure/application smoke tests.
- `setup/TERRAFORM-TEST.ps1` — Terraform validation/plan/apply test layer.
- `docker-compose.yml` — canonical local runtime.
- `.env.example` — environment template.
