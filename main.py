if __name__ == "__main__":
    import json
    import core
    from PIL import Image
    import os

    print("# NEA Viewer - Imagemapper")
    print()

    id = None
    while id is None:
        id = input("Enter ID: ")
        try:
            id = int(id)
            break
        except ValueError:
            print("Wrong format.")
            id = None

    print(f"Fetching info for {id}...")
    print()

    features = core.get_features(id)

    with open("features.json", "w") as f:
        json.dump(features, f, indent=2)
    
    feature = features["data"]["images"]["features"][0]

    print(f">> Image name: {feature['properties']['imagepath']}")
    print(f">> Image date: {feature['properties']['bildflugdatum']}")

    print()

    zoom = None
    while zoom is None:
        zoom = input(f"Enter Zoom-Level ({feature['properties']['image_minzoom']}-{feature['properties']['image_maxzoom']}): ")
        try:
            zoom = int(zoom)
            break
        except ValueError:
            print("Wrong zoom-level.")
            zoom = None

    (image_width, image_height), tile_list = core.construct_all_meta(feature, zoom)
    print()
    print(f">> Final image size: {image_width}x{image_height}")
    print(f">> Tilecount: {len(tile_list)}")
    print()
    input("Press Enter to download or Ctrl+C to exit now or anytime during download.")
    print()
    img = core.download_all(((image_width, image_height), tile_list))
    path_n = f'output_{id}_{zoom}'
    path = path_n
    i = 2
    while os.path.exists(path + ".jpg"):
        path = f"{path_n} ({i})"
        i += 1
    path += ".jpg"
    img.convert('RGB').save(path, quality=95)
    print(f"Saved to {path}")
    
    print("\nDone")