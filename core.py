from typing import Callable
from PIL import Image
import json
import requests
from urllib.parse import urlencode, quote
from io import BytesIO
from math import ceil

def get_features(id: str|int) -> dict:
    params = {
        "bild_id": str(id)
    }
    
    response = requests.get(f"https://nea.geofly.eu/api.php/getFeature?{urlencode(params)}")
    content = response.content.decode()
    return dict(json.loads(content))

def construct_all_meta(feature: dict, for_zoom_level: int) -> tuple[tuple[int, int], list[tuple[int, int, str]]]:
    """Use 1 specific feature from json["data"]["images"]["features"] (list) for parameter "feature" """
    min_zoom = int(feature["properties"]["image_minzoom"])
    max_zoom = int(feature["properties"]["image_maxzoom"])
    if for_zoom_level < min_zoom or for_zoom_level > max_zoom:
        raise ValueError(f"Invalid zoom level. max =  {max_zoom}; min = {min_zoom}")

    image_tile_base_id = feature["properties"]["bildflugnummer"]

    divisor = 2 ** (max_zoom - for_zoom_level)

    total_width = int(feature["properties"]["image_width"] / divisor)
    total_height = int(feature["properties"]["image_height"] / divisor)
    imagepath = str(feature["properties"]["imagepath"])
    TILE_WIDTH, TILE_HEIGHT = (256, 256)
    result = []
    for y in range(ceil(total_height / TILE_HEIGHT)):
        for x in range(ceil(total_width / TILE_WIDTH)):
            url = f"https://nea.geofly.eu/tiles/{quote(str(image_tile_base_id))}/{quote(imagepath)}/{quote(str(for_zoom_level))}/{x}/{y}.jpg"
            result.append((x * TILE_WIDTH, y * TILE_HEIGHT, url))
    
    return ((total_width, total_height), result)

def download_all(meta) -> Image:
    image_size, tile_list = meta
    img = Image.new("RGBA", image_size, 0)

    try:
        for i, (x, y, url) in enumerate(tile_list):
            print(f"Downloading Tile #{i+1} of {len(tile_list)} [{url}]")
            tile_response = requests.get(url)
            try:
                with Image.open(BytesIO(tile_response.content)) as tile:
                    img.paste(tile, box=(x, y))
            except KeyboardInterrupt as ki:
                raise ki
            except:
                pass
    except KeyboardInterrupt:
        print("Interrupting download.")
    
    return img