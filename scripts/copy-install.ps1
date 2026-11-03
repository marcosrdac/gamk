[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string] $Target
)

$ErrorActionPreference = 'Stop'
$SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$TargetRoot = [System.IO.Path]::GetFullPath($Target)
if (-not (Test-Path -LiteralPath $TargetRoot)) {
    New-Item -ItemType Directory -Path $TargetRoot | Out-Null
}

# Minimal copy-only path: refuse known existing context; never migrate/overwrite it.
foreach ($relative in @('AGENTS.md', 'CLAUDE.md', 'GEMINI.md', '.cursorrules', '.ai')) {
    $candidate = Join-Path $TargetRoot $relative
    if (Test-Path -LiteralPath $candidate) {
        Write-Error "Copy install refused: existing project context at $candidate. No files were copied. Use scripts/install.ps1 plan '$TargetRoot' for migration-aware planning." -ErrorAction Continue
        exit 2
    }
}

foreach ($relative in @('.cursor/rules', '.github/instructions', '.cline/rules', '.roo/rules', '.windsurf/rules')) {
    $candidate = Join-Path $TargetRoot $relative
    if (Test-Path -LiteralPath $candidate) {
        Write-Error "Copy install refused: existing agent configuration at $candidate. No files were copied. Use scripts/install.ps1 plan '$TargetRoot' for migration-aware planning." -ErrorAction Continue
        exit 2
    }
}

$directories = @(
    'decisions', 'forms/creating', 'forms/pending', 'forms/answered',
    'investigations/doing', 'investigations/closed/done', 'investigations/closed/wontdo',
    'logs', 'rules', 'skills', 'templates', 'wiki', 'work/doing', 'work/next',
    'work/pool/backlog', 'work/pool/blocked', 'work/pool/ideas',
    'work/closed/done', 'work/closed/wontdo', 'workflows'
)

New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot '.ai') | Out-Null
foreach ($relative in $directories) {
    New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot (Join-Path '.ai' $relative)) | Out-Null
}

Copy-Item -LiteralPath (Join-Path $SourceRoot 'global/templates/project/AGENTS.md') -Destination (Join-Path $TargetRoot 'AGENTS.md')
Write-Output "Files copied into $TargetRoot"
Write-Output 'This minimal installer did not configure a global link or write a provenance manifest.'
Write-Output 'For global linking, provenance, broader conflict detection, or migration planning, use scripts/install.ps1.'
