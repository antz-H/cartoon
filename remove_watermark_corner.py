"""Remove Jimeng (即梦AI) bottom-right mark.

- **Flat bottom band** (绘本大留白底): median color from left strip + masked seam, no bilateral (avoids speckles).
- **Textured corner** (草地等): clone from the left + optional light bilateral.
"""
import sys

import cv2
import numpy as np

SRC = r"c:\home\workspace\cartoon\02 相交.png"
OUT = r"c:\home\workspace\cartoon\02 相交_no_watermark.png"

# If max channel std of watermark ROI and of ref strip are below these, use solid fill.
# 略低于草地+水印混合区的方差（~14），高于大留白底+水印（~11）。
WM_STD_MAX_SOLID = 12.5
REF_STD_MAX_SOLID = 10.0
# Solid-mode feather: only pixels very close to paper color (avoid eating text anti-alias).
FEATHER_COLOR_DIST = 28.0


def _imread_unicode(path: str):
    data = np.fromfile(path, dtype=np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def _imwrite_unicode(path: str, img, params=None) -> None:
    ok, buf = cv2.imencode(path[path.rfind(".") :], img, params or [])
    if not ok:
        raise SystemExit(f"failed to encode: {path}")
    buf.tofile(path)


def _bbox(h: int, w: int) -> tuple[int, int, int, int]:
    ref = 1024.0
    mw = int(round(278 * w / ref * 1.12)) + 24
    mh = int(round(86 * h / ref * 1.12)) + 16
    mw = min(mw, w // 2 - 2)
    mh = min(mh, h // 4)
    y0, x0 = h - mh, w - mw
    return y0, x0, mw, mh


def _mw_logo_strip(w: int) -> int:
    """仅盖住即梦角标+光晕的窄条宽度（略宽于标体，吃掉白边/残影）。"""
    ref = 1024.0
    m = int(round(285 * w / ref * 1.1)) + 28
    # 上限约 1/4 宽：2048 时约 512px，一般仍碰不到居中台词最右端
    return max(112, min(m, w // 4))


def _remove_flat(img: np.ndarray, y0: int, w: int) -> np.ndarray:
    """只替换底条内右下角窄条 [w-mw_logo : w]（不向上越过 y0，避免涂到主画面）。"""
    h = img.shape[0]
    mw_logo = _mw_logo_strip(w)
    x_fill = w - mw_logo
    y_fill = y0
    strip_w = min(max(w // 10, 48), max(1, x_fill - 1))
    ref_strip = img[y0:h, 0:strip_w]
    color = np.median(ref_strip.reshape(-1, 3), axis=0).astype(np.float32)

    out = img.astype(np.float32)
    out[y_fill:h, x_fill:w] = color

    feather = min(26, max(10, mw_logo // 18))
    for k in range(feather):
        xi = x_fill - feather + k
        if xi < 0:
            continue
        t = (k + 1) / feather
        col = img[y_fill:h, xi].astype(np.float32)
        blended = (1.0 - t) * col + t * color
        dist = np.linalg.norm(col - color, axis=1)
        mask = dist < FEATHER_COLOR_DIST
        out[y_fill:h, xi] = np.where(mask[:, None], blended, col)

    res = np.clip(out, 0, 255).astype(np.uint8)
    # 去掉纯色条里偶发的深色噪点（不影响条外文字）
    sub = res[y_fill:h, x_fill:w]
    if sub.shape[0] >= 3 and sub.shape[1] >= 3:
        res[y_fill:h, x_fill:w] = cv2.medianBlur(sub, 3)

    return res


def _remove_clone(img: np.ndarray, y0: int, x0: int, mw: int, w: int) -> np.ndarray:
    """Original clone-from-left + light bilateral for textured backgrounds."""
    h = img.shape[0]
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

    sub = res[y0:h, x0:w]
    if sub.shape[0] > 5 and sub.shape[1] > 5:
        sm = cv2.bilateralFilter(sub, d=5, sigmaColor=28, sigmaSpace=7)
        res[y0:h, x0:w] = cv2.addWeighted(sub, 0.72, sm, 0.28, 0)

    return res


def remove_watermark(img: np.ndarray) -> np.ndarray:
    h, w = img.shape[:2]
    y0, x0, mw, mh = _bbox(h, w)

    wm_roi = img[y0:h, x0:w]
    std_wm = wm_roi.reshape(-1, 3).std(axis=0)

    strip_w = min(max(w // 10, 48), max(1, x0 - 1))
    ref_strip = img[y0:h, 0:strip_w]
    std_ref = ref_strip.reshape(-1, 3).std(axis=0)

    use_solid = np.all(std_wm < WM_STD_MAX_SOLID) and np.all(std_ref < REF_STD_MAX_SOLID)

    if use_solid:
        return _remove_flat(img, y0, w)
    return _remove_clone(img, y0, x0, mw, w)


def main() -> None:
    src, out = SRC, OUT
    if len(sys.argv) >= 2:
        src = sys.argv[1]
    if len(sys.argv) >= 3:
        out = sys.argv[2]

    img = _imread_unicode(src)
    if img is None:
        raise SystemExit(f"failed to read: {src}")

    res = remove_watermark(img)
    _imwrite_unicode(out, res, [int(cv2.IMWRITE_PNG_COMPRESSION), 3])
    print("wrote", out)


if __name__ == "__main__":
    main()
