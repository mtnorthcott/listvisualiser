import os.path
from PIL import Image, ImageDraw

COLOUR_WHITE = (255, 255, 255)
COLOUR_RED = (255, 0, 0)

class ArrayPlot(object):
    count_processed = 0
    count_set = 0
    count_get = 0
    array = None
    size = 0

    def __init__(self, path, items=None):
        if os.path.exists(path):
            self.path = path
        else:
            raise FileNotFoundError("Path must exist")

        if type(items) == list:
            self.array = items
            self.size = len(items)
            self.max = max(items)
        else:
            raise TypeError("Parameter must be a list")

    def swap(self, i, j):
        self._record([i, j])
        self.array[i], self.array[j] = self.array[j], self.array[i]
        self._record([i, j])

    def _record(self, highlight):
        img = Image.new(mode="RGB", size=(self.size, self.size))
        draw = ImageDraw.Draw(img)

        for i, value in enumerate(self.array):
            c = COLOUR_RED if i in highlight else COLOUR_WHITE
            h = round(self.size * value / self.max)
            draw.line([(i, self.size - 1), (i, self.size - h)], c, 1)
        
        img.save(os.path.join(self.path, "{num}.jpg".format(num=self.count_processed)))
        self.count_processed += 1
    
    def __contains__(self, item):
        return item in self.array

    def __getitem__(self, index):
        self.count_get += 1
        self._record([index])
        return self.array.__getitem__(index)
    
    def __iter__(self):
        for item in self.array:
            yield item
    
    def __len__(self):
        return self.size

    def __repr__(self):
        return repr(self.array)
    
    def __setitem__(self, index, value):
        self.count_set += 1
        self._record([index])
        self.array.__setitem__(index, value)

    def __sizeof__(self):
        return self.frames.__sizeof__() + self.array.__sizeof__() + 16
    
    def __str__(self):
        return str(self.array)

if __name__ == "__main__":
    arr = list(range(1,65))
    a = ArrayPlot(r"C:\Programming\listplot\out", items=arr)
    print(a)
    a[0], a[3] = a[3], a[0]
    print(a)
