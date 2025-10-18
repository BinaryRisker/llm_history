#!/bin/bash
# Manuscript Directory Structure Fix Script (Bash version)
# Purpose: Fix duplicate directory numbering and reorganize by timeline
# Generated: 2025-10-18

set -e  # Exit on error

echo "=== Manuscript Directory Structure Fix Script ==="
echo ""

BASE_DIR="manuscript"
BACKUP_BRANCH="backup-manuscript-structure-$(date +%Y%m%d-%H%M%S)"

# Function to show current structure
show_structure() {
    echo ""
    echo "Current manuscript structure:"
    for dir in "$BASE_DIR"/*/; do
        dirname=$(basename "$dir")
        filecount=$(find "$dir" -type f | wc -l)
        echo "  $dirname ($filecount files)"
    done
}

echo "This script will reorganize the manuscript directory structure."
echo "It will fix duplicate directory numbering and align with timeline order."
echo ""
echo "IMPORTANT: This will:"
echo "  1. Create a git backup branch"
echo "  2. Delete empty directories"
echo "  3. Rename and reorganize directories"
echo "  4. Move files between directories"
echo "  5. Update chapter numbers in frontmatter"
echo ""

read -p "Do you want to proceed? (yes/no): " proceed
if [ "$proceed" != "yes" ]; then
    echo "Aborted by user."
    exit 0
fi

show_structure

# Step 0: Git backup
echo ""
echo ">>> Creating git backup branch '$BACKUP_BRANCH'"
git checkout -b "$BACKUP_BRANCH"
git add .
git commit -m "Backup before manuscript structure reorganization" || true
echo "✓ Backup created"

# Step 1: Delete empty directory
echo ""
echo ">>> Delete empty directory: 03-parallel-developments"
if [ -d "$BASE_DIR/03-parallel-developments" ]; then
    if [ -z "$(ls -A $BASE_DIR/03-parallel-developments)" ]; then
        rm -rf "$BASE_DIR/03-parallel-developments"
        echo "  Deleted: 03-parallel-developments"
    else
        echo "  Warning: Directory not empty, skipping"
    fi
fi
echo "✓ Completed"

# Step 2: Rename directories
echo ""
echo ">>> Rename directories to new structure"

# Create temporary directory for staging
mkdir -p "$BASE_DIR/.tmp_rename"

# Rename in specific order to avoid conflicts
if [ -d "$BASE_DIR/03-alignment-breakthrough" ]; then
    mv "$BASE_DIR/03-alignment-breakthrough" "$BASE_DIR/03-alignment"
    echo "  Renamed: 03-alignment-breakthrough → 03-alignment"
fi

if [ -d "$BASE_DIR/04-chatgpt-mainstream" ]; then
    mv "$BASE_DIR/04-chatgpt-mainstream" "$BASE_DIR/04-chatgpt-revolution"
    echo "  Renamed: 04-chatgpt-mainstream → 04-chatgpt-revolution"
fi

if [ -d "$BASE_DIR/04-global-competition" ]; then
    mv "$BASE_DIR/04-global-competition" "$BASE_DIR/05-global-race-2023"
    echo "  Renamed: 04-global-competition → 05-global-race-2023"
fi

if [ -d "$BASE_DIR/05-multimodal-agent" ]; then
    mv "$BASE_DIR/05-multimodal-agent" "$BASE_DIR/07-multimodal-era"
    echo "  Renamed: 05-multimodal-agent → 07-multimodal-era"
fi

if [ -d "$BASE_DIR/06-recent-developments" ]; then
    mv "$BASE_DIR/06-recent-developments" "$BASE_DIR/08-present"
    echo "  Renamed: 06-recent-developments → 08-present"
fi

rmdir "$BASE_DIR/.tmp_rename" 2>/dev/null || true
echo "✓ Completed"

# Step 3: Move meta-llama.md
echo ""
echo ">>> Move meta-llama.md to 05-global-race-2023/"
if [ -f "$BASE_DIR/05-global-competition/meta-llama.md" ]; then
    mv "$BASE_DIR/05-global-competition/meta-llama.md" "$BASE_DIR/05-global-race-2023/meta-llama.md"
    echo "  Moved: meta-llama.md"
fi
echo "✓ Completed"

# Step 4: Delete now-empty 05-global-competition
echo ""
echo ">>> Delete now-empty 05-global-competition directory"
if [ -d "$BASE_DIR/05-global-competition" ]; then
    if [ -z "$(ls -A $BASE_DIR/05-global-competition)" ]; then
        rm -rf "$BASE_DIR/05-global-competition"
        echo "  Deleted: 05-global-competition"
    else
        echo "  Warning: Directory not empty, skipping"
    fi
fi
echo "✓ Completed"

# Step 5: Create missing directories
echo ""
echo ">>> Create missing directory: 06-chinese-ai"
mkdir -p "$BASE_DIR/06-chinese-ai"
echo "  Created: 06-chinese-ai"
echo "✓ Completed"

# Step 6: Update chapter numbers in frontmatter
echo ""
echo ">>> Update chapter numbers in file frontmatter"

update_chapter_number() {
    local file="$1"
    local old_num="$2"
    local new_num="$3"

    if [ -f "$file" ]; then
        if grep -q "chapter_number: $old_num" "$file"; then
            sed -i.bak "s/chapter_number: $old_num/chapter_number: $new_num/" "$file"
            rm -f "$file.bak"
            echo "  Updated: $(basename $file) (Chapter $old_num → $new_num)"
        else
            echo "  Warning: Pattern not found in $(basename $file)"
        fi
    else
        echo "  Warning: File not found: $file"
    fi
}

update_chapter_number "$BASE_DIR/04-chatgpt-revolution/chatgpt-launch.md" 6 5
update_chapter_number "$BASE_DIR/05-global-race-2023/ai-race-2023.md" 5 6
update_chapter_number "$BASE_DIR/07-multimodal-era/2024-breakthroughs.md" 6 10

echo "✓ Completed"

# Show new structure
echo ""
echo "=================================================="
show_structure

echo ""
echo "=== Fix completed! ==="
echo ""
echo "Next steps:"
echo "  1. Review the changes with: git status"
echo "  2. Review the full diff with: git diff"
echo "  3. If satisfied, commit: git add . && git commit -m 'Fix manuscript directory structure'"
echo "  4. If issues found, rollback: git checkout 001-llm-history-chronicle && git branch -D $BACKUP_BRANCH"
echo "  5. Update tasks.md to match new structure"
echo "  6. Create missing chapters (Chapter 7, 9)"
echo ""
