import pygame
import random
import itertools

# Initialize Pygame
pygame.init()

# Game window settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Simple Blackjack')

portraits = [
  pygame.image.load(f'portrait/1.png'),
  pygame.image.load(f'portrait/1.png'),  
]

dealer_portrait_img = pygame.image.load(f'portrait/dealer.png'),  

winner_image = pygame.transform.scale(pygame.image.load(f'symbols/winner.png'), (200, 200))

# Load card images
card_images = {}
suits = ['hearts', 'diamonds', 'clubs', 'spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
player_portrait = pygame.transform.scale(random.choice(portraits), (80, 160))
dealer_portrait = pygame.transform.scale(random.choice(dealer_portrait_img), (80, 160))

for suit in suits:
    for value in values:
        image_scale = 0.5
        card_img =  pygame.image.load(f'cards/{value}_of_{suit}.png')
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
    
    def __lt__(self, other):
        # Definindo a ordem dos valores das cartas
        order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                 'jack': 11, 'queen': 12, 'king': 13, 'ace': 14}

        # Comparar primeiro pelo valor, depois pelo naipe
        if order[self.value] == order[other.value]:
            return self.suit < other.suit
        return order[self.value] < order[other.value]
######################################
#
# Seu agente deve ser colocado nessa região
# Lembre-se que a regra do blackjack foi modificada
# nesse versão o dealer joga primeiro que você
# e você joga vendo a primeira carta dele
#
#
class Player:
    def __init__(self, learning_rate=0.1, discount_factor=0.91, exploration_prob=1.0, exploration_decay=1.0):
        # Inicialização da classe Player com parâmetros para aprendizado e exploração
        self.q_values = {}  # Dicionário para armazenar os valores Q
        self.learning_rate = learning_rate  # Taxa de aprendizado para ajuste dos valores Q
        self.discount_factor = discount_factor  # Fator de desconto usado no cálculo dos valores Q futuros
        self.exploration_prob = exploration_prob  # Probabilidade inicial de exploração
        self.exploration_decay = exploration_decay  # Fator de decaimento para a probabilidade de exploração

    def get_state_key(self, your_hand, dealer_first_card, dealer_sum):
        # Retorna uma chave de estado única baseada na mão do jogador, na primeira carta do dealer e na soma do dealer
        return tuple(sorted(your_hand)), dealer_first_card, dealer_sum

    def decay_exploration(self):
        # Atualiza a probabilidade de exploração multiplicando pelo fator de decaimento
        self.exploration_prob *= self.exploration_decay

    def decision(self, your_hand, dealer_first_card, dealer_sum):
        # Decide entre "hit" ou "stop" baseado na exploração ou na melhor ação estimada pelos valores Q
        state = self.get_state_key(your_hand, dealer_first_card, dealer_sum)

        print(self.q_values)
        if random.random() < self.exploration_prob:
            # Escolha aleatória para explorar o espaço de ações
            return random.choice(["hit", "stop"])
        else:
            # Escolha baseada no maior valor Q estimado
            hit_value = self.get_q_value(state, "hit")
            stop_value = self.get_q_value(state, "stop")
            return "hit" if hit_value > stop_value else "stop"
        

    def result(self, your_hand, dealer_first_card, decision, reward, is_not_done, dealer_sum):
        # Atualiza os valores Q com base no resultado e na recompensa recebida
        state = self.get_state_key(your_hand, dealer_first_card, dealer_sum)

        next_state = self.get_state_key(your_hand, dealer_first_card, dealer_sum)
        max_next_q_value = max(self.get_q_value(next_state, "hit"), self.get_q_value(next_state, "stop"))
        target_value = reward + self.discount_factor * max_next_q_value

        self.update_q_value(state, decision, target_value)

    def update_q_value(self, state, action, value):
        # Atualiza o valor Q para um determinado estado e ação
        if state not in self.q_values:
            # Se o estado ainda não está no dicionário, inicialize os valores Q para as ações
            self.q_values[state] = {"hit": 0, "stop": 0}

        # Ajuste do valor Q com base na diferença entre o valor alvo e o valor Q atual
        self.q_values[state][action] += self.learning_rate * (value - self.q_values[state][action])

    def get_q_value(self, state, action):
        # Obtém o valor Q para um determinado estado e ação
        return self.q_values.get(state, {"hit": 0, "stop": 0}).get(action, 0)

    def decay_exploration(self):
        # Método duplicado, pode ser removido ou mantido para garantir consistência na classe
        self.exploration_prob *= self.exploration_decay

class DealerPlayer:
  def decision(self, your_hand, dealer_hand):
    dealer_value = calculate_hand_value(dealer_hand)
    if dealer_value < 17:
      return "hit"
    else:
      return "stop"

  def result(self, your_hand, dealer_hand, decision, reward, is_not_done):
    pass

# Main game loop
def play_blackjack(player):
    running = True
    player_turn = False  # True if it's player's turn, False for dealer's turn
    dealer_turn = True
    
    # Create a deck of cards and deal initial hands
    deck = [Card(s,v) for s,v in itertools.product(suits, values)]
    player_hand = []
    dealer_hand = []
    hand_result = 0
    random.shuffle(deck)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Clear screen (black background)
        
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
            dealer_sum = calculate_hand_value(dealer_hand)  # Calculate dealer's total value
            decision = player.decision(player_hand, dealer_hand[0], dealer_sum)  # Pass dealer_sum as the third argument
            if decision == "hit":
               draw_card(deck, player_hand)
            else:
               player_turn = False

            if calculate_hand_value(player_hand) >= 21:
              player_turn = False                
               
            score = 0   
            
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
            decision = player.result(player_hand, dealer_hand[0], decision, hand_result, player_turn, dealer_sum)  # Add dealer_sum here as well
        
        render_hand(player_hand, (150, 100))
        render_hand(dealer_hand, (150, 300))     
        render_portrait(player_portrait, (50, 100))
        render_portrait(dealer_portrait, (50, 300))                
        pygame.display.flip()  # Update the display
        # pygame.time.wait(1000)
    return hand_result


# Insira seu jogador abaixo:
player = Player()

results = []
for _ in range(1000):
  results.append(play_blackjack(player))
  
import statistics
print(f"Player expected score was {statistics.fmean(results)}")
def add_to_file(decisions):
    
    file_path = "/home/neiva/Desktop/Eng.Comp/Classes/Inteligencia_Computacional/Trabalho_Blackjack/"+"resultados.txt"
    with open(file_path, "a") as file:
        file.write(f"\nscore: {decisions}\n")
        file.write(f"wins: {wins}\n")
        file.write(f"loses: {loses}\n")
        percentage = wins / (wins + loses)
        file.write(f"percentage: {percentage}\n")
wins = 0
loses = 0

for i in results:
    if i == 1:
        wins += 1
    else:
        loses += 1
add_to_file(statistics.fmean(results))
print(f"wins: {wins}\n")
print(f"loses: {loses}\n")
pygame.quit()

