import sys
from typing import Final

from PIL import Image, ImageDraw
from MergeDefinition import (
    MergeDefinitionLoader,
    Definition,
    ImageProcessor,
    PixelProcessor,
)

import psutil


def run():
    if len(sys.argv) < 2:
        raise Exception("json file path not provided.")

    definitions: Final[list[Definition]] = MergeDefinitionLoader(
        sys.argv[1]
    ).getDefinitions()

    for definition in definitions:
        sys.stdout.write("start processing '{0}'.\n".format(definition.outputPath))
        runDefinition(definition)
        sys.stdout.write("saved '{0}'.\n".format(definition.outputPath))


def runDefinition(definition: Definition):
    result: Image.Image = Image.new("RGBA", (0, 0))

    pixelProcessors: list[PixelProcessor] = []
    for processor in definition.processors:
        if isinstance(processor, PixelProcessor):
            sys.stdout.write(
                "\tEnqueue pixel processor '{0}'.\n".format(processor.name)
            )
            pixelProcessors.append(processor)
        else:
            if len(pixelProcessors) > 0:
                sys.stdout.write("\tApply pixel processors.\n")
                runPixelProcessors(pixelProcessors, result)
                pixelProcessors.clear()
        if isinstance(processor, ImageProcessor):
            sys.stdout.write("\tApply image processor '{0}'.\n".format(processor.name))
            result = processor.handleImage(result)
    result.save(definition.outputPath)


def runPixelProcessors(
    processors: list[PixelProcessor], result: Image.Image
) -> Image.Image:
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(result)
    data: Final[list[tuple[int, int, int, int]]] = list(result.getdata())
    xy: tuple[int, int] = (0, 0)
    w = result.size[0]
    i: int = 0
    for pixel in data:
        xy = (i % w, i // w)
        for processor in processors:
            processor.handlePixel(draw, xy, pixel)
        i = i + 1
    return result


if __name__ == "__main__":
    m1 = psutil.virtual_memory()
    run()
    m2 = psutil.virtual_memory()
    print(f"memory used {0}".format(m2.used - m1.used))
