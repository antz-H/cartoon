# remove-image-watermark examples

## Single image

```bash
python .cursor/skills/remove-image-watermark/scripts/remove_watermark.py --input "作品/04 旅途.png" --region "1710,980,220,70"
```

Expected output:

```text
作品/04 旅途_clean.png
```

## Batch mode

```bash
python .cursor/skills/remove-image-watermark/scripts/remove_watermark.py --input-dir "作品" --glob "*.png" --region "1710,980,220,70"
```

This creates cleaned sibling files such as:

```text
作品/03 同望日出_clean.png
作品/04 旅途_clean.png
```

## Tight-mask retry

If the first result smears nearby strokes, rerun with a smaller region:

```bash
python .cursor/skills/remove-image-watermark/scripts/remove_watermark.py --input "作品/04 旅途.png" --region "1740,995,180,52"
```
