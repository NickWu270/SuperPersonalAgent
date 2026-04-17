# Usage: from repo root,  .\scripts\run_with_langgraph.ps1
# Requires: conda env "langgraph", and .env or env vars for API keys.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

conda run -n langgraph python main.py
