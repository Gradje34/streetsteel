# ============================================================
# inventariseer.ps1 — Streetsteel migratie voorbereiding
# Draaien op: WERKLAPTOP
# Gebruik: Rechtsklik > "Uitvoeren met PowerShell"
#          of in terminal: .\inventariseer.ps1
# ============================================================

$rapport = @()
$rapport += "===== STREETSTEEL MIGRATIE RAPPORT ====="
$rapport += "Gegenereerd op: $(Get-Date -Format 'dd-MM-yyyy HH:mm')"
$rapport += ""

# --- Git ---
$rapport += "--- GIT ---"
try {
    $gitVersie = git --version 2>&1
    $rapport += "Versie: $gitVersie"
    $rapport += "Gebruiker: $(git config --global user.name)"
    $rapport += "E-mail: $(git config --global user.email)"
} catch {
    $rapport += "Git NIET gevonden!"
}
$rapport += ""

# --- Node.js en npm ---
$rapport += "--- NODE.JS ---"
try {
    $nodeVersie = node --version 2>&1
    $npmVersie  = npm --version 2>&1
    $rapport += "Node versie: $nodeVersie"
    $rapport += "npm versie:  $npmVersie"
} catch {
    $rapport += "Node.js NIET gevonden!"
}
$rapport += ""

# --- Globale npm packages ---
$rapport += "--- GLOBALE NPM PACKAGES ---"
try {
    $globals = npm list -g --depth=0 2>&1
    $rapport += $globals
} catch {
    $rapport += "(geen of fout)"
}
$rapport += ""

# --- Netlify CLI ---
$rapport += "--- NETLIFY CLI ---"
try {
    $netlifyVersie = netlify --version 2>&1
    $rapport += "Versie: $netlifyVersie"
} catch {
    $rapport += "Netlify CLI NIET gevonden"
}
$rapport += ""

# --- VS Code ---
$rapport += "--- VS CODE ---"
try {
    $codeVersie = code --version 2>&1
    $rapport += "Versie: $($codeVersie[0])"
    $rapport += ""
    $rapport += "Extensies:"
    $extensies = code --list-extensions 2>&1
    $rapport += $extensies
    # Sla extensielijst ook apart op voor gebruik in installeer.ps1
    $extensies | Out-File -FilePath ".\vscode-extensies.txt" -Encoding UTF8
    $rapport += "(ook opgeslagen als vscode-extensies.txt)"
} catch {
    $rapport += "VS Code NIET gevonden of niet in PATH"
}
$rapport += ""

# --- Zoek streetsteel projectmap ---
$rapport += "--- STREETSTEEL PROJECT ---"
$zoekPaden = @(
    "$env:USERPROFILE\streetsteel",
    "$env:USERPROFILE\Documents\streetsteel",
    "$env:USERPROFILE\Projects\streetsteel",
    "$env:USERPROFILE\Desktop\streetsteel",
    "C:\Projects\streetsteel",
    "C:\dev\streetsteel"
)

$gevonden = $null
foreach ($pad in $zoekPaden) {
    if (Test-Path $pad) {
        $gevonden = $pad
        break
    }
}

if ($gevonden) {
    $rapport += "Projectmap gevonden: $gevonden"
    Push-Location $gevonden

    # Git remote
    try {
        $remote = git remote get-url origin 2>&1
        $rapport += "GitHub remote: $remote"
    } catch {
        $rapport += "Geen git remote gevonden"
    }

    # Git status
    try {
        $status = git status --short 2>&1
        if ($status) {
            $rapport += ""
            $rapport += "LET OP — uncommitted wijzigingen:"
            $rapport += $status
        } else {
            $rapport += "Git status: alles committed"
        }
    } catch {}

    # package.json scripts
    if (Test-Path ".\package.json") {
        $rapport += ""
        $rapport += "package.json scripts:"
        $pkg = Get-Content ".\package.json" | ConvertFrom-Json
        $pkg.scripts.PSObject.Properties | ForEach-Object {
            $rapport += "  $($_.Name): $($_.Value)"
        }
    }

    # .env bestanden
    $rapport += ""
    $rapport += ".env bestanden (INHOUD NIET gelogd — kopieer handmatig):"
    Get-ChildItem -Filter ".env*" -Force | ForEach-Object {
        $rapport += "  Gevonden: $($_.Name)"
    }

    # Netlify koppeling
    if (Test-Path ".\.netlify\state.json") {
        $rapport += ""
        $rapport += "Netlify site koppeling:"
        $rapport += (Get-Content ".\.netlify\state.json" -Raw)
    }

    Pop-Location
} else {
    $rapport += "Projectmap NIET automatisch gevonden."
    $rapport += "Zoek handmatig en noteer het pad hieronder:"
    $rapport += "  PAD: ___________________________________"
}
$rapport += ""

# --- Samenvatting acties voor vertrek ---
$rapport += "===== ACTIES VOOR 16 JUNI ====="
$rapport += "[ ] Git push gedaan vanuit projectmap (git push)"
$rapport += "[ ] .env bestand(en) veilig opgeslagen (USB / wachtwoordmanager)"
$rapport += "[ ] Dit rapport opgeslagen"
$rapport += "[ ] vscode-extensies.txt opgeslagen"
$rapport += ""

# Rapport wegschrijven
$rapport | Out-File -FilePath ".\streetsteel-migratie-rapport.txt" -Encoding UTF8
$rapport | ForEach-Object { Write-Host $_ }

Write-Host ""
Write-Host "✓ Rapport opgeslagen als: streetsteel-migratie-rapport.txt" -ForegroundColor Green
Write-Host "  Bewaar dit bestand samen met vscode-extensies.txt op een USB-stick of stuur het naar jezelf." -ForegroundColor Cyan
