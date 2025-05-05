import pygame
import random
import sys
import time
import math
from collections import deque
from heapq import heappush, heappop

class Question:
    def __init__(self, question, options, correct, explanation=""):
        self.question = question
        self.options = options
        self.correct = correct
        self.explanation = explanation

class LevelConfig:
    def __init__(self, maze_size, computer_speed, question_difficulty, 
                 checkpoint_count, sabotage_cooldown, wall_duration):
        self.maze_size = maze_size
        self.computer_speed = computer_speed
        self.question_difficulty = question_difficulty
        self.checkpoint_count = checkpoint_count
        self.sabotage_cooldown = sabotage_cooldown
        self.wall_duration = wall_duration

class GameData:
    questions = {
        "ages_3_5": {
            "easy": [
            Question("What color is a banana?", ["Yellow", "Blue"], "Yellow", "Bananas are yellow when they're ripe"),
            Question("How many ears do you have?", ["1", "2"], "2", "People have two ears, one on each side of their head"),
            Question("Which animal says 'meow'?", ["Cat", "Dog"], "Cat", "Cats make a 'meow' sound"),
            Question("What shape is a ball?", ["Square", "Round"], "Round", "Balls are round so they can roll"),
            Question("Which is bigger?", ["Elephant", "Mouse"], "Elephant", "Elephants are very large animals"),
            Question("What color is an apple?", ["White", "Red"], "Red", "Many apples are red in color"),
            Question("What shape is an ice cream cone?", ["Cone", "Circle"], "Cone", "Ice cream cones are cone-shaped to hold ice cream"),
            Question("What animal says 'woof'?", ["Dog", "Duck"], "Dog", "Dogs make a 'woof' sound"),
            Question("Which of these is a fruit?", ["Potato", "Mango"], "Mango", "Mangoes are sweet fruits that grow in tropical climates"),
            Question("What do you use to brush your teeth?", ["Toothbrush", "Hairbrush"], "Toothbrush", "Dental hygiene requires specific tools")
            ],
            "medium": [
            Question("What comes after number 5?", ["6", "7"], "6", "The numbers go 4, 5, 6, 7"),
            Question("Which fruit is red?", ["Apple", "Banana"], "Apple", "Many apples are red in color"),
            Question("What do you wear on your feet?", ["Hat", "Shoes"], "Shoes", "Shoes protect your feet when walking"),
            Question("Where do fish live?", ["Water", "Trees"], "Water", "Fish breathe underwater using gills"),
            Question("When it's cold outside, we wear a...", ["Swimsuit", "Coat"], "Coat", "Coats keep us warm in cold weather"),
            Question("What comes after C in alphabets?", ["D", "A"], "D", "Letters in the English alphabet follow a specific order"),
            Question("What is a baby dog called?", ["Puppy", "Kitten"], "Puppy", "Different animal babies have specific names"),
            Question("What do you use to draw pictures?", ["Pencil", "Spoon"], "Pencil", "Art supplies serve specific creative purposes"),
            Question("Which of these is a number?", ["One", "Ball"], "One", "Numbers are used for counting and mathematics"),
            Question("What number comes before 3?", ["2", "10"], "2", "Numbers follow a sequential order")
            ],
            "hard": [
            Question("Which has wings?", ["Bird", "Fish"], "Bird", "Birds have wings to help them fly"),
            Question("What do we use to write?", ["Pencil", "Spoon"], "Pencil", "Pencils make marks on paper"),
            Question("Which animal has a long neck?", ["Giraffe", "Turtle"], "Giraffe", "Giraffes have very long necks to reach tall trees"),
            Question("What color is grass?", ["Green", "Purple"], "Green", "Grass is usually green because of chlorophyll"),
            Question("Where does rain come from?", ["Clouds", "Trees"], "Clouds", "Rain falls from clouds in the sky"),
            Question("What shape is a ball?", ["Rectangle", "Sphere"], "Sphere", "Three-dimensional objects have specific geometric shapes"),
            Question("Where do fish live?", ["Water", "Air"], "Water", "Animals adapt to specific habitats"),
            Question("What do you wear on your head?", ["Hat", "Pants"], "Hat", "Clothing items are designed for specific body parts"),
            Question("What do you drink from a cup?", ["Shoes", "Water"], "Water", "Containers are designed for specific purposes")
            ]
        },

        "ages_6_8": {
            "easy": [
            Question("What is 5 + 3?", ["7", "8"], "8", "Adding 5 and 3 equals 8"),
            Question("Which planet do we live on?", ["Mars", "Earth"], "Earth", "Earth is the third planet from the sun"),
            Question("How many days are in a week?", ["5", "7"], "7", "There are 7 days in a week: Monday through Sunday"),
            Question("What animal has black and white stripes?", ["Zebra", "Giraffe"], "Zebra", "Zebras have distinctive black and white striped pattern"),
            Question("Which is a fruit?", ["Carrot", "Apple"], "Apple", "Apples grow on trees and contain seeds"),
            Question("What comes after number 5?", ["6", "7"], "6", "The numbers go 4, 5, 6, 7"),
            Question("Which fruit is red?", ["Apple", "Banana"], "Apple", "Many apples are red in color"),
            Question("What do you wear on your feet?", ["Hat", "Shoes"], "Shoes", "Shoes protect your feet when walking"),
            Question("Where do fish live?", ["Water", "Trees"], "Water", "Fish breathe underwater using gills"),
            Question("When it's cold outside, we wear a...", ["Swimsuit", "Coat"], "Coat", "Coats keep us warm in cold weather"),
            Question("Who flies an aeroplane?", ["driver", "pilot"], "pilot", "Pilots are trained professionals who fly aircraft"),
            Question("What is 25+15?", ["40", "50"], "40", "25 plus 15 equals 40")
            ],
            "medium": [
            Question("What is 4 × 2?", ["6", "8"], "8", "Multiplication: 4 × 2 = 8"),
            Question("Which sense uses your nose?", ["Hearing", "Smell"], "Smell", "Your nose helps you smell different scents"),
            Question("What do plants need to grow?", ["Candy", "Water"], "Water", "Plants need water, sunlight, and soil to grow"),
            Question("Which month comes after April?", ["May", "June"], "May", "The months go: April, May, June"),
            Question("What is water made of?", ["Hydrogen and Oxygen", "Sugar and Salt"], "Hydrogen and Oxygen", "Water (H₂O) is made of hydrogen and oxygen"),
            Question("Which planet is nearer to the Earth?", ["Mars", "Saturn"], "Mars", "Mars is the closest neighboring planet to Earth"),
            Question("Which planet is known as the 'red planet'?", ["mars", "earth"], "mars", "Mars appears red due to iron oxide on its surface"),
            Question("How many continents are there?", ["seven", "two"], "seven", "The seven continents are Africa, Antarctica, Asia, Australia, Europe, North America, and South America"),
            Question("What is the capital of France?", ["paris", "london"], "paris", "Paris is the capital and largest city of France"),
            Question("Which of these is a verb?", ["draw", "cat"], "draw", "Draw is an action word, which is a verb"),
            Question("What is the opposite of cold?", ["cool", "hot"], "hot", "Hot is the opposite of cold on the temperature spectrum"),
            Question("What do plants need to grow?", ["paper and toys", "Sunlight and water"], "Sunlight and water", "Plants require sunlight and water for photosynthesis and growth")
            ],
            "hard": [
            Question("How many sides does a triangle have?", ["3", "4"], "3", "A triangle has exactly 3 sides and 3 angles"),
            Question("Which animal lays eggs?", ["Cat", "Chicken"], "Chicken", "Chickens, like most birds, lay eggs"),
            Question("What is the opposite of hot?", ["Cold", "Wet"], "Cold", "Hot and cold are temperature opposites"),
            Question("What is 12 - 5?", ["7", "8"], "7", "Subtracting 5 from 12 equals 7"),
            Question("What do we call frozen water?", ["Steam", "Ice"], "Ice", "Water freezes at 0°C to become ice"),
            Question("Which of these is a type of triangle?", ["Equilateral", "circle"], "Equilateral", "An equilateral triangle has three equal sides and angles"),
            Question("Name the force which pulls objects towards the Earth?", ["gravity", "electricity"], "gravity", "Gravity is the force that attracts objects toward the center of the Earth"),
            Question("Who painted the Mona Lisa?", ["Michelangelo", "Leonardo da Vinci"], "Leonardo da Vinci", "Leonardo da Vinci painted the Mona Lisa in the early 16th century"),
            Question("In what country would you find the Eiffel Tower?", ["france", "italy"], "france", "The Eiffel Tower is located in Paris, France"),
            Question("Which of these is a type of a Fish?", ["shark", "pug"], "shark", "Sharks are a group of elasmobranch fish"),
            Question("How many sides does a hexagon have?", ["6", "7"], "6", "A hexagon is a polygon with six sides"),
            Question("If you had 10 apples and you gave 4 of them to your friend, how many apples are you left with?", ["6", "3"], "6", "10 apples minus 4 apples equals 6 apples")
            ]
        },

        "ages_9_10": {
            "easy": [
                Question("What is 7 × 8?", ["56", "64"], "56", "Multiplication: 7 × 8 = 56"),
                Question("Which planet is known as the Red Planet?", ["Venus", "Mars"], "Mars", "Mars appears red due to iron oxide (rust) on its surface"),
                Question("What is the largest ocean on Earth?", ["Atlantic", "Pacific"], "Pacific", "The Pacific Ocean is the largest and deepest ocean"),
                Question("What is the main gas in Earth's atmosphere?", ["Oxygen", "Nitrogen"], "Nitrogen", "Nitrogen makes up about 78% of Earth's atmosphere"),
                Question("Who wrote 'Romeo and Juliet'?", ["Charles Dickens", "William Shakespeare"], "William Shakespeare", "William Shakespeare wrote many famous plays, including Romeo and Juliet"),
                Question("What is 16 times 4?", ["64", "32"], "64", "16 multiplied by 4 equals 64"),
                Question("Which is the largest planet in our solar system?", ["jupiter", "mars"], "jupiter", "Jupiter is the largest planet in our solar system"),
                Question("What is 25 times 4?", ["100", "200"], "100", "25 multiplied by 4 equals 100")
            ],
            "medium": [
                Question("What is the square root of 81?", ["9", "8"], "9", "9 × 9 = 81, so the square root of 81 is 9"),
                Question("Which element has the chemical symbol O?", ["Oxygen", "Osmium"], "Oxygen", "O is the symbol for Oxygen on the periodic table"),
                Question("What is the capital of France?", ["London", "Paris"], "Paris", "Paris is the capital city of France"),
                Question("What type of cell generates electricity in the body?", ["Nerve cell", "Muscle cell"], "Nerve cell", "Nerve cells (neurons) transmit electrical signals"),
                Question("What force keeps us on the Earth?", ["Magnetism", "Gravity"], "Gravity", "Gravity pulls objects toward the Earth's center"),
                Question("What process do plants use to make their food?", ["circulation", "Photosynthesis"], "Photosynthesis", "Plants use photosynthesis to convert sunlight into energy"),
                Question("What is the perimeter of a square with sides of 5 cm each?", ["20", "40"], "20", "The perimeter is calculated by adding all sides: 5+5+5+5=20"),
                Question("Which of these is a synonym for 'happy'?", ["sad", "joyful"], "joyful", "Joyful means the same as happy"),
                Question("What punctuation mark is used at the end of a simple sentence?", ["period", "question mark"], "period", "A period (.) is used to end declarative sentences"),
                Question("Which continent is India located in?", ["asia", "africa"], "asia", "India is a country in the continent of Asia")
            ],
            "hard": [
                Question("What is the square root of 144?", ["12", "14"], "12", "√144 = 12, as 12² = 144"),
                Question("Which element has the symbol Au?", ["Silver", "Gold"], "Gold", "Au is the symbol for Gold (from Latin 'Aurum')"),
                Question("Who discovered penicillin?", ["Alexander Fleming", "Marie Curie"], "Alexander Fleming", "Alexander Fleming discovered penicillin in 1928"),
                Question("What is photosynthesis?", ["How plants sleep", "How plants make food"], "How plants make food", "Plants use sunlight to convert water and carbon dioxide into food"),
                Question("Which planet has the most moons?", ["Jupiter", "Saturn"], "Saturn", "Saturn has over 80 moons, more than any other planet"),
                Question("How many days are there in a year?", ["365 or 366", "370"], "365 or 366", "Regular years have 365 days, leap years have 366"),
                Question("Which part of the body pumps blood?", ["heart", "skull"], "heart", "The heart is responsible for pumping blood through the body"),
                Question("What is 36 divided by 6?", ["6", "7"], "6", "36 divided by 6 equals 6"),
                Question("What is the chemical symbol for water?", ["H2O", "CO2"], "H2O", "Water's chemical formula is H2O"),
                Question("What is the largest organ in the human body?", ["skin", "brain"], "skin", "The skin is the largest organ in the human body"),
                Question("How many chambers does a human heart have?", ["four", "six"], "four", "The human heart has four chambers"),
                Question("What do white blood cells in our body do?", ["fight infections", "digest food"], "fight infections", "White blood cells are part of the immune system and fight infections")
            ]
        }
    }

    legacy_questions = {
        "easy": [
            Question("What is 2 + 2?", ["3", "4"], "4", "Basic addition: 2 + 2 = 4"),
            Question("What is the capital of France?", ["London", "Paris"], "Paris", "Paris is the capital of France"),
            Question("Which planet is closest to the sun?", ["Venus", "Mercury"], "Mercury", "Mercury is the closest planet to the sun"),
            Question("What color are bananas?", ["Yellow", "Blue"], "Yellow", "Ripe bananas have a yellow peel"),
            Question("How many legs does a spider have?", ["6", "8"], "8", "Spiders have 8 legs, insects have 6"),
            Question("Which animal says 'moo'?", ["Cow", "Duck"], "Cow", "Cows make the 'moo' sound")
        ],
        "medium": [
            Question("What is 7 × 8?", ["56", "64"], "56", "Multiplication: 7 × 8 = 56"),
            Question("Which element has the chemical symbol 'O'?", ["Oxygen", "Osmium"], "Oxygen", "O is the symbol for Oxygen"),
            Question("Who wrote 'Romeo and Juliet'?", ["Charles Dickens", "William Shakespeare"], "William Shakespeare", "Romeo and Juliet was written by William Shakespeare"),
            Question("What is the largest organ in the human body?", ["Heart", "Skin"], "Skin", "The skin is the largest organ covering the entire body"),
            Question("How many continents are there on Earth?", ["6", "7"], "7", "There are 7 continents: Africa, Antarctica, Asia, Australia, Europe, North America, and South America"),
            Question("What is the largest ocean on Earth?", ["Atlantic", "Pacific"], "Pacific", "The Pacific Ocean is the largest and deepest ocean")
        ],
        "hard": [
            Question("What is the square root of 144?", ["12", "14"], "12", "√144 = 12, as 12² = 144"),
            Question("Which element has the symbol Au?", ["Silver", "Gold"], "Gold", "Au is the symbol for Gold (from Latin 'Aurum')"),
            Question("Who discovered penicillin?", ["Alexander Fleming", "Marie Curie"], "Alexander Fleming", "Alexander Fleming discovered penicillin in 1928"),
            Question("What is the capital of Australia?", ["Sydney", "Canberra"], "Canberra", "Canberra is the capital city of Australia, not Sydney"),
            Question("Which planet has the most moons?", ["Jupiter", "Saturn"], "Saturn", "Saturn has over 80 moons, more than any other planet in our solar system"),
            Question("What is the hardest natural substance on Earth?", ["Steel", "Diamond"], "Diamond", "Diamond is the hardest known natural material")
        ]
    }
    
    level_config = {
        1: LevelConfig((7, 5), 25, "easy", 2, 20, 10),
        2: LevelConfig((10, 7), 20, "easy", 3, 25, 8),
        3: LevelConfig((13, 9), 15, "medium", 4, 30, 6),
        4: LevelConfig((15, 11), 10, "medium", 5, 35, 5),
        5: LevelConfig((17, 13), 5, "medium", 5, 40, 4),
        6: LevelConfig((19, 15), 2, "hard", 6, 45, 3),
        7: LevelConfig((21, 17), 1, "hard", 7, 50, 2)
    }

