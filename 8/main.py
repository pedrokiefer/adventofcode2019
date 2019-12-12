
def decode_stream(stream, width, height):
    img = []
    while stream != "":
        layer = []
        for i in range(height):
            layer.extend([int(x) for x in stream[:width]])
            stream = stream[width:]
        img.append(layer)
    return img

def render_img(img, width, height):
    render = [[None for i in range(width)] for j in range(height)]
    for l in img:
        print(render)
        print(l)
        for i in range(height):
            for j in range(width):
                v = l[i * width + j]
                print(v, i, j)
                if v != 2 and render[i][j] == None:
                    render[i][j] = v
    print(render)
    return "\n".join(["".join(["■" if x == 0 else "□" for x in l]) for l in render])


def count_zeros(img):
    zeros = []
    for i, l in enumerate(img):
        zeros.append(l.count(0))
    _max = min(zeros)
    print(_max)
    return zeros.index(_max)

def calc(img, layer):
    _one = img[layer].count(1)
    _two = img[layer].count(2)
    return _one * _two

def main():
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()
    img = decode_stream(data, 25, 6)
    least_zeros_layer = count_zeros(img)
    print(calc(img, least_zeros_layer))
    print(render_img(img, 25, 6))

if __name__ == "__main__":
    main()


