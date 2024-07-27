from module import *

game = Game(*load_game_data("data.json"))
game.fill_hands()

print(game.players[Role.OFFENSE])
print(game.players[Role.DEFENSE])
print("\n".join(map(str, game.districts)))
