#!/bin/bash

# Prompt for input
read -p "Enter a decimal number (<= 100000): " decimal

# Check if input is valid
if ! [[ "$decimal" =~ ^[0-9]+$ ]]; then
    echo "Error: Input is not a valid number."
    exit 1
fi

if (( decimal > 100000 )); then
    echo "Error: Number exceeds the limit of 100000."
    exit 1
fi

# Convert to hexadecimal and binary
hexadecimal=$(echo "obase=16; $decimal" | bc)
binary=$(echo "obase=2; $decimal" | bc)

# Output results
echo "Decimal: $decimal" > conversion_result.txt
echo "Hexadecimal: $hexadecimal" >> conversion_result.txt
echo "Binary: $binary" >> conversion_result.txt

# Display results
cat conversion_result.txt
