
import sys
import time
import random
# Game settings - Easy Mode
WIDTH = 50
HEIGHT = 24
NUM_ROBOTS = 5
NUM_WALLS = 30
NUM_TELEPORTS = 6

# Game symbols
EMPTY = ' '
PLAYER = '@'
ROBOT = 'R'
WALL = '#'
DEAD = 'X'


# Create the game board
def create_board():
    board = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # Create boundary walls
    for x in range(WIDTH):
        board[0][x] = WALL
        board[HEIGHT - 1][x] = WALL

    for y in range(HEIGHT):
        board[y][0] = WALL
        board[y][WIDTH - 1] = WALL

    # Add random walls
    count = 0
    while count < NUM_WALLS:
        x = random.randint(1, WIDTH - 2)
        y = random.randint(1, HEIGHT - 2)

        if board[y][x] == EMPTY:
            board[y][x] = WALL
            count += 1

    return board


# Find an empty position
def find_empty(board, robots, safe=False):
    positions = []

    for y in range(1, HEIGHT - 1):
        for x in range(1, WIDTH - 1):
            if board[y][x] == EMPTY and (x, y) not in robots:
                if safe:
                    distance = min(
                        abs(x - rx) + abs(y - ry)
                        for rx, ry in robots
                    ) if robots else 100

                    if distance < 7:
                        continue

                positions.append((x, y))

    if not positions:
        return None

    return random.choice(positions)


# Place robots randomly
def create_robots(board):
    robots = []

    for _ in range(NUM_ROBOTS):
        position = find_empty(board, robots)

        if position is not None:
            robots.append(position)

    return robots


# Display the game board
def show_board(board, robots, player, turn):
    print("\n" * 2)
    print("=" * 50)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            position = (x, y)

            if position == player:
                print(PLAYER, end='')
            elif position in robots:
                print(ROBOT, end='')
            else:
                print(board[y][x], end='')

        print()

    print("=" * 50)
    print("Robots remaining:", len(robots))
    print("Turn:", turn)


# Move the player
def player_move(board, robots, player, teleports):

    directions = {
        'Q': (-1, -1),
        'W': (0, -1),
        'E': (1, -1),
        'A': (-1, 0),
        'D': (1, 0),
        'Z': (-1, 1),
        'X': (0, 1),
        'C': (1, 1),
        'S': (0, 0)
    }

    while True:
        print("\nMovement controls:")
        print(" Q   W   E")
        print(" A   S   D")
        print(" Z   X   C")
        print("\nT = Teleport")
        print("QUIT = Exit")

        print("Teleports remaining:", teleports)

        move = input("Enter your move: ").upper().strip()

        if move == "QUIT":
            print("Thanks for playing!")
            raise SystemExit

        elif move == "T" and teleports > 0:
            new_position = find_empty(
                board, robots, safe=True
            )

            if new_position is not None:
                return new_position, teleports - 1

            print("No safe teleport position available!")

        elif move == "T":
            print("No teleports remaining!")

        elif move in directions:
            dx, dy = directions[move]

            new_x = player[0] + dx
            new_y = player[1] + dy

            if board[new_y][new_x] not in (WALL, DEAD):
                return (new_x, new_y), teleports

            print("That position is blocked!")

        else:
            print("Invalid move! Try again.")


# Calculate the next robot position
def calculate_robot_move(board, robot, player):
    rx, ry = robot
    px, py = player

    dx = (px > rx) - (px < rx)
    dy = (py > ry) - (py < ry)

    nx = rx + dx
    ny = ry + dy

    if board[ny][nx] in (WALL, DEAD):

        if dx != 0 and board[ry][nx] == EMPTY:
            ny = ry

        elif dy != 0 and board[ny][rx] == EMPTY:
            nx = rx

        else:
            nx, ny = rx, ry

    return (nx, ny)


# Move robots and detect collisions
def move_robots(board, robots, player):
    destinations = []
    survivors = []

    for robot in robots:
        new_position = calculate_robot_move(
            board, robot, player
        )

        if board[new_position[1]][new_position[0]] == DEAD:
            board[robot[1]][robot[0]] = DEAD
        else:
            destinations.append(new_position)

    # Count robots at each destination
    position_counts = {}

    for position in destinations:
        position_counts[position] = (
            position_counts.get(position, 0) + 1
        )

    # Keep robots that do not collide
    for position, count in position_counts.items():

        if count == 1:
            survivors.append(position)

        else:
            x, y = position
            board[y][x] = DEAD

    return survivors


# Main game
def main():
    print("=" * 50)
    print("             HUNGRY ROBOTS")
    print("                EASY MODE")
    print("=" * 50)

    print("\nEscape from the hungry robots!")
    print("Make the robots crash into each other.")
    print("Use teleportation when you are in danger.")

    input("\nPress Enter to start...")

    board = create_board()
    robots = create_robots(board)

    player = find_empty(board, robots)

    teleports = NUM_TELEPORTS
    turn = 0

    while True:


        show_board(board, robots, player, turn)

        # Check winning condition
        if len(robots) == 0:
            print("\nCONGRATULATIONS!")
            print("You defeated all the robots!")
            print("You won the game!")
            break
        # Player movement
        player, teleports = player_move(
            board, robots, player, teleports
        )

        # Move robots
        robots = move_robots(board, robots, player)

        turn += 1

        # Check losing condition
        if player in robots:
            show_board(board, robots, player, turn)
            print("\nGAME OVER!")
            print("A robot caught you!")
            break


if __name__ == "__main__":
    main()