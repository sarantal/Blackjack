import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Blackjack")
        self.set_default_size(600,400)
        
        # Grid to contain boxes
        grid = Gtk.Grid()
        self.add(grid)
        
        # Box for dealers cards
        self.box_dealer = Gtk.Box(spacing = 20)
        self.box_dealer.set_orientation(0)    # vertical box = 1, horizontal is default or '0'
        self.box_dealer.set_margin_start(30)
        self.box_dealer.set_margin_end(30)
        self.box_dealer.set_margin_top(20)
        
        # Box for players cards
        
        
        # Label for text
        
        
        #   Buttons
        # Deal button
        button_deal = Gtk.Button(label="Deal cards")
        button_deal.connect("clicked", self.deal_button_clicked)
        
        # Hit button
        button_hit = Gtk.Button(label="Hit")
        button_hit.connect("clicked", self.hit_button_clicked)

        # Stay button
        button_stay = Gtk.Button(label="Stay")
        button_stay.connect("clicked", self.stay_button_clicked)

        # Quit button
        button_quit = Gtk.Button(label="Quit")
        button_quit.connect("clicked", self.quit_button_clicked)            
        
        # Box for buttons
        self.box_buttons = Gtk.Box(spacing = 30)
        self.box_buttons.pack_start(button_deal, True, True, 0)
        self.box_buttons.pack_start(button_hit, True, True, 0)
        self.box_buttons.pack_start(button_stay, True, True, 0)
        self.box_buttons.pack_start(button_quit, True, True, 0)
        
        

        # Pixbuf for all cards  (card size: w=72, h=96)
        all_cards = Gtk.Image()
        #all_cards.new_from_file("cards.png")                       # Image object
        all_cards = GdkPixbuf.Pixbuf.new_from_file("cards.png")     # Pixbuf object

  
        # Dealers cards
        dealer_card1 = Gtk.Image()
        #cardvalue = 7
        #suite = 2              (cardvalue-1)*72, (suite-1)*96
        pixbuf = GdkPixbuf.Pixbuf(width=72, height=96)
        print(pixbuf.get_width())   # =1 ??
        print(pixbuf.get_height())  # =1 ??
        #all_cards.copy_area(0, 0, 72, 96, pixbuf, 0, 0)
        """
        GdkPixbuf-CRITICAL **: 17:21:43.779: gdk_pixbuf_copy_area: assertion 'dest_x >= 0 && dest_x + width <= dest_pixbuf->width' failed
        """
        #pixbuf = all_cards.subpixbuf(0, 0, 72, 96)      # ...object has no attribute 'subpixbuf'
        dealer_card1.set_from_pixbuf(pixbuf)
        
        #dealer_card1 = Gtk.Button(label="Card 1")      # testing with buttons
        dealer_card2 = Gtk.Button(label="Card 2")
        # TODO: max 6 cards?
        dealer_card1.set_size_request(72, 96)
        dealer_card2.set_size_request(72, 96)
        self.box_dealer.pack_start(dealer_card1, True, True, 0)
        self.box_dealer.pack_start(dealer_card2, True, True, 0)
        
        
        
        # Players cards

        

        # Put boxes in grid
        #   could also be vertical box containing other boxes?
        grid.add(self.box_dealer)
        grid.attach_next_to(self.box_buttons, self.box_dealer, Gtk.PositionType.BOTTOM, 1, 1)
        
        
    def deal_button_clicked(self, widget):
        print("Lets deal cards!")
        # TODO
        
    def hit_button_clicked(self, widget):
        print("Get another card")
        # TODO

    def stay_button_clicked(self, widget):
        print("Stay")
        # TODO

    def quit_button_clicked(self, widget):
        print("Quit")        
        # TODO


        
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
