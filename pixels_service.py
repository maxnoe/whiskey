"""
Long running process running as root receiving commands from a redis queue
"""
import redis
import time
import math
from threading import Thread, Event
import json
from functools import partial

try:
    import board
    import neopixel
except (ImportError, NotImplementedError):
    # not on a pi
    pass



OFF = (0, 0, 0)
RED = (0xff, 0, 0)
GREEN = (0, 0xff, 0)
BLUE = (0, 0, 0xff)

N_PIX_JEWELL = 7


class Pixels(Thread):
    def __init__(self, pin, n_jewells, interval=0.001):
        super().__init__()

        self.stop_event = Event()

        self.n_pixels = N_PIX_JEWELL * n_jewells
        self.pixels = neopixel.NeoPixel(
            pin,
            self.n_pixels,
            auto_write=False,
            brightness=1.0,
        )
        all_off(self.pixels)

        self.colors = [OFF] * self.n_pixels
        self.on = False
        self.current_cmd = None
        self.interval = interval


    def run(self):
        while not self.stop_event.is_set():
            if self.on:
                if self.current_cmd is not None:
                    self.current_cmd(self.pixels)

                self.pixels.show()
            self.stop_event.wait(self.interval)

    def terminate(self):
        self.stop_event.set()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_event.set()
        all_off(self.pixels)


def hsv2rgb(h, s, v):
    h = h / (1/6)
    c = s * v
    x = c * (1 - abs(h % 2 - 1))

    if h < 1:
        r, g, b = (c, x, 0)
    elif h < 2:
        r, g, b = (x, c, 0)
    elif h < 3:
        r, g, b = (0, c, x)
    elif h < 4:
        r, g, b = (0, x, c)
    elif h < 5:
        r, g, b = (x, 0, c)
    else:
        r, g, b = (c, 0, x)

    m = v - c
    return (int(255 * (r + m)), int(255 * (g + m)), int(255 * (b + m)))


def all_off(pixels):
    pixels.fill(OFF)
    pixels.show()


def set_colors(pixels, colors):
    for pix, color in enumerate(colors):
        pixels[pix] = color


def sine_wave(pixels, period, basecolor=(0xff, 0xff, 0xff)):
    t = time.time()
    intensity = 0.5 * (1 + math.sin(2 * math.pi * t / period))
    color = tuple(int(intensity * c) for c in basecolor)
    pixels.fill(color)

def rainbow(pixels, period):
    t = time.time()
    h = (t % period) / period
    color = hsv2rgb(h=h, s=1.0, v=0.25)
    pixels.fill(color)


def clock(pixels, period):
    t = (time.time() % period) / period
    idx = 1 + int((N_PIX_JEWELL - 1) * t)
    pixels.fill(OFF)

    for jewell in range(len(pixels) // N_PIX_JEWELL):
        pixels[jewell * N_PIX_JEWELL + idx] = (0, 0, 0x10)


def handle_cmd(command, pixels):
    cmd = command.get("cmd")

    pixel_colors = pixels.colors

    if cmd == "off":
        pixels.on = False
        all_off(pixels.pixels)

    elif cmd == "on":
        pixels.on = True

    elif cmd == "rainbow":
        period = command.get("period", 1.0)
        pixels.current_cmd = partial(rainbow, period=period)

    elif cmd == "clock":
        period = command.get("period", 1.0)
        pixels.current_cmd = partial(clock, period=period)

    elif cmd == "sine":
        period = command.get("period", 1.0)
        basecolor = command.get("color", [64, 64, 64])
        pixels.current_cmd = partial(sine_wave, period=period, basecolor=basecolor)

    elif cmd == 'none':
        pixels.current_cmd = None

    elif cmd == 'set_pix':
        pix = command['pix']
        color = command['color']
        pixel_colors[pix] = color
        pixels.current_cmd = partial(set_colors, colors=pixel_colors)

    elif cmd == 'set_all':
        color = command['color']
        for pix in range(pixels.n_pixels):
            pixel_colors[pix] = color
        pixels.current_cmd = partial(set_colors, colors=pixel_colors)

    elif cmd == 'set':
        colors = command['colors']
        for pix, color in enumerate(colors):
            pixel_colors[pix] = color
        pixels.current_cmd = partial(set_colors, colors=pixel_colors)

    elif cmd == 'get':
        return {"status": "ok", "on": pixels.on, "colors": pixel_colors}

    else:
        return {"status": "error", "msg": f"Unknown command: {cmd}"}

    return {"status": "ok"}



def main():
    r = redis.StrictRedis()
    r.delete("commands")
    r.delete("response")

    with Pixels(board.D21, n_jewells=2) as pixels:
        pixels.current_cmd = partial(clock, period=1.0)
        pixels.start()

        try:
            print(f"Ready to accept commands on: {r}")
            while True:
                response = r.blpop("commands")
                if response:
                    _, data = response
                    try:
                        command = json.loads(data.decode('utf-8'))
                        print('Got:', command)
                        result = handle_cmd(command, pixels)
                        print('Resp: ', result)
                        r.rpush("response", json.dumps(result))
                    except Exception as err:
                        r.rpush("response", json.dumps({"status": "error", "msg": str(err)}))
                        print(f"Error handling cmd: {err}")
        except KeyboardInterrupt:
            print("Interrupted")
            pass




if __name__ == '__main__':
    main()
