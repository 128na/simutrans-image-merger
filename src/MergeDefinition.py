import json
from PIL import Image, ImageDraw
from src.SimutransColor import (
    SPECIAL_COLORS,
    TRANSPARENT_COLOR,
)
from typing import Final
import logging


class BaseProcessor:
    def __init__(self, data: dict) -> None:
        self.modifyPixel: Final[bool] = False
        self.name: Final[str] = data["name"]
        self.comment: Final[str] | None = data.get("comment")


class ImageProcessor(BaseProcessor):
    "画像単位の操作"

    def handleImage(self, canvas: Image.Image) -> Image.Image:
        return canvas


class PixelProcessor(BaseProcessor):
    "pixel単位の操作"

    def handlePixel(
        self,
        draw: ImageDraw.ImageDraw,
        xy: tuple[int, int],
        pixel: tuple[int, int, int, int],
    ) -> None:
        pass


class MergeImage(ImageProcessor):
    "画像合成"

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.pathes: Final[list[str]] = data["pathes"]
        self.mode: Final[str] = data["mode"]
        self.offset: Final[tuple[int, int]] = (data["offset"]["x"], data["offset"]["y"])

    def handleImage(self, canvas):
        for path in self.pathes:
            addImage = Image.open(path)
            if addImage.size > canvas.size:  # 追加画像が大きい場合はキャンバスを拡大する
                canvas = self.doResize(canvas, addImage.size)
            if addImage.size < canvas.size:  # 追加画像が小さい場合はキャンバスのサイズに拡大する
                addImage = self.doResize(addImage, canvas.size)
            if self.offset != (0, 0):  # オフセット指定があれば追加画像をずらす
                addImage = self.doOffset(addImage)
            logging.info("'{0}' merged.".format(path))
            canvas = Image.alpha_composite(
                canvas.convert("RGBA"), addImage.convert("RGBA")
            )
        return canvas

    def doResize(self, original: Image.Image, size: tuple[int, int]) -> Image.Image:
        newImage = Image.new("RGBA", size)
        newImage.paste(original, (0, 0), original)
        return newImage

    def doOffset(self, original: Image.Image) -> Image.Image:
        newImage = Image.new("RGBA", original.size)
        newImage.paste(original, self.offset, original)
        return newImage


class RemoveTransparent(PixelProcessor):
    "透明->透過色"

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.threthold: Final[int] = data["threthold"]

    def handlePixel(self, draw, xy, pixel):
        if pixel[3] == 255:  # 不透過はそのまま
            return draw
        if pixel[3] >= self.threthold:  # 半透過は閾値以上は塗りつぶす
            return draw.point(xy, (pixel[0], pixel[1], pixel[2], 255))
        else:  # 閾値未満は透過色にする
            return draw.point(xy, TRANSPARENT_COLOR)


class ReplaceColor(PixelProcessor):
    "指定色置換"

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.search: tuple[int, int, int] = (
            data["search"]["r"],
            data["search"]["g"],
            data["search"]["b"],
        )
        self.replace: tuple[int, int, int] = (
            data["replace"]["r"],
            data["replace"]["g"],
            data["replace"]["b"],
        )

    def handlePixel(self, draw, xy, pixel):
        if (pixel[0], pixel[1], pixel[2]) == self.search:
            draw.point(xy, self.replace)


class RemoveSpecialColor(PixelProcessor):
    "特殊色削除"

    def __init__(self, data: dict) -> None:
        super().__init__(data)

    def handlePixel(self, draw, xy, pixel):
        if (pixel[0], pixel[1], pixel[2]) in SPECIAL_COLORS:
            draw.point(
                xy,
                (
                    min(255, pixel[0] + 1),
                    min(255, pixel[1] + 1),
                    min(255, pixel[2] + 1),
                ),
            )


class Definition:
    def __init__(self, data: dict) -> None:
        self.outputPath: str = data["outputPath"]
        self.processors: list[ImageProcessor | PixelProcessor] = list(
            map(self.processorFactory, data["rules"])
        )
        self.comment: str | None = data.get("comment")

    def processorFactory(self, rule: dict) -> ImageProcessor | PixelProcessor:
        match rule["name"]:
            case "mergeImage":
                return MergeImage(rule)
            case "removeTransparent":
                return RemoveTransparent(rule)
            case "replaceColor":
                return ReplaceColor(rule)
            case "removeSpecialColor":
                return RemoveSpecialColor(rule)

        raise KeyError("{0} is not defined rule.".format(rule["name"]))


class MergeDefinitionLoader:
    def __init__(self, path: str) -> None:
        self.path = path
        file = open(self.path, "r")
        data: dict = json.load(file)
        self.version: int = data["version"]
        self.comment: str | None = data.get("comment")
        self.definitions: list[Definition] = list(map(Definition, data["definitions"]))

    def getDefinitions(self) -> list[Definition]:
        return self.definitions