class Particle:
    def __init__(self, x, y, color, lifetime=30):
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.size = random.randint(2, 4)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        self.color = (*self.color[:3], alpha) if len(self.color) > 3 else (*self.color, alpha)
        return self.lifetime > 0
        
    def draw(self, screen):
        if len(self.color) < 4:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        else:
            s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.circle(s, self.color, (self.size, self.size), self.size)
            screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))

class PriorityQueue:
    def __init__(self):
        self.elements = []
        self.set = set()
        
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        key = f"{item[0]},{item[1]}"
        if key not in self.set:
            heappush(self.elements, (priority, item))
            self.set.add(key)
    
    def get(self):
        _, item = heappop(self.elements)
        key = f"{item[0]},{item[1]}"
        self.set.remove(key)
        return item

class MazeGame:
    def __init__(self):
        pygame.init()
        display_info = pygame.display.Info()
        self.fullscreen = False
        
        if self.fullscreen:
            self.screen_width = display_info.current_w
            self.screen_height = display_info.current_h
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        else:
            self.screen_width = 800
            self.screen_height = 600
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            
        pygame.display.set_caption("Maze Race Challenge")

        self.maze_offset_x = 0
        self.maze_offset_y = 0

        try:
            self.player_img = pygame.image.load("images/dino.png")
            self.computer_img = pygame.image.load("images/turtle.png")
        except pygame.error:
            self.player_img = self._create_default_image((0, 255, 0))  
            self.computer_img = self._create_default_image((255, 0, 0)) 
        
        self.age_group = "ages_6_8"

        self.level = 1
        self.score = 0
        self.maze = []
        self.player_pos = [1, 1]
        self.computer_pos = [1, 1]
        self.end_pos = [0, 0]
        self.checkpoints = []
        self.checkpoint_status = {}
        self.temporary_walls = []
        self.player_speed_boost = 0
        self.computer_speed_penalty = 0
        self.sabotage_cooldown = 0
        self.frame_counter = 0
        self.computer_path = []
        self.computer_path_index = 0
        self.cell_size = 20  
        self.particles = []  

        self.font_large = pygame.font.SysFont('Arial', 32, bold=True)
        self.font_medium = pygame.font.SysFont('Arial', 24)
        self.font_small = pygame.font.SysFont('Arial', 18)

        try:
            pygame.mixer.init()
            print("Mixer initialized successfully")
            self.sound_checkpoint = pygame.mixer.Sound("sounds/checkpoint.wav")
            print("Checkpoint sound loaded")
            self.sound_win = pygame.mixer.Sound("sounds/win.wav")  # Change to WAV format
            print("Win sound loaded")
            self.sound_lose = pygame.mixer.Sound("sounds/lose.wav")
            print("Lose sound loaded")
            self.sound_wall = pygame.mixer.Sound("sounds/walls.wav")
            print("Wall sound loaded")
            self.sound_enabled = True
        except Exception as e:
            print(f"Error loading sounds: {e}")
            self.sound_enabled = False

        self.show_welcome_screen()
    
    def _create_default_image(self, color):
        """Create a default image if file not found"""
        img = pygame.Surface((20, 20))
        img.fill(color)
        return img
    
    def add_particles(self, x, y, color, count=10):
        """Add particles at the specified position"""
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    def update_particles(self):
        """Update and remove expired particles"""
        self.particles = [p for p in self.particles if p.update()]
    
    def draw_particles(self):
        """Draw all active particles"""
        for p in self.particles:
            p.draw(self.screen)
    
    def show_welcome_screen(self):
        running = True
        bg_color = (0, 0, 30)  
        stars = []
        for _ in range(100):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            stars.append((x, y, size, brightness))
        
        while running:
            self.screen.fill(bg_color)

            for x, y, size, brightness in stars:
                pygame.draw.circle(self.screen, (brightness, brightness, brightness), (x, y), size)

            title = self.font_large.render("MAZE RACE CHALLENGE", True, (255, 255, 255))
            subtitle = self.font_medium.render("Educational Racing Game", True, (200, 200, 255))

            shadow_offset = 2
            shadow_color = (0, 0, 100)

            shadow_title = self.font_large.render("MAZE RACE CHALLENGE", True, shadow_color)
            self.screen.blit(shadow_title, (self.screen_width/2 - title.get_width()/2 + shadow_offset, 
                                    self.screen_height/2 - 120 + shadow_offset))

            self.screen.blit(title, (self.screen_width/2 - title.get_width()/2, 
                                self.screen_height/2 - 120))
            self.screen.blit(subtitle, (self.screen_width/2 - subtitle.get_width()/2, 
                                    self.screen_height/2 - 70))

            age_text = self.font_medium.render("Select your age group:", True, (255, 255, 255))
            self.screen.blit(age_text, (self.screen_width/2 - age_text.get_width()/2, 
                                    self.screen_height/2 - 10))

            button_width = 180
            button_height = 40
            button_spacing = 20
            total_width = 3 * button_width + 2 * button_spacing
            
            ages_3_5_button = pygame.Rect(self.screen_width/2 - total_width/2, 
                                        self.screen_height/2 + 40, 
                                        button_width, button_height)
            ages_6_8_button = pygame.Rect(self.screen_width/2 - button_width/2, 
                                        self.screen_height/2 + 40, 
                                        button_width, button_height)
            ages_9_10_button = pygame.Rect(self.screen_width/2 + total_width/2 - button_width, 
                                        self.screen_height/2 + 40, 
                                        button_width, button_height)

            mouse_pos = pygame.mouse.get_pos()
            hover_3_5 = ages_3_5_button.collidepoint(mouse_pos)
            hover_6_8 = ages_6_8_button.collidepoint(mouse_pos)
            hover_9_10 = ages_9_10_button.collidepoint(mouse_pos)

            pygame.draw.rect(self.screen, (100, 100, 200) if not hover_3_5 else (120, 120, 220), ages_3_5_button, 0, 10)
            pygame.draw.rect(self.screen, (100, 100, 200) if not hover_6_8 else (120, 120, 220), ages_6_8_button, 0, 10)
            pygame.draw.rect(self.screen, (100, 100, 200) if not hover_9_10 else (120, 120, 220), ages_9_10_button, 0, 10)

            pygame.draw.rect(self.screen, (255, 255, 255), ages_3_5_button, 2, 10)
            pygame.draw.rect(self.screen, (255, 255, 255), ages_6_8_button, 2, 10)
            pygame.draw.rect(self.screen, (255, 255, 255), ages_9_10_button, 2, 10)

            text_3_5 = self.font_small.render("Ages 3-5", True, (255, 255, 255))
            text_6_8 = self.font_small.render("Ages 6-8", True, (255, 255, 255))
            text_9_10 = self.font_small.render("Ages 9-10", True, (255, 255, 255))
            
            self.screen.blit(text_3_5, (ages_3_5_button.x + ages_3_5_button.width/2 - text_3_5.get_width()/2, 
                                    ages_3_5_button.y + ages_3_5_button.height/2 - text_3_5.get_height()/2))
            self.screen.blit(text_6_8, (ages_6_8_button.x + ages_6_8_button.width/2 - text_6_8.get_width()/2, 
                                    ages_6_8_button.y + ages_6_8_button.height/2 - text_6_8.get_height()/2))
            self.screen.blit(text_9_10, (ages_9_10_button.x + ages_9_10_button.width/2 - text_9_10.get_width()/2, 
                                    ages_9_10_button.y + ages_9_10_button.height/2 - text_9_10.get_height()/2))

            quit_text = self.font_small.render("Press ESC to quit", True, (200, 200, 200))
            self.screen.blit(quit_text, (self.screen_width/2 - quit_text.get_width()/2, 
                                    self.screen_height/2 + 120))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if ages_3_5_button.collidepoint(event.pos):
                        self.age_group = "ages_3_5"
                        running = False
                        self.show_instructions()
                    elif ages_6_8_button.collidepoint(event.pos):
                        self.age_group = "ages_6_8"
                        running = False
                        self.show_instructions()
                    elif ages_9_10_button.collidepoint(event.pos):
                        self.age_group = "ages_9_10"
                        running = False
                        self.show_instructions()

    def show_instructions(self):
        running = True
        
        while running:
            self.screen.fill((240, 240, 255))

            title = self.font_large.render("HOW TO PLAY", True, (0, 0, 100))
            self.screen.blit(title, (self.screen_width/2 - title.get_width()/2, 50))

            instructions = [
                "1. Use ARROW KEYS or WASD to move the player (green)",
                "2. Race against the computer (red) to reach the end",
                "3. Capture checkpoints by answering questions",
                "4. Press SPACE to place walls and block the computer",
                "5. Answer questions correctly to get speed boosts",
                "",
                "The player who reaches the end first wins!"
            ]
            
            y = 150
            for line in instructions:
                text = self.font_medium.render(line, True, (0, 0, 0))
                self.screen.blit(text, (self.screen_width/2 - text.get_width()/2, y))
                y += 40

            button = pygame.Rect(self.screen_width/2 - 100, self.screen_height - 100, 200, 50)
            pygame.draw.rect(self.screen, (50, 100, 200), button)
            pygame.draw.rect(self.screen, (0, 0, 100), button, 2)  # Border
            
            button_text = self.font_medium.render("Start Game", True, (255, 255, 255))
            self.screen.blit(button_text, (button.x + button.width/2 - button_text.get_width()/2,
                                       button.y + button.height/2 - button_text.get_height()/2))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        running = False
                        self.show_level_transition(self.level)
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button.collidepoint(event.pos):
                        running = False
                        self.show_level_transition(self.level)
    
    def show_level_transition(self, level):
        running = True
        start_time = time.time()

        radius = 0
        max_radius = int(math.sqrt(self.screen_width**2 + self.screen_height**2) / 2)
        speed = max_radius / 1.5
        
        while running and time.time() - start_time < 2.0:
            self.screen.fill((0, 0, 0))

            radius = min(int((time.time() - start_time) * speed), max_radius)
            pygame.draw.circle(self.screen, (0, 0, 50), 
                            (self.screen_width//2, self.screen_height//2), 
                            radius)

            if radius > 100:
                level_text = self.font_large.render(f"Level {level}", True, (255, 255, 255))
                difficulty = "★" * level
                diff_text = self.font_medium.render(f"Difficulty: {difficulty}", True, (255, 255, 0))
                
                self.screen.blit(level_text, (self.screen_width/2 - level_text.get_width()/2, 
                                          self.screen_height/2 - 30))
                self.screen.blit(diff_text, (self.screen_width/2 - diff_text.get_width()/2, 
                                         self.screen_height/2 + 20))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        running = False
                        
        self.setup_level(level)
    
    def setup_level(self, level):
        config = GameData.level_config.get(level)
        if not config:
            return

        width, height = config.maze_size
        self.maze = self.generate_maze(width, height)

        self.cell_size = min(
            (self.screen_width - 100) // (2 * width + 1),
            (self.screen_height - 100) // (2 * height + 1)
        )

        maze_width = (2 * width + 1) * self.cell_size
        maze_height = (2 * height + 1) * self.cell_size
        self.maze_offset_x = (self.screen_width - maze_width) // 2
        self.maze_offset_y = (self.screen_height - maze_height) // 2

        self.player_img = pygame.transform.scale(self.player_img, (self.cell_size, self.cell_size))
        self.computer_img = pygame.transform.scale(self.computer_img, (self.cell_size, self.cell_size))
  
        self.player_pos = [1, 1]
        self.computer_pos = [1, 1]
        self.end_pos = [2 * width - 1, 2 * height - 1]

        start_pos = (1, 1)
        goal_pos = (self.end_pos[0], self.end_pos[1])
        self.computer_path = self.astar(self.maze, start_pos, goal_pos)
        self.computer_path_index = 0
        
        path = self.dijkstra(self.maze, start_pos, goal_pos)

        num_checkpoints = config.checkpoint_count
        self.checkpoints = []
        self.checkpoint_status = {}
        
        for i in range(1, num_checkpoints + 1):
            index = i * len(path) // (num_checkpoints + 1)
            if index < len(path):
                self.checkpoints.append(path[index])
                key = f"{path[index][0]},{path[index][1]}"
                self.checkpoint_status[key] = None

        self.temporary_walls = []
        self.player_speed_boost = 0
        self.sabotage_cooldown = config.sabotage_cooldown
        self.frame_counter = 0
        self.particles = []

        self.run_game()
    
    def run_game(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_event(event)

            self.update_game()

            self.draw_game()

            if self.player_pos[0] == self.end_pos[0] and self.player_pos[1] == self.end_pos[1]:
                if self.sound_enabled:
                    self.sound_win.play()
                self.score += 100 * self.level
                if self.show_winner(True):
                    running = False
            elif self.computer_pos[0] == self.end_pos[0] and self.computer_pos[1] == self.end_pos[1]:
                if self.sound_enabled:
                    self.sound_lose.play()
                if self.show_winner(False):
                    running = False
            
            pygame.display.flip()
            clock.tick(60)

    def update_game(self):
            self.frame_counter += 1
            config = GameData.level_config.get(self.level)
            if not config:
                return

            if self.player_speed_boost > 0:
                self.player_speed_boost -= 1
            
            if self.computer_speed_penalty > 0:
                self.computer_speed_penalty -= 1

            self.update_particles()

            if self.sabotage_cooldown > 0:
                self.sabotage_cooldown -= 1

            for i in range(len(self.temporary_walls) - 1, -1, -1):
                wall = self.temporary_walls[i]
                if wall[2] <= 0:
                    self.temporary_walls.pop(i)
                    
            computer_move_freq = config.computer_speed
            
            if self.player_speed_boost > 0 and self.frame_counter % 2 == 0:
                self.move_player_ai()
                
            if self.computer_speed_penalty > 0:
                if self.frame_counter % (computer_move_freq * 2) == 0: 
                    self.move_computer_player()
            elif self.frame_counter % computer_move_freq == 0:
                self.move_computer_player()
        
    def move_player_ai(self):
        if self.player_speed_boost > 0:
            self.player_speed_boost -= 1
        
        if self.computer_speed_penalty > 0:
            self.computer_speed_penalty -= 1
        self.update_particles()

        if self.player_speed_boost > 0:
            self.player_speed_boost -= 1

        if self.sabotage_cooldown > 0:
            self.sabotage_cooldown -= 1

        for i in range(len(self.temporary_walls) - 1, -1, -1):
            wall = self.temporary_walls[i]
            if wall[2] <= 0:
                self.temporary_walls.pop(i)
        config = GameData.level_config.get(self.level)
        computer_move_freq = config.computer_speed
        
        if self.player_speed_boost > 0 and self.frame_counter % 2 == 0:
            self.move_player_ai()
            
        if self.computer_speed_penalty > 0:
            if self.frame_counter % (computer_move_freq * 2) == 0:  # Double the delay
                self.move_computer_player()
        elif self.frame_counter % computer_move_freq == 0:
            self.move_computer_player()
        
        computer_move_freq = config.computer_speed
        if self.player_speed_boost > 0:
            if self.frame_counter % 2 == 0:
                self.move_computer_player()
        elif self.frame_counter % computer_move_freq == 0:
            self.move_computer_player()
    
    def draw_game(self):
        for i in range(self.screen_height):
            r = int(180 + (220 - 180) * (1 - i / self.screen_height))
            g = int(210 + (240 - 210) * (1 - i / self.screen_height))
            b = 255
            pygame.draw.line(self.screen, (r, g, b), (0, i), (self.screen_width, i))

        rainbow_colors = [
            (89, 173, 246), 
        ]
        
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                if self.maze[y][x] == 1:
                    color = random.choice(rainbow_colors)
                    pygame.draw.rect(self.screen, color,
                                (self.maze_offset_x + x * self.cell_size, 
                                    self.maze_offset_y + y * self.cell_size, 
                                    self.cell_size, self.cell_size))

        for wall in self.temporary_walls:
            opacity = int(255 * (wall[2] / GameData.level_config[self.level].wall_duration))
            wall_color = (255, 0, 0, opacity)

            wall_surf = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            wall_surf.fill(wall_color)
            
            self.screen.blit(wall_surf, 
                        (self.maze_offset_x + wall[0] * self.cell_size,
                            self.maze_offset_y + wall[1] * self.cell_size))
        
        pulse = (math.sin(self.frame_counter / 10) + 1) * 0.5  # 0 to 1
        end_color = (
            int(0 + pulse * 50),     
            int(200 + pulse * 55),   
            int(0 + pulse * 50)      
        )
        pygame.draw.rect(self.screen, end_color,
                    (self.maze_offset_x + self.end_pos[0] * self.cell_size, 
                        self.maze_offset_y + self.end_pos[1] * self.cell_size, 
                        self.cell_size, self.cell_size))
        
        for checkpoint in self.checkpoints:
            key = f"{checkpoint[0]},{checkpoint[1]}"
            
            if self.checkpoint_status[key] == "player":
                color = (50, 220, 50)

                if self.frame_counter % 30 == 0: 
                    x = self.maze_offset_x + checkpoint[0] * self.cell_size + self.cell_size/2
                    y = self.maze_offset_y + checkpoint[1] * self.cell_size + self.cell_size/2
                    self.add_particles(x, y, (220, 255, 100, 150), 2)
                    
            elif self.checkpoint_status[key] == "computer":
                color = (220, 50, 50)
                
            else:
                color = (80, 120, 255)

                if self.frame_counter % 60 == 0:
                    x = self.maze_offset_x + checkpoint[0] * self.cell_size + self.cell_size/2
                    y = self.maze_offset_y + checkpoint[1] * self.cell_size + self.cell_size/2
                    self.add_particles(x, y, (180, 180, 255, 150), 2)

            pygame.draw.rect(self.screen, color,
                           (self.maze_offset_x + checkpoint[0] * self.cell_size, 
                            self.maze_offset_y + checkpoint[1] * self.cell_size, 
                            self.cell_size, self.cell_size))

            highlight_size = max(2, int(self.cell_size * 0.3))
            highlight_rect = pygame.Rect(
                self.maze_offset_x + checkpoint[0] * self.cell_size + highlight_size,
                self.maze_offset_y + checkpoint[1] * self.cell_size + highlight_size,
                self.cell_size - highlight_size*2,
                self.cell_size - highlight_size*2
            )

            inner_color = tuple(min(255, c + 50) for c in color)
            pygame.draw.rect(self.screen, inner_color, highlight_rect, 0, 
                            int(highlight_size/2))  
            
        player_to_computer = self.heuristic((self.player_pos[0], self.player_pos[1]), 
                                        (self.computer_pos[0], self.computer_pos[1]))

        player_distance = self.heuristic((self.player_pos[0], self.player_pos[1]), 
                                    (self.end_pos[0], self.end_pos[1]))
        computer_distance = self.heuristic((self.computer_pos[0], self.computer_pos[1]), 
                                        (self.end_pos[0], self.end_pos[1]))

        wrong_direction = False
        if hasattr(self, 'last_player_distance') and hasattr(self, 'second_last_player_distance'):
            wrong_direction = (player_distance > self.last_player_distance and 
                            self.last_player_distance > self.second_last_player_distance)
        
        computer_is_ahead = computer_distance < player_distance

        should_show_path = computer_is_ahead and (wrong_direction or player_to_computer > 5)
        
        if should_show_path:
            hint_path = self.astar(self.maze, 
                                (self.player_pos[0], self.player_pos[1]), 
                                (self.computer_pos[0], self.computer_pos[1]))

            for i, pos in enumerate(hint_path[1:6]):
                alpha = 180 - i * 30 

                hint_surf = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                hint_surf.fill((255, 255, 0, alpha))
                arrow_points = []
                if self.cell_size >= 10: 
                    half = self.cell_size // 2
                    quarter = self.cell_size // 4

                    if i < len(hint_path) - 1:
                        next_pos = hint_path[i+1]
                        dx = next_pos[0] - pos[0]
                        dy = next_pos[1] - pos[1]
           
                        if dx > 0:  
                            arrow_points = [
                                (quarter, half), 
                                (half + quarter, half),
                                (half, quarter), 
                                (half, half + quarter)
                            ]
                        elif dx < 0: 
                            arrow_points = [
                                (half + quarter, half),
                                (quarter, half),
                                (half, quarter),
                                (half, half + quarter)
                            ]
                        elif dy > 0: 
                            arrow_points = [
                                (half, quarter),
                                (half, half + quarter),
                                (quarter, half),
                                (half + quarter, half)
                            ]
                        elif dy < 0: 
                            arrow_points = [
                                (half, half + quarter),
                                (half, quarter),
                                (quarter, half),
                                (half + quarter, half)
                            ]

                    if arrow_points:
                        pygame.draw.polygon(hint_surf, (255, 128, 0, alpha), arrow_points)

                self.screen.blit(hint_surf, 
                            (self.maze_offset_x + pos[0] * self.cell_size,
                                self.maze_offset_y + pos[1] * self.cell_size))

                if i == 0 and self.frame_counter % 10 == 0:
                    self.add_particles(
                        self.maze_offset_x + pos[0] * self.cell_size + self.cell_size/2,
                        self.maze_offset_y + pos[1] * self.cell_size + self.cell_size/2,
                        (255, 255, 0, 150), 2
                    )

        if wrong_direction and computer_is_ahead and self.frame_counter % 10 < 5:
            computer_highlight = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            computer_highlight.fill((255, 0, 0, 128)) 
            
            self.screen.blit(self.computer_img, 
                        (self.maze_offset_x + self.computer_pos[0] * self.cell_size, 
                            self.maze_offset_y + self.computer_pos[1] * self.cell_size))
            self.screen.blit(computer_highlight,
                        (self.maze_offset_x + self.computer_pos[0] * self.cell_size, 
                            self.maze_offset_y + self.computer_pos[1] * self.cell_size))

            if self.frame_counter % 5 == 0:
                self.add_particles(
                    self.maze_offset_x + self.computer_pos[0] * self.cell_size + self.cell_size/2,
                    self.maze_offset_y + self.computer_pos[1] * self.cell_size + self.cell_size/2,
                    (255, 50, 50, 200), 3
                )
        else:
            self.screen.blit(self.computer_img, 
                        (self.maze_offset_x + self.computer_pos[0] * self.cell_size, 
                            self.maze_offset_y + self.computer_pos[1] * self.cell_size))

        if wrong_direction and self.frame_counter % 10 < 5:
            computer_highlight = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            computer_highlight.fill((255, 0, 0, 128))
            
            self.screen.blit(self.computer_img, 
                        (self.maze_offset_x + self.computer_pos[0] * self.cell_size, 
                            self.maze_offset_y + self.computer_pos[1] * self.cell_size))
            self.screen.blit(computer_highlight,
                        (self.maze_offset_x + self.computer_pos[0] * self.cell_size, 
                            self.maze_offset_y + self.computer_pos[1] * self.cell_size))

            if self.frame_counter % 5 == 0:
                self.add_particles(
                    self.maze_offset_x + self.computer_pos[0] * self.cell_size + self.cell_size/2,
                    self.maze_offset_y + self.computer_pos[1] * self.cell_size + self.cell_size/2,
                    (255, 50, 50, 200), 3
                )
        else:
            self.screen.blit(self.computer_img, 
                        (self.maze_offset_x + self.computer_pos[0] * self.cell_size, 
                            self.maze_offset_y + self.computer_pos[1] * self.cell_size))

        self.screen.blit(self.player_img, 
                    (self.maze_offset_x + self.player_pos[0] * self.cell_size, 
                        self.maze_offset_y + self.player_pos[1] * self.cell_size))

        self.draw_particles()
        
        level_text = self.font_small.render(f"Level: {self.level}", True, (0, 0, 0))
        score_text = self.font_small.render(f"Score: {self.score}", True, (0, 0, 0))
        
        self.screen.blit(level_text, (20, 20))
        self.screen.blit(score_text, (20, 50))
        
        if self.player_speed_boost > 0:
            boost_text = self.font_small.render(f"SPEED BOOST: {self.player_speed_boost//10}s", True, (255, 255, 0))
            pygame.draw.rect(self.screen, (50, 50, 0), (self.screen_width - 220, 20, 200, 30), 0, 5)
            self.screen.blit(boost_text, (self.screen_width - 210, 25))
        
        if self.sabotage_cooldown > 0:
            sabotage_text = self.font_small.render(f"WALL COOLDOWN: {self.sabotage_cooldown//10}s", True, (255, 0, 0))
            pygame.draw.rect(self.screen, (50, 0, 0), (self.screen_width - 220, 60, 200, 30), 0, 5)
            self.screen.blit(sabotage_text, (self.screen_width - 210, 65))
        else:
            ready_text = self.font_small.render("WALL READY! (SPACE)", True, (0, 255, 0))
            pygame.draw.rect(self.screen, (0, 50, 0), (self.screen_width - 220, 60, 200, 30), 0, 5)
            self.screen.blit(ready_text, (self.screen_width - 210, 65))

        help_text = self.font_small.render("WASD/Arrows: Move | SPACE: Place Wall", True, (0, 0, 0))
        self.screen.blit(help_text, 
                    (self.screen_width - help_text.get_width() - 10, 
                        self.screen_height - help_text.get_height() - 10))
    
    def handle_key_event(self, event):
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        
        prev_pos = self.player_pos.copy()
        new_pos = self.player_pos.copy()
        
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            new_pos[1] -= 1
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            new_pos[1] += 1
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            new_pos[0] -= 1
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            new_pos[0] += 1
        elif event.key == pygame.K_SPACE:
            self.perform_sabotage()
            return

        if self.can_move_to_position(new_pos):
            current_distance = self.heuristic((self.player_pos[0], self.player_pos[1]), 
                                            (self.end_pos[0], self.end_pos[1]))

            if hasattr(self, 'last_player_distance'):
                self.second_last_player_distance = self.last_player_distance
            else:
                self.second_last_player_distance = current_distance
                
            self.last_player_distance = current_distance

            self.player_pos = new_pos

            x = self.maze_offset_x + new_pos[0] * self.cell_size + self.cell_size/2
            y = self.maze_offset_y + new_pos[1] * self.cell_size + self.cell_size/2
            self.add_particles(x, y, (0, 255, 0, 100), 3)

            key = f"{self.player_pos[0]},{self.player_pos[1]}"
            if key in self.checkpoint_status and self.checkpoint_status[key] != "player":
                self.handle_checkpoint_interaction(key)
    
    def can_move_to_position(self, pos):
        if pos[1] < 0 or pos[1] >= len(self.maze) or pos[0] < 0 or pos[0] >= len(self.maze[0]):
            return False

        if self.maze[pos[1]][pos[0]] == 1:
            return False
        
        for wall in self.temporary_walls:
            if wall[0] == pos[0] and wall[1] == pos[1]:
                return False
        
        return True
    
    def perform_sabotage(self):
        config = GameData.level_config.get(self.level)
        if not config:
            return
        
        if (self.sabotage_cooldown <= 0 and self.computer_path_index + 1 < len(self.computer_path)):
            next_pos = self.computer_path[self.computer_path_index + 1]
  
            if next_pos[0] != self.player_pos[0] or next_pos[1] != self.player_pos[1]:
                self.temporary_walls.append([next_pos[0], next_pos[1], config.wall_duration * 10])
                self.sabotage_cooldown = config.sabotage_cooldown * 10

                if self.sound_enabled:
                    self.sound_wall.play()

                x = self.maze_offset_x + next_pos[0] * self.cell_size + self.cell_size/2
                y = self.maze_offset_y + next_pos[1] * self.cell_size + self.cell_size/2
                self.add_particles(x, y, (255, 0, 0), 15)

                self.recalculate_computer_path()
    
    def move_computer_player(self):
        if self.computer_path_index < len(self.computer_path) - 1:
            config = GameData.level_config.get(self.level)
            if not config:
                return

            player_distance = self.heuristic((self.player_pos[0], self.player_pos[1]), 
                                        (self.end_pos[0], self.end_pos[1]))
            computer_distance = self.heuristic((self.computer_pos[0], self.computer_pos[1]), 
                                            (self.end_pos[0], self.end_pos[1]))

            player_to_computer = self.heuristic((self.player_pos[0], self.player_pos[1]), 
                                            (self.computer_pos[0], self.computer_pos[1]))
            
            wrong_direction = False
            if hasattr(self, 'last_player_distance'):
                wrong_direction = player_distance > self.last_player_distance
            self.last_player_distance = player_distance
            should_move = True 
            if computer_distance < player_distance and player_to_computer > 3:
                if random.random() < 0.7:
                    x = self.maze_offset_x + self.computer_pos[0] * self.cell_size + self.cell_size/2
                    y = self.maze_offset_y + self.computer_pos[1] * self.cell_size + self.cell_size/2
                    
                    if self.frame_counter % 60 == 0:
                        self.add_particles(x, y, (200, 200, 0), 2) 
                    should_move = False
            elif player_distance < computer_distance - 8:
                should_move = True
                if player_distance < computer_distance - 12 and random.random() < 0.4:
                    self.computer_speed_penalty = 0 
                    if player_distance < computer_distance - 20:
                        catch_up_moves = 3
                    elif player_distance < computer_distance - 15:
                        catch_up_moves = 2
                    else:
                        catch_up_moves = 1

                    for _ in range(catch_up_moves):
                        if self.computer_path_index < len(self.computer_path) - 1:
                            self._move_computer_one_step()

            elif wrong_direction:
                should_move = True

            if should_move:
                self._move_computer_one_step()

    def _move_computer_one_step(self):
        if self.computer_path_index < len(self.computer_path) - 1:
            next_pos = self.computer_path[self.computer_path_index + 1]

            has_wall = False
            for wall in self.temporary_walls:
                if wall[0] == next_pos[0] and wall[1] == next_pos[1]:
                    has_wall = True
                    break

            is_checkpoint = False
            checkpoint_key = f"{next_pos[0]},{next_pos[1]}"
            if checkpoint_key in self.checkpoint_status:
                if self.checkpoint_status[checkpoint_key] is None:
                    is_checkpoint = True

                    x = self.maze_offset_x + self.computer_pos[0] * self.cell_size + self.cell_size/2
                    y = self.maze_offset_y + self.computer_pos[1] * self.cell_size + self.cell_size/2
                    
                    if self.frame_counter % 30 == 0:
                        self.add_particles(x, y, (200, 200, 0), 3)
                    return
            
            if not has_wall:
                self.computer_path_index += 1
                self.computer_pos[0] = next_pos[0]
                self.computer_pos[1] = next_pos[1]

                x = self.maze_offset_x + next_pos[0] * self.cell_size + self.cell_size/2
                y = self.maze_offset_y + next_pos[1] * self.cell_size + self.cell_size/2
                self.add_particles(x, y, (255, 100, 100, 100), 2)

                key = f"{self.computer_pos[0]},{self.computer_pos[1]}"
                if key in self.checkpoint_status and self.checkpoint_status[key] is None:
                    self.checkpoint_status[key] = "computer"

                    self.add_particles(x, y, (255, 0, 0), 10)
            else:
                self.recalculate_computer_path()
    
    def recalculate_computer_path(self):
        temp_maze = [row[:] for row in self.maze]

        for wall in self.temporary_walls:
            if wall[1] < len(temp_maze) and wall[0] < len(temp_maze[0]):
                temp_maze[wall[1]][wall[0]] = 1
        
        self.computer_path = self.astar(temp_maze, 
                                      (self.computer_pos[0], self.computer_pos[1]), 
                                      (self.end_pos[0], self.end_pos[1]))
        self.computer_path_index = 0
    
    def handle_checkpoint_interaction(self, key):
        config = GameData.level_config.get(self.level)
        if not config:
            return

        base_difficulty = config.question_difficulty

        if self.checkpoint_status[key] == "computer":
            difficulties = ["easy", "medium", "hard"]
            current_idx = difficulties.index(base_difficulty)
            if current_idx < len(difficulties) - 1:
                base_difficulty = difficulties[current_idx + 1]

        age_questions = GameData.questions.get(self.age_group, {})
        questions_for_difficulty = age_questions.get(base_difficulty, [])

        if not questions_for_difficulty:
            questions_for_difficulty = GameData.legacy_questions.get(base_difficulty, [])

        if questions_for_difficulty:
            question = random.choice(questions_for_difficulty)
            self.show_question(question, key)
    
    def show_question(self, question, checkpoint_key):
        running = True
        selected = None

        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 50))
        
        while running:
            self.screen.blit(overlay, (0, 0))

            question_box = pygame.Rect(self.screen_width/2 - 350, 100, 700, 400)
            pygame.draw.rect(self.screen, (240, 240, 255), question_box)
            pygame.draw.rect(self.screen, (0, 0, 100), question_box, 3)  # Border

            title = self.font_medium.render("Answer correctly for a speed boost!", True, (0, 0, 100))
            question_text = self.font_medium.render(question.question, True, (0, 0, 0))
            self.screen.blit(title, (self.screen_width/2 - title.get_width()/2, 120))
            self.screen.blit(question_text, (self.screen_width/2 - question_text.get_width()/2, 180))

            button_a = pygame.Rect(self.screen_width/2 - 300, 250, 250, 70)
            button_b = pygame.Rect(self.screen_width/2 + 50, 250, 250, 70)

            mouse_pos = pygame.mouse.get_pos()
            hover_a = button_a.collidepoint(mouse_pos)
            hover_b = button_b.collidepoint(mouse_pos)

            pygame.draw.rect(self.screen, (200, 200, 230) if not hover_a else (180, 180, 220), button_a)
            pygame.draw.rect(self.screen, (200, 200, 230) if not hover_b else (180, 180, 220), button_b)

            pygame.draw.rect(self.screen, (0, 0, 100), button_a, 2)
            pygame.draw.rect(self.screen, (0, 0, 100), button_b, 2)

            option_a = self.font_medium.render(f"A: {question.options[0]}", True, (0, 0, 0))
            option_b = self.font_medium.render(f"B: {question.options[1]}", True, (0, 0, 0))
            
            self.screen.blit(option_a, (button_a.x + button_a.width/2 - option_a.get_width()/2,
                                    button_a.y + button_a.height/2 - option_a.get_height()/2))
            self.screen.blit(option_b, (button_b.x + button_b.width/2 - option_b.get_width()/2,
                                    button_b.y + button_b.height/2 - option_b.get_height()/2))

            hint_text = self.font_small.render("Click on the correct answer", True, (100, 100, 100))
            self.screen.blit(hint_text, (self.screen_width/2 - hint_text.get_width()/2, 350))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_a.collidepoint(event.pos):
                        selected = question.options[0]
                        running = False
                    elif button_b.collidepoint(event.pos):
                        selected = question.options[1]
                        running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_1:
                        selected = question.options[0]
                        running = False
                    elif event.key == pygame.K_b or event.key == pygame.K_2:
                        selected = question.options[1]
                        running = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

        correct = (selected == question.correct)

        self.show_answer_feedback(question, selected, correct)
        
        if correct:
            self.checkpoint_status[checkpoint_key] = "player"
            self.player_speed_boost = 150
            self.computer_speed_penalty = 150  
            self.score += 25 

            x = self.maze_offset_x + self.player_pos[0] * self.cell_size + self.cell_size/2
            y = self.maze_offset_y + self.player_pos[1] * self.cell_size + self.cell_size/2
            self.add_particles(x, y, (0, 255, 0), 20)

            if self.sound_enabled:
                self.sound_checkpoint.play()
        else:
            self.checkpoint_status[checkpoint_key] = "computer"
            self.computer_speed_penalty = 0
            self.player_speed_boost = 0

            x = self.maze_offset_x + self.computer_pos[0] * self.cell_size + self.cell_size/2
            y = self.maze_offset_y + self.computer_pos[1] * self.cell_size + self.cell_size/2
            self.add_particles(x, y, (255, 0, 0), 15)

            if self.frame_counter % 5 == 0:
                self.move_computer_player()
    
    def show_answer_feedback(self, question, selected, correct):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(220)
        overlay.fill((20, 20, 50))
        self.screen.blit(overlay, (0, 0))

        feedback_box = pygame.Rect(self.screen_width/2 - 350, 100, 700, 400)
        pygame.draw.rect(self.screen, (240, 240, 255), feedback_box)

        border_color = (0, 200, 0) if correct else (200, 0, 0)
        pygame.draw.rect(self.screen, border_color, feedback_box, 4)

        if correct:
            result_text = self.font_large.render("Correct!", True, (0, 200, 0))
            bonus_text = self.font_medium.render("You got a speed boost!", True, (0, 0, 0))
        else:
            result_text = self.font_large.render("Incorrect", True, (200, 0, 0))
            bonus_text = self.font_medium.render(f"The correct answer was: {question.correct}", True, (0, 0, 0))
        
        self.screen.blit(result_text, (self.screen_width/2 - result_text.get_width()/2, 130))
        self.screen.blit(bonus_text, (self.screen_width/2 - bonus_text.get_width()/2, 190))

        explanation_lines = self._wrap_text(question.explanation, 60)
        y = 250
        for line in explanation_lines:
            text = self.font_small.render(line, True, (50, 50, 50))
            self.screen.blit(text, (self.screen_width/2 - text.get_width()/2, y))
            y += 30

        continue_button = pygame.Rect(self.screen_width/2 - 100, 420, 200, 50)
        pygame.draw.rect(self.screen, (100, 100, 200), continue_button)
        pygame.draw.rect(self.screen, (0, 0, 100), continue_button, 2)
        
        continue_text = self.font_medium.render("Continue", True, (255, 255, 255))
        self.screen.blit(continue_text, (continue_button.x + continue_button.width/2 - continue_text.get_width()/2,
                                      continue_button.y + continue_button.height/2 - continue_text.get_height()/2))
        
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.collidepoint(event.pos):
                        waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        waiting = False
    
    def _wrap_text(self, text, max_chars):
        """Wrap text to a maximum number of characters per line"""
        words = text.split(' ')
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + len(current_line) <= max_chars:
                current_line.append(word)
                current_length += len(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def show_winner(self, player_won):
        screenshot = self.screen.copy()

        if player_won:
            for _ in range(100):
                x = random.randint(0, self.screen_width)
                y = random.randint(0, self.screen_height)
                color = (random.randint(0, 255), random.randint(0, 255), 0)
                self.add_particles(x, y, color, 1)

        for alpha in range(0, 180, 5):
            self.screen.blit(screenshot, (0, 0))

            self.update_particles()
            self.draw_particles()

            overlay = pygame.Surface((self.screen_width, self.screen_height))
            overlay.set_alpha(alpha)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            pygame.display.flip()
            pygame.time.delay(30)

        if player_won:
            title = self.font_large.render("YOU WIN THIS LEVEL!", True, (255, 255, 255))
            subtitle = self.font_medium.render(f"Score: {self.score}", True, (255, 255, 0))
            
            button_text = "Next Level"
            if self.level >= 7:
                button_text = "Complete Game"
        else:
            title = self.font_large.render("COMPUTER WINS!", True, (255, 255, 255))
            subtitle = self.font_medium.render("Would you like to try again?", True, (255, 255, 255))
            button_text = "Retry"
        
        button = pygame.Rect(self.screen_width/2 - 100, self.screen_height/2 + 50, 200, 50)
        quit_button = pygame.Rect(self.screen_width/2 - 100, self.screen_height/2 + 120, 200, 50)
        
        waiting = True
        result = False
        start_time = time.time()
        
        while waiting:
            self.screen.blit(screenshot, (0, 0))

            self.update_particles()
            self.draw_particles()
            
            overlay = pygame.Surface((self.screen_width, self.screen_height))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            pulse = (math.sin((time.time() - start_time) * 5) + 1) * 0.1  # Subtle pulse

            mouse_pos = pygame.mouse.get_pos()
            hover_continue = button.collidepoint(mouse_pos)
            hover_quit = quit_button.collidepoint(mouse_pos)

            continue_color = (80, 200, 80) if hover_continue else (50, 150, 50)
            quit_color = (200, 80, 80) if hover_quit else (150, 50, 50)

            if hover_continue:
                button_expanded = button.inflate(pulse * 20, pulse * 20)
                pygame.draw.rect(self.screen, continue_color, button_expanded, 0, 10)
                pygame.draw.rect(self.screen, (255, 255, 255), button_expanded, 2, 10)
            else:
                pygame.draw.rect(self.screen, continue_color, button, 0, 10)
                pygame.draw.rect(self.screen, (200, 200, 200), button, 2, 10)
                
            if hover_quit:
                quit_expanded = quit_button.inflate(pulse * 20, pulse * 20)
                pygame.draw.rect(self.screen, quit_color, quit_expanded, 0, 10)
                pygame.draw.rect(self.screen, (255, 255, 255), quit_expanded, 2, 10)
            else:
                pygame.draw.rect(self.screen, quit_color, quit_button, 0, 10)
                pygame.draw.rect(self.screen, (200, 200, 200), quit_button, 2, 10)
            
            self.screen.blit(title, (self.screen_width/2 - title.get_width()/2, self.screen_height/2 - 80))
            self.screen.blit(subtitle, (self.screen_width/2 - subtitle.get_width()/2, self.screen_height/2 - 20))
            
            button_label = self.font_small.render(button_text, True, (255, 255, 255))
            self.screen.blit(button_label, (button.x + button.width/2 - button_label.get_width()/2,
                                         button.y + button.height/2 - button_label.get_height()/2))
            
            quit_label = self.font_small.render("Quit", True, (255, 255, 255))
            self.screen.blit(quit_label, (quit_button.x + quit_button.width/2 - quit_label.get_width()/2,
                                       quit_button.y + quit_button.height/2 - quit_label.get_height()/2))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button.collidepoint(event.pos):
                        waiting = False
                        result = True
                        
                        if player_won:
                            self.level += 1
                            if self.level <= 7:
                                self.show_level_transition(self.level)
                            else:
                                self.show_game_completion()
                        else:
                            self.show_level_transition(self.level)
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        waiting = False
                        result = True
                        
                        if player_won:
                            self.level += 1
                            if self.level <= 7:
                                self.show_level_transition(self.level)
                            else:
                                self.show_game_completion()
                        else:
                            self.show_level_transition(self.level)
        
        return result
    
    def show_game_completion(self):
        stars = []
        for _ in range(200):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = random.randint(1, 4)
            brightness = random.randint(150, 255)
            speed = random.uniform(0.5, 2.0)
            stars.append([x, y, size, brightness, speed])
        
        for _ in range(300):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            self.add_particles(x, y, (r, g, b), 1)
        
        waiting = True
        start_time = time.time()
        
        while waiting:
            self.screen.fill((0, 0, 30))

            for star in stars:
                x, y, size, brightness, speed = star
                y = (y + speed) % self.screen_height
                star[1] = y
                pygame.draw.circle(self.screen, (brightness, brightness, brightness), (int(x), int(y)), size)
            
            self.update_particles()
            self.draw_particles()
            
            pulse = (math.sin((time.time() - start_time) * 2) + 1) * 0.1  # Subtle pulse
            
            title = self.font_large.render("YOU COMPLETED ALL LEVELS!", True, (255, 255, 255))
            subtitle = self.font_medium.render("Congratulations! You've beaten the game!", True, (255, 255, 0))
            score_text = self.font_medium.render(f"Final Score: {self.score}", True, (255, 255, 255))
            
            title_rect = title.get_rect(center=(self.screen_width/2, self.screen_height/2 - 50))
            subtitle_rect = subtitle.get_rect(center=(self.screen_width/2, self.screen_height/2 + 20))
            score_rect = score_text.get_rect(center=(self.screen_width/2, self.screen_height/2 + 70))
            
            title_rect = title_rect.inflate(title_rect.width * pulse, title_rect.height * pulse)
            
            self.screen.blit(title, title_rect)
            self.screen.blit(subtitle, subtitle_rect)
            self.screen.blit(score_text, score_rect)
            
            if int(time.time() * 2) % 2 == 0:
                continue_text = self.font_small.render("Press any key to exit", True, (200, 200, 200))
                self.screen.blit(continue_text, (self.screen_width/2 - continue_text.get_width()/2, 
                                             self.screen_height - 100))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    sys.exit()
    
    def generate_maze(self, width, height):
        maze = [[1 for _ in range(2 * width + 1)] for _ in range(2 * height + 1)]
        
        def carve_passages(x, y):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < width and 0 <= ny < height and maze[2 * ny + 1][2 * nx + 1] == 1:
                    maze[2 * y + 1 + dy][2 * x + 1 + dx] = 0
                    maze[2 * ny + 1][2 * nx + 1] = 0
                    carve_passages(nx, ny)
        
        maze[1][1] = 0
        carve_passages(0, 0)
        return maze
    
    def dijkstra(self, maze, start, end):
        width = len(maze[0])
        height = len(maze)
        
        distances = {f"{start[0]},{start[1]}": 0}
        queue = [(0, start)]
        came_from = {f"{start[0]},{start[1]}": None}
        
        while queue:
            current_distance, current = queue.pop(0)
            
            if current[0] == end[0] and current[1] == end[1]:
                break
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                
                if (0 <= neighbor[0] < width and 0 <= neighbor[1] < height and
                    maze[neighbor[1]][neighbor[0]] == 0):
                    
                    distance = distances[f"{current[0]},{current[1]}"] + 1
                    neighbor_key = f"{neighbor[0]},{neighbor[1]}"
                    
                    if neighbor_key not in distances or distance < distances[neighbor_key]:
                        distances[neighbor_key] = distance
                        queue.append((distance, neighbor))
                        queue.sort()
                        came_from[neighbor_key] = current
        
        path = []
        current = end
        
        while current:
            path.append(current)
            key = f"{current[0]},{current[1]}"
            current = came_from.get(key)
        
        return list(reversed(path))
    
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def astar(self, maze, start, goal):
        width = len(maze[0])
        height = len(maze)
        
        frontier = PriorityQueue()
        frontier.put(start, self.heuristic(start, goal))
        
        came_from = {}
        cost_so_far = {f"{start[0]},{start[1]}": 0}
        
        while not frontier.empty():
            current = frontier.get()
            current_key = f"{current[0]},{current[1]}"
            
            if current[0] == goal[0] and current[1] == goal[1]:
                break
                
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                neighbor_key = f"{neighbor[0]},{neighbor[1]}"
                
                if (0 <= neighbor[0] < width and 0 <= neighbor[1] < height and 
                    maze[neighbor[1]][neighbor[0]] == 0):
                    
                    new_cost = cost_so_far[current_key] + 1
                    
                    if neighbor_key not in cost_so_far or new_cost < cost_so_far[neighbor_key]:
                        cost_so_far[neighbor_key] = new_cost
                        priority = new_cost + self.heuristic(neighbor, goal)
                        frontier.put(neighbor, priority)
                        came_from[neighbor_key] = current
        
        path = []
        current = goal
        
        while current != start:
            path.append(current)
            current_key = f"{current[0]},{current[1]}"
            if current_key not in came_from:
                return [start]
            current = came_from[current_key]
        
        path.append(start)
        path.reverse()
        
        return path

if __name__ == "__main__":
    game = MazeGame()