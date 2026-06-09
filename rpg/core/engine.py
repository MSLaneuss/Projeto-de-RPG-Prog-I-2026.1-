"""Loop principal do jogo e estados."""

from utils.helpers import clear_screen


class GameEngine:
    def __init__(self):
        self.state = "menu"

    def run(self):
        while True:
            clear_screen()
            if self.state == "menu":
                self.show_menu()
            elif self.state == "playing":
                self.play()
            elif self.state == "game_over":
                self.game_over()
                break
            else:
                break

    def show_menu(self):
        print("Bem-vindo ao RPG!")
        print("1. Iniciar jogo")
        print("2. Sair")
        choice = input("Escolha: ")
        if choice == "1":
            self.state = "playing"
        else:
            self.state = "game_over"

    def play(self):
        print("Jogo em progresso...")
        input("Pressione Enter para encerrar o jogo.")
        self.state = "game_over"

    def game_over(self):
        print("Fim de jogo. Obrigado por jogar!")
