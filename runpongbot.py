import pongbot
import time
import sys


if __name__ == '__main__':

    nbots = 16
    if len(sys.argv) > 1:
        nbots = int(sys.argv[1])

    print 'starting %d bots...' % nbots
    bots = [pongbot.PongBot() for c in xrange(nbots)]

    for bot in bots:
        bot.start()
        time.sleep(1.0)

    while True:
        time.sleep(10)
        print '---------------'
        for bot in bots:
            bot.printStats()
