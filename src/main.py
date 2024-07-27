from module import Game, Role, load_game_data

game = Game(*load_game_data("data.json"))
game.fill_hands()

print(game.players[Role.DEFENSE])
print(game.players[Role.OFFENSE])
print("".join(str(d) for d in game.districts))
