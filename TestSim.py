#ANDES Lab - University of California, Merced
#Author: UCM ANDES Lab
#$Author: abeltran2 $
#$LastChangedDate: 2014-08-31 16:06:26 -0700 (Sun, 31 Aug 2014) $
#! /usr/bin/python
import sys
from TOSSIM import *
from CommandMsg import *

class TestSim:
    moteids=[]
    # COMMAND TYPES
    CMD_PING = 0
    CMD_NEIGHBOR_DUMP=1
    CMD_ROUTE_DUMP=3
    CMD_TEST_CLIENT=4
    CMD_TEST_SERVER=5
    CMD_START_CHAT_SERVER=10
    CMD_MSG=11
    CMD_HELLO=12
    CMD_WHISPER=13
    CMD_LIST_USERS=14

    # CHANNELS - see includes/channels.h
    COMMAND_CHANNEL="command";
    GENERAL_CHANNEL="general";

    # Project 1
    NEIGHBOR_CHANNEL="neighbor";
    FLOODING_CHANNEL="flooding";

    # Project 2
    ROUTING_CHANNEL="routing";

    # Project 3
    TRANSPORT_CHANNEL="transport";

    # Personal Debuggin Channels for some of the additional models implemented.
    HASHMAP_CHANNEL="hashmap";

    # Initialize Vars
    numMote=0

    def __init__(self):
        self.t = Tossim([])
        self.r = self.t.radio()

        #Create a Command Packet
        self.msg = CommandMsg()
        self.pkt = self.t.newPacket()
        self.pkt.setType(self.msg.get_amType())

    # Load a topo file and use it.
    def loadTopo(self, topoFile):
        print ("Creating Topo!")
        # Read topology file.
        topoFile = 'topo/'+topoFile
        f = open(topoFile, "r")
        self.numMote = int(f.readline());
        print ('Number of Motes', self.numMote)
        for line in f:
            s = line.split()
            if s:
                print (" ", s[0], " ", s[1], " ", s[2]);
                self.r.add(int(s[0]), int(s[1]), float(s[2]))
                if not int(s[0]) in self.moteids:
                    self.moteids=self.moteids+[int(s[0])]
                if not int(s[1]) in self.moteids:
                    self.moteids=self.moteids+[int(s[1])]

    # Load a noise file and apply it.
    def loadNoise(self, noiseFile):
        if self.numMote == 0:
            print ("Create a topo first")
            return;

        # Get and Create a Noise Model
        noiseFile = 'noise/'+noiseFile;
        noise = open(noiseFile, "r")
        for line in noise:
            str1 = line.strip()
            if str1:
                val = int(str1)
            for i in self.moteids:
                self.t.getNode(i).addNoiseTraceReading(val)

        for i in self.moteids:
            print ("Creating noise model for {}".format(i))
            self.t.getNode(i).createNoiseModel()

    def bootNode(self, nodeID):
        if self.numMote == 0:
            print ("Create a topo first")
            return;
        self.t.getNode(nodeID).bootAtTime(1333*nodeID);

    def bootAll(self):
        i=0;
        for i in self.moteids:
            self.bootNode(i);

    def moteOff(self, nodeID):
        self.t.getNode(nodeID).turnOff();

    def moteOn(self, nodeID):
        self.t.getNode(nodeID).turnOn();

    def run(self, ticks):
        for i in range(ticks):
            self.t.runNextEvent()

    # Rough run time. tickPerSecond does not work.
    def runTime(self, amount):
        self.run(amount*1000)

    # Generic Command
    def sendCMD(self, ID, dest, payloadStr):
        self.msg.set_dest(dest);
        self.msg.set_id(ID);
        self.msg.setString_payload(payloadStr)

        self.pkt.setData(self.msg.data)
        self.pkt.setDestination(dest)
        self.pkt.deliver(dest, self.t.time()+5)

    def ping(self, source, dest, msg):
        self.sendCMD(self.CMD_PING, source, "{0}{1}".format(chr(dest),msg));

    def neighborDMP(self, destination):
        self.sendCMD(self.CMD_NEIGHBOR_DUMP, destination, "neighbor command");

    def routeDMP(self, destination):
        self.sendCMD(self.CMD_ROUTE_DUMP, destination, "routing command");

    def setTestClient(self, source, destination, sourcePort, destinationPort, msg):
        self.sendCMD(self.CMD_TEST_CLIENT, source, "{0}{1}{2}{3}".format(chr(destination),chr(sourcePort),chr(destinationPort),msg));

    def setTestServer(self, source, port):
        self.sendCMD(self.CMD_TEST_SERVER, source, "{0}".format(chr(port)))

    def startChatServer(self, source):
        self.sendCMD(self.CMD_START_CHAT_SERVER, source, "chat server")

    def hello(self, source, username, port):
        self.sendCMD(self.CMD_HELLO, source, "{0}{1}".format(username, chr(port)))

    def msg(self, source, message):
        self.sendCMD(self.CMD_MSG, source, "{0}".format(message))

    def whisper(self, source, username, message):
        self.sendCMD(self.CMD_WHISPER, source, "{0}{1}".format(username, message))


    def addChannel(self, channelName, out=sys.stdout):
        print ('Adding Channel', channelName);
        self.t.addChannel(channelName, out);

def main():
    s = TestSim();
    s.runTime(10);
    # s.loadTopo("long_line.topo");
    s.loadTopo("example.topo");
    s.loadNoise("no_noise.txt");
    s.bootAll();
    s.addChannel(s.COMMAND_CHANNEL);
    s.addChannel(s.GENERAL_CHANNEL);
    # s.addChannel(s.FLOODING_CHANNEL);
    s.addChannel(s.NEIGHBOR_CHANNEL);
    # s.addChannel(s.ROUTING_CHANNEL);
    s.addChannel(s.TRANSPORT_CHANNEL);

    #Flooding Test
    # s.runTime(1);
    # s.ping(2, 3, "Hello, World");
    # s.runTime(1);

    # s.ping(1, 10, "Hi!");
    # s.runTime(1);
    
    # Neighbor Discovery Test
    # for i in range(1, 10):
    #     s.runTime(10);
    #     s.neighborDMP(i);

    # s.runTime(5);

    # s.neighborDMP(5);
    # s.runTime(5);

    # s.moteOff(3);
    # s.runTime(15);

    # s.neighborDMP(5);
    # s.runTime(5);

    # LinkState Test
    # s.runTime(100);
    # for i in range(1, 10):
    #     s.routeDMP(i);
    #     s.runTime(5);

    # s.ping(2, 9, "Test");
    # s.runTime(5);
    
    # # Test routing with invalidated path
    # s.moteOff(3);
    # s.runTime(100);

    # s.routeDMP(9);
    # s.runTime(5);

    # s.ping(2, 9, "Test");
    # s.runTime(5);

    # Transport Test
    s.runTime(250);
    s.setTestServer(2,10); #port 20
    s.runTime(100);
    s.setTestClient(3, 2, 20, 21, 'ABC');
    s.runTime(500);
    

    # # Chat server Test
    # s.startChatServer(1);
    # s.runTime(100);
    # s.hello(5, 'joe', 42);
    # s.runTime(250);
    # s.whisper(5, 'joe', 'Hi Joe');
    # s.runTime(250);
    # s.msge(5, 'Hi Everyone!');
    # s.runTime(250);
    # s.listusr(1);
    # s.runTime(250);

if __name__ == '__main__':
    main()
