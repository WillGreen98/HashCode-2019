class Submission:
    def __init__(self, slideshow):
        self.slideshow = slideshow

    def submit(self, filename):
        file = open(filename, "w")
        file.write(str(len(self.slideshow + "\n")))
        for slides in self.slideshow:
            for value in slides.id:
                file.write(str(value), end=" ")
            file.write("\n")