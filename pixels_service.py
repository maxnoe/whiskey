"""
Long running process running as root receiving commands from a redis queue
"""
import redis
import board
import neopixel
import time
import math
from threading import Thread, Event
import json
from functools import partial

PIN = board.D21

OFF = (0, 0, 0)
RED = (0xff, 0, 0)
GREEN = (0, 0xff, 0)
BLUE = (0, 0, 0xff)

N_PIX_JEWELL = 7


class Pixels(Thread):
    def __init__(self, n_jewells, interval=0.001):
        super().__init__()

        self.stop_event = Event()

        self.n_pixels = N_PIX_JEWELL * n_jewells
        self.pixels = neopixel.NeoPixel(
            PIN,
            self.n_pixels,
            auto_write=False,
            brightness=1.0,
        )
        all_off(self.pixels)
        self.current_cmd = None
        self.interval = interval

    def run(self):
        while not self.stop_event.is_set():
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
    
    c = int(255 * c)
    x = int(255 * x)

    if h < 1:
        rgb = (c, x, 0)
    elif h < 2:
        rgb = (x, c, 0)
    elif h < 3:
        rgb = (0, c, x)
    elif h < 4:
        rgb = (0, x, c)
    elif h < 5:
        rgb = (x, 0, c)
    else:
        rgb = (c, 0, x)

    return rgb


def all_off(pixels):
    pixels.fill(OFF)
    pixels.show()


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

    if cmd == "off":
        all_off(pixels.pixels)
        pixels.current_cmd = None

    elif cmd == "rainbow":
        period = command.get("period", 1.0)
        pixels.current_cmd = partial(rainbow, period=period)

    elif cmd == "sine":
        period = command.get("period", 1.0)
        basecolor = command.get("color", [64, 64, 64])
        pixels.current_cmd = partial(sine_wave, period=period, basecolor=basecolor)

    elif cmd == 'none':
        pixels.current_cmd = None

    elif cmd == 'set_pix':
        pixels.current_cmd = None
        pix = command['pix']
        color = command['color']
        pixels.pixels[pix] = color

    elif cmd == 'set_all':
        pixels.current_cmd = None
        color = command['color']
        pixels.pixels.fill(color)

    elif cmd == 'set':
        pixels.current_cmd = None
        colors = command['colors']
        for pix, color in enumerate(colors):
            pixels.pixels[pix] = color

    else:
        print("Unknown command:", cmd)



def main():
    r = redis.StrictRedis()

    with Pixels(n_jewells=2) as pixels:
        pixels.current_cmd = partial(clock, period=1.0)
        pixels.start()

        try:
            while True:
                response = r.blpop("commands")
                if response:
                    _, data = response
                    try:
                        command = json.loads(data.decode('utf-8'))
                        handle_cmd(command, pixels)
                    except Exception as err:
                        print(f"Error handling cmd: {err}")
        except KeyboardInterrupt:
            pass




if __name__ == '__main__':
    main()
