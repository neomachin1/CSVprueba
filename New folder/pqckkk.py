import struct
import time
 
def writedata(filename, data):
    '''Write data to a file with a header'''
    count = len(data)
    stime = int(time.time())
    with open(filename, "wb") as file:
        buffer = struct.pack('=IBBHiII', 460, 0, 30, 1, stime, 10, count)
        file.write(buffer)
        buffer = struct.pack(f'={count}i', *data)
        file.write(buffer)
 
def readdata(filename):
    '''Read data from a file.  Data count is in the header'''
    with open(filename, "rb") as file:
        buffer = file.read(20)
        size, vtype, x, index, stime, srate, count = struct.unpack('=IBBHIII', buffer)
        print(size, x, index, stime, srate, count)
 
        buffer = file.read(4 * count)
        values = struct.unpack(f'={count}I', buffer)
        return values
 
writedata('junk.bin', [1, 1, 2, 3, 5, 8, 13])
print(readdata('junk.bin'))