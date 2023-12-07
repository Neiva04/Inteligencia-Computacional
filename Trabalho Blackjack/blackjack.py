import pygame
import random
import itertools

# Initialize Pygame
pygame.init()

# Game window settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Simple Blackjack')

portraits = [
  pygame.image.load(f'/home/neiva/Desktop/Eng.Comp/Classes/Inteligencia_Computacional/Trabalho Blackjack/portrait/1.png'),
  pygame.image.load(f'/home/neiva/Desktop/Eng.Comp/Classes/Inteligencia_Computacional/Trabalho Blackjack/portrait/2.png'),  
]

dealer_portrait_img = pygame.image.load(f'/home/neiva/Desktop/Eng.Comp/Classes/Inteligencia_Computacional/Trabalho Blackjack/portrait/dealer.png'),  

winner_image = pygame.transform.scale(pygame.image.load(f'/home/neiva/Desktop/Eng.Comp/Classes/Inteligencia_Computacional/Trabalho Blackjack/symbols/winner.png'), (200, 200))

# Load card images (assuming we have basic card images named as '2_of_clubs.png', '3_of_hearts.png', etc.)
card_images = {}
suits = ['hearts', 'diamonds', 'clubs', 'spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
player_portrait = pygame.transform.scale(random.choice(portraits), (80, 160))
dealer_portrait = pygame.transform.scale(random.choice(dealer_portrait_img), (80, 160))

for suit in suits:
    for value in values:
        image_scale = 0.5
        card_img =  pygame.image.load(f'/home/neiva/Desktop/Eng.Comp/Classes/Inteligencia_Computacional/Trabalho Blackjack/cards/{value}_of_{suit}.png')
        scaled_card = pygame.transform.scale(card_img, (int(200 * image_scale), int(300 * image_scale)))        
        card_images[(suit, value)] = scaled_card


# Card values
card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
               'jack': 10, 'queen': 10, 'king': 10, 'ace': [1, 11]}

# Function to calculate hand value
def calculate_hand_value(hand):
    value = 0
    ace_count = 0
    for card in hand:
        #print(card)
        if card.value == 'ace':
            ace_count += 1
        else:
            value += card_values[card.value]

    for _ in range(ace_count):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1

    return value

# Draw card function
def draw_card(deck, hand):
    card = random.choice(deck)
    hand.append(card)
    deck.remove(card)
    return card

def render_card(card, pos):
    screen.blit(card_images[(card.suit, card.value)], pos) 
    
def render_hand(hand, pos):
    for idx, c in enumerate(hand):
      screen.blit(card_images[(c.suit, c.value)], pos)
      pos = (pos[0] + 120, pos[1])

def render_portrait(portrait, pos):
    screen.blit(portrait, pos) 

def render_winner(pos):
    screen.blit(winner_image, pos) 

class Card:
  def __init__(self, suit, value):
    self.value = value
    self.suit = suit
    
  def __repr__(self):
    return f'[{self.value}-{self.suit}]'
    
 ######################################
 #
 # Seu agente deve ser colocado nessa região
 # Lembre-se que a regra do blackjack foi modificada
 # nesse versão o dealer joga primeiro que você
 # e você joga vendo a primeira carta dele
 #
 #
import random

class Player:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, start_exploration_prob=1.0, exploration_decay=0.995):
        self.q_values = {}  # Dicionário para armazenar os valores Q
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = start_exploration_prob
        self.exploration_decay = exploration_decay

    def get_state_key(self, your_hand, dealer_hand):
        your_hand_value = calculate_hand_value(your_hand)
        dealer_hand_value = calculate_hand_value([dealer_hand[0]])  # Apenas a primeira carta do dealer
        has_ace = any(card.value == 'ace' for card in your_hand)
        return (your_hand_value, dealer_hand_value, has_ace)

    def get_q_value(self, state, action):
        return self.q_values.get((state, action), 0.0)

    def update_q_value(self, state, action, reward, next_state):
        current_value = self.get_q_value(state, action)
        future_rewards = max(self.get_q_value(next_state, a) for a in ["hit", "stop"])
        updated_value = current_value + self.learning_rate * (reward + self.discount_factor * future_rewards - current_value)
        self.q_values[(state, action)] = updated_value

    def choose_action(self, your_hand, dealer_hand):
        state = self.get_state_key(your_hand, dealer_hand)
        if random.random() < self.exploration_prob:
            action = random.choice(["hit", "stop"])
        else:
            q_values = {a: self.get_q_value(state, a) for a in ["hit", "stop"]}
            action = max(q_values, key=q_values.get)
        self.exploration_prob *= self.exploration_decay  # Decaimento do epsilon
        return action

    def update(self, your_hand, dealer_hand, action, reward, next_hand):
        state = self.get_state_key(your_hand, dealer_hand)
        next_state = self.get_state_key(next_hand, dealer_hand)
        self.update_q_value(state, action, reward, next_state)

