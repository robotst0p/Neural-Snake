class input:
    def __init__(self, key):
        self.key = key
        self.direction = ""

    def direction_update(self, key):
        if key == "left":
            self.direction = "left"
        elif key == "right":
            self.direction = "right"
        elif key == "up":
            self.direction = "up"
        elif key == "down":
            self.direction = "down" 
        else:
            self.direction = ""