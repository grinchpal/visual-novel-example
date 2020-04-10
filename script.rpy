# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.


init python:



    import random

    # init random nos.
    random.seed()

    # Snow particles

    def Snow(image, max_particles=50, speed=150, wind=100, xborder=(0,100), yborder=(50,400), **kwargs):
        """

        @parm {image} image: "snow.png"
            image for snowflake

        @parm {int} max_particles: 50
            max no. particles on screen

        @parm {float} speed: 1
            falling speed

        @parm {float} wind: 10
            wind speed

        @parm {Tuple ({int} min, {int} max)} xborder:
            x border

        @parm {Tuple ({int} min, {int} max)} yborder:
            y border
        """
        return Particles(SnowFactory(image, max_particles, speed, wind, xborder, yborder, **kwargs))

    # ---------------------------------------------------------------
    class SnowFactory(object):
        """
        factory 2 create particles
        """
        def __init__(self, image, max_particles, speed, wind, xborder, yborder, **kwargs):
            """
            init factory
            """
            # max no. particles
            self.max_particles = max_particles

            # particle's speed
            self.speed = speed

            # wind's speed
            self.wind = wind

            # x/y range 4 creating the particles
            self.xborder = xborder
            self.yborder = yborder

            # max depth
            self.depth = kwargs.get("depth", 10)

            # init imgs
            self.image = self.image_init(image)


        def create(self, particles, st):
            """
            if # particles < wanted, create
            """
            # if can create new particle:
            if particles is None or len(particles) < self.max_particles:

                # then random depth
                depth = random.randint(1, self.depth)

                # change speed of depth
                depth_speed = 1.5-depth/(self.depth+0.0)

                return [ SnowParticle(self.image[depth-1],      # img 4 particle
                                      random.uniform(-self.wind, self.wind)*depth_speed,  # wind force
                                      self.speed*depth_speed,  # y speed
                                      random.randint(self.xborder[0], self.xborder[1]), # x border
                                      random.randint(self.yborder[0], self.yborder[1]), # y border
                                      ) ]


        def image_init(self, image):
            """
            init img
            """
            rv = [ ]

            # generate array of images for each possible depth value
            for depth in range(self.depth):
                # resize/adjust  alpha value based on img depth
                p = 1.1 - depth/(self.depth+0.0)
                if p > 1:
                    p = 1.0

                rv.append( im.FactorScale( im.Alpha(image, p), p ) )

            return rv


        def predict(self):
            """
            predict images of particles
            """
            return self.image

    # ---------------------------------------------------------------
    class SnowParticle(object):
        """
        for all particles on screen
        """
        def __init__(self, image, wind, speed, xborder, yborder):
            """
            init snow particle
            """

            # particle img
            self.image = image

            if speed <= 0:
                speed = 1

            # wind speed
            self.wind = wind

            # particle speed
            self.speed = speed

            # last time when particle was updated
            self.oldst = None

            # the x/y positions of particle
            self.xpos = random.uniform(0-xborder, renpy.config.screen_width+xborder)
            self.ypos = -yborder


        def update(self, st):
            """
            upadate particle each frame
            """

            # for calculating lag...
            if self.oldst is None:
                self.oldst = st

            lag = st - self.oldst
            self.oldst = st

            # for updating position...
            self.xpos += lag * self.wind
            self.ypos += lag * self.speed

            # check if particle went out of the screen so can b destroyed
            if self.ypos > renpy.config.screen_height or\
               (self.wind< 0 and self.xpos < 0) or (self.wind > 0 and self.xpos > renpy.config.screen_width):
                ##  print "Dead"
                return None

            return int(self.xpos), int(self.ypos), st, self.image
    dressup_show = False
    dressup_button_show = False
    beard, ears, hat = 1, 1, 1 # default dressup items
    beard_styles_num, ears_styles_num, hat_styles_num = 1, 1, 1 # number of styles 4 each dressup item

    def marek(st, at): # combine the dressup items into one displayable
        return LiveComposite(
            (337, 645), # image size
            (400, 100), "marek.jpg",
            #(0, 0), "glasses%d.png"%glasses,
            #(0, 0), "tie%d.png"%tie,
            (501, 163), "beard%d.png"%beard,
# (0, 0) is position of each dressup item-- bc these images r saved w spacing around them, we dnt need 2 position them
            (480, 115), "ears%d.png"%ears,
            (460, 100), "hat%d.png"%hat
            ),.1

    def marek_side(st, at): # same thing as above, just scaled and positioned for the sideimage
        return LiveComposite(
            (337, 645), #257, 560
            (10, 400), im.FactorScale("marek.jpg", .45, .45),
            (10, 400), im.FactorScale("beard%d.png"%beard, .45, .45),
            (10, 400), im.FactorScale("ears%d.png"%ears, .45, .45),
            (10, 400), im.FactorScale("hat%d.png"%hat, .45, .45)
            ),.1



