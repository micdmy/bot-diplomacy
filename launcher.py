import asyncio
import argparse
from diplomacy.utils import constants

def launch(bot_class):
    name = str(bot_class) 
    PARSER = argparse.ArgumentParser(description="Run bots \'%s\' for diplomacy game." % name)
    PARSER.add_argument('--powers', '-P', type=str, nargs='+',
                        help='powers (nations) i.e. ENGLAND')
    PARSER.add_argument('--name', '-n', type=str, default=name,
                        help='arbitrary name(default: %s)' % name)
    PARSER.add_argument('--ip-address', '-a', type=str, default=constants.DEFAULT_HOST,
                        help='IP of server (default: %s)' % constants.DEFAULT_HOST)
    PARSER.add_argument('--port', '-p', type=int, default=constants.DEFAULT_PORT,
                        help='port of server (default: %s)' % constants.DEFAULT_PORT)
    ARGS = PARSER.parse_args()

    bots = [bot_class(power_name = p, name = ARGS.name + '_' + p, ip_address = ARGS.ip_address, port = ARGS.port) for p in ARGS.powers]

    try:
        asyncio.run(_play_bots(bots))
    except KeyboardInterrupt:
        print("Kyboard interruption")

async def _play_bots(bots):
    await asyncio.gather(*[bot.play() for bot in bots])