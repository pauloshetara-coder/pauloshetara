#!/bin/bash
# Converte as mídias baixadas para o projeto HyperFrames (JPG 1920px, MP4 H.264 sem áudio)
set -e
cd "$(dirname "$0")"
HF=../elesbao-hf/assets
mkdir -p $HF/img $HF/vid
for f in assets/img/*.{jpg,jpeg,png,JPG}; do
  [ -s "$f" ] || continue
  n=$(basename "${f%.*}")
  python3 -I -c "
from PIL import Image; import sys
im=Image.open(sys.argv[1]).convert('RGB'); w,h=im.size
s=min(1.0, 2200/max(w,h)) if max(w,h)>2200 else 1.0
if s<1: im=im.resize((int(w*s),int(h*s)), Image.LANCZOS)
im.save(sys.argv[2], quality=90)" "$f" "$HF/img/$n.jpg"
done
for f in assets/vid/*; do
  [ -s "$f" ] || continue
  case "$f" in *.txt) continue;; esac
  n=$(basename "${f%.*}")
  ffmpeg -v error -y -ss 4 -i "$f" -t 24 -an -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30" -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart "$HF/vid/$n.mp4"
done
ls -la $HF/img $HF/vid
