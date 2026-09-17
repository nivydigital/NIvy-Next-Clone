terraform {
  required_version = ">= 1.6.0"
}

# This module is intentionally local and non-destructive by default.
# Docker Compose remains the runtime definition; Terraform validates the
# local test contract and can optionally execute the existing smoke suite.

resource "terraform_data" "aios_runtime_contract" {
  input = {
    repository = "nivyindia/Nivy-Next-AIOS"
    runtime    = "docker-compose"
    test_runner = "setup/RUN-ALL-TESTS.ps1"
  }

  provisioner "local-exec" {
    interpreter = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command"]
    command     = "& '${path.root}/../setup/RUN-ALL-TESTS.ps1' -NoDockerStart"
  }
}

output "runtime_contract" {
  value = terraform_data.aios_runtime_contract.input
}
