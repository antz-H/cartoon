"""Remove Jimeng (即梦AI) corner mark: clone pixels left of logo + soft vertical seam."""
import cv2
import numpy as np

SRC = r"c:\home\workspace\cartoon\02 相交.png"
OUT = r"c:\home\workspace\cartoon\02 相交_no_watermark.png"


def _imread_unicode(path: str):
    data = np.fromfile(path, dtype=np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def _imwrite_unicode(path: str, img, params=None) -> None:
    ok, buf = cv2.imencode(path[path.rfind(".") :], img, params or [])
    if not ok:
        raise SystemExit(f"failed to encode: {path}")
    buf.tofile(path)


def main() -> None:
    img = _imread_unicode(SRC)
    if img is None:
        raise SystemExit(f"failed to read: {SRC}")
    h, w = img.shape[:2]

    # Logo bbox was tuned for ~1024px exports; scale for 2K/4K and add margin for glow/halo.
    ref = 1024.0
    mw = int(round(278 * w / ref * 1.12)) + 20
    mh = int(round(86 * h / ref * 1.12)) + 12
    mw = min(mw, w // 2 - 2)
    mh = min(mh, h // 4)
    y0, x0 = h - mh, w - mw
    if x0 - mw < 1:
        raise SystemExit("image too narrow")

    patch = img[y0:h, x0 - mw : x0].astype(np.float32)
    edge = img[y0:h, x0 - 1 : x0].astype(np.float32)
    feather = min(max(32, mw // 10), mw)

    new_block = patch.copy()
    for k in range(feather):
        t = k / max(feather - 1, 1)
        new_block[:, k, :] = (1.0 - t) * edge[:, 0, :] + t * new_block[:, k, :]

    out = img.astype(np.float32)
    out[y0:h, x0:w] = new_block
    res = np.clip(out, 0, 255).astype(np.uint8)

    # Light bilateral only (no inpaint — inpaint smears the corner on painterly backgrounds).
    sub = res[y0:h, x0:w]
    if sub.shape[0] > 5 and sub.shape[1] > 5:
        sm = cv2.bilateralFilter(sub, d=5, sigmaColor=28, sigmaSpace=7)
        res[y0:h, x0:w] = cv2.addWeighted(sub, 0.72, sm, 0.28, 0)

    _imwrite_unicode(OUT, res, [int(cv2.IMWRITE_PNG_COMPRESSION), 3])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
