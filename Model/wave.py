__author__ = 'umqra'
import random


class Wave:
    def __init__(self, state, start_time, warriors, gates):
        self.state = state
        self.start_time = start_time
        self.warriors = warriors
        self.gates = gates

    def empty(self):
        return len(self.warriors) == 0

    def tick(self, dt):
        if self.state.time >= self.start_time:
            self.run_warriors()

    def run_warriors(self):
        random.shuffle(self.warriors)
        random.shuffle(self.gates)

        for gate in self.gates:
            for creator in self.warriors:
                warrior = creator(gate)
                if self.state.map.can_put_item(warrior):
                    self.state.map.add_warrior(warrior)
                    self.warriors.remove(creator)
                    return



