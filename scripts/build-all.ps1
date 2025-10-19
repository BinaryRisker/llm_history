# Build All Formats - PowerShell Script
# Fixed version with proper encoding

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "LLM History Chronicle - Format Conversion" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Default cover image (you can change this to any cover 1-5)
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

# Chapter files in correct chronological order
$mdFiles = @(
    # Front matter
    "manuscript/00-frontmatter/preface.md",
    "manuscript/00-frontmatter/reading-guide.md",
    "manuscript/00-frontmatter/acknowledgments.md",

    # Chapter 1: Transformer Revolution (2017)
    "manuscript/01-foundation/transformer-revolution.md",

    # Chapter 2: Pre-training Paradigm (2018)
    "manuscript/01-foundation/early-applications.md",

    # Chapter 3: Scaling Up (2019-2020)
    "manuscript/02-gpt-era/scaling-up.md",

    # Chapter 4: Google's Response (2019-2022)
    "manuscript/02-gpt-era/google-response.md",

    # Chapter 5: RLHF and ChatGPT (2021-2022)
    "manuscript/03-alignment/rlhf-chatgpt.md",

    # Chapter 6: ChatGPT Launch (2022-11)
    "manuscript/04-chatgpt-revolution/chatgpt-launch.md",

    # Chapter 7: 2023 AI Race
    "manuscript/05-global-race-2023/ai-race-2023.md",

    # Chapter 8: Meta's Open Source Strategy
    "manuscript/05-global-race-2023/meta-llama.md",

    # Chapter 9: Chinese AI Development
    "manuscript/06-chinese-ai/chinese-development.md",

    # Chapter 10: Multimodal Era (2024)
    "manuscript/07-multimodal-era/2024-breakthroughs.md",

    # Chapter 11: 2025 Present
    "manuscript/08-present/2025-present.md",

    # Back matter
    "manuscript/99-backmatter/glossary.md",
    "manuscript/99-backmatter/references.md",
    "manuscript/99-backmatter/index.md"
)

Write-Host "Total chapters: $($mdFiles.Count)" -ForegroundColor Cyan
Write-Host ""

# 1. Generate HTML
Write-Host "[1/3] Generating HTML..." -ForegroundColor Yellow
try {
    # Create cover page HTML
    $coverHtml = @"
<div style="text-align: center; page-break-after: always;">
    <img src="$coverImage" alt="Book Cover" style="max-width: 100%; height: auto;">
</div>
"@
    $coverHtml | Out-File -FilePath "temp-cover.html" -Encoding UTF8

    $htmlArgs = @(
        "temp-cover.html",
        $mdFiles,
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

    # Clean up temp file
    Remove-Item "temp-cover.html" -ErrorAction SilentlyContinue

    if (Test-Path "output/llm-history-chronicle.html") {
        $htmlSize = (Get-Item "output/llm-history-chronicle.html").Length / 1KB
        Write-Host "[OK] HTML generated with cover: output/llm-history-chronicle.html ($([math]::Round($htmlSize, 1)) KB)" -ForegroundColor Green
    }
} catch {
    Write-Host "[ERROR] HTML generation failed: $_" -ForegroundColor Red
    Remove-Item "temp-cover.html" -ErrorAction SilentlyContinue
}

# 2. Generate ePub
Write-Host ""
Write-Host "[2/3] Generating ePub..." -ForegroundColor Yellow
try {
    $epubArgs = @(
        $mdFiles,
        "-o", "output/llm-history-chronicle.epub",
        "--metadata-file=config/epub-metadata.yaml",
        "--toc",
        "--toc-depth=2",
        "--css=config/epub-style.css"
    )
    & pandoc $epubArgs

    if (Test-Path "output/llm-history-chronicle.epub") {
        $epubSize = (Get-Item "output/llm-history-chronicle.epub").Length / 1KB
        Write-Host "[OK] ePub generated: output/llm-history-chronicle.epub ($([math]::Round($epubSize, 1)) KB)" -ForegroundColor Green
    }
} catch {
    Write-Host "[ERROR] ePub generation failed: $_" -ForegroundColor Red
}

# 3. Generate PDF (if XeLaTeX is available)
Write-Host ""
Write-Host "[3/3] Generating PDF..." -ForegroundColor Yellow

if (Get-Command xelatex -ErrorAction SilentlyContinue) {
    try {
        $pdfArgs = @(
            $mdFiles,
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
            Write-Host "[OK] PDF generated: output/llm-history-chronicle.pdf ($([math]::Round($pdfSize, 1)) KB)" -ForegroundColor Green
        }
    } catch {
        Write-Host "[ERROR] PDF generation failed: $_" -ForegroundColor Red
    }
} else {
    Write-Host "[WARN] XeLaTeX not installed, skipping PDF generation" -ForegroundColor Yellow
    Write-Host "       Install from: https://www.tug.org/texlive/windows.html" -ForegroundColor Cyan
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
Write-Host "[INFO] Chapters ordered chronologically (2017-2025)" -ForegroundColor Green
Write-Host "[INFO] Cover image: $coverImage" -ForegroundColor Green
Write-Host ""
Write-Host "To use a different cover, edit line 10 in this script:" -ForegroundColor Cyan
Write-Host "  cover-1-minimal.svg   - Simple and elegant" -ForegroundColor White
Write-Host "  cover-2-geometric.svg - Geometric neural network" -ForegroundColor White
Write-Host "  cover-3-tech.svg      - Tech and AI chip" -ForegroundColor White
Write-Host "  cover-4-brain.svg     - Brain and neurons" -ForegroundColor White
Write-Host "  cover-5-complex.svg   - Multi-layer network (default)" -ForegroundColor White
Write-Host ""
Write-Host "See cover preview: start cover-preview.html" -ForegroundColor Cyan
Write-Host "See report: output/FORMAT_CONVERSION_REPORT.md" -ForegroundColor Cyan
