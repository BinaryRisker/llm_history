# Quick Start Guide - Format Conversion

## Problem Fixed!

The PowerShell script had encoding issues with Chinese characters.
**Fixed version** is now available: `scripts/build-all.ps1`

---

## How to Use

### Option 1: Run the Build Script (Recommended)

```powershell
# In PowerShell, navigate to project directory
cd D:\code\github\llm_history

# Run the build script
.\scripts\build-all.ps1
```

**What it does**:
- Generates HTML format (always works)
- Generates ePub format (always works)
- Generates PDF format (only if XeLaTeX is installed)

---

### Option 2: Generate Specific Format

#### Generate HTML only:
```powershell
pandoc `
  manuscript/00-frontmatter/preface.md `
  manuscript/00-frontmatter/reading-guide.md `
  manuscript/00-frontmatter/acknowledgments.md `
  manuscript/01-foundation/transformer-revolution.md `
  manuscript/01-foundation/early-applications.md `
  manuscript/02-gpt-era/scaling-up.md `
  manuscript/02-gpt-era/google-response.md `
  manuscript/03-alignment/rlhf-chatgpt.md `
  manuscript/04-chatgpt-revolution/chatgpt-launch.md `
  manuscript/05-global-race-2023/ai-race-2023.md `
  manuscript/05-global-race-2023/meta-llama.md `
  manuscript/06-chinese-ai/chinese-development.md `
  manuscript/07-multimodal-era/2024-breakthroughs.md `
  manuscript/08-present/2025-present.md `
  manuscript/99-backmatter/glossary.md `
  manuscript/99-backmatter/references.md `
  manuscript/99-backmatter/index.md `
  -o output/llm-history-chronicle.html `
  --standalone `
  --toc `
  --toc-depth=2 `
  --number-sections `
  --css=config/html-style.css `
  --metadata title="LLM History Chronicle"
```

#### Generate ePub only:
```powershell
pandoc `
  manuscript/00-frontmatter/preface.md `
  manuscript/00-frontmatter/reading-guide.md `
  manuscript/00-frontmatter/acknowledgments.md `
  manuscript/01-foundation/transformer-revolution.md `
  manuscript/01-foundation/early-applications.md `
  manuscript/02-gpt-era/scaling-up.md `
  manuscript/02-gpt-era/google-response.md `
  manuscript/03-alignment/rlhf-chatgpt.md `
  manuscript/04-chatgpt-revolution/chatgpt-launch.md `
  manuscript/05-global-race-2023/ai-race-2023.md `
  manuscript/05-global-race-2023/meta-llama.md `
  manuscript/06-chinese-ai/chinese-development.md `
  manuscript/07-multimodal-era/2024-breakthroughs.md `
  manuscript/08-present/2025-present.md `
  manuscript/99-backmatter/glossary.md `
  manuscript/99-backmatter/references.md `
  manuscript/99-backmatter/index.md `
  -o output/llm-history-chronicle.epub `
  --metadata-file=config/epub-metadata.yaml `
  --toc `
  --toc-depth=2 `
  --css=config/epub-style.css
```

---

## Troubleshooting

### Error: "Execution Policy Restriction"

If you see:
```
.\scripts\build-all.ps1 : cannot be loaded because running scripts is disabled
```

**Solution**:
```powershell
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try running the script again.

---

### Error: "Pandoc not found"

**Solution**: Install Pandoc from https://pandoc.org/installing.html

---

### Error: "XeLaTeX not found" (for PDF)

This is normal if you haven't installed LaTeX yet.

**Solution**:
- For PDF generation, install MiKTeX: https://miktex.org/download
- Or use browser to print HTML to PDF (immediate solution)

---

## Expected Output

After running successfully, you should see:

```
[OK] HTML generated: output/llm-history-chronicle.html (666 KB)
[OK] ePub generated: output/llm-history-chronicle.epub (255 KB)
[WARN] XeLaTeX not installed, skipping PDF generation
```

---

## Files Generated

Check the `output/` folder:
- `llm-history-chronicle.html` - Web version
- `llm-history-chronicle.epub` - E-reader version
- `llm-history-chronicle.pdf` - Print version (if XeLaTeX installed)

---

## Next Steps

1. **View HTML**:
   ```powershell
   start output\llm-history-chronicle.html
   ```

2. **Read ePub**:
   - Open with Calibre, Apple Books, or any ePub reader

3. **Generate PDF** (optional):
   - Install MiKTeX from https://miktok.org/download
   - Re-run `.\scripts\build-all.ps1`

---

## Need Help?

If you encounter any issues:
1. Make sure you're in the correct directory: `D:\code\github\llm_history`
2. Check that Pandoc is installed: `pandoc --version`
3. Run PowerShell as Administrator if you have permission issues
