#!/usr/bin/python3
#Final Project for Python 3 - text based adventure!
#Learned many things from google, W3Schools, and Python.org. I also referenced a couple things on stack overflow and reddit. I was also probably too trusting of intelisense.
#Used AI for the storyline, but all descriptions were written by my brain :)
#For a more immersed experience, listen to the Riven OST playlist: https://www.youtube.com/watch?v=ltCbUlPGC0o&t=1729s
from tkinter import *
from tkinter import Toplevel

#Defines the properties and methods of the main form
class MainFormClass:
    def __init__(self, master):
        self.master = master
        master.title("Library Anomaly")
        master.bind("<Key>", self.keyPress) #Bind the key event to the form so it can be used to move around the library and get items
        master.grid_rowconfigure(0, weight=1) #Allows the form to resize with the window
        master.grid_columnconfigure(0, weight=1)
        #Use dictionaries to define rooms and how they connect
        self.rooms = { 
            #1st floor
            "Entrance": {"name": "Entrance", 
                         "description": "You have bravely ventured into the Library and now stand in the dusty entrance. The door swings partly shut behind you, moving surprisingly easily and quietly for an old library. The setting sun casts long patches of light across the arched halls and tall shelves, casting an eerie but beautiful scene.", 
                         "w": "Main Hall", "a": "Reference Section", "s": "Exit", "d": "Map Room"},

            "Exit": {"name": "Exit", 
                     "description": "You exit the Library, backing away from its enormous doors that swing shut with hardly a sound. Uneasy feeling get to you? Go back in if you dare...", 
                     "w": "Entrance", "a": None, "s": None, "d": None},

            "Main Hall": {"name": "Main Hall", 
                          "description": "The bookshelves in the Main Hall tower high above you, filled with books almost to the top of the vaulted ceiling. The air is thick with dust and the scent of old paper. To the right and left of you are two large rooms; in front of you is an ornate carpet, stretching down the entire hall and leading to a pair of shut wooden doors.", 
                          "w": "Librarian's Office" , "a": "Study Hall", "s": "Entrance", "d": "Picture Gallery"},

            "Map Room": {"name": "Map Room", 
                         "description": "You venture into a large room and discover the map room, its walls lined with ancient maps and charts. Library ladders adorn the towering shelves, stuffed with ancient books containing coveted knowledge of the world and its history. The floor is littered with old, crumbling maps so that you stand still for fear of destroying them with your steps. You gaze about the room from your position, craning your neck to see so that you need not move and risk damagine the maps further. As your gaze flickers from map to map, you realize that some belong to different worlds, some to different times of the same world, and some even to the very city you yourself live in. On the map that matches your world, you notice that certain edges of land are altered, with new boundaries traced in different patterns over the old lines that seem to have been faded or scratched out.", 
                         "w": "Picture Gallery" , "a": "Entrance", "s": None, "d": None},
    
            "Reference Section": {"name": "Reference Section", 
                                  "description": "You wander into a large room and discover the reference section. The short, wide shelves are filled with encyclopedias, dictionaries, and other reference materials. Strangely enough, the references seem to reach into years far beyond the active life of the Library.", 
                                  "w": "Study Hall" , "a": None, "s": None, "d": "Entrance"},

            "Picture Gallery": {"name": "Picture Gallery", 
                                "description": "You step into a room and find that it is filled with paintings and photographs rather than books. Some have been placed for art and some preserved for history. As you walk the length of the room slowly, you gradually begin to notice that the Library itself is in many of the frames, even a picture that looks startlingly recent. In the row of pictures dedicated to past librarians, seemingly random faces are scratched out, as if someone had tried to erase them. The last frame in the room is empty. It is simply labled 'Today'. Off to the right of the room, you see a staircase winding upwards and out of sight.", #finish description
                                "w": None , "a": "Main Hall", "s": "Map Room", "d": {"name": "Winding staircase", "room": "Landing"}}, #Winding staircase leads to 2nd floor landing

            "Study Hall": {"name": "Study Hall", 
                           "description": "You come across a lofty room filled with large tables, comfortable chairs, and tall windows that let in natural light. One table is covered with ancient, open books and rolled scrolls. As you pass by, you glance over a few of the parchments. Some of the ink on the scrolls seems to have disappeard gradually, as if soaking into the paper or perhaps being forgotten by the Library. One book is dated in the future; its spine significantly less dusty than its neighbors. ", #finish description
                           "w": "Reading Room" , "a": None, "s": "Reference Section", "d": "Main Hall"},

            "Reading Room": {"name": "Reading Room", 
                          "description": "This place of quiet contemplation seems abnormally neat. Long tables sit in the center of the room, with open books lined up along their edges. You walk the length of a table, scanning books as you go. The first book is full of archaic words you are unable to understand. The second book is written in a language you recognize but still cannot read. By the fourth book, you are able to read the books, but they are full of old knowledge too grand to comprehend in a glance. As you near the end of the table, the books begin to feel oddly familiar. One page strikes you with eerie intimacy as you recognize your favorite childhood memory written out upon it. As you skim this page, you notice that some details differ from how you remember them. Some of the details are large and some are small, but this book feels as if it is rewriting something, someone's destiny. The last open book holds one sentence: 'They entered the Library believing themselves to be the one searching.' You bend to study the words and realize that the ink is still wet. ",
                          "w": "Balcony" , "a": None, "s": "Study Hall", "d": None},

            "Balcony": {"name": "Reading Room Balcony",
                            "description": "This small outside area of the library is quiet, with a view of the surrounding landscape. However, what should be an ordinary quiet instead carries the unsettling impression of something being carefully kept subdued, pretending that silence is its natural state.",
                            "w": None , "a": None, "s": "Reading Room", "d": None},

            "Librarian's Office": {"name": "Librarian's Office", 
                                  "description": "You find yourself in a modest office lined with dark bookshelves containing ledgers, sealed books, and cataloged records. The room's singular window lies opposite the doorway, spreading light over a broad desk that sits in the middle of the room, covered with heavy books and parchments. Although there is a layer of dust covering everything, the room feels preserved rather than abandoned, as if its occupant had left with every intent to return.",
                                  "w": None , "a": {"name": "Descending staircase", "room": "Hallway"}, "s": "Main Hall", "d": "Filing Room",
                                  "item": {"name": "Key", "description": "an old key that looks like it may have been gold at some point, but is now faded with dirt and age. It lies among various parchments on the librarians desk, looking as if it had been hastily set aside by its last user. It is almost as big as your hand."}},

            "Filing Room": {"name": "Filing Room", 
                            "description": "You duck through an archway into a room that feels more like an extension of the Librarian's Office than a seperate room. The small room is cramped with filing cabinets and documents of all sorts; some cabinets labeled meticulously, others labled haphazardly or not at all. Curious, you began to thumb through different cabinets and folders, ignorning the growing feeling that perhaps you should not be looking. At first glance, the systems seem complete and orderly, even in the absence of their keeper and some lables. However, the longer you remain, the more unsettling the organization becomes, causing your unease to grow with it. Categories began to blur in ways that should not be: people are filed under 'Objects', Places under 'Events', and events under 'Evaluations'. There is even a file with your name on it, but when you open it, the file is empty except for a single sentence: 'Visitor behavior corresponds to the previously unrecorded but anticipated pattern of Library interaction.'",
                            "w": None , "a": "Librarian's Office", "s": None, "d": None},

            #Basement
            "Hallway": {"name": "Hallway", 
                                    "description": "You dismount the stairs to find yourself in a narrow, dim hallway that leads forward and then vanishes into darkness.",
                                    "w": None , "a": "??", "s": None, "d": {"name": "Ascending staircase", "room": "Librarian's Office"}},

            "??": {"name": "??", #Must have lantern to navigate past #darkness of hallway
                    "description": "As you move further into the hallway, complete darkness surrounds you. Is there a wall ahead? An endless void? Which way is which?",
                    "w": None , "a": "???", "s": None, "d": "Hallway"},

            "???": {"name": "???", #Add password or access code to get into this room #lock on vault door 
                    "description": "Your advance through the darkness is brought up short by a heavy, locked door. As you stoop and attempt to peer through the keyhole, your view is obstructed by cobwebs and dust in the keyhole, stuck from years of unuse.",
                    "w": None , "a": {"name": "????", "room": "Book Vault"}, "s": None, "d": "??"},

            "Book Vault": {"name": "Book Vault", #Must have key to access this room
                            "description": "You bend slightly to enter the book vault, stepping cautiously past the large, heavy door. You squint in the dim lantern light, expecting to see rows of short bookcases for storing rare, important books safely away from greedy minds. Instead, you find short metal shelves divided into sections by small but sturdy lock boxes. Each one is opened, its lock hanging undone from the door, as if waiting for someone, for you, to inspect the contents. You slowly approach a shelf of lock boxes, holding the lantern up with one hand and sifting through files with the other. The volumes are bound in such bizzare ways that you are sure made sense to the former librarian, but have no use for you now. The writing on the lables too small and sloppy to make out, you look through whatever is closest to you, though for what you search you are not sure. Unexpectedly, the records uniform and begin to be somewhat coherent. Records of past librarians, matching the names you remember from the Picture Gallery...librairians appointed... the Library stabilizes under their oversight... and then, at an indistinct point, the librarian is no longer present in the records. Some records go on for years without a new librarian being determined. The cause of the asbent librarian is inconsistently described in the records. In some 'transition' is used, while in others 'removal' is used, but in all records, no description is given, it is simply noted as fact. The only thing that remains consistent is the response: the Library continues functioning even without oversight, searching once more for a replacement to provide stability. In another box you find a file marked 'compatability thresholds', which seem to be some twisted version of screening someone for a job position. The criteria does not involve a person's character or behavior, but simply perception: does the Library approve? As you near the end of the file, the record shifts, the title at the top of the new page indicating that it is a record of selected librarians. All the previous records fade away from the page so subtly and quickly that you question if you even saw them at all or if it was only a mirage. What remains is a single entry. SUBJECT: CURRENT VISITOR. STATUS: SELECTED. There is no reason as to why the selection occurred; only confirmation that it has. Suddenly you realize there were no errors in the recordkeeping, but simply rejections. The things scratched out and missing from the Library's rooms had chosen the Library, but the Library had not chosen them, so it rejected them, and rewrote over them. You step back, your head spinning as you try in vain to organize what you have seen in such a short time. What happens, you wonder, when the Library chooses you and you do not choose the Library?",
                            "w": None , "a": None, "s": None, "d": "Hallway"},

            #2nd floor
            "Landing": {"name": "Landing", 
                        "description": "You reach the top of the stairs and pause for a moment to catch your breath. A window the height of the ceiling opens to your right, its panes letting in the setting sun's rays. You are in a small landing area, with doors opening up new rooms and discoveries in every direction. Which will you choose first?", #finish description
                        "w": "Science Section" , "a": "Fiction Section", "s": None, "d": {"name": "Winding staircase", "room": "Picture Gallery"}}, #Staircase leads back down to picture gallery

            "Science Section": {"name": "Science Section",
                                "description": "The Science section is joltingly sterile compared to the cluttered and dusty but charming rooms of the first floor. The shelves are metal and the books stored on them are newer, with less dust and more modern titles. The room has no windows, the wall space sacrificed completely to bookshelves. The only lightsource is a single skylight up above that washes the room in faint, distant light from the setting sun. As you walk through the aisles, you notice that the books in this section seem to be more focused on the future rather than the past, their titles displaying cutting-edge technology and scientific discoveries that have yet to be made. The further you go into the aisles, the more you notice that certain books are carefully stored within the wrong section, with some subjects straying into unsettlingly unrelated sections. You find a large book titled 'On Structural Continuity in Autonomous Archival Systems' wedged onto the shelf. You run your fingers over the raised letters along the spine, grasping the edges in an attempt to dislodge it from the shelf. The book does not budge. You yank harder, but strangely enough, this book does not seem shelved; it seems embedded. Your curiosity will have go unsatisfied.",
                                "w": "Astronomy Section" , "a": "Scriptorium", "s": "Landing", "d": None},

            "Astronomy Section": {"name": "Astronomy Section",
                                  "description": "Strange contraptions and devices are scattered about the room, their handles and sides worn smooth by years of use. The walls being mostly adorned with astronomical charts and parchments of different constellations, this room has little wall space for bookshelves. Your attention is drawn to a large book on of the few shelves, its smooth blank spine catching your eye. You pick it up, turn it over, flip through it, but to no avail. It is a completely empty book, although its pages are torn in the spot where all well-used books are torn: the bottom of the page as it curves into the spine. As you slide it back onto the shelf, you notice that there is indeed a title on the book, faded and worn as it is. As you bend your neck in an effort to read it, you realize that the title has been scratched out by the same mark that marred the faces in the picture gallery.",
                                  "w": "Observatory" , "a": None, "s": "Science Section", "d": None},

            "Observatory": {"name": "Observatory",
                            "description": "You step into the room connected directly to the Astrology section: the Observatory. This is one of the Library's most immense and imposing chambers, its vast glass dome opening up above you to let in sunset and starlight. Although the dome has been dimmed by age, weather, and dust, you can still see the room clearly as it opens into a circular space once dedicated to studying the night sky. At the center of the room stands a large telescope, mounted stiffly but proudly atop a brass rotating mechanism. Lining the circular room are dark red desks, their backs carved to fit the unique shape of the room. Each serface is covered with star charting devices and papers containing records, diagrams, and lunar maps. As you walk the length of the room, running your hand over the smooth wood and rough paper of the desks, you notice a pair of large glass doors at the front of the room, framed by bookshelves and shrouded in dark, sweeping curtains. You push through them to discover a moderate, curved balcony that contains chart tables and observation stations still littered with methodically arrayed objects, despite years of illusioned unuse. Small telescopes stand at attention along the railing, their models that of the dome-crowned one.", #finish description
                            "w": None , "a": None, "s": "Astronomy Section", "d": None},
                            

            "Fiction Section": {"name": "Fiction Section",
                                "description": "Although the lighting is dim here, you are still struck by the warm, inviting atmosphere of this room that contrasts the colder precision of the Science and Astronomy sections. Faded green curtains fall from the ceiling and sweep the floor, their fabric pulled back into hooks to reveal padded window seats hidden behind each pair. Reading lamps, side tables, and cushioned chairs are dotted throughout the wide rows, creating a leisurely although dusty scene. This space had clearly been designed for comfort and even small children, running quietly to and fro amid hushed whispering and giggling. You can almost feel the strange weight of the Library lift as you wander down the long aisles filled with fiction and old classics, your eyes browsing over the spines of the books. ",
                                "w": "Scriptorium" , "a": "History Section", "s": None, "d": "Landing"},

            "History Section": {"name": "History Section.",
                                "description": "Tall, dense shelves greet you as you enter the room past the Fiction section of the Library. The vaulted ceiling of the History section lends to its air of grandeur, with tall brass candelabras standing at attention along the walls next to windows spanning the height of the lofty walls. Desks dedicated to research are accompanied by stiff but stately chairs, their backs still ridgid after centuries of scholars researching in their support. The history books of this section seem to be the oldest books in the Library, their spines cracked and faded, their pages yellowed and brittle. Yet as you pick up a large gilded one, you notice that the scent of a new book fills the air as you open it, and hardly any of the ink inside is faded. Curious, you inspect an adjacent volume titled 'On the History of Establishment and Continuity of the Regional Memory', only to find the same mysterious quality as the previous book. Pondering this, you move to close the book and place it back on the shelf, but something catches your eye. Surprised, you realize that the history of the Library itself is within this book, with many blank pages still left at the back of the book, as if expecting more entries. The most recent entry is dated 'Today', altough the previous entry is dated for many years before the present. Your eyes scan over the last written page, landing on the last sentence: 'Behavior corresponds to the previously unrecorded but anticipated pattern of library interaction.' The filing status at the top of the entry is marked as ongoing.",
                                "w": None , "a": None, "s": None, "d": "Fiction Section"},

            "Scriptorium": {"name": "Scriptorium",
                            "description": "This space dedicated to the art of writing and copying manuscripts is connected to two of the main sections of the Library, with ease of access to all sections on the second floor. The tables and desks in this room are long and narrow in order to accommodate long scrolls and multiple writing stations. Each station is equipped with ink wells, writing supplies, and parchment, but everything appears untouched. Everything is still rigid, the inkwells full and the pens unstained. The chairs are pushed up to the lip of each table, their cushions faded by sunlight and age, but not by use. The walls are empty, as if not to distract from the work of copying, but whatever this room was designed to record, it no longer seems necessary for it to be written here; as though everything worth copying has already been recorded elsewhere.",
                            "w": None , "a": "Gallery", "s": "Fiction Section", "d": "Science Section",
                            "item": {"name": "Lantern", "description": "a rusty lantern that still has some oil left in it sitting discarded on a shelf, its glass fogged with age."}},

            "Gallery": {"name": "Scriptorium Gallery",
                        "description": "The small outside gallery is connected to the Scriptorium by a set of glass doors that appear small next to the wall of windows that let natural light pour into the Scriptorium. The gallery is bare, devoid of furniture as the occupants would have stood outside to rest from their work of bent precision. The view from the gallery is wooded, the tall trees secluding the gallery and swaying gently as the sun filters through their leaves, casting a dappled pattern of light across the grass.",
                        "w": None , "a": None, "s": None, "d": "Scriptorium"}
        }
        #Place frame on the form  
        frame1=Frame(master, highlightbackground="white", highlightthickness=10) #Create a frame to contain the main parts of the game
        frame1.place(relx=0.5, rely=0.5, relheight=0.8, relwidth=0.8, anchor='center') #Center the frame in the form
        frame1.grid_rowconfigure(0, weight=1) #Allows the frame to resize with the window
        frame1.grid_rowconfigure(1, weight=1)
        frame1.grid_rowconfigure(2, weight=1)
        frame1.grid_columnconfigure(0, weight=1) #Allows the frame to resize with the window
        frame1.grid_columnconfigure(1, weight=1)
        frame1.grid_columnconfigure(2, weight=1)
        #Enter the library
        self.btnEnter=Button(frame1, text="Enter Library", command=self.btnEnter_Click)
        self.btnEnter.pack(side=BOTTOM, anchor='s') #Centers the button in the form
        #Place labels to keep track of descriptions and rooms in all directions
        #Descriptions
        self.lblDescription=Label(frame1, text="A vast library looms before you, seeming to sprawl simultaneously upwards and outwards, its entrance shrouded by shadows cast by the descending sun. Will you venture inside and fall prey to curiosity? Or will you stay outside, safe but unsatisfied?",wraplength=2000, justify=LEFT) #Welcome message. Show before entering the library and wrap text so all of it shows
        self.lblDescription.place(relx=0.5, rely=0.5, anchor='center') #Center the label in the form. (Found .place on Google)
        #Current room
        self.lblCurrentRoom=Label(frame1, text="You are in the entrance of the Library.") #show once the Library is entered
        #Rooms in all directions of current room
        self.lblRRoom=Label(master, text="The room to the right of the current room.") #show once library is entered. Change as you move
        self.lblLRoom=Label(master, text="The room to the left of the current room.") #show once library is entered. Change as you move
        self.lblFRoom=Label(master, text="The room in front of the current room.") #show once library is entered. Change as you move
        self.lblBRoom=Label(master, text="The room behind the current room.") #show once library is entered. Change as you move
        #Item descriptions
        self.lblItem=Label(frame1, text="The item in the current room, if there is one.", wraplength=2000, justify=LEFT) #show once library is entered. Change as you move and wrap text
        #Controls
        self.lblControls=Label(master, text="Use the W, A, S, D keys to navigate the Library's corridors and the I key to pick up items.", highlightbackground="black", highlightthickness=2)
        #Inventory display
        self.inventory=[] #Create an empty list to store the player's inventory
        self.lblInventory=Label(master, text="Inventory: " + ", ".join(self.inventory) if self.inventory else "Inventory: Empty") #Label to display the player's inventory. Update as items are added or removed from inventory
        self.lblInventory.pack(side=BOTTOM, anchor='se') #Place the inventory label in the bottom right corner of the form
        #Styling
        self.btnEnter.config(bg="white", fg="black") #change button look
        #Begin the game outside
        self.currentRoom=None

    def btnEnter_Click(self): #!fix so this text splits onto two different lines in output!
        self.currentRoom="Entrance" #Set the current room to the entrance once the Library has been entered #Just set equal to "Entrance"?
        self.btnEnter.pack_forget() #Removes the button from the form after it has been clicked
        self.lblDescription.config(text="You have bravely ventured into the Library and now stand in the dusty entrance. The setting sun casts long patches of light across the arched halls and tall shelves, casting an eerie but beautiful scene.") #Entered the main room of the Library
        self.lblControls.pack(side=BOTTOM, anchor='sw') #Show controls once library is entered
        #Show room labels once the Library is entered
        self.lblCurrentRoom.grid(row=0, column=1)
        self.lblRRoom.pack(side=RIGHT, anchor='e')
        self.lblLRoom.pack(side=LEFT, anchor='w')
        self.lblFRoom.pack(side=TOP, anchor='n')
        self.lblBRoom.pack(side=BOTTOM, anchor='s')
        self.lblItem.grid(row=2, column=1) #Show item label in the middle of the frame, below the current room label
        #self.inventory.append("Lantern", "Key") #For presentation purposes
        self.updateDisplay() #Update the display to show the current rooms


    def updateDisplay(self):
        
        room=self.rooms[self.currentRoom] #Get the current room from the rooms dictionary
        self.lblCurrentRoom.config(text=f"You are in the {room['name']}") #Update the current room label
        self.lblDescription.config(text=room["description"]) #Update the description label
        #Display a different message if the Library is exited
        if self.currentRoom == "Exit":
            self.lblCurrentRoom.config(text="You are outside the Library.")
        #Room in each direction
        #Room in front [W]
        #Special case for staircases
        if isinstance(room["w"], dict):
            self.lblFRoom.config(text=f"{room['w']['name']}.") #If there is a staircase in that direction, show the name of the room it leads to
        elif room["w"] is not None: #no staircase but there is a room
            self.lblFRoom.config(text=f"{room['w']}.")
        else:            
            self.lblFRoom.config(text=" ") #If there is no room in that direction, don't show anything
        #Room behind [S]
        #Staircases
        if isinstance(room["s"], dict):
            self.lblBRoom.config(text=f"{room['s']['name']}.")
        elif room["s"] is not None:
            self.lblBRoom.config(text=f"{room['s']}.")
        else:
            self.lblBRoom.config(text=" ")
        #Left room [A]
        #Staircases
        if isinstance(room["a"], dict):
            self.lblLRoom.config(text=f"{room['a']['name']}.")
        elif room["a"] is not None:
            self.lblLRoom.config(text=f"{room['a']}.")
        else:
            self.lblLRoom.config(text=" ")
        #Right room [D]
        #Staircases
        if isinstance(room["d"], dict):
            self.lblRRoom.config(text=f"{room['d']['name']}.")
        elif room["d"] is not None:
            self.lblRRoom.config(text=f"{room['d']}.")
        else:
            self.lblRRoom.config(text=" ")

        #Items
        if room.get("item") is not None: #If there is an item in the room, show its description
            self.lblItem.config(text=f"You see {room['item']['description']}")
        else:
            self.lblItem.config(text="") #If there is no item in the room, don't show anything

        

    def keyPress(self, event):
        key = event.char
        #Latern required to advance from hallway to Book Vault through darkness
        if self.currentRoom == "??":
            if key == 'a': 
                if "Lantern" in self.inventory:
                    self.lblDescription.config(text="You hastily sweep the latern in front of you as the darkness threatens to envelope you again. The light reveals a dim path.") #Latern allows passage
                    self.currentRoom = "???"
                    self.master.after(4000, self.updateDisplay) #Pause for 4 seconds to let the player read the message
                else: 
                    self.lblDescription.config(text="You need a light source to navigate through this cold darkness.") #Latern required
                return

        #Key required to access Book vault if they try to press 'a' in the hallway
        if self.currentRoom == "???":
            if key == 'a': 
                if "Key" in self.inventory:
                    self.currentRoom = "Book Vault"
                    self.lblDescription.config(text="The key fits perfectly into the lock and you turn the massive key with surpirsingly little effort until it clicks softly into place. You swing the enormous door out into the hall and hold up your latern to see.") #Key unlocks door
                    self.master.after(7000, self.updateDisplay) #Pause for 7 seconds to let the player read the message
                else:
                    self.lblDescription.config(text="You will need a key get into this vault.") #Key required
                return

        if key in ["w", "a", "s", "d"]:
            self.moveAround(event)
        elif key in ["i"]:
            self.getItems(event)

        #NEW CODE Once player has entered the book vault and read the description, end the game if they try to move
        if self.currentRoom == "Book Vault" and key in ["w", "a", "s", "d"]:
            final=Toplevel(self.master) #Create a new window to show the final message
            final.geometry("500x500") #Set the size of the final message window
            final.title("The Library's Choice") #Set the title of the final message window
            lblFinal=Label(final, text="Congratulations, newest Librarian...")
            lblFinal.pack(expand=True) #Center the final message in the window
            self.master.after(2000, self.master.destroy) #Pause for 2s seconds to let the player read the message before closing the game
            return

    def moveAround(self, event):
        key = event.char
        #The player cannot move around the Library until they have entered
        if self.currentRoom is None:
            return
        room = self.rooms[self.currentRoom] #Get the current room from the rooms dictionary
        adjacentRoom = room[key] #Get the room in the direction of the key pressed
        if adjacentRoom is None: #If there is no room in that direction, don't do anything
            return
            #special case for staircases
        if isinstance(adjacentRoom, dict):
            self.currentRoom = adjacentRoom["room"] #Update the current room to the room that the staircase leads to
        else:
            self.currentRoom = adjacentRoom #Update the current room to the adjacent room
        self.updateDisplay() #Update the display to show the new room and its description

    def getItems(self, event):
            room = self.rooms[self.currentRoom] #Get the current room from the rooms dictionary
            if room.get("item") is not None: #If there is an item in the room
                self.inventory.append(room["item"]["name"]) #Add the item to the inventory
                room["item"] = None #Remove the item from the room
                self.lblInventory.config(text="Inventory: " + ", ".join(self.inventory)) #Update the inventory display
                self.updateDisplay() #Update the display to show that the item has been taken

#Create a main function
def main():
    form=Tk() #Create the main form
    form.geometry("2000x2000") #Set the size of the form
    mainForm=MainFormClass(form) #Create an instance of the main form class
    form.mainloop() #Start the event loop

main()