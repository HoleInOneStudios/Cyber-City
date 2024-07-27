from module.game import Game, Role, load_game_data

game = Game(*load_game_data("data.json"))
game.fill_hands()

print(game.players[Role.OFFENSE])
print(game.players[Role.DEFENSE])
print(", ".join(str(district) for district in game.districts))
