#!/usr/bin/env bash
# Gộp các file trong noi_dung_chi_tiet/ thành 1 file Word. Cần pandoc: brew install pandoc
set -euo pipefail
cd "$(dirname "$0")"

OUT="TranNhatHung_MAT6206_BaoCaoCuoiKy.docx"
TMP="$(mktemp -d)"
PAGEBREAK=$'\n\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'

MERGED="$TMP/merged.md"
: > "$MERGED"
for f in noi_dung_chi_tiet/[0-9][0-9]_*.md; do
  cat "$f" >> "$MERGED"
  printf '%s' "$PAGEBREAK" >> "$MERGED"
done

# Đặt reference.docx (font Times New Roman 13, lề...) cạnh script nếu muốn định dạng theo mẫu
REF=()
[[ -f reference.docx ]] && REF=(--reference-doc=reference.docx)

pandoc "$MERGED" -f markdown -t docx --toc --toc-depth=3 -M toc-title="MỤC LỤC" \
  --resource-path=noi_dung_chi_tiet "${REF[@]}" -o "$OUT"

rm -rf "$TMP"
echo "Đã tạo $OUT"
