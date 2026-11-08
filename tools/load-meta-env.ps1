# Load only the harness settings; never evaluate dotenv contents as code.
param([string]$Path = (Join-Path $PSScriptRoot '..\meta.env'))
$required = @('SWARM_LLM_BASE_URL', 'SWARM_LLM_MODEL', 'SWARM_LLM_API_KEY')
$settings = @{}
foreach ($line in [System.IO.File]::ReadAllLines((Resolve-Path -LiteralPath $Path).Path)) {
    if ($line.Trim().StartsWith('#') -or -not $line.Contains('=')) { continue }
    $pair = $line.Split(@('='), 2)
    $name = $pair[0].Trim()
    if ($name -notin $required) { continue }
    $value = $pair[1].Trim()
    if ($value.Length -ge 2 -and (($value.StartsWith('"') -and $value.EndsWith('"')) -or ($value.StartsWith("'") -and $value.EndsWith("'")))) {
        $value = $value.Substring(1, $value.Length - 2)
    }
    $settings[$name] = $value
}
$missing = @($required | Where-Object { [string]::IsNullOrWhiteSpace($settings[$_]) })
if ($missing.Count) { throw ('Fill these fields in meta.env first: ' + ($missing -join ', ')) }
foreach ($name in $required) {
    [System.Environment]::SetEnvironmentVariable($name, $settings[$name], 'Process')
}
Write-Host 'Loaded all three harness variables into this PowerShell session. Values are hidden.'
