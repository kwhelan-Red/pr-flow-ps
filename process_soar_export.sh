#!/bin/bash
# Script to process the full SOAR export CSV

echo "Looking for SOAR CSV export files in Downloads..."
echo ""

# Find the most recent CSV file that looks like a Jira export
LATEST_CSV=$(ls -t /Users/kwhelan/Downloads/*"Red Hat Issue Tracker"*.csv 2>/dev/null | head -1)

if [ -z "$LATEST_CSV" ]; then
    echo "❌ No Jira export CSV found in Downloads"
    echo ""
    echo "Please:"
    echo "1. Go to https://issues.redhat.com/projects/SOAR/issues"
    echo "2. Remove all filters (show ALL issues, not just open)"
    echo "3. Click Export → CSV (all fields)"
    echo "4. Save to Downloads folder"
    echo "5. Run this script again"
    exit 1
fi

echo "Found: $LATEST_CSV"
echo ""

# Check how many issues it has
ISSUE_COUNT=$(tail -n +2 "$LATEST_CSV" | wc -l | xargs)
echo "Issues in CSV: $ISSUE_COUNT"
echo ""

if [ "$ISSUE_COUNT" -lt 1000 ]; then
    echo "⚠️  Warning: This CSV only has $ISSUE_COUNT issues."
    echo "   For all STIs, you need to export ALL issues (should be ~3,545)"
    echo "   Make sure you removed status filters in Jira!"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Processing CSV to extract all STIs..."
echo ""

python3 extract_stis_from_csv.py "$LATEST_CSV" --output "SOAR_ALL_STIs_and_CMDB_IDs.xlsx"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Done! Check SOAR_ALL_STIs_and_CMDB_IDs.xlsx"
else
    echo ""
    echo "❌ Error processing CSV"
    exit 1
fi




