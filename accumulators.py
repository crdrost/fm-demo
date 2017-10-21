
class Accumulator:
    def run(self, stream):
        for item in stream:
            self.update(item)
        return self.digest()

