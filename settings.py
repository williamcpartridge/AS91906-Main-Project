import json
from os.path import exists

DEFAULTS = {
    "brightness": 100,
    "fullscreen": False,
    "volume": 100

}

TEST_FILENAME = "test.json"
MIN_BRIGHTNESS = 0
MAX_BRIGHTNESS = 200
MIN_VOLUME = 0
MAX_VOLUME = 100



class Settings():
    # initialization:
    def __init__ (self, filename): 
        self._filename = filename
        self._settings = DEFAULTS
        self.read_settings(filename)


    # write setting to the setting file
    def write_setting(self):
        result = self.write_json(self._filename, self._settings)
        return result

    def write_json(self, filename, obj):
        with open(filename, 'w') as f:
            json.dump(obj, f)
            print("Data written successfully")

    def read_settings(self):
        result = self.json_read(self._filename, self._settings)
        return result

    # read settings from setting file
    def json_read(self, filename, obj):
        with open(filename, 'r') as f:
            obj = json.load(f)
            print("Data read successfully:")
            print(obj)


    # brightness:
    def get_brightness(self):
        return self._settings["brightness"] # get brightness setting

    def set_brightness(self, brightness):
        print("set")
        #clamp to mix / max brightness
        if brightness < MIN_BRIGHTNESS:
            self._settings["brightness"] = MIN_BRIGHTNESS
        elif brightness > MAX_BRIGHTNESS:
            self._settings["brightness"] = MAX_BRIGHTNESS
        else:
            self._settings["brightness"] = brightness # set brightness

    brightness = property(get_brightness, set_brightness) # property shortcut for brightness


    # fullscreen:
    def get_fullscreen(self):
        return self._settings["fullscreen"] # get fullscreen setting

    def set_fullscreen(self, fullscreen):
        self._settings["fullscreen"] = fullscreen # set fullscreen

    fullscreen = property(get_fullscreen, set_fullscreen) # property shortcut for fullscreen


    # volume:
    def get_volume(self):
        return self._settings["volume"] # get volume setting

    def set_volume(self, volume):
        if volume < MIN_VOLUME:
            self._settings["volume"] = MIN_VOLUME # clamp to minimum
        elif volume > MAX_VOLUME:
            self._settings["volume"] = MAX_VOLUME # clamp to maximum
        else:
            self._settings["volume"] = volume # set volume

    volume = property(get_volume, set_volume, write_setting) # property shortcut for volume


if __name__ == "__main__":
    my_settings = Settings(TEST_FILENAME)
    