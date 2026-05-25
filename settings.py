import json
from os.path import exists
import debug
debug.DEBUG_LEVEL = 0

DEFAULTS = {
    "brightness": 100,
    "fullscreen": False,
    "volume": 100,
    "size": (10, 7),
    "speed": 20,
    "apple count": 1
}

TEST_FILENAME = "test.json"
MIN_BRIGHTNESS = 0
MAX_BRIGHTNESS = 200
MIN_VOLUME = 0
MAX_VOLUME = 100
MAX_SIZE = (100, 100)
MIN_SIZE = (5, 5)
MAX_SPEED = 60
MIN_SPEED = 5
MAX_APPLES = 10
MIN_APPLES = 1



class Settings():
    # initialization:
    def __init__ (self, filename, reset=False): 
        self._filename = filename
        self._settings = DEFAULTS
        self.read_settings()


    # write setting to the setting file
    def write_setting(self):
        result = self.write_json(self._filename, self._settings)
        return result

    def write_json(self, filename, obj):
        with open(filename, 'w') as f:
            json.dump(obj, f)
            debug.dprint(1, "Data written successfully")
            debug.dprint(1, obj)

    def read_settings(self):
        result = self.json_read(self._filename, self._settings)
        return result

    # read settings from setting file
    def json_read(self, filename, obj):
        with open(filename, 'r') as f:
            obj = json.load(f)
            debug.dprint(1, "Data read successfully:")
            debug.dprint(1, obj)
            return obj


    # brightness:
    def get_brightness(self):
        return self._settings["brightness"] # get brightness setting

    def set_brightness(self, brightness):
        #clamp to mix / max brightness
        if brightness < MIN_BRIGHTNESS:
            self._settings["brightness"] = MIN_BRIGHTNESS
        elif brightness > MAX_BRIGHTNESS:
            self._settings["brightness"] = MAX_BRIGHTNESS
        else:
            self._settings["brightness"] = brightness # set brightness

    brightness = property(get_brightness, set_brightness, write_setting) # property shortcut for brightness


    # fullscreen:
    def get_fullscreen(self):
        return self._settings["fullscreen"] # get fullscreen setting

    def set_fullscreen(self, fullscreen):
        self._settings["fullscreen"] = fullscreen # set fullscreen

    fullscreen = property(get_fullscreen, set_fullscreen, write_setting) # property shortcut for fullscreen


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

    def get_size(self):
        return self._settings["size"]
    
    def set_size(self, size):
        if size < MIN_SIZE:
            self._settings["size"] = MIN_SIZE
        elif size > MAX_SIZE:
            self._settings["size"] = MAX_SIZE
        else:
            self._settings["size"] = size

    size = property(get_size, set_size, write_setting)

    def get_speed(self):
        return self._settings["speed"]
    
    def set_speed(self, speed):
        if speed < MIN_SPEED:
            self._settings["speed"] = MIN_SPEED
        elif speed > MAX_SPEED:
            self._settings["speed"] = MAX_SPEED
        else:
            self._settings["speed"] = speed

    speed = property(get_speed, set_speed, write_setting)

    def get_apple_count(self):
        return self._settings["apple count"]
    
    def set_apple_count(self, apples):
        if apples < MIN_APPLES:
            self._settings["apple count"] = MIN_APPLES
        elif apples > MAX_APPLES:
            self._settings["apple count"] = MAX_APPLES
        else:
            self._settings["apple count"] = apples

    apples = property(get_apple_count, set_apple_count, write_setting)



if __name__ == "__main__":
    my_settings = Settings(TEST_FILENAME, True)
    my_settings.write_setting
    my_settings.brightness = 50
    my_settings.fullscreen = True
    my_settings.read_settings

    #settings = Settings("settings.json", True)
