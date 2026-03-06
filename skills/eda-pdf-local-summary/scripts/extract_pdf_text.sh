#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <pdf_path> [out_dir]" >&2
  exit 1
fi

pdf_path="$1"
out_dir="${2:-docs/papers/summaries/raw}"

if [[ ! -f "$pdf_path" ]]; then
  echo "ERROR: pdf not found: $pdf_path" >&2
  exit 2
fi

mkdir -p "$out_dir"
base_name="$(basename "${pdf_path%.*}")"
txt_path="$out_dir/${base_name}.txt"
headings_path="$out_dir/${base_name}.headings.txt"
tei_path="$out_dir/${base_name}.tei.xml"

if [[ "${DISABLE_GROBID:-0}" != "1" ]] && command -v python3.11 >/dev/null 2>&1 && python3.11 - <<'PY' >/dev/null 2>&1
import importlib.util, sys
ok = importlib.util.find_spec("grobid_client") and importlib.util.find_spec("lxml")
sys.exit(0 if ok else 1)
PY
then
  grobid_server="${GROBID_SERVER:-https://kermitt2-grobid.hf.space}"
  tmp_in="$(mktemp -d)"
  tmp_out="$(mktemp -d)"
  cp "$pdf_path" "$tmp_in/"
  if python3.11 -m grobid_client.grobid_client \
    --server "$grobid_server" \
    --input "$tmp_in" \
    --output "$tmp_out" \
    --n 1 \
    --force \
    processFulltextDocument >/dev/null 2>&1
  then
    src_tei="$tmp_out/${base_name}.grobid.tei.xml"
  else
    src_tei=""
  fi
  if [[ -n "$src_tei" && -f "$src_tei" ]]; then
    cp "$src_tei" "$tei_path"
    python3.11 - "$tei_path" "$txt_path" <<'PY'
import sys
from lxml import etree

tei_path = sys.argv[1]
txt_path = sys.argv[2]
ns = {"tei": "http://www.tei-c.org/ns/1.0"}

tree = etree.parse(tei_path)
lines = []

title = tree.xpath("string(//tei:titleStmt/tei:title[@type='main'][1])", namespaces=ns).strip()
if title:
    lines.append(title)
    lines.append("")

abstract_nodes = tree.xpath("//tei:profileDesc/tei:abstract//tei:p", namespaces=ns)
if abstract_nodes:
    lines.append("Abstract")
    for p in abstract_nodes:
        t = " ".join(p.xpath("string()").split())
        if t:
            lines.append(t)
    lines.append("")

for div in tree.xpath("//tei:text/tei:body/tei:div", namespaces=ns):
    head = " ".join(div.xpath("string(tei:head)", namespaces=ns).split())
    if head:
        lines.append(head)
    for p in div.xpath(".//tei:p", namespaces=ns):
        t = " ".join(p.xpath("string()").split())
        if t:
            lines.append(t)
    lines.append("")

refs = tree.xpath("//tei:listBibl/tei:biblStruct", namespaces=ns)
if refs:
    lines.append("References")
    for ref in refs:
        t = " ".join(" ".join(ref.xpath(".//text()")).split())
        if t:
            lines.append(t)

with open(txt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines).strip() + "\n")
PY
    # Guard against empty/near-empty TEI parsing (common on some protected IEEE PDFs).
    if [[ ! -s "$txt_path" || "$(wc -c < "$txt_path")" -lt 500 ]]; then
      echo "WARN: GROBID output is too sparse for $base_name, falling back to local extractor." >&2
      rm -f "$txt_path"
    fi
  else
    echo "WARN: GROBID unavailable/failed at ${grobid_server}, falling back to local extractor." >&2
  fi
  rm -rf "$tmp_in" "$tmp_out"
fi

if [[ -f "$txt_path" ]]; then
  :
elif command -v pdftotext >/dev/null 2>&1; then
  pdftotext -layout "$pdf_path" "$txt_path"
elif command -v mutool >/dev/null 2>&1; then
  mutool draw -F txt -o "$txt_path" "$pdf_path"
elif command -v python3.11 >/dev/null 2>&1 && python3.11 - <<'PY' >/dev/null 2>&1
import importlib.util, sys
sys.exit(0 if importlib.util.find_spec("pypdf") else 1)
PY
then
  python3.11 - "$pdf_path" "$txt_path" <<'PY'
import sys
from pathlib import Path
from pypdf import PdfReader

pdf_path = Path(sys.argv[1])
txt_path = Path(sys.argv[2])
reader = PdfReader(str(pdf_path))

with txt_path.open("w", encoding="utf-8") as out:
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        out.write(f"\n\n===== PAGE {i} =====\n")
        out.write(text)
PY
else
  echo "ERROR: no extractor available (need grobid/pdftotext/mutool or python3.11+pypdf)." >&2
  exit 3
fi

rg -n "^(Abstract|Introduction|Related Work|Method|Methods|Experiment|Experiments|Results|Conclusion|References)\\b" "$txt_path" > "$headings_path" || true

echo "text=$txt_path"
echo "headings=$headings_path"
if [[ -f "$tei_path" ]]; then
  echo "tei=$tei_path"
fi
