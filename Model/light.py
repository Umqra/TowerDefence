__author__ = 'umqra'


class LightImpulse:
    def __init__(self, value=0, fading=0.5, speed=0.1):
        self.value = value
        self.fading = fading
        self.speed = speed


class Lighting:
    def __init__(self, value=0, light_impulse=LightImpulse()):
        self.value = value
        self.light_impulse = light_impulse

    def apply_impulse(self, other, dt):
        if self.light_impulse.value <= 0:
            return
        quantum = min(self.light_impulse.speed * dt, self.light_impulse.value)
        self.light_impulse.value -= quantum
        self.value += quantum
        other.light_impulse.value += quantum * self.light_impulse.fading

    def add_impulse(self, impulse):
        self.light_impulse.value += impulse.value
        self.light_impulse.fading = max(self.light_impulse.fading, impulse.fading)
        self.light_impulse.speed = min(self.light_impulse.speed, impulse.speed)

    def change_to_value(self, value, dt):
        delta = value - self.value
        value += delta * dt