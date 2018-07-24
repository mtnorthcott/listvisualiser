import os.path
from random import shuffle
from PIL import Image, ImageDraw

COLOUR_WHITE = (255, 255, 255)
COLOUR_RED = (255, 0, 0)

class BytesWrapper(bytearray):
    def write(self, data):
        self.extend(data)

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
        else:
            raise TypeError("Parameter must be a list")

    def swap(self, i, j):
        self._record([i, j])
        self.array[i], self.array[j] = self.array[j], self.array[i]
        self._record([i, j])

    def _record(self, highlight=[]):
        img = Image.new(mode="RGB", size=(self.size, self.size))
        draw = ImageDraw.Draw(img)

        for i, value in enumerate(self.array):
            c = COLOUR_RED if i in highlight else COLOUR_WHITE
            h = round(self.size * value / max(self.array))
            draw.line([(i, self.size - 1), (i, self.size - h)], c, 1)
        
        img_bytes = BytesWrapper()
        img.save(img_bytes, format="JPEG")

        # TODO handle img bytes

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
    
    def __str__(self):
        return str(self.array)

if __name__ == "__main__":
    arr = list(range(1,65))
    shuffle(arr)
    a = ArrayPlot(r"C:\Programming\listvisualiser\in", items=arr)
    
    from algorithms import selection_sort
    selection_sort.sort(a, 0, len(a))
