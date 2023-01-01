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
  /* DynamicJsonDocument doc(1024); */
  StaticJsonDocument<1024> doc;
  auto err = deserializeJson(doc, Serial);

  if (err != DeserializationError::Ok) {
    Serial.print(F("Error decoding doc: "));
    Serial.println(err.f_str());
    delay(10);
    while (Serial.available() > 0) {
      Serial.read();
      delay(10);
    }
    return;
  }

  JsonObject obj = doc.as<JsonObject>();
  if (!obj) {
    Serial.println(F("command must be an object"));
    return;
  }

  if (!obj["cmd"].is<String>()) {
    Serial.println(F("command must have key 'cmd' with string value"));
    return;
  }

  String cmd = obj["cmd"];

  if (cmd == "on") {
    on = true;
    set_color();
  } else if (cmd == "off") {
    on = false;
    all_off();
  } else if (cmd == "set_pix") {
    if (!obj["pix"].is<int>()) {
      Serial.println("set_pix cmd must have key 'pix' with int value");
      return;
    }
    int pix = obj["pix"];
    if (pix < 0 || pix >= N_PIXELS) {
      Serial.println(F("Invalid pix index"));
      return;
    }

    JsonArray color = obj["color"];
    if (!color || color.size() != 3) {
      Serial.println(F("set_pix cmd must have key 'color' as array of 3 RGB values"));
      return;
    }

    colors[pix] = pixels.Color(color[0], color[1], color[2]);
    pixels.setPixelColor(pix, colors[pix]);
    pixels.show();

  } else if (cmd == "set") {
    JsonArray new_colors = obj["colors"];

    if (!new_colors || new_colors.size() != N_PIXELS) {
      Serial.println(F("set cmd must have key 'colors' with RGB values for each pixel"));
      return;
    }

    for (int pix=0; pix < N_PIXELS; pix++) {
      JsonArray color = new_colors[pix];
      if (!color || color.size() != 3) {
        Serial.print(F("Pixel color must be 3 RGB values, got"));
        Serial.println(color.size());
        return;
      }

      colors[pix] = pixels.Color(color[0], color[1], color[2]);
      pixels.setPixelColor(pix, colors[pix]);
    }
    pixels.show();

  } else if (cmd == "get") {
    doc.to<JsonObject>();
    doc["on"] = on;
    for (int pix=0; pix < N_PIXELS; pix++) {
        RGB rgb(colors[pix]);
        doc["colors"][pix][0] = rgb.r;
        doc["colors"][pix][1] = rgb.g;
        doc["colors"][pix][2] = rgb.b;
    }

    if (doc.overflowed()) {
      Serial.println(F("Overflow!!!"));
      return;
    }
    serializeJson(doc, Serial);
    Serial.println();
    return;
  } else {
    Serial.print(F("Unknown command: "));
    Serial.println(cmd);
    return;
  }

  Serial.print(F("ok: "));
  Serial.println(cmd);
}


void loop() {
  if (on) set_color();
  delay(10);
}
