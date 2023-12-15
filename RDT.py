import Network
import argparse
import time
from time import sleep
import hashlib

debug = True    
# default = False


def debug_log(message):
    if debug:
        print(message)


class Packet:
    # packet = [size, seq_num, checksum, data ]

    # the number of bytes(chars) used to store the size of the packet
    size_len = 8

    # the number of bytes(chars) used to store sequence number
    seq_num_len = 8
    
    # the number of bytes(chars) of md5 checksum in hex
    checksum_len = 32

    # Receive packet format settings at initialization
    def __init__(self, size_len=8, seq_num_len=8, checksum_len=32):
        self.size_len = size_len
        self.seq_num_len = seq_num_len
        self.checksum_len = checksum_len


    def code(self, seq_num, msg):

        # create size (int and str)
        self.size = self.size_len + self.seq_num_len + self.checksum_len + len(msg)
        self.size_str = str(self.size).zfill(self.size_len)

        # create seq_num (int and str)
        self.seq_num = seq_num
        self.seq_num_str = str(seq_num).zfill(self.seq_num_len)

        # compute the checksum (str)
        self.checksum = hashlib.md5((self.size_str + self.seq_num_str + msg).encode('utf-8')).hexdigest()

        # save message (str)
        self.msg = msg

        # compile into a string
        self.packet = self.size_str + self.seq_num_str + self.checksum_str + self.msg

        return self.packet
    

    def split(self, packet):

        # split packet into respective variables
        limits = [self.size_len, self.size_len+self.seq_num_len, self.size_len+self.seq_num_len+self.checksum_len]
        
        size_str = packet[0 : limits[0]]
        seq_num_str = packet[limits[0] : limits[1]]
        checksum = packet[limits[0] : limits[0]]
        msg = packet[limits[0] : ]

        return size_str, seq_num_str, checksum, msg


    def corrupt(self, packet):

        # extract the fields
        size_str, seq_num_str, checksum, msg = Packet.split(packet)

        # compute the checksum locally
        computed = hashlib.md5(str(size_str + seq_num_str + msg).encode('utf-8')).hexdigest()

        # and check if they are the same
        return checksum != computed


    def decode(self, packet):

        if Packet.corrupt(packet):
            raise RuntimeError('Cannot extract packet: it is corrupted')

        # extract the fields
        size_str, seq_num_str, checksum, msg = Packet.split(packet)
        
        # save into object variables
        self.size = int(size_str)
        self.size_str = size_str

        self.seq_num = int(seq_num_str)
        self.seq_num_str = seq_num_str

        self.checksum = checksum

        self.msg = msg

        self.packet = packet

        # split packet into its components
        return size_str, seq_num_str, checksum, msg
    
    
    def get_ack(self):
        # when ACK is sent, it is formated as ACK.XX, XX = seq_num
        if "ACK" in self.msg:
            return int(self.msg[3:])
        
        return -1


class RDT:
    # latest sequence number used in a packet
    seq_num = 0
    # buffer of bytes read from network
    byte_buffer = ''
    timeout = 3

    def __init__(self, role_S, server_S, port):
        self.network = Network.NetworkLayer(role_S, server_S, port)

    def disconnect(self):
        self.network.disconnect()

    def rdt_3_0_send(self, msg_S):
        pass

    def rdt_3_0_receive(self):
        pass


if __name__ == '__main__':
    p = Packet(20, "teste")
    print (p.get_packet())

        
