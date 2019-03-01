vertical = 'v'
horizontal = 'h'

class Grouping():
    def __init__(self):
        self.group = []

class Image():
    def __init__(self, id, tags, orientation):
        self.id = id
        self.tags = tags
        self.orientation = orientation

        if len(tags) >= 1 or (len(tags)) <= 100: pass
        else: print("Check amount of tags")

        def get_tags():
            return tags

        def __repr__(self):
            return "({0}, {1}, {2}, {3})".format(self.id, self.orientation, self.num_tags, self.tags.split())