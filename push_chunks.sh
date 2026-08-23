#!/bin/bash
folders=(frontend/public/final-products/*)
chunk_size=10
for ((i=0; i < ${#folders[@]}; i+=chunk_size)); do
  chunk=("${folders[@]:i:chunk_size}")
  echo "Adding chunk $i..."
  git add "${chunk[@]}"
  git commit -m "feat: add image chunk $i"
  git push origin main
done
