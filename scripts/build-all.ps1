# Build All Formats - PowerShell Script

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "LLM History Chronicle - Format Conversion" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Default cover image
$coverImage = "assets/images/cover-5-complex.svg"
Write-Host "[INFO] Using cover: $coverImage" -ForegroundColor Cyan

# Check if Pandoc is installed
if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Pandoc not installed" -ForegroundColor Red
    Write-Host "Download from: https://pandoc.org/installing.html" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Pandoc installed: " -NoNewline -ForegroundColor Green
pandoc --version | Select-Object -First 1

# Create output directory
New-Item -ItemType Directory -Force -Path output | Out-Null

# Copy assets to output directory for HTML
New-Item -ItemType Directory -Force -Path output/assets/images | Out-Null
Copy-Item assets/images/*.svg output/assets/images/ -Force

# Copy config files for HTML styling
New-Item -ItemType Directory -Force -Path output/config | Out-Null
Copy-Item config/html-style.css output/config/ -Force

# Chapter files in correct chronological order
$mdFiles = @(
    "manuscript/00-frontmatter/cover.md",
    "manuscript/00-frontmatter/preface.md",
    "manuscript/00-frontmatter/reading-guide.md",
    "manuscript/00-frontmatter/acknowledgments.md",
    "manuscript/01-foundation/transformer-revolution.md",
    "manuscript/01-foundation/early-applications.md",
    "manuscript/02-gpt-era/scaling-up.md",
    "manuscript/02-gpt-era/google-response.md",
    "manuscript/03-alignment/rlhf-chatgpt.md",
    "manuscript/04-chatgpt-revolution/chatgpt-launch.md",
    "manuscript/05-global-race-2023/ai-race-2023.md",
    "manuscript/05-global-race-2023/meta-llama.md",
    "manuscript/06-chinese-ai/chinese-development.md",
    "manuscript/07-multimodal-era/2024-breakthroughs.md",
    "manuscript/08-present/2025-present.md",
    "manuscript/99-backmatter/glossary.md",
    "manuscript/99-backmatter/references.md",
    "manuscript/99-backmatter/index.md"
)

Write-Host "Total files: $($mdFiles.Count) (including cover)" -ForegroundColor Cyan
Write-Host ""

# 1. Generate HTML
Write-Host "[1/3] Generating HTML..." -ForegroundColor Yellow
$htmlArgs = $mdFiles + @(
    "-o", "output/llm-history-chronicle.html",
    "--standalone",
    "--toc",
    "--toc-depth=2",
    "--number-sections",
    "--css=config/html-style.css",
    "--metadata", "title=LLM History Chronicle",
    "--metadata", "author=AI History Chronicler"
)
& pandoc $htmlArgs

if (Test-Path "output/llm-history-chronicle.html") {
    $htmlSize = (Get-Item "output/llm-history-chronicle.html").Length / 1KB
    $htmlSizeRounded = [math]::Round($htmlSize, 1)
    Write-Host "[OK] HTML generated with cover: output/llm-history-chronicle.html ($htmlSizeRounded KB)" -ForegroundColor Green
}

# 2. Generate ePub
Write-Host ""
Write-Host "[2/3] Generating ePub..." -ForegroundColor Yellow
$epubArgs = $mdFiles + @(
    "-o", "output/llm-history-chronicle.epub",
    "--metadata-file=config/epub-metadata.yaml",
    "--toc",
    "--toc-depth=2",
    "--css=config/epub-style.css"
)
& pandoc $epubArgs

if (Test-Path "output/llm-history-chronicle.epub") {
    $epubSize = (Get-Item "output/llm-history-chronicle.epub").Length / 1KB
    $epubSizeRounded = [math]::Round($epubSize, 1)
    Write-Host "[OK] ePub generated: output/llm-history-chronicle.epub ($epubSizeRounded KB)" -ForegroundColor Green
}

# 3. Generate PDF
Write-Host ""
Write-Host "[3/3] Generating PDF..." -ForegroundColor Yellow

if (Get-Command xelatex -ErrorAction SilentlyContinue) {
    $pdfArgs = $mdFiles + @(
        "-o", "output/llm-history-chronicle.pdf",
        "--metadata-file=config/pdf-metadata.yaml",
        "--pdf-engine=xelatex",
        "--toc",
        "--number-sections",
        "-V", "CJKmainfont=SimSun"
    )
    & pandoc $pdfArgs

    if (Test-Path "output/llm-history-chronicle.pdf") {
        $pdfSize = (Get-Item "output/llm-history-chronicle.pdf").Length / 1KB
        $pdfSizeRounded = [math]::Round($pdfSize, 1)
        Write-Host "[OK] PDF generated: output/llm-history-chronicle.pdf ($pdfSizeRounded KB)" -ForegroundColor Green
    }
} else {
    Write-Host "[WARN] XeLaTeX not installed, skipping PDF generation" -ForegroundColor Yellow
}

# Display generated files
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Generated Files:" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

if (Test-Path "output/llm-history-chronicle.*") {
    Get-ChildItem output/llm-history-chronicle.* | Format-Table Name, @{Label="Size"; Expression={"{0:N1} KB" -f ($_.Length / 1KB)}}
}

Write-Host ""
Write-Host "[SUCCESS] Format conversion completed!" -ForegroundColor Green
Write-Host "[INFO] Cover image: $coverImage" -ForegroundColor Green
Write-Host ""
Write-Host "To use a different cover, edit manuscript/00-frontmatter/cover.md" -ForegroundColor Cyan
Write-Host "Available covers:" -ForegroundColor Cyan
Write-Host "  cover-1-minimal.svg   - Simple and elegant" -ForegroundColor White
Write-Host "  cover-2-geometric.svg - Geometric neural network" -ForegroundColor White
Write-Host "  cover-3-tech.svg      - Tech and AI chip" -ForegroundColor White
Write-Host "  cover-4-brain.svg     - Brain and neurons" -ForegroundColor White
Write-Host "  cover-5-complex.svg   - Multi-layer network (default)" -ForegroundColor White
Write-Host ""
Write-Host "View covers: start cover-preview.html" -ForegroundColor Cyan
