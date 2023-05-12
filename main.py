if __name__ == "__main__":
    import json
    import core
    from PIL import Image
    id = None
    id = 48101765
    while id is None:
        id = input("Enter ID: ")
        try:
            id = int(id)
            break
        except ValueError:
            print("Wrong format.")
            id = None

    print(f"Fetching info for {id}...")

    features = core.get_features(id)

    with open("features.json", "w") as f:
        json.dump(features, f, indent=2)
    
    feature = features["data"]["images"]["features"][0]

    print(f"Image name: {feature['properties']['imagepath']}")

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
    print(f"Final image size: {image_width}x{image_height}")
    print(f"Tilecount: {len(tile_list)}")
    try:
        input("Press Enter to download or Ctrl+C to exit now or anytime during download.")
        img = core.download_all(((image_width, image_height), tile_list))
        path = f'output_{id}_{zoom}.jpg'
        img.convert('RGB').save(path, quality=95)
        print(f"Saved to {path}")
    except KeyboardInterrupt:
        pass
    
    print("\nDone")