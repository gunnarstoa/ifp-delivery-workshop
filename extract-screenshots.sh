#!/bin/bash

# IFP Workshop v2.1 Screenshot Extraction Script
# Extracts frames from v2.1 recordings and optimizes for web
# Usage: ./extract-screenshots.sh <path-to-mp4>

set -e

if [ $# -lt 1 ]; then
    echo "Usage: $0 <path-to-mp4> [output-dir]"
    echo ""
    echo "Extracts screenshots from v2.1 live recording at predefined timestamps"
    echo "and optimizes for web display."
    echo ""
    echo "Example: $0 ~/ifp-v2.1-recording.mp4 img/v2.1-screenshots/"
    exit 1
fi

VIDEO_FILE="$1"
OUTPUT_DIR="${2:-img/v2.1-screenshots}"

# Verify ffmpeg is available
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg not found. Install with: brew install ffmpeg"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "📹 IFP Workshop Screenshot Extraction"
echo "==========================================="
echo "Source: $VIDEO_FILE"
echo "Output: $OUTPUT_DIR"
echo ""

# Define extraction timestamps and target pages
# Format: HH:MM:SS | filename | page_destination | description
declare -a TIMESTAMPS=(
    "00:05:30|app-framework-overview.jpg|docs/03-ifp-overview.html|App Framework configurator overview with 44 questions"
    "00:12:45|hierarchy-list.jpg|docs/03-ifp-overview.html|IFP hierarchy lists showing Location, Customer, Job"
    "00:18:20|system-modules.jpg|docs/03-ifp-overview.html|SYS modules list after v2.1 generation"
    "00:25:10|configurator-walkthrough.jpg|docs/05-configurator-walkthrough.html|Configurator showing Location dimension"
)

count=0
for entry in "${TIMESTAMPS[@]}"; do
    IFS='|' read -r timestamp filename page description <<< "$entry"
    
    echo "🎬 Extracting: $filename"
    echo "   Timestamp: $timestamp"
    echo "   Description: $description"
    
    # Extract single frame at timestamp
    ffmpeg -i "$VIDEO_FILE" \
        -ss "$timestamp" \
        -vframes 1 \
        -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
        -q:v 2 \
        "$OUTPUT_DIR/$filename" 2>/dev/null
    
    if [ -f "$OUTPUT_DIR/$filename" ]; then
        filesize=$(du -h "$OUTPUT_DIR/$filename" | cut -f1)
        echo "   ✅ Saved ($filesize)"
    else
        echo "   ❌ Failed to extract"
    fi
    
    ((count++))
    echo ""
done

echo "==========================================="
echo "✅ Extraction complete: $count screenshots"
echo ""
echo "Next steps:"
echo "1. Review extracted images in $OUTPUT_DIR"
echo "2. Test image quality and content"
echo "3. Wire into HTML pages using the page destinations listed above"
echo "4. Update figure captions with v2.1 reference"
echo ""
echo "Quick verification:"
ls -lh "$OUTPUT_DIR"/*.jpg 2>/dev/null || echo "(No screenshots found)"
