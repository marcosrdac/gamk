[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet('plan', 'install', 'repair-link', 'plan-mother', 'init-mother')]
    [string] $Command = 'plan',
    [Parameter(Position = 1)]
    [string] $Target,
    [ValidateSet('full', 'local', 'global')]
    [string] $Mode,
    [switch] $Local,
    [Alias('y')]
    [switch] $Yes
)

$ErrorActionPreference = 'Stop'
$ScriptPath = Join-Path $PSScriptRoot 'install.py'
$InstallerArguments = @($Command)

if ($PSBoundParameters.ContainsKey('Target')) {
    if ($Command -notin @('init-mother', 'plan-mother')) {
        $InstallerArguments += $Target
    }
    else {
        # Mother link commands operate on the current checkout, matching the Python CLI.
        if ((Resolve-Path -LiteralPath $Target).Path -ne (Resolve-Path -LiteralPath $PSScriptRoot).Path) {
            throw 'Mother link commands do not accept a separate target path.'
        }
    }
}
if ($Local) {
    $InstallerArguments += '--local'
}
if ($PSBoundParameters.ContainsKey('Mode')) {
    $InstallerArguments += @('--mode', $Mode)
}
if ($Yes) {
    $InstallerArguments += '--yes'
}

if (Get-Command python3 -ErrorAction SilentlyContinue) {
    & python3 $ScriptPath @InstallerArguments
    exit $LASTEXITCODE
}

if (Get-Command python -ErrorAction SilentlyContinue) {
    & python $ScriptPath @InstallerArguments
    exit $LASTEXITCODE
}

if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $ScriptPath @InstallerArguments
    exit $LASTEXITCODE
}

if (Get-Command nix -ErrorAction SilentlyContinue) {
    Write-Warning 'Python is not on PATH; launching through Nix (nixpkgs#python3).'
    & nix shell nixpkgs#python3 --command python3 $ScriptPath @InstallerArguments
    exit $LASTEXITCODE
}

Write-Error 'Python 3.10+ is required. Install Python or make python available through Nix.'
exit 127
