from random import randint
import Player
import Board

class Chess():
    def whatColor(self):
        return randint(0, 9)

    def newgame(self):
        m = Chess()
        print (""" "Welcome, please enter your names in order to start the game and press the enter key. """)
        player1, player2 = m.getPlayers()
        player1.setOpp(player2)
        player2.setOpp(player1)
        game = Board.Board(player1, player2)
        menu = """

        Player 1: {} - Will use uppercase lettering
        Player 2: {} - Will use lowercase lettering
        (Move format is 'a2b3'. Type 'exit' to quit the game.""".format(player1.name, player2.name, player1, player2)
        print (menu)
        input("\n\nHit the Enter button to play")
        randNum = m.whatColor()
        if (randNum == 0):
            player = player1
        else:
            player = player2
        try:
            result, player = game.run(player)
        except TypeError:
            pass
        else:
            print (game.end(player, result))
            input("\n\nPress any key to continue")

    def getPlayers(self):
        loop1 = True
        loop2 = True
        while loop1:
            name1 = input("\nPlayer 1 (white): ")
            if not name1:
                print ("Try again")
            else:
                player1 = Player.Player('white', name1)
                loop1 = False
        while loop2:
            name2 = input("\nPlayer 2 (black): ")
            if not name2:
                print ("Try again")
            else:
                player2 = Player.Player('black', name2)
                loop2 = False
        return player1, player2

    def chess(self):
        m = Chess()
        endGame="""To play again press enter. To quit type 'exit' >>  """
        try:
            while True:
                m.newgame()
                choice=input(endGame)
                if choice == 'exit':
                    print ("\nNew Chess Game!")
                    break
        except KeyboardInterrupt:
            sys.exit("\n\nErrorl. Abort.")
m = Chess()
m.chess()