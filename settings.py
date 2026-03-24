import json

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




#with open('test.json', 'r') as f:
#    loaded_data = json.load(f)
#    print("Data read successfully:")
#    print(loaded_data)


class Settings():
    def __init__ (self, filename):
        self._filename = filename
        self._settings = DEFAULTS


    def get_brightness(self):
        return self._settings["brightness"]

    def set_brightness(self, brightness):
        print("set")
        #clamp to mix / max brightness
        if brightness < MIN_BRIGHTNESS:
            self._settings["brightness"] = MIN_BRIGHTNESS
        elif brightness > MAX_BRIGHTNESS:
            self._settings["brightness"] = MAX_BRIGHTNESS
        else:
            self._settings["brightness"] = brightness


    def get_fullscreen(self):
        return self._settings["fullscreen"]

    def set_fullscreen(self, fullscreen):
        self._settings["fullscreen"] = fullscreen


    def get_volume(self):
        return self._settings["volume"]

    def set_volume(self, volume):
        if volume < MIN_VOLUME:
            self._settings["volume"] = MIN_VOLUME
        elif volume > MAX_VOLUME:
            self._settings["volume"] = MAX_VOLUME
        else:
            self._settings["volume"] = volume

    def write_setting(self):
        with open(TEST_FILENAME, 'w') as f:
            json.dump(self._settings, f)
            print("Data written successfully")

    brightness = property(get_brightness, set_brightness)
    fullscreen = property(get_fullscreen, set_fullscreen)
    volume = property(get_volume, set_volume, write_setting)
    



    

if __name__ == "__main__":
    my_settings = Settings(TEST_FILENAME)
    my_settings.brightness = 50
    my_settings.write_setting()