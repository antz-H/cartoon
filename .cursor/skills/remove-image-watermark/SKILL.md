---
name: remove-image-watermark
description: Removes watermarks or small overlays by masking a user-specified rectangular region; supports single file or batch folder; writes a new `_clean` sibling file without overwriting the source. Use when the user mentions 去水印, 消除水印, remove watermark, logo removal, image cleanup, or batch processing.
---

# Remove Image Watermark

## Purpose

Mask-based cleanup on a tight `x,y,w,h` region; single image or `--input-dir` batch; output is always a new file (default suffix `_clean`).

## Inputs To Gather

Before running the script, confirm or infer:

- source image path, or a directory / list of image paths for batch mode
- target watermark region as `x,y,w,h`
- whether the watermark is small and local enough for inpainting to work cleanly

If the user does not give the region, ask for it.

## Default Workflow

### 1. Confirm scope

Prefer a tight rectangular mask around the watermark instead of a large area.

Use one region per watermark in this format:

```text
x,y,w,h
```

Example:

```text
1710,980,220,70
```

### 2. Run the helper script

For one image:

```bash
python .cursor/skills/remove-image-watermark/scripts/remove_watermark.py --input "path/to/image.png" --region "x,y,w,h"
```

For batch mode on a folder:

```bash
python .cursor/skills/remove-image-watermark/scripts/remove_watermark.py --input-dir "path/to/folder" --glob "*.png" --region "x,y,w,h"
```

By default the script writes a sibling file with `_clean` appended before the extension.

### 3. Verify result

After processing:

- confirm the cleaned file path
- remind the user that inpainting works best for small, local marks
- if the result is imperfect, retry with a tighter mask rather than a larger one

## Output Rules

- never overwrite the original file unless the user explicitly asks
- prefer `_clean` as the output suffix
- for batch mode, process each matching file into a new sibling file
- report the created output path or paths back to the user

## Limitations

- best for small watermarks, logos, or corner overlays
- not ideal for large removals across detailed faces or complex foreground subjects
- if a large region crosses important subject detail, warn the user that manual retouching may still be needed

## Notes For Region Selection

- keep the box as small as possible
- include the full watermark glow or shadow if present
- avoid covering nearby character outlines or text you want to keep

## Additional Resources

- For concrete commands and examples, see [examples.md](examples.md)
