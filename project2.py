import random
suits=("hearts","diamond","spades","clubs")
ranks=("two","three","four","five","six","seven","eight","nine","ten","jack","queen","king")
values={"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"jack":10,"queen":10,"king":10,"ace":11}

playing= True

class card:
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
    def __str__(self):
        return self.rank+" of "+self.suit

class Deck:
    def __init__(self):
        self.deck=[] #start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(card(suit,rank))  #build card objects and add them to the list

    def __str__(self):
        deck_comp=""              #start with an empty string
        for card in self.deck:
            deck_comp += "\n" + card.__str__() #add each card objects print string
        return "the deck has: "+deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card=self.deck.pop()
        return single_card

class hand:
    def __init__(self):
        self.cards=[]
        self.value=0
        self.aces=0

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "ace":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces >0:
            self.value -= 10
            self.aces -= 1

class chips:
    def __init__(self,total=100):
        self.total=total
        self.bet=0

    def win_bet(self):
        self.total+=self.bet

    def lost_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet=int(input("how many chips would you like to bet? "))
        except:
            print("sorry please provide an integer")
        else:
            if chips.bet > chips.total:
                print("sorry, you do nat have enough chips! you have: {}".format(chips.total))
            else:
                break

def hit(deck,hand):
    single_card=deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing
    while True:
        x=input("hit or stand? enter 'h' or 's'")
        if x[0].lower()=="h":
            hit(deck,hand)
        elif x[0].lower()=="s":
            print("player stands Dealer's Turn")
            playing=False
        else:
            print("sorry, i did no understand that, please enter h or s only!")
            continue
        break

def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')

def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)

def player_busts(player,dealer,chips):
    print("BUST PLAYER!")
    chips.lost_bet()

def player_wins(player,dealer,chips):
    print("PLAYER WINS!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("PLAYER WINS! DEALER BUSTED!")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("DEALER WINS!")
    chips.lost_bet()

def push(player,dealer):
    print("Dealer and player tie! PUSH")

while True:
    print("WELCOME TO BLACK JACK")
    deck=Deck()
    deck.shuffle()

    player_hand=hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_chips=chips()
    take_bet(player_chips)
    show_some(player_hand,dealer_hand)

    while playing:
        hit_or_stand(deck,player_hand)
        show_some(player_hand,dealer_hand)
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    if player_hand.value <= 21:
        while dealer_hand.value < player_hand.value:
            hit(deck, dealer_hand)

        show_all(player_hand,dealer_hand)
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand)

    print("\n player total chips are at: {}".format(player_chips.total))
    new_game=input("would you like to play another hand? y/n")

    if new_game[0].lower()=="y":
        playing=True
        continue
    else:
        print("thank you for playing!")
        break

test_deck=Deck()
test_deck.shuffle()
test_player=hand()
pulled_card = test_deck.deal()
print(pulled_card)
test_player.add_card(pulled_card)
print(test_player.value)