#define e = Character("Eileen")
define n = Character(None, kind=nvl, what_font="adobe.ttf")

init:
    image marey = "marek.jpg"
    image p1 = "p1.png"
    image fl = "fl.jpg"
    image fl2 = "fl2.jpg"
    image b = "boat.jpg"
    image r = "room.jpg"
    image r1 = "room1.jpg"
    image hat1 = "hat1.png"
    image beard1 = "beard1.png"
    image ears1 = "ears1.png"
    image gm = "gm.jpg"

    image snow = Snow("snow.png")

    image m = DynamicDisplayable(marek)



screen dressup:
  if dressup_show:
    add "m" xalign 0 yalign 0 xpos 60
    python:

        # set all the values 2 change styles 2 previous/next ver
        beard_n = beard + 1 # if next one is chosen
        beard_p = beard - 0 # if previous one is chosen
        if beard_p < 1:
            beard_p = 1
        if beard_n > 2:
            beard_n = 1


        ears_n = ears + 1
        ears_p = ears - 0
        if ears_p < 1:
            ears_p = 1
        if ears_n > 2:
            ears_n = 1


        hat_n = hat + 1
        hat_p = hat - 0
        if hat_p < 1:
            hat_p = 1
        if hat_n > 2:
            hat_n = 1



        # display buttons for changing (itself)
        y = 50
        ui.imagebutton("ears1.png", "ears1.png", clicked=SetVariable("ears", ears_n), ypos=200, xpos=100)
        y += 80
        ui.imagebutton("beard1.png", "beard1.png", clicked=SetVariable("beard", beard_n), ypos=350, xpos=125)
        y += 80
        ui.imagebutton("hat1.png", "hat1.png", clicked=SetVariable("hat", hat_n), ypos=80, xpos=90)
        y += 80



        #ui.textbutton("Done", clicked=SetVariable("dressup_show", False))








# The game starts here.

