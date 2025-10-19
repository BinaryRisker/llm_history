# Fix EPUB Cover for E-Reader Shelf Display
# Adds EPUB 2.0 compatible meta tag for better compatibility

$epubPath = "output/llm-history-chronicle.epub"
$tempDir = "output/temp_epub_fix"

Write-Host "Adding EPUB 2.0 cover meta tag..." -ForegroundColor Yellow

# Check if EPUB exists
if (-not (Test-Path $epubPath)) {
    Write-Host "[ERROR] EPUB file not found: $epubPath" -ForegroundColor Red
    exit 1
}

# Backup original EPUB
$backupPath = "output/llm-history-chronicle-backup.epub"
if (Test-Path $backupPath) { Remove-Item $backupPath -Force }
Copy-Item $epubPath $backupPath -Force

# Rename to .zip temporarily
$zipPath = "output/llm-history-chronicle-temp.zip"
Copy-Item $epubPath $zipPath -Force

# Extract ZIP
if (Test-Path $tempDir) { Remove-Item -Recurse -Force $tempDir }
Expand-Archive -Path $zipPath -DestinationPath $tempDir -Force
Remove-Item $zipPath -Force

# Find content.opf
$opfPath = Get-ChildItem -Path $tempDir -Filter "content.opf" -Recurse | Select-Object -First 1 -ExpandProperty FullName

if (-not $opfPath) {
    Write-Host "[ERROR] content.opf not found in EPUB" -ForegroundColor Red
    Remove-Item -Recurse -Force $tempDir
    exit 1
}

Write-Host "[INFO] Found content.opf at: $opfPath" -ForegroundColor Cyan

$content = [System.IO.File]::ReadAllText($opfPath, [System.Text.Encoding]::UTF8)

# Add EPUB 2.0 cover meta tag if not present
if ($content -notmatch '<meta name="cover"') {
    # Insert before </metadata> closing tag
    $content = $content -replace '([ \t]*</metadata>)', "  <meta name=`"cover`" content=`"cover-5-complex_png`"/>`r`n`$1"
    [System.IO.File]::WriteAllText($opfPath, $content, [System.Text.Encoding]::UTF8)
    Write-Host "[OK] Added EPUB 2.0 cover meta tag" -ForegroundColor Green
} else {
    Write-Host "[INFO] Cover meta tag already exists" -ForegroundColor Cyan
    Remove-Item -Recurse -Force $tempDir
    exit 0
}

# Repackage EPUB using correct ZIP structure
Write-Host "[INFO] Repackaging EPUB..." -ForegroundColor Cyan

# Remove old EPUB
Remove-Item $epubPath -Force

# Change to temp directory
Push-Location $tempDir

# Use 7-Zip if available, otherwise use System.IO.Compression
$use7zip = Get-Command "7z.exe" -ErrorAction SilentlyContinue

if ($use7zip) {
    Write-Host "[INFO] Using 7-Zip for packaging" -ForegroundColor Cyan
    # 7-Zip creates proper EPUB without compression issues
    & 7z.exe a -tzip "../llm-history-chronicle.epub" * -mx0 | Out-Null
} else {
    Write-Host "[INFO] Using .NET compression" -ForegroundColor Cyan
    # Use .NET compression with store method to preserve EPUB structure
    Add-Type -AssemblyName System.IO.Compression.FileSystem

    $epubFullPath = Join-Path (Split-Path $tempDir -Parent) "llm-history-chronicle.epub"

    # Create new ZIP archive
    $zip = [System.IO.Compression.ZipFile]::Open($epubFullPath, [System.IO.Compression.ZipArchiveMode]::Create)

    # Add all files maintaining directory structure
    Get-ChildItem -Recurse -File | ForEach-Object {
        $relativePath = $_.FullName.Substring($tempDir.Length + 1).Replace('\', '/')
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $_.FullName, $relativePath, [System.IO.Compression.CompressionLevel]::Optimal) | Out-Null
    }

    $zip.Dispose()
}

Pop-Location

# Clean up
Remove-Item -Recurse -Force $tempDir

if (Test-Path $epubPath) {
    Remove-Item $backupPath -Force
    $epubSize = (Get-Item $epubPath).Length / 1KB
    $epubSizeRounded = [math]::Round($epubSize, 1)
    Write-Host "[SUCCESS] EPUB fixed: $epubSizeRounded KB" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to create EPUB, restoring backup" -ForegroundColor Red
    Move-Item $backupPath $epubPath -Force
    exit 1
}
