import asyncio
from diplomacy.client.connection import connect


class Bot():

    def __init__(self, ip_address, port, name, power_name):
        self._network_port = port
        self._network_ip_address = ip_address
        self.name = name
        self.power_name = power_name
    
    async def play(self):
        connection = await connect(self._network_ip_address, self._network_port)
        channel = await connection.authenticate(self.name, 'password')

        while True:
            data_game_infos = await channel.list_games()
            if not data_game_infos:
                await asyncio.sleep(1.)
            else:
                break
        
        game_id = data_game_infos[0].game_id
        game = await channel.join_game(game_id=game_id, power_name=self.power_name)

        # Playing game
        while not game.is_game_done:
            current_phase = game.get_current_phase()
            if game.get_orderable_locations(self.power_name):
                # Virtual function call (should be implemented in child classes):
                orders = self.get_orders(game, self.power_name)
                print('[%s/%s] - Submitted: %s' % (self.power_name, game.get_current_phase(), orders))
                await game.set_orders(power_name=self.power_name, orders=orders, wait=False)
            # Waiting for game to be processed
            while current_phase == game.get_current_phase():
                await asyncio.sleep(0.1)
