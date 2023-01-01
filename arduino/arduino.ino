#include <Adafruit_NeoPixel.h>
#include <ArduinoJson.h>



const int PIN = 6;

const int N_PIXELS_RING = 7;
const int N_RINGS = 2;
const int N_PIXELS = N_PIXELS_RING * N_RINGS;

Adafruit_NeoPixel pixels(N_PIXELS, PIN, NEO_GRB + NEO_KHZ800);

const auto OFF = pixels.Color(0, 0, 0);
const auto MAX = pixels.Color(255, 255, 255);

const auto RED = pixels.Color(64, 0, 0);
const auto GREEN = pixels.Color(0, 64, 0);
const auto BLUE = pixels.Color(0, 0, 64);


StaticJsonDocument<512> json;

uint32_t colors[N_PIXELS];

bool on = true;

uint32_t white(float intensity) {
    auto value = static_cast<uint8_t>(255 * intensity);
    return pixels.Color(value, value, value);
}


void all_off() {
  for (int i=0; i < N_PIXELS; i++) {
    pixels.setPixelColor(i, OFF);
  }
  pixels.show();
}

void set_color() {
  for (int i=0; i < N_PIXELS; i++) {
    pixels.setPixelColor(i, colors[i]);
  }
  pixels.show();
}

void setup() {
  pixels.begin();

  for (int pixel=0; pixel < N_PIXELS; pixel++) {
    colors[pixel] = RED;
  }

  /* all_off(); */
  set_color();

  Serial.begin(115200);
  while (!Serial) delay(10);
}

struct RGB {
    uint8_t r;
    uint8_t g;
    uint8_t b;

    RGB(uint32_t color) {
        r = (color & (0xfful << 16)) >> 16;
        g = (color & (0xfful << 8)) >> 8;
        b = color & 0xfful;
    }
};


void serialEvent() {
  auto err = deserializeJson(json, Serial);
  if (err != DeserializationError::Ok) {
    Serial.print("Error decoding json: ");
    Serial.println(err.c_str());
    return;
  }

  JsonObject obj = json.as<JsonObject>();
  if (!obj) {
    Serial.println("Json command must be an object");
    return;
  }

  if (!obj["cmd"].is<String>()) {
    Serial.println("Json command must have key 'cmd' with string value");
    return;
  }

  String cmd = obj["cmd"];

  if (cmd == "on") {
    on = true;
    set_color();
  } else if (cmd == "off") {
    on = false;
    all_off();
  } else if (cmd == "set") {
    if (!obj["pix"].is<int>()) {
      Serial.println("Json set cmd must have key 'pix' with int value");
      return;
    }
    int pix = obj["pix"];
    if (pix < 0 || pix >= N_PIXELS) {
      Serial.println("Invalid pix index");
      return;
    }

    JsonArray color = obj["color"];
    if (!color || color.size() != 3) {
      Serial.println("Json set cmd must have key 'color' as array of 3 RGB values");
      return;
    }

    const uint8_t r = color[0];
    const uint8_t g = color[1];
    const uint8_t b = color[2];
    colors[pix] = pixels.Color(r, g, b);
    pixels.setPixelColor(pix, colors[pix]);
    pixels.show();
  } else if (cmd == "get") {
    json.clear();
    json["on"] = on;
    for (int pix=0; pix < N_PIXELS; pix++) {
        RGB rgb(colors[pix]);
        json["colors"][pix][0] = rgb.r;
        json["colors"][pix][1] = rgb.g;
        json["colors"][pix][2] = rgb.b;
    }
    serializeJson(json, Serial);
    Serial.println();
    return;
  } else {
    Serial.print("Unknown command: ");
    Serial.println(cmd);
    return;
  }

  Serial.print("ok: ");
  Serial.println(cmd);
}


void loop() {
  delay(10);
}