label start:


    #show marek
    show snow
    n "Once upon a time-- specifically 1941--, there lived a man named Marek:"
    show marey at left
    n "twenty-five years old,"
    n "six-foot,"
    n "dark-haired"
    n "and bushy-browed."

    hide marey

    nvl clear
    #show marek w shoe
    n "He worked as a shoe-shiner in Fort Lauderdale, Florida."

    nvl clear

    n "With a few rags of cloth, he would go up to men standing in line waiting for their boats to arrive at the river,
    and he would ask them if they would fancy his fine service that day, pointing out little stains here and there on their shoes--"
    n "'Is that duck… you know... right there on your laces, sir?'"
    n "--, explaining to them how a common man might find it difficult to rid the shoes of such stains,
    but he has been in business for a few years now, and has the experience and right polish to make the shoes presentable--"
    n "'Fine and presentable to match the man you are, sir.'"
    n "For a few shiny pennies Marek would bend down with his rags, a bottle of shoe polish, and get to work making the worst and worn out shoes appear just a little newer again."

    nvl clear

    n "It was an art--"
    n "not the shoe-shining part so much (a common man can very well get rid of most stains on his shoe if he tries),"
    n "but convincing people that they do not have the power he has to make themselves look good,
    and convincing people that there is a need for them to look good"
    n "(perhaps to impress or keep a lady because when she looks down to lift the hem of her dress to not get wet in a puddle she will also notice his shoes,
    and be appalled to see the giant discoloration on them, and never answer the door to him again)."
    n "And so like this Marek made his business six days a week with Sunday off for leisure."

    nvl clear

    n "Yet, despite the decent income he made from his job, for he was quite a good shoe-shiner, Marek found it difficult to feel satisfied."
    n "He would watch the grand American flags blow softly in the wind as the boats boasting them with pride went along the river."
    n "They were quiet reminders that he, in his mundane little world, was alone and separate from his country."
    n "He felt abandoned of life, stuck in a routine sans liberty, and if only he really knew what happiness was, perhaps he would like to be in pursuit of it;"
    n "there was nothing in his life that could metaphorically be likened to bursting in vibrant colors, like red, white, and blue--"
    n "unless, does one consider blacks and browns of leather shoes to be colors that make a man feel impassioned and excited to be alive,"
    n "ready to seize each day and make three-hundred sixty-five unforgettable memories a year?"
    n "Assuming not, all Marek knew was his life was missing something,"
    n "a greater purpose perhaps,"
    n "but he just could not imagine what that purpose could be."
    n "This was the disheartening feeling he went to sleep with each day."

    nvl clear

    n "In a country where he was taught he could be living a dream, he found himself simply living, and that was all."

    nvl clear

    n "But the rest is still unwritten."

    nvl clear
    #scene

    scene gm
    play music "zatyou.mp3"

    "This is your Grinchpalz Mad Libz 4 U story."
    "For this to work you will have to follow a few rules:"
    "1. Do NOT capitalize OR punctuate UNLESS you are told to do so. Messing this up really affects the story in many cases."
    "2. Really unleash your creativity when inputting words and responses. This is YOUR story, so make it as YOU as possible."
    "3. You may save every so often to keep the story, as scrolling back only takes you so far."
    #"Let's practice a line."


    #"Okay, now let's take a look at your mini story."

    #"It was %(adj1)s when %(name)s woke up to a sky so %(color)s that he %(v)s outside to snap some selfies of himself, which he posted on Instagram 4 da likes."

    #"Hopefully the line looks alright to you, with no words capitalized unnecessarily or punctuations where they should not be."

    "Let us now start."


    $ adj1 = renpy.input("Give an adjective.")

    $ adj1 = adj1.strip()
    if adj1 == "":
        $ adj1="dank"



    $ home = renpy.input("Give a type of shelter.")

    $ home = home.strip()
    if home == "":
        $ home="shack"

    $ v = renpy.input("Give a verb in past tense.")

    $ v = v.strip()
    if v == "":
        $ v="ran"

    $ adj2 = renpy.input("Give an adjective.")

    $ adj2 = adj2.strip()
    if adj2 == "":
        $ adj2="lovely"

    $ pn = renpy.input("Give a pet name.")

    $ pn = pn.strip()
    if pn == "":
        $ pn="loverbug"

    $ v2 = renpy.input("Give a verb in past tense.")

    $ v2 = v2.strip()
    if v2 == "":
        $ v2="winked"

    $ v3 = renpy.input("Give another verb in past tense.")

    $ v3 = v3.strip()
    if v3 == "":
        $ v3="scurried"

    $ ving = renpy.input("Give a verb in verb-ing form.")

    $ ving = ving.strip()
    if ving == "":
        $ ving="dancing"

    $ body = renpy.input("Give a body part.")

    $ body = body.strip()
    if body == "":
        $ body="elbow"

    $ f = renpy.input("Give the name of a female you know/have heard of. Capitalize their name as necessary.")

    $ f = f.strip()
    if f == "":
        $ f="Anjali"

    $ adj11 = renpy.input("Give an adjective.")

    $ adj11 = adj11.strip()
    if adj11 == "":
        $ adj11="terrible"

    $ what = renpy.input("What would you say in response if someone commented fairly negatively about something you're wearing? Capitalize and punctuate your answer as you wish, but you don't have to. Make this input as YOU as possible!")

    $ what = what.strip()
    if what == "":
        $ what="well, okay..."

    $ adj3 = renpy.input("Give an adjective.")

    $ adj3 = adj3.strip()
    if adj3 == "":
        $ adj3="dirty"

    $ feel1 = renpy.input("Give a feeling.")

    $ feel1 = feel1.strip()
    if feel1 == "":
        $ feel1="washed"

    $ adj4 = renpy.input("Give an adjective.")

    $ adj4 = adj4.strip()
    if adj4 == "":
        $ adj4="cute"

    $ number = renpy.input("Give a number.")

    $ number = number.strip()
    if number == "":
        $ number="6"

    $ profession = renpy.input("Give a job.")

    $ profession = profession.strip()
    if profession == "":
        $ profession="CEO"

    $ lot = renpy.input("Give a length of time.")

    $ lot = lot.strip()
    if lot == "":
        $ lot="928 yrs"

    $ m = renpy.input("Give the name of a male you know/have heard of. Capitalize their name as necessary.")

    $ m = m.strip()
    if m == "":
        $ m="Joe Biden"

    $ p = renpy.input("Give the name of one of your friends. Capitalize their name as necessary.")

    $ p = p.strip()
    if p == "":
        $ p="Alex"

    $ ns = renpy.input("Give a noun in plural form. Capitalize as necessary.")

    $ ns = ns.strip()
    if ns == "":
        $ ns="winked"

    $ food = renpy.input("Give a food.")

    $ food = food.strip()
    if food == "":
        $ food="chicken parm"

    $ adj90 = renpy.input("Give an adjective.")

    $ adj90 = adj90.strip()
    if adj90 == "":
        $ adj90="stinky"

    $ profession2 = renpy.input("Give a job.")

    $ profession2 = profession2.strip()
    if profession2 == "":
        $ profession2="banker"

    $ adv = renpy.input("Give an adverb.")

    $ adv = adv.strip()
    if adv == "":
        $ adv="merrily"

    $ exc = renpy.input("Give an exclamation. Capitalize as you want, and definitely punctuate. Be as you as you want.")

    $ exc = exc.strip()
    if exc == "":
        $ exc="ZOOWEEMAMA!!"

    $ pn2 = renpy.input("Give a pet name.")

    $ pn2 = pn2.strip()
    if pn2 == "":
        $ pn2="booboo"

    $ ns2 = renpy.input("Give a noun in plural form.")

    $ ns2 = ns2.strip()
    if ns2 == "":
        $ ns2="drinks"

    $ body2 = renpy.input("Give a body part.")

    $ body2 = body2.strip()
    if body2 == "":
        $ body2="hair"

    $ adv30 = renpy.input("Give an adverb.")

    $ adv30 = adv30.strip()
    if adv30 == "":
        $ adv30="angrily"

    $ adj10 = renpy.input("Give an adjective.")

    $ adj10 = adj10.strip()
    if adj10 == "":
        $ adj10="cute"

    $ adv2 = renpy.input("Give an adverb.")

    $ adv2 = adv2.strip()
    if adv2 == "":
        $ adv2="swiftly"

    "Your story shall now resume."

    stop music fadeout 2.0

    #marek's room

    play music "lilxmas.mp3"

    queue music ["iuxmas.mp3"]

    scene r

    show marey

    "It was %(adj1)s outside when Marek woke up in his %(home)s. It was Christmas Eve."
    "Another day of work."
    "He %(v)s over to the bathroom to shower and choose his outfit of the day from the mess of clothes scattered across his floor."
    "Deciding to add a little something extra to his day, Marek decided to accessorize his outfit too."

    #dressup scene for accessorizing (3 accessories?)

    jump dressup

    label dressup:

        #scene purple
    scene r
    #show screen dressup_button
    show screen dressup
    #$ dressup_button_show = True
    $ dressup_show = True

    label ok:

        "Click the accesories to take them off/put them on. When done, hit enter."

        menu:
            "Are you done? Click 'Not yet!' to return if you are not done. Click 'Done!' if you are done."
            "Not yet!":
                jump ok
            "Done!":
                jump right


    label right:

    hide screen dressup

    scene r

    show m


    "'Lookin' %(adj2)s, %(pn)s,' Marek %(v2)s at his reflection in the mirror."
    "With that, he had some breakfast, brushed his teeth, grabbed his work tools, and %(v3)s off into the city with much gusto."

    #city

    scene fl
    show m


    "Once in the city, he began cleaning and %(ving)s shoes as usual, and managed to get a decent handful of customers by sundown."

    #city sundown

    scene fl2

    show m

    "Just as he was about to head back home for the day, he felt a tap on his %(body)s."
    "'Well, I don't mean to be so rude and come up to you like this, but I was wondering if you would also shine my shoes, sir.'"
    "The voice of a female spoke. Marek turned and gasped. Why, he knew this female! It was %(f)s!"
    show p1 at left
    "'%(f)s! So unexpected to see you here, but some %(adj11)s surprise nonetheless. How do you do?' Marek asked."
    "'I am doing quite well, thank you for asking. Merry Christmas Eve. Unique choice of accessory you have there...' %(f)s remarked, glancing at the accessory Marek chose to wear today."
    "'%(what)s' Marek said in response."
    "'Anyway... as I asked earlier, I would like my shoes shined, please,' %(f)s said."
    "'Right, of course,' Marek said. He then bent down at %(f)s's feet, and pulled out his rag and shoe shiner."
    "%(f)s was wearing quite %(adj3)s shoes, and Marek could not help but feel %(feel1)s upon seeing them. He began shining them."
    "'Well, do you hear of the war? With the oh so %(adj4)s Nazis,' %(f)s said."
    "'Yes, I have. Many of my customers have brought it up with me lately, as you may be surprised to know,' Marek said sarcastically-- but with good nature!"
    "'Oh, I would imagine so. Would you consider signing up to fight?' %(f)s asked, ignoring his sarcasm."
    "'Perhaps,' Marek responded."
    "'Hm,' %(f)s looked at him. He returned her gaze for a second, then went back to focusing on her shoes."
    "'Another thing you may be surprised to know is not many ladies ask me to shine their shoes for them,' Marek said, a hint of inquisitiveness in his voice, omitting the sarcasm this time."
    "Catching onto the question, %(f)s responded, 'Yes, well, I suppose I am lucky to have finally caught you today. Call it a Christmas miracle! I actually came to Ft. Lauderdale to find you some %(number)s days ago.'"
    "She stepped back from him, breaking off his work on her shoes. 'I wanted to ask you for a favor, and well, I suppose shoe shining broke the ice,' she said, a small grin on her face."
    "Marek stepped up. 'What may that favor be?'"
    "'Would you go out to war with me?' She shyly asked."
    "'With you? How with you?' Marek asked, bewildered at the question."
    "'I am going as a %(profession)s, and I know when I last spoke with you, even if, like, %(lot)s ago, you did not want to be here! I know that, Marek,' %(f)s brought her hand to his shoulder."
    "'And I want to escape. I want to escape this place-- this country-- and there is not better person I know who I could trust with this want than you. And you can escape too,' she whispered."
    "'But why do you want to escape? Last I thought you loved this country,' Marek said, confused."
    "'I... I was set up to be married, and I just cannot carry on with it,' %(f)s said, looking away from him."
    "'To who, %(f)s?' Marek asked."
    "'To, well, %(m)s,' %(f)s said. Marek's eyes widened."
    "'Really? Well, then I wholeheartedly understand why you would want to leave, %(f)s. Can we talk more about this over some dinner? Would you like to come over? And where even have you been staying up til now?' Marek said."
    "'Dinner would be lovely, thank you. I have been hiding in your friend, %(p)s's, place, believe it or not. At first it was just an open door to sneak in through, and then it turned out to be %(p)s's door,' %(f)s shrugged."
    "'Really now?' Marek asked, surprised again."
    "'You would not even begin to fathom the-- the wild intensity in which they have in interest in %(ns)s! It is like, %(ns)s this, %(ns)s that... even a box that just spews books on %(ns)s each time it is opened! Ridiculous!' %(f)s exclaimed."
    "'Interesting,' Marek said, wondering where such an obsession could have stemmed from."
    "'Interesting indeed. Now, show me where your house is! I am quite glad to be out of that house,' %(f)s said."
    "With that, Marek led her to his house."

    #marek's room

    scene r1

    show p1 at left

    show m



    "'So, now that our bellies are full on %(food)s, please tell me more about your, if I must say, crazy idea to involve me in your plan to leave with the war,' Marek said, holding in a nice, big, %(adj90)s fart."
    "'Well, I plan on leaving tomorrow now that I have found you, and only if you agree. But I believe we can sneak out. I have a plan. You can say you are coming along as a %(profession2)s,' %(f)s said, eyes staring back at Marek vacuously."
    "Marek shifted in his seat %(adv)s in response to the idea. 'What... is the plan though?'"
    "'We... we will find an opening! Do not worry, trust me. To my understanding %(profession)ss are highly regarded in war, and so are %(profession2)ss,' %(f)s said."
    "'I... I suppose so. Well...' Marek broke off, taking a look around his room, remembering the emptiness he always felt living here. Despite the holiday cheer that had been going around, he had yet to catch on thoroughly, and knew such cheer would only be temporary anyway."
    "'Well, alright, I shall go with you,' Marek finished his sentence."
    "'%(exc)s! Thank you, Marek! You will not regret this!' %(f)s smiled."

    stop music fadeout 2.0

    #on a boat

    scene b

    play music "ocean.mp3"

    show m

    "Marek regretted this. It has been far too long for him to be on this boat without some delicious %(food)s, and %(f)s had slowly began coming onto him lately."
    "He stared at the ocean, basking in the cold winter breeze that would wash over him from the waves."

    show p1 at left
    show m

    "'Oh, Marek, %(pn2)s. Come to the dining cabin with me. It's Christmas, you know! Let's celebrate together. And please get me some %(ns2)s to eat,' %(f)s batted her eyelashes at him, holding his %(body2)s. With that, she walked away %(adv30)s."

    hide p1
    show m

    "As she was walking away, Marek noticed her %(adj3)s shoes. Those shoes. Those shoes that made him feel so %(feel1)s. To feel so %(feel1)s on Christmas day... it just was not right."
    "He turned his head towards the water again. Deep, mysterious, %(adj10)s... things that %(f)s could never be even if she tried."
    "Without a second thought, he hurled himself off %(adv2)s."

    hide m

    "He could not take it anymore."

    #water splash sound
    play sound "splash.mp3"

    ""

    "Sweet escape."

    "THE END."




    return