# Função de cálculo de valor de mão modificada para incluir a lógica de Ás
def calculate_hand_value(hand):
    value, ace_count = 0, 0
    for card in hand:
        if card.value == 'ace':
            ace_count += 1
        else:
            value += card_values[card.value]
    for _ in range(ace_count):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1
    return value
 

class DealerPlayer:
  def decision(self, your_hand, dealer_hand):
    dealer_value = calculate_hand_value(dealer_hand)
    if dealer_value < 17:
      return "hit"
    else:
      return "stop"

  def result(self, your_hand, dealer_hand, decision, reward, is_not_done):
    print("Reward :", reward)
    pass

# Main game loop
def play_blackjack(player):
    running = True
    player_turn = False  # True if it's player's turn, False for dealer's turn
    dealer_turn = True
    

    # Create a deck of cards and deal initial hands
    # [rest of the initial setup is the same]
    deck = [Card(s,v) for s,v in itertools.product(suits, values)]
    player_hand = []
    dealer_hand = []
    hand_result = 0
    random.shuffle(deck)
    #print([d for d in deck])
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle player input here (e.g., hit or stand)
            # You can use keys or mouse clicks for player decisions

        screen.fill((0, 0, 0))  # Clear screen (black background)
        #render_card(deck[0], (100, 100))
        
        # Display the cards and scores

        if dealer_turn:
            # Dealer's turn logic
            dealer_value = calculate_hand_value(dealer_hand)
            if dealer_value < 17:
                draw_card(deck, dealer_hand) 
            else:
              dealer_turn = False
              player_turn = True       
        elif player_turn:
            # Player's turn logic
            # Implement hit or stand decision
            decision = player.decision(player_hand, dealer_hand[0])
            if decision == "hit":
               draw_card(deck, player_hand)
            else:
               player_turn = False

            if calculate_hand_value(player_hand) >= 21:
              player_turn = False                
               
            score = 0   
            #decision = player.result(player_hand, dealer_hand[0], decision)   
            
            if not player_turn:
                # Compare hands and decide winner
                player_value = calculate_hand_value(player_hand)
                if (player_value > 21):
                  hand_result = -1
                elif (dealer_value > 21):
                  hand_result = +1
                elif (player_value >= dealer_value):
                  hand_result = +1
                elif (player_value == dealer_value):
                  hand_result = 0
                else:
                  hand_result = -1
                print(f"Round result {hand_result}")                     
                running = False
            # Decision
            decision = player.result(player_hand, dealer_hand[0], decision, hand_result, player_turn)
        
        render_hand(player_hand, (150, 100))
        render_hand(dealer_hand, (150, 300))     
        render_portrait(player_portrait, (50, 100))
        render_portrait(dealer_portrait, (50, 300))                
        pygame.display.flip()  # Update the display
        pygame.time.wait(1000)  
        
    pygame.time.wait(1000)  

    return hand_result


# Insire seu jogador abaixo:
player = Player()

results = []
for _ in range(10):
  results.append(play_blackjack(player))
  
import statistics
print(f"Player expected score was {statistics.fmean(results)}")
def add_to_file(decisions):
    
    file_path = "/home/neiva/Desktop/Eng.Comp/Classes/Inteligencia_Computacional/Trabalho Blackjack/"+"decisions_log.txt"
    with open(file_path, "a") as file:
        file.write(f"{decisions}\n")
add_to_file(statistics.fmean(results))
pygame.time.wait(3000)
pygame.quit()
