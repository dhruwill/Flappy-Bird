import pygame as game
from random import randint
from pygame.locals import *
from collections import deque


# Bird image loader
BIRD_SPRITE = game.image.load("bird.png")
g = 0.001						# Gravitational Acceleration
BIRD_HEIGHT = 80				# Height of the bounding box of the bird
BIRD_WIDTH = 80					# Width of the bounding box of the bird
BIRD_VELOCITY = 0.1				# Initial velocity of the bird
''' Start at the Center '''
INIT_X = 100
INIT_Y = 200
PIPE_WIDTH = 80					# Pipe Width
PIPE_PIECE_HEIGHT = 30			# Height of a piece of a pipe
PIPE_ADD_RATE = 1750			# Rate at which pipes appear
PIPE_SCROLL_SPEED = .2			# Speed of the leftward motion of the pipe
SCREEN_WIDTH = 500				# Display window size of the game
SCREEN_HEIGHT = 600
game.init()
screen = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
myfont = game.font.SysFont("monospace", 32)


# def init_setting:
	# SCREEN_WIDTH = 500
	# SCREEN_HEIGHT = 600
	# game.init()
	# screen = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# ========================== CLASS : BIRD ==============================
#Class for representing the bird entity : initialisation and update of motion parameters
class Bird(game.sprite.Sprite):

	def __init__(self):
		game.sprite.Sprite.__init__(self)
		self.x = INIT_X			# Set the bird's starting coordinates
		self.y = INIT_Y
		# Fit the image in the bounding box of the above mentioned size
		self.sprite = game.transform.scale(BIRD_SPRITE,(BIRD_HEIGHT,BIRD_WIDTH))
		self.velocity = BIRD_VELOCITY		# Set the bird's initial velocity
		self.mask = game.mask.from_surface(self.sprite)

	# Update the motion parameters, i.e. the velocity of the bird, and the bird's y position
	def update_no_flap(self):
		self.velocity += g
		self.y += self.velocity

	# Flap : Setting the velocities of the bird on flap, depending upon the threshold of velocities
	def update_flap(self):
		self.velocity -= BIRD_VELOCITY * 10
		if self.velocity < -BIRD_VELOCITY * 5:
			self.velocity = -BIRD_VELOCITY * 5

	# Returns a new copy of the rectangle(the bird's bounding box) bsed on the changes in the bird's position
	@property
	def rect(self):
	    return Rect(self.x, self.y, BIRD_HEIGHT, BIRD_WIDTH)
#============================= XXXXXXXXXXX =====================================


#============================= CLASS : PIPE =====================================
class Pipe(game.sprite.Sprite):

	def __init__(self):
		self.x = SCREEN_WIDTH - 2	# Set the pipe's X position at initialisation
		self.passed_flag = False	# Flag that checks if the bird has crossed that pipe pair or not

		# Some IP for displaying the pipe
		self.sprite = game.Surface((PIPE_WIDTH, SCREEN_HEIGHT), SRCALPHA)
		self.sprite.convert()
		self.sprite.fill((0,0,0,0))
		# Set the length of the total vertical length covered by the pipe pair on the screen
		total_pipe_body_pieces = int((SCREEN_HEIGHT - 3 * BIRD_HEIGHT - 3 * PIPE_PIECE_HEIGHT) / PIPE_PIECE_HEIGHT)

		# Set the vertical length of the bottom piece of the pipe pair
		self.bottom_pieces = randint(1, total_pipe_body_pieces-1)

		# Set the vertical length of the to piece of the pipe pair
		self.top_pieces = total_pipe_body_pieces - self.bottom_pieces

		# Load the pipe's images
		pipe_sprite =game.image.load("pipe.png")
		pipe_sprite = game.transform.scale(pipe_sprite, (PIPE_WIDTH, 80))

		# Blitting the lower pipe
		for i in range(1, self.bottom_pieces + 1):
			piece_pos = (0, SCREEN_HEIGHT - i*PIPE_PIECE_HEIGHT)
			self.sprite.blit(pipe_sprite, piece_pos)


		for i in range(self.top_pieces):
			self.sprite.blit(pipe_sprite, (0, i * PIPE_PIECE_HEIGHT))

		# As we have added end pieces, compensate for them
		self.top_pieces += 1
		self.bottom_pieces += 1
		self.bot_height = self.bottom_pieces * PIPE_PIECE_HEIGHT

		# Helps in collision detection
		self.mask = game.mask.from_surface(self.sprite)

	# Returns the new bounding box of the pipe pair
	@property
	def rect(self):
		return Rect(self.x, 0, PIPE_WIDTH, PIPE_PIECE_HEIGHT)

	# Check if the pipe pair is on the screen , i.e. whether it is visible or not
	@property
	def visible(self):
		return -PIPE_WIDTH < self.x < SCREEN_WIDTH

	# Update the x- coordinates of the pipe as they are in motion
	def update(self):
		self.x -= PIPE_SCROLL_SPEED

	# Check whether the birds collides with the pipe or not
	def collides_with(self, bird):
		return game.sprite.collide_mask(self, bird)
#=========================XXXXXXXXXXXXXXXXXXXX====================================

# Main function, which enables the AI to be controlled
def play(headless=False, ai=None):

	# Instantiate bird and pipes
	bird = Bird()
	pipes = deque()
	# Initialise the score and done (Means whether the game is over or not)
	frame = 0
	score = 0
	done = False

	while True:
		# draw bird on the screen
		bird.update_no_flap()

		# Display the entire game iff headless is set to false, else let the screen remain black.
		if not headless:
			screen.fill((0, 255, 255))
			screen.blit(bird.sprite, (bird.x, bird.y))

		# Displaying a new pipe based on the chosen pipe add rate
		if frame % PIPE_ADD_RATE == 0:
			p = Pipe()
			pipes.append(p)

		# Check if there is even 1 collision of any pipe with the bird
		collision_detected = any(p.collides_with(bird) for p in pipes)

		# Some basic , essential and necessary error checking
		if bird.y > 600 or bird.y < 0 or collision_detected:
			break

		# Remove from the list of pipes, as soon as a pipe crosses the left part of the screen
		while pipes and not pipes[0].visible:
			pipes.popleft()

		# Bird crosses the pipe now
		for p in pipes:
			if p.x + PIPE_WIDTH/2 < bird.x and not p.passed_flag:
				# Pipe's center successfully crossed by the bird, add 1 to the score, set passed -> True
				p.passed_flag = True
				score += 1

			# Update the pipes
			p.update()

			# If headless is true, then display this game, else don't
			if not headless:
				screen.blit(p.sprite, (p.x, 0))

		# As this is a game not solely made to be controlled using an AI only,
		# If ai = false, then handle external users playing.
		if not ai:
			for event in game.event.get():
				if event.type == game.QUIT:
					break

				if event.type == game.KEYDOWN and event.key == game.K_SPACE:
					bird.update_flap()

		# Now if the feed forward value of the current positions of the bird, comes out to be
		# >0.5, do an update with a flap, else don't do this one.
		elif ai.forward([bird.x - pipes[0].x,SCREEN_HEIGHT - bird.y - pipes[0].bot_height]) > 0.5:
			bird.update_flap()
		label = myfont.render("Score =" + str(score), 1, (255,100,0))
		screen.blit(label, (316, 40))

		# update screen after the update in the motions of the bird.
		if not headless:
			game.display.flip()
		frame += 1

	# Print score at the end of 1 game
	print 'Score: ' + str(score)
	return score
