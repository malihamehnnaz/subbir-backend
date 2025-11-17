<#
Run the FastAPI app locally using settings from .env.dev.

Usage:
1. (Optional) Start MailHog with Docker to capture test emails:
   docker compose up -d mailhog

2. From project root, activate your virtualenv (if you have one):
   # Windows PowerShell example (created with python -m venv .venv)
   .\.venv\Scripts\Activate.ps1

3. Run this script from the services/email_api folder or from repo root:
   .\services\email_api\run-local.ps1

This script reads `services/email_api/.env.dev` and sets environment variables
in the current PowerShell session, then starts uvicorn.
#>

$envFile = Join-Path -Path $PSScriptRoot -ChildPath ".env.dev"
if (-not (Test-Path $envFile)) {
    Write-Error "Env file not found: $envFile"
    exit 1
}

Write-Host "Loading environment from $envFile"
Get-Content $envFile | ForEach-Object {
    $_ = $_.Trim()
    if ($_ -eq "" -or $_.StartsWith("#")) { return }
    $parts = $_ -split '='
    if ($parts.Count -ge 2) {
        $name = $parts[0].Trim()
        $value = ($parts[1..($parts.Count-1)] -join '=').Trim()
        Write-Host "Setting $name"
        Set-Item -Path Env:\$name -Value $value
    }
}

Write-Host "Starting uvicorn..."
python -m uvicorn services.email_api.main:app --reload --port 8000
