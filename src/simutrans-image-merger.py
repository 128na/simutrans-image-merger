import sys
from typing import Final
from PIL import Image, ImageDraw
import argparse


sys.path.append("./")

from src.MergeDefinition import (
    MergeDefinitionLoader,
    Definition,
    ImageProcessor,
    PixelProcessor,
)

from src.Logger import stdoutLogger, stderrLogger


def run():
    greeting = "simutrans image merger version %%APP_VERSION%%."
    parser = argparse.ArgumentParser(description=greeting)
    parser.add_argument("jsonPath", type=str, help="path to definition json file")
    args = parser.parse_args()
    try:
        stdoutLogger.info(greeting)

        loader: Final[MergeDefinitionLoader] = MergeDefinitionLoader(args.jsonPath)
        definitions: Final[list[Definition]] = loader.getDefinitions()

        stdoutLogger.info(
            "Definition file load successed. version is {0}.".format(loader.version)
        )

        for definition in definitions:
            stdoutLogger.info(
                "Start processing for '{0}'.".format(definition.outputPath)
            )
            runDefinition(definition)
            stdoutLogger.info("File saved '{0}'.".format(definition.outputPath))

    except Exception as e:
        stderrLogger.error("Merge failed")
        raise e


def runDefinition(definition: Definition):
    result: Image.Image = Image.new("RGBA", (0, 0))

    pixelProcessors: list[PixelProcessor] = []
    for processor in definition.processors:
        if isinstance(processor, PixelProcessor):
            stdoutLogger.info("\tEnqueue pixel processor '{0}'.".format(processor.name))
            pixelProcessors.append(processor)
        else:
            if len(pixelProcessors) > 0:
                stdoutLogger.info("\tApply pixel processors.")
                runPixelProcessors(pixelProcessors, result)
                pixelProcessors.clear()
        if isinstance(processor, ImageProcessor):
            stdoutLogger.info("\tApply image processor '{0}'.".format(processor.name))
            result = processor.handleImage(result)
    if len(pixelProcessors) > 0:
        stdoutLogger.info("\tApply pixel processors.")
        runPixelProcessors(pixelProcessors, result)

    result.save(definition.outputPath)


def runPixelProcessors(
    processors: list[PixelProcessor], result: Image.Image
) -> Image.Image:
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(result, "RGBA")
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
