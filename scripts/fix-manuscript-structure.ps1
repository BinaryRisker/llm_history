#!/usr/bin/env pwsh
# Manuscript Directory Structure Fix Script
# Purpose: Fix duplicate directory numbering and reorganize by timeline
# Generated: 2025-10-18

Write-Host "=== Manuscript Directory Structure Fix Script ===" -ForegroundColor Cyan
Write-Host ""

# Configuration
$baseDir = "D:\code\github\llm_history\manuscript"
$backupBranch = "backup-manuscript-structure-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

# Function to show current structure
function Show-CurrentStructure {
    Write-Host "`nCurrent manuscript structure:" -ForegroundColor Yellow
    Get-ChildItem -Path $baseDir -Directory | ForEach-Object {
        $fileCount = (Get-ChildItem -Path $_.FullName -File -Recurse).Count
        Write-Host "  $($_.Name) ($fileCount files)" -ForegroundColor Gray
    }
}

# Function to execute step with confirmation
function Execute-Step {
    param(
        [string]$Description,
        [scriptblock]$Action,
        [bool]$RequireConfirm = $true
    )

    Write-Host "`n>>> $Description" -ForegroundColor Green

    if ($RequireConfirm) {
        $confirm = Read-Host "Execute this step? (Y/n)"
        if ($confirm -eq 'n' -or $confirm -eq 'N') {
            Write-Host "Skipped." -ForegroundColor Yellow
            return $false
        }
    }

    try {
        & $Action
        Write-Host "✓ Completed" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "✗ Error: $_" -ForegroundColor Red
        return $false
    }
}

# Main execution
Write-Host "This script will reorganize the manuscript directory structure." -ForegroundColor Cyan
Write-Host "It will fix duplicate directory numbering and align with timeline order." -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT: This will:" -ForegroundColor Yellow
Write-Host "  1. Create a git backup branch" -ForegroundColor Yellow
Write-Host "  2. Delete empty directories" -ForegroundColor Yellow
Write-Host "  3. Rename and reorganize directories" -ForegroundColor Yellow
Write-Host "  4. Move files between directories" -ForegroundColor Yellow
Write-Host "  5. Update chapter numbers in frontmatter" -ForegroundColor Yellow
Write-Host ""

$proceed = Read-Host "Do you want to proceed? (yes/no)"
if ($proceed -ne 'yes') {
    Write-Host "Aborted by user." -ForegroundColor Red
    exit 0
}

Show-CurrentStructure

# Step 0: Git backup
Execute-Step "Creating git backup branch '$backupBranch'" {
    Set-Location "D:\code\github\llm_history"
    git checkout -b $backupBranch
    git add .
    git commit -m "Backup before manuscript structure reorganization"
} -RequireConfirm $false

# Step 1: Delete empty directory
Execute-Step "Delete empty directory: 03-parallel-developments" {
    $dir = Join-Path $baseDir "03-parallel-developments"
    if (Test-Path $dir) {
        $isEmpty = (Get-ChildItem -Path $dir -File -Recurse).Count -eq 0
        if ($isEmpty) {
            Remove-Item -Path $dir -Force -Recurse
            Write-Host "  Deleted: $dir"
        } else {
            Write-Host "  Warning: Directory not empty, skipping" -ForegroundColor Yellow
        }
    }
}

# Step 2: Rename directories (按照方案A)
Execute-Step "Rename directories to new structure" {
    $renames = @(
        @{Old = "03-alignment-breakthrough"; New = "03-alignment"}
        @{Old = "04-chatgpt-mainstream"; New = "04-chatgpt-revolution"}
        @{Old = "04-global-competition"; New = "05-global-race-2023"}
        @{Old = "05-multimodal-agent"; New = "07-multimodal-era"}
        @{Old = "06-recent-developments"; New = "08-present"}
    )

    foreach ($rename in $renames) {
        $oldPath = Join-Path $baseDir $rename.Old
        $newPath = Join-Path $baseDir $rename.New

        if (Test-Path $oldPath) {
            if (Test-Path $newPath) {
                Write-Host "  Warning: Target already exists: $($rename.New)" -ForegroundColor Yellow
            } else {
                Move-Item -Path $oldPath -Destination $newPath
                Write-Host "  Renamed: $($rename.Old) → $($rename.New)"
            }
        } else {
            Write-Host "  Not found: $($rename.Old)" -ForegroundColor Yellow
        }
    }
}

