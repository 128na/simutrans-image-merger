from PIL import Image

from src.MergeDefinition import MergeImage


def _makeMergeImage(pathes: list[str]) -> MergeImage:
    return MergeImage(
        {
            "name": "mergeImage",
            "pathes": pathes,
            "mode": "RGBA",
            "offset": {"x": 0, "y": 0},
        }
    )


def _savedImage(path, size: tuple[int, int], color) -> str:
    Image.new("RGBA", size, color).save(path)
    return str(path)


def test_handleImage_wider_but_shorter_addImage_is_not_cropped(tmp_path):
    # canvas: 100x100, addImage: 120x80 (幅は大きいが高さは小さい非対称ケース)
    canvasPath = _savedImage(tmp_path / "canvas.png", (100, 100), (255, 0, 0, 255))
    addPath = _savedImage(tmp_path / "add.png", (120, 80), (0, 255, 0, 255))
    canvas = Image.open(canvasPath)

    result = _makeMergeImage([addPath]).handleImage(canvas)

    # 両画像が完全に収まるサイズまで拡大され、どちらの領域もクロップされない
    assert result.size == (120, 100)
    assert result.getpixel((0, 99)) == (255, 0, 0, 255)  # canvas由来の下端が残っている
    assert result.getpixel((119, 0)) == (
        0,
        255,
        0,
        255,
    )  # addImage由来の右端が残っている


def test_handleImage_taller_but_narrower_addImage_is_not_cropped(tmp_path):
    # canvas: 100x100, addImage: 80x120 (逆方向の非対称ケース)
    canvasPath = _savedImage(tmp_path / "canvas.png", (100, 100), (255, 0, 0, 255))
    addPath = _savedImage(tmp_path / "add.png", (80, 120), (0, 255, 0, 255))
    canvas = Image.open(canvasPath)

    result = _makeMergeImage([addPath]).handleImage(canvas)

    assert result.size == (100, 120)
    assert result.getpixel((99, 0)) == (255, 0, 0, 255)  # canvas由来の右端が残っている
    assert result.getpixel((0, 119)) == (
        0,
        255,
        0,
        255,
    )  # addImage由来の下端が残っている
