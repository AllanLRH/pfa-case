import pathlib
import pydantic

case_root = pathlib.Path(__file__).parents[1].absolute()
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


class Settings(pydantic.BaseSettings):
    mlflow_server_port: str
    mlflow_ui_port: str
    mlflow_database_uri: str

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
