path_to_folders="./repos"

# Loop through each subfolder
for folder in "$path_to_folders"/*/; do
  if [ -d "$folder/.git" ]; then
    echo "Pulling latest changes in $folder"
    cd "$folder"
    git pull
    cd - > /dev/null
  else
    echo "$folder is not a git repository"
  fi
done