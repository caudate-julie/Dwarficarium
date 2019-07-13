import random


def generate_map(width, height, depth, seed):
    size = 1
    while size < width or size < height:
        size *= 2
    h = generate_height_map(size, seed)
    min_z = min(min(row[:width]) for row in h[:height])
    max_z = max(max(row[:width]) for row in h[:height])
    step = (max_z - min_z) / (depth / 2)
    # ave = sum(sum(row[:width]) for row in h[:height]) / (width * height)

    result = []
    for _ in range(depth // 2):
        result.append([])
        for _ in range(height):
            result[-1].append([])
            for _ in range(width):
                result[-1][-1].append('#')

    for k in range(depth // 2, depth):
        result.append([])
        for i in range(height):
            result[-1].append([])
            for j in range(width):
                if h[i][j] > min_z + step * (k - depth / 2):
                    result[-1][-1].append('#')
                else:
                    result[-1][-1].append('.')

    return result


def generate_height_map(size, seed):
    # Diamond-square algorithm
    assert (size & (size - 1)) == 0
    rnd = random.Random(seed)
    h = [[None] * size for _ in range(size)]

    h[0][0] = 0

    spread = size
    step = size
    while step > 1:
        step //= 2
        for i in range(0, size // step, 2):
            i0 = i * step
            i1 = (i + 2) * step % size
            i_mid = (i + 1) * step % size
            for j in range(0, size // step, 2):
                j0 = j * step
                j1 = (j + 2) * step % size
                j_mid = (j + 1) * step % size
                ave = (h[i0][j0] + h[i1][j0] + h[i0][j1] + h[i1][j1]) * 0.25
                assert h[i_mid][j_mid] is None
                h[i_mid][j_mid] = ave + (rnd.random() - 0.5) * spread
        spread *= 0.5**0.5
        for i in range(size // step):
            i0 = i * step
            i1 = (i + 2) * step % size
            i_mid = (i + 1) * step % size
            for j in range(size // step):
                if (i + j) % 2 == 0:
                    continue
                j0 = j * step
                j1 = (j + 2) * step % size
                j_mid = (j + 1) * step % size
                ave = (h[i0][j_mid] + h[i1][j_mid] + h[i_mid][j0] + h[i_mid][j1]) * 0.25
                assert h[i_mid][j_mid] is None
                h[i_mid][j_mid] = ave + (rnd.random() - 0.5) * spread
        spread *= 0.5**0.5

    return h


def main():
    seed = random.randrange(10**6)
    print('seed:', seed)
    h = generate_height_map(32, seed)
    a = min(map(min, h))
    b = max(map(max, h))
    for row in h:
        print(' '.join(str(int((x - a) / (b - a + 1e-6) * 10)) for x in row))


if __name__ == '__main__':
    main()
