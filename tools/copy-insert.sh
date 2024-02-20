#!/bin/bash                                                                                                      

# Source directory
source_dir="/path/to/source/directory"

# Destination directory
destination_dir="/path/to/destination/directory"

# Insert line
line_to_insert="Your line to insert"

echo 
echo "#### "$(basename "$0")" ####"
echo
echo $(date)



# Copy all files from source directory to destination directory
cp -r "$source_dir"/* "$destination_dir"

# Change to the destination directory
cd "$destination_dir" || exit

# Another script 

# Loop through each file in the destination directory and insert the line
for file in *; do
  # Check if the item is a file
  if [ -f "$file" ]; then
    # change to sed because insert line no add
    echo "$line_to_insert" >> "$file"
  fi
done

