#!/bin/bash

echo "Starting Docker Compose validation..."
echo "----------------------------------------"

# Find all docker-compose.yml files
files=$(find . -name "docker-compose.yml")
total=0
passed=0
failed=0

for file in $files; do
    total=$((total+1))
    echo "Checking $file..."
    
    # Run docker-compose config in quiet mode to validate syntax
    # Redirect stderr to stdout to capture error messages if any
    output=$(docker-compose -f "$file" config -q 2>&1)
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "✅ Valid: $file"
        passed=$((passed+1))
    else
        echo "❌ Invalid: $file"
        echo "   Error: $output"
        failed=$((failed+1))
    fi
    echo "----------------------------------------"
done

echo "Validation Complete!"
echo "Total Files: $total"
echo "Passed: $passed"
echo "Failed: $failed"

if [ $failed -gt 0 ]; then
    exit 1
else
    exit 0
fi
