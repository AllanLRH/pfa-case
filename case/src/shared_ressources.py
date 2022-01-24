import pathlib
from unittest.util import unorderable_list_difference
import pydantic
from loguru import logger
from typing import Union, TextIO, Any
import sys


class Settings(pydantic.BaseSettings):
    mlflow_server_port: str
    mlflow_ui_port: str
    mlflow_database_uri: str
    loguru_logging_level: str
    loguru_debug_destination: Any
    cache_as_parquet_if_no_cached_file_exists = bool

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

    @pydantic.validator("loguru_debug_destination", pre=True)
    def cast_to_path_or_system_stream(cls, v) -> Union[TextIO, pathlib.Path]:
        if v.lower() == "stdout":
            return sys.stdout
        elif v.lower() == "stderr":
            return sys.stderr
        return pathlib.Path(v)


settings = Settings()

logger.remove()
logger.add(sink=sys.stderr, level="INFO")
if settings.loguru_logging_level == "DEBUG":
    logger.add(sink=settings.loguru_debug_destination, level="DEBUG")

case_root = pathlib.Path(__file__).parents[1].absolute()

pfa_red = "#990735"
# From Adobe Kuler color picker, Triad color for pfa_red . https://color.adobe.com/create/color-wheel
pfa_blue = "#177C99"

weekdays = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

streamlit_keplergl_config = {
    "version": "v1",
    "config": {
        "visState": {
            "layers": [
                {
                    "type": "hexagonId",
                    "visualChannels": {
                        "sizeField": {"type": "integer", "name": "value"},
                        "coverageField": None,
                        "colorScale": "quantize",
                        "coverageScale": "linear",
                        "colorField": {"type": "integer", "name": "value"},
                        "sizeScale": "linear",
                    },
                    "config": {
                        "dataId": "data_1",
                        "color": [250, 116, 0],
                        "textLabel": {
                            "color": [255, 255, 255],
                            "field": None,
                            "size": 50,
                            "anchor": "middle",
                            "offset": [0, 0],
                        },
                        "label": "H3 Hexagon",
                        "isVisible": True,
                        "visConfig": {
                            "coverageRange": [0, 1],
                            "opacity": 0.8,
                            "elevationScale": 5,
                            "hi-precision": False,
                            "coverage": 1,
                            "enable3d": True,
                            "sizeRange": [0, 500],
                            "colorRange": {
                                "category": "Uber",
                                "type": "sequential",
                                "colors": [
                                    "#194266",
                                    "#355C7D",
                                    "#63617F",
                                    "#916681",
                                    "#C06C84",
                                    "#D28389",
                                    "#E59A8F",
                                    "#F8B195",
                                ],
                                "reversed": False,
                                "name": "Sunrise 8",
                            },
                        },
                        "columns": {"hex_id": "hex_id"},
                    },
                    "id": "jdys7lp",
                }
            ],
            "interactionConfig": {
                "brush": {"enabled": False, "size": 0.5},
                "tooltip": {
                    "fieldsToShow": {"data_1": ["hex_id", "value"]},
                    "enabled": True,
                },
            },
            "splitMaps": [],
            "layerBlending": "normal",
            "filters": [],
        },
        "mapState": {
            "bearing": 2.6192893401015205,
            "dragRotate": True,
            "zoom": 12.32053899007826,
            "longitude": -122.42590232651203,
            "isSplit": False,
            "pitch": 37.374216241015446,
            "latitude": 37.76209132041332,
        },
        "mapStyle": {
            "mapStyles": {},
            "topLayerGroups": {},
            "styleType": "dark",
            "visibleLayerGroups": {
                "building": True,
                "land": True,
                "3d building": False,
                "label": True,
                "water": True,
                "border": False,
                "road": True,
            },
        },
    },
}

seaborn_context = dict(
    context="paper",
    style="whitegrid",
    color_codes=True,
    font_scale=1.2,
)
