import gi, time, random

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf


"""
TODO:
    blackjackin voi saada vain kahdella ensimmäisellä kortilla..
        blackjack voittaa 21:n
        
    deal_card ja reveal_card tekee samoja asioita -> joku uus funktio jossa yhteiset jutut?
    
    viive korttien välille, time.sleep ei toimi, animaatio? revealer?

    vihreä taustaväri, buttoneille joku väri/fontti/läpinäkyvyys?
"""



class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Blackjack")
        self.set_default_size(700,500)
        
        # Vertical box to contain other boxes
        self.box = Gtk.Box()
        self.box.set_orientation(1)
        self.add(self.box)
        
        # Box for dealers cards
        self.box_dealer = Gtk.Box(spacing = 20)
        self.box_dealer.set_orientation(0)    # vertical box = 1, horizontal is default or '0'
        self.box_dealer.set_margin_start(30)
        self.box_dealer.set_margin_end(30)
        self.box_dealer.set_margin_top(20)
        self.box_dealer.set_size_request(600, 150)
        
        # Label for text
        self.box_label = Gtk.Box()
        self.label = Gtk.Label()
        self.player_score = Gtk.Label()
        self.dealer_score = Gtk.Label()
        self.box_label.pack_start(self.player_score, True, True, 0)
        self.box_label.pack_start(self.label, True, True, 0)
        self.box_label.pack_start(self.dealer_score, True, True, 0)
        
        # Box for players cards
        self.box_player = Gtk.Box(spacing = 20)
        self.box_player.set_orientation(0)
        self.box_player.set_margin_start(30)
        self.box_player.set_margin_end(30)
        self.box_player.set_margin_top(20)        
        self.box_player.set_size_request(600, 150)

        #   BUTTONS
        # Play button
        self.button_play = Gtk.Button(label="Play")
        self.button_play.connect("clicked", self.play_button_clicked)
        
        # Hit button
        self.button_hit = Gtk.Button(label="Hit")
        self.button_hit.connect("clicked", self.hit_button_clicked)
        self.button_hit.set_sensitive(False)        

        # Stay button
        self.button_stay = Gtk.Button(label="Stay")
        self.button_stay.connect("clicked", self.stay_button_clicked)
        self.button_stay.set_sensitive(False)

        # Quit button
        self.button_quit = Gtk.Button(label="Quit")
        self.button_quit.connect("clicked", self.quit_button_clicked)            
        
        # Box for buttons
        self.box_buttons = Gtk.Box(spacing = 30)
        self.box_buttons.set_margin_start(20)
        self.box_buttons.set_margin_end(20)
        self.box_buttons.set_margin_bottom(10)
        self.box_buttons.set_margin_top(20)
        self.box_buttons.pack_start(self.button_play, True, True, 0)
        self.box_buttons.pack_start(self.button_hit, True, True, 0)
        self.box_buttons.pack_start(self.button_stay, True, True, 0)
        self.box_buttons.pack_start(self.button_quit, True, True, 0)
        
        #   CARDS
        self.all_cards = Gtk.Image()
        self.all_cards = GdkPixbuf.Pixbuf.new_from_file("deck.png")        # Pixbuf object
        
        # Put boxes in main box
        self.box.pack_start(self.box_dealer, True, True, 0)
        self.box.pack_start(self.box_label, True, True, 0)
        self.box.pack_start(self.box_player, True, True, 0)
        self.box.pack_start(self.box_buttons, True, True, 0)
        
        
    def setup(self):
        self.dealer_values = []
        self.player_values = []
        self.dealer_sum = 0
        self.player_sum = 0
        self.deck = [ "s1","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","s12","s13",
                         "h1","h2","h3","h4","h5","h6","h7","h8","h9","h10","h11","h12","h13",
                         "d1","d2","d3","d4","d5","d6","d7","d8","d9","d10","d11","d12","d13",
                         "c1","c2","c3","c4","c5","c6","c7","c8","c9","c10","c11","c12","c13" ]
        random.seed()        
        
        # destroy previous card widgets
        for card in self.box_dealer:
            card.destroy()
        for card in self.box_player:
            card.destroy()
        # reset labels
        self.player_score.set_text("Player: -")
        self.label.set_text("")
        self.dealer_score.set_text("Dealer: -")
        
        
    def deal_card(self, receiver, facing):
        card = Gtk.Image()
        card_str = random.choice(self.deck)
        if card_str[0] == "s":
            suite = 1
        elif card_str[0] == "h":
            suite = 2
        elif card_str[0] == "d":
            suite = 3
        elif card_str[0] == "c":
            suite = 4
        cardvalue = int(card_str[1:])
        self.deck.remove(card_str)
        
        # Face down card
        if facing == "down":
            pixbuf = self.all_cards.new_subpixbuf(4*98, 4*144, 98, 144)
            card.set_from_pixbuf(pixbuf)        
            card.set_size_request(98, 144)
            self.box_dealer.pack_start(card, False, True, 0)
            self.box_dealer.show_all()
            self.hidden_card = card_str     # to be revealed later
        
        # Face up cards
        else:
            pixbuf = self.all_cards.new_subpixbuf((cardvalue-1)*98, (suite-1)*144, 98, 144)
            card.set_from_pixbuf(pixbuf)        
            card.set_size_request(98, 144)
            if receiver == "dealer":
                self.box_dealer.pack_start(card, False, True, 0)
                self.box_dealer.show_all()                
            else:
                self.box_player.pack_start(card, False, True, 0)
                self.box_player.show_all()        
        
        if cardvalue >= 10:
            cardvalue = 10
        elif cardvalue == 1:
            cardvalue = 11
        
        if receiver == "dealer":
            self.dealer_values.append(cardvalue)
            self.dealer_sum = sum(self.dealer_values)
            if self.dealer_sum == 21:
                self.label.set_text("Dealer got blackjack! You lose!")      # not always
                self.button_play.set_sensitive(True)
                self.button_hit.set_sensitive(False)
                self.button_stay.set_sensitive(False)  
            elif self.dealer_sum > 21:
                if 11 in self.dealer_values:
                    self.dealer_values.remove(11)
                    self.dealer_values.append(1)
                    self.dealer_sum = sum(self.dealer_values)
                else:
                    self.label.set_text("Dealer goes bust! You win!")
                    self.button_play.set_sensitive(True)
                    self.button_hit.set_sensitive(False)
                    self.button_stay.set_sensitive(False) 
            if len(self.dealer_values) > 2:     # show score after dealers 2ns card is revealed
                self.dealer_score.set_text("Dealer: " + str(self.dealer_sum))

        else:
            self.player_values.append(cardvalue)
            self.player_sum = sum(self.player_values)  
            if self.player_sum == 21:
                self.label.set_text("BLACKJACK! You win!")
                self.button_play.set_sensitive(True)
                self.button_hit.set_sensitive(False)
                self.button_stay.set_sensitive(False)                
            elif self.player_sum > 21:
                if 11 in self.player_values:
                    self.player_values.remove(11)
                    self.player_values.append(1)
                    self.player_sum = sum(self.player_values)
                else:
                    self.label.set_text("Bust! You lose!")
                    self.button_play.set_sensitive(True)
                    self.button_hit.set_sensitive(False)
                    self.button_stay.set_sensitive(False)
            self.player_score.set_text("Player: " + str(self.player_sum))
            
            
    def reveal_card(self, card_str):
        children = self.box_dealer.get_children()       # remove facedown image
        children[-1].destroy()    
        card = Gtk.Image()
        if card_str[0] == "s":
            suite = 1
        elif card_str[0] == "h":
            suite = 2
        elif card_str[0] == "d":
            suite = 3
        elif card_str[0] == "c":
            suite = 4
        cardvalue = int(card_str[1:])  
        pixbuf = self.all_cards.new_subpixbuf((cardvalue-1)*98, (suite-1)*144, 98, 144)
        card.set_from_pixbuf(pixbuf)        
        card.set_size_request(98, 144)
        self.box_dealer.pack_start(card, False, True, 0)
        self.box_dealer.show_all()   
        self.dealer_score.set_text("Dealer: " + str(self.dealer_sum))

        
    def play_button_clicked(self, widget):
        self.button_play.set_sensitive(False)
        self.setup()
        
        # TODO
        #   sleep ei toimi oikein, joku animaatio?
        
        self.deal_card("dealer", "up")
        #time.sleep(1)
        self.deal_card("player", "up")
        #time.sleep(1)
        self.deal_card("dealer", "down")
        #time.sleep(1)
        self.button_hit.set_sensitive(True)
        self.button_stay.set_sensitive(True)        
        self.deal_card("player", "up")        
        
        
        
    def hit_button_clicked(self, widget):
        self.deal_card("player", "up")
        

    def stay_button_clicked(self, widget):
        self.reveal_card(self.hidden_card)
        while self.dealer_sum < 17:
            self.deal_card("dealer", "up")
        if self.dealer_sum == self.player_sum:
            self.label.set_text("Nobody wins")
            self.button_play.set_sensitive(True)
            self.button_hit.set_sensitive(False)
            self.button_stay.set_sensitive(False)             
        elif self.dealer_sum > self.player_sum and self.dealer_sum <= 21:
            self.label.set_text("Dealer wins")
            self.button_play.set_sensitive(True)
            self.button_hit.set_sensitive(False)
            self.button_stay.set_sensitive(False)   
        elif self.dealer_sum < self.player_sum:
            self.label.set_text("You win")
            self.button_play.set_sensitive(True)
            self.button_hit.set_sensitive(False)
            self.button_stay.set_sensitive(False)
        

    def quit_button_clicked(self, widget):
        Gtk.main_quit()
        # TODO  popup confirmation?
        


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
