import argparse
from pathlib import Path

import cv2
import numpy as np


def parse_region(region_text: str) -> tuple[int, int, int, int]:
    parts = [p.strip() for p in region_text.split(",")]
    if len(parts) != 4:
        raise ValueError("region must be x,y,w,h")
    x, y, w, h = [int(p) for p in parts]
    if w <= 0 or h <= 0:
        raise ValueError("region width and height must be positive")
    return x, y, w, h


def imread_unicode(path: Path):
    data = np.fromfile(str(path), dtype=np.uint8)
    if data.size == 0:
        return None
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def imwrite_unicode(path: Path, img) -> None:
    suffix = path.suffix.lower() or ".png"
    ok, buf = cv2.imencode(suffix, img)
    if not ok:
        raise RuntimeError(f"failed to encode output: {path}")
    buf.tofile(str(path))


def clamp_region(x: int, y: int, w: int, h: int, image_width: int, image_height: int) -> tuple[int, int, int, int]:
    x = max(0, min(x, image_width - 1))
    y = max(0, min(y, image_height - 1))
    w = max(1, min(w, image_width - x))
    h = max(1, min(h, image_height - y))
    return x, y, w, h


def remove_watermark(image: np.ndarray, region: tuple[int, int, int, int], radius: int) -> np.ndarray:
    height, width = image.shape[:2]
    x, y, w, h = clamp_region(*region, width, height)

    mask = np.zeros((height, width), dtype=np.uint8)
    mask[y : y + h, x : x + w] = 255

    # TELEA is fast and works well for small logos and corner watermarks.
    return cv2.inpaint(image, mask, radius, cv2.INPAINT_TELEA)


def output_path_for(source: Path, explicit_output: str | None, suffix: str) -> Path:
    if explicit_output:
        return Path(explicit_output)
    return source.with_name(f"{source.stem}{suffix}{source.suffix}")


def process_file(source: Path, region: tuple[int, int, int, int], radius: int, explicit_output: str | None, suffix: str) -> Path:
    image = imread_unicode(source)
    if image is None:
        raise RuntimeError(f"failed to read image: {source}")

    cleaned = remove_watermark(image, region, radius)
    out_path = output_path_for(source, explicit_output, suffix)
    imwrite_unicode(out_path, cleaned)
    return out_path


def iter_files(input_dir: Path, glob_pattern: str):
    for path in sorted(input_dir.glob(glob_pattern)):
        if path.is_file():
            yield path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Remove a watermark from an image or batch of images.")
    parser.add_argument("--input", help="Single input image path")
    parser.add_argument("--input-dir", help="Directory containing images for batch mode")
    parser.add_argument("--glob", default="*.png", help="Glob for batch mode, default: *.png")
    parser.add_argument("--region", required=True, help="Watermark region as x,y,w,h")
    parser.add_argument("--output", help="Explicit output path for single-image mode")
    parser.add_argument("--suffix", default="_clean", help="Output suffix when output is not specified")
    parser.add_argument("--radius", type=int, default=3, help="OpenCV inpaint radius")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.input and not args.input_dir:
        raise SystemExit("provide --input or --input-dir")
    if args.input and args.input_dir:
        raise SystemExit("use either --input or --input-dir, not both")

    region = parse_region(args.region)

    if args.input:
        source = Path(args.input)
        out_path = process_file(source, region, args.radius, args.output, args.suffix)
        print(out_path)
        return

    input_dir = Path(args.input_dir)
    outputs = []
    for source in iter_files(input_dir, args.glob):
        outputs.append(process_file(source, region, args.radius, None, args.suffix))

    for out_path in outputs:
        print(out_path)


if __name__ == "__main__":
    main()