# Step 3: Move meta-llama.md to new location
Execute-Step "Move meta-llama.md to 05-global-race-2023/" {
    $source = Join-Path $baseDir "05-global-competition\meta-llama.md"
    $dest = Join-Path $baseDir "05-global-race-2023\meta-llama.md"

    if (Test-Path $source) {
        Move-Item -Path $source -Destination $dest -Force
        Write-Host "  Moved: meta-llama.md"
    } else {
        Write-Host "  Warning: Source file not found" -ForegroundColor Yellow
    }
}

# Step 4: Delete now-empty 05-global-competition
Execute-Step "Delete now-empty 05-global-competition directory" {
    $dir = Join-Path $baseDir "05-global-competition"
    if (Test-Path $dir) {
        $isEmpty = (Get-ChildItem -Path $dir -File -Recurse).Count -eq 0
        if ($isEmpty) {
            Remove-Item -Path $dir -Force -Recurse
            Write-Host "  Deleted: $dir"
        } else {
            Write-Host "  Warning: Directory not empty, skipping" -ForegroundColor Yellow
        }
    }
}

# Step 5: Create missing directories
Execute-Step "Create missing directory: 06-chinese-ai" {
    $dir = Join-Path $baseDir "06-chinese-ai"
    if (-not (Test-Path $dir)) {
        New-Item -Path $dir -ItemType Directory -Force | Out-Null
        Write-Host "  Created: $dir"
    } else {
        Write-Host "  Already exists: $dir"
    }
}

# Step 6: Update chapter numbers in frontmatter
Execute-Step "Update chapter numbers in file frontmatter" {
    $updates = @(
        @{File = "04-chatgpt-revolution\chatgpt-launch.md"; OldNum = 6; NewNum = 5}
        @{File = "05-global-race-2023\ai-race-2023.md"; OldNum = 5; NewNum = 6}
        @{File = "07-multimodal-era\2024-breakthroughs.md"; OldNum = 6; NewNum = 10}
    )

    foreach ($update in $updates) {
        $filePath = Join-Path $baseDir $update.File

        if (Test-Path $filePath) {
            $content = Get-Content -Path $filePath -Raw
            $pattern = "chapter_number: $($update.OldNum)"
            $replacement = "chapter_number: $($update.NewNum)"

            if ($content -match $pattern) {
                $newContent = $content -replace $pattern, $replacement
                Set-Content -Path $filePath -Value $newContent -NoNewline
                Write-Host "  Updated: $($update.File) (Chapter $($update.OldNum) → $($update.NewNum))"
            } else {
                Write-Host "  Warning: Pattern not found in $($update.File)" -ForegroundColor Yellow
            }
        } else {
            Write-Host "  Warning: File not found: $($update.File)" -ForegroundColor Yellow
        }
    }
}

# Show new structure
Write-Host "`n" + "="*50 -ForegroundColor Cyan
Show-CurrentStructure

Write-Host "`n=== Fix completed! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review the changes with: git status" -ForegroundColor Gray
Write-Host "  2. Review the full diff with: git diff" -ForegroundColor Gray
Write-Host "  3. If satisfied, commit: git add . && git commit -m 'Fix manuscript directory structure'" -ForegroundColor Gray
Write-Host "  4. If issues found, rollback: git checkout 001-llm-history-chronicle && git branch -D $backupBranch" -ForegroundColor Gray
Write-Host "  5. Update tasks.md to match new structure" -ForegroundColor Gray
Write-Host "  6. Create missing chapters (Chapter 7, 9)" -ForegroundColor Gray
Write-Host ""
