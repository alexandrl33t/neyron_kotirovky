import numpy_da as np_da


def get_vector():
    vector = np_da.DynamicArray(shape=2, index_expansion=True)
    with open("GAZP_180901_220915.txt", 'r') as file:
        new = file.readlines()
        del new[0]
        for line in new:
            zap = line.rfind(",")
            line = line[:zap]
            zap = line.rfind(",")
            line = line[:zap]
            zap = line.rfind(",")
            line = line[zap + 1:]
            vector.append(float(line))
    return vector