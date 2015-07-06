__author__ = 'umqra'
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


class LightImpulse:
    def __init__(self, value=0.0, fading=0.95, speed=600):
        self.value = value
        self.fading = fading
        self.speed = speed


class Lighting:
    max_value = 255

    def __init__(self, value=0, light_impulse=None):
        self.value = value
        self.light_impulse = light_impulse if light_impulse is not None else LightImpulse()

    def emit(self, dt):
        quantum = min(self.light_impulse.value, self.light_impulse.speed * dt)
        self.light_impulse.value -= quantum
        self.value += quantum
        self.value = min(self.value, Lighting.max_value)
        return quantum * self.light_impulse.fading

    def add_impulse(self, impulse):
        self.light_impulse.value += impulse.value
        self.light_impulse.fading = max(self.light_impulse.fading, impulse.fading)
        self.light_impulse.speed = min(self.light_impulse.speed, impulse.speed)

    def change_to_value(self, value, dt):
        delta = value - self.value
        self.value += delta * dt