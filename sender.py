from threading import Thread
import time


class Colors:
    ENDC = "\033[0m"

    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @staticmethod
    def cprint(colors, *args, **kwargs):
        print(colors, end="")
        print(*args, end="")
        print(Colors.ENDC, end="")
        print(**kwargs)

    @staticmethod
    def print_sender(action, *args, **kwargs):
        Colors.cprint(Colors.OKBLUE + Colors.BOLD, "Sender:", end=" ")
        Colors.cprint(Colors.OKBLUE + Colors.UNDERLINE, action, end=" ")
        print(*args, **kwargs)

    @staticmethod
    def print_reciver(action, *args, **kwargs):
        Colors.cprint(Colors.OKGREEN + Colors.BOLD, "Reciver:", end=" ")
        Colors.cprint(Colors.OKGREEN + Colors.UNDERLINE, action, end=" ")
        print(*args, **kwargs)

    @staticmethod
    def print_network(action, *args, **kwargs):
        Colors.cprint(Colors.FAIL + Colors.BOLD, "Network_layer:", end=" ")
        Colors.cprint(Colors.FAIL + Colors.UNDERLINE, action, end=" ")
        print(Colors.FAIL, *args, **kwargs)


class SenderProcess:
    """Represent the sender process in the application layer"""

    __buffer: list[str] = list()

    @staticmethod
    def set_outgoing_data(buffer):
        """To set the message the process would send out over the network
        :param buffer:  a python list of characters represent the outgoing message
        :return: no return value
        """
        SenderProcess.__buffer = buffer
        return

    @staticmethod
    def get_outgoing_data():
        """To get the message the process would send out over the network
        :return:  a python list of characters represent the outgoing message
        """
        return SenderProcess.__buffer


class RDTSender:
    """Implement the Reliable Data Transfer Protocol V2.2 Sender Side"""

    def __init__(self, net_srv):
        """This is a class constructor
        It initialize the RDT sender sequence number  to '0' and the network layer services
        The network layer service provide the method udt_send(send_pkt)
        """
        self.sequence = "0"
        self.net_srv = net_srv
        self.timeout = net_srv.delay * 2

    @staticmethod
    def get_checksum(data):
        """Calculate the checksum for outgoing data
        :param data: one and only one character, for example data = 'A'
        :return: the ASCII code of the character, for example ASCII('A') = 65
        """
        return ord(data)

    @staticmethod
    def clone_packet(packet):
        """Make a copy of the outgoing packet
        :param packet: a python dictionary represent a packet
        :return: return a packet as python dictionary
        """
        pkt_clone = {
            "sequence_number": packet["sequence_number"],
            "data": packet["data"],
            "checksum": packet["checksum"],
        }
        return pkt_clone

    @staticmethod
    def is_corrupted(reply):
        """Check if the received reply from receiver is corrupted or not
        :param reply: a python dictionary represent a reply sent by the receiver
        :return: True -> if the reply is corrupted | False ->  if the reply is NOT corrupted
        """

        return reply["checksum"] != ord(reply["ack"])

    @staticmethod
    def is_expected_seq(reply, exp_seq):
        """Check if the received reply from receiver has the expected sequence number
        :param reply: a python dictionary represent a reply sent by the receiver
        :param exp_seq: the sender expected sequence number '0' or '1' represented as a character
        :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        return reply["ack"] == exp_seq

    @staticmethod
    def make_pkt(seq, data, checksum):
        """Create an outgoing packet as a python dictionary
        :param seq: a character represent the sequence number of the packet, the one expected by the receiver '0' or '1'
        :param data: a single character the sender want to send to the receiver
        :param checksum: the checksum of the data the sender will send to the receiver
        :return: a python dictionary represent the packet to be sent
        """
        packet = {"sequence_number": seq, "data": data, "checksum": checksum}
        return packet

    def net_udt_send(self, pkt, reply):
        reply_ = self.net_srv.udt_send(pkt)
        for key in reply_:
            reply[key] = reply_[key]

    def rdt_send(self, process_buffer):
        """Implement the RDT v2.2 for the sender
        :param process_buffer:  a list storing the message the sender process wish to send to the receiver process
        :return: terminate without returning any value
        """

        # for every character in the buffer
        for data in process_buffer:
            checksum = RDTSender.get_checksum(data)
            pkt = RDTSender.make_pkt(self.sequence, data, checksum)

            while True:
                Colors.print_sender("expection_seq_num", self.sequence)
                Colors.print_sender("sending", pkt)

                pkt_clone = RDTSender.clone_packet(pkt)

                reply = {}
                thread = Thread(target=self.net_udt_send, args=(pkt_clone, reply))

                thread.start()
                old_time = time.time()

                while time.time() - old_time < self.timeout:
                    if reply != {}:
                        break

                thread.join()

                if reply == {}:  # timeout
                    Colors.print_sender("timeout")
                    continue
                else:
                    Colors.print_sender("received", reply)

                if not RDTSender.is_corrupted(reply) and RDTSender.is_expected_seq(
                    reply, self.sequence
                ):
                    break

            self.sequence = "0" if self.sequence == "1" else "1"

        print("Sender Done!")
