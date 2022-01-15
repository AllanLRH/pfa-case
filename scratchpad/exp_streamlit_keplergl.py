"""
Kepler.gl map in stremlit
Source: https://github.com/chrieke/streamlit-keplergl
"""

import streamlit as st
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
import pandas as pd

st.header("This is a kepler.gl map in streamlit")

df = pd.DataFrame(
    {
        "category": {
            5069701104134: "assault",
            6074729204104: "assault",
            7103536315201: "assault",
            11082415274000: "missing person",
            4037801104134: "assault",
        },
        "description": {
            5069701104134: "battery",
            6074729204104: "assault",
            7103536315201: "stalking",
            11082415274000: "missing adult",
            4037801104134: "battery",
        },
        "weekday": {
            5069701104134: "wednesday",
            6074729204104: "saturday",
            7103536315201: "tuesday",
            11082415274000: "saturday",
            4037801104134: "friday",
        },
        "date": {
            5069701104134: "06/22/2005",
            6074729204104: "07/15/2006",
            7103536315201: "09/25/2007",
            11082415274000: "09/24/2011",
            4037801104134: "12/12/2003",
        },
        "time": {
            5069701104134: "12:20",
            6074729204104: "00:55",
            7103536315201: "00:01",
            11082415274000: "11:00",
            4037801104134: "12:00",
        },
        "resolution": {
            5069701104134: "none",
            6074729204104: "none",
            7103536315201: "none",
            11082415274000: "located",
            4037801104134: "none",
        },
        "longitude": {
            5069701104134: -122.428223303176,
            6074729204104: -122.410672425337,
            7103536315201: -122.458226300605,
            11082415274000: -122.459172646607,
            4037801104134: -122.386667033903,
        },
        "latitude": {
            5069701104134: 37.7818959488603,
            6074729204104: 37.799788690123,
            7103536315201: 37.7413616001449,
            11082415274000: 37.7082001648459,
            4037801104134: 37.7898821569191,
        },
        "label": {
            5069701104134: "violent",
            6074729204104: "violent",
            7103536315201: "violent",
            11082415274000: "other",
            4037801104134: "violent",
        },
    }
)
config = {
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

map_1 = KeplerGl(height=900, data={"Crimes": df}, config=config)
keplergl_static(map_1)


st.map(df, use_container_width=True)
