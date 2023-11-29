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


class ReceiverProcess:
    """Represent the receiver process in the application layer"""

    __buffer = list()

    @staticmethod
    def deliver_data(data):
        """deliver data from the transport layer RDT receiver to the application layer
        :param data: a character received by the RDT RDT receiver
        :return: no return value
        """
        ReceiverProcess.__buffer.append(data)
        return

    @staticmethod
    def get_buffer():
        """To get the message the process received over the network
        :return:  a python list of characters represent the incoming message
        """
        return "".join(ReceiverProcess.__buffer)


class RDTReceiver:
    """ " Implement the Reliable Data Transfer Protocol V2.2 Receiver Side"""

    def __init__(self):
        self.sequence = "0"

    @staticmethod
    def is_corrupted(packet):
        """Check if the received packet from sender is corrupted or not
        :param packet: a python dictionary represent a packet received from the sender
        :return: True -> if the reply is corrupted | False ->  if the reply is NOT corrupted
        """
        return packet["checksum"] != ord(packet["data"])

    @staticmethod
    def is_expected_seq(rcv_pkt, exp_seq):
        """Check if the received reply from receiver has the expected sequence number
        :param rcv_pkt: a python dictionary represent a packet received by the receiver
        :param exp_seq: the receiver expected sequence number '0' or '1' represented as a character
        :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        return rcv_pkt["sequence_number"] == exp_seq

    @staticmethod
    def make_reply_pkt(seq, checksum):
        """Create a reply (feedback) packet with to acknowledge the received packet
        :param seq: the sequence number '0' or '1' to be acknowledged
        :param checksum: the checksum of the ack the receiver will send to the sender
        :return:  a python dictionary represent a reply (acknowledgement)  packet
        """
        reply_pck = {"ack": seq, "checksum": checksum}
        return reply_pck

    def rdt_rcv(self, rcv_pkt) -> dict[str, str]:
        """Implement the RDT v2.2 for the receiver
        :param rcv_pkt: a packet delivered by the network layer 'udt_send()' to the receiver
        :return: the reply packet
        """

        Colors.print_reciver("expecting_seq_num", self.sequence)

        if RDTReceiver.is_corrupted(rcv_pkt) or not RDTReceiver.is_expected_seq(
            rcv_pkt, self.sequence
        ):
            last_seq = "0" if self.sequence == "1" else "1"
            reply_pkt = RDTReceiver.make_reply_pkt(last_seq, ord(last_seq))

            Colors.print_reciver("reply with", reply_pkt)

            return reply_pkt

        # deliver the data to the process in the application layer
        ReceiverProcess.deliver_data(rcv_pkt["data"])

        reply_pkt = RDTReceiver.make_reply_pkt(self.sequence, ord(self.sequence))

        self.sequence = "0" if self.sequence == "1" else "1"

        Colors.print_reciver("reply with", reply_pkt)

        return reply_pkt
