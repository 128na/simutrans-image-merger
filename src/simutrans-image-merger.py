import sys
from typing import Final
from PIL import Image, ImageDraw
import logging

logging.basicConfig(format="%(funcName)s: %(message)s", level=logging.INFO)
sys.path.append("./")

from src.MergeDefinition import (
    MergeDefinitionLoader,
    Definition,
    ImageProcessor,
    PixelProcessor,
)


def run():
    if len(sys.argv) < 2:
        raise Exception("json file path not provided.")

    loader: Final[MergeDefinitionLoader] = MergeDefinitionLoader(sys.argv[1])
    definitions: Final[list[Definition]] = loader.getDefinitions()

    logging.info(
        "definition file load successed. version is {0}.".format(loader.version)
    )

    for definition in definitions:
        logging.info("start processing for '{0}'.".format(definition.outputPath))
        runDefinition(definition)
        logging.info("file saved '{0}'.".format(definition.outputPath))


def runDefinition(definition: Definition):
    result: Image.Image = Image.new("RGBA", (0, 0))

    pixelProcessors: list[PixelProcessor] = []
    for processor in definition.processors:
        if isinstance(processor, PixelProcessor):
            logging.info("Enqueue pixel processor '{0}'.".format(processor.name))
            pixelProcessors.append(processor)
        else:
            if len(pixelProcessors) > 0:
                logging.info("Apply pixel processors.")
                runPixelProcessors(pixelProcessors, result)
                pixelProcessors.clear()
        if isinstance(processor, ImageProcessor):
            logging.info("Apply image processor '{0}'.".format(processor.name))
            result = processor.handleImage(result)
    if len(pixelProcessors) > 0:
        logging.info("Apply pixel processors.")
        runPixelProcessors(pixelProcessors, result)

    result.save(definition.outputPath)


def runPixelProcessors(
    processors: list[PixelProcessor], result: Image.Image
) -> Image.Image:
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(result, 'RGBA')
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
    run()
