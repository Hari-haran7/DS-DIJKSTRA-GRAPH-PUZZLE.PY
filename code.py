import heapq

class Puzzle:
    def __init__(self, state, moves=0, move_sequence=""):
        self.state = state  # Current state of the puzzle
        self.blank_index = state.index(0)  # Index of the blank space (0)
        self.moves = moves  # Number of moves taken to reach this state
        self.move_sequence = move_sequence  # String of moves taken

    def get_possible_moves(self):
        moves = []
        row, col = divmod(self.blank_index, 4)  # Convert index to (row, col)
        directions = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]  # Up, Down, Left, Right

        for dr, dc, move_char in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                new_index = new_row * 4 + new_col
                new_state = list(self.state)
                # Swap the blank space with the adjacent tile
                new_state[self.blank_index], new_state[new_index] = new_state[new_index], new_state[self.blank_index]
                moves.append(Puzzle(tuple(new_state), self.moves + 1, self.move_sequence + move_char))

        return moves

    def is_solved(self):
        return self.state == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)

    def __lt__(self, other):
        return self.moves < other.moves

def dijkstra(initial_state):
    pq = []
    heapq.heappush(pq, Puzzle(initial_state))
    visited = set()

    while pq:
        current_puzzle = heapq.heappop(pq)

        if current_puzzle.is_solved():
            return current_puzzle.moves, current_puzzle.move_sequence

        if current_puzzle.state in visited:
            continue
        visited.add(current_puzzle.state)

        for next_puzzle in current_puzzle.get_possible_moves():
            if next_puzzle.state not in visited:
                heapq.heappush(pq, next_puzzle)

    return -1, ""

def get_user_input():
    numbers = set()
    state = []

    print("Enter the 15-puzzle configuration (0 for blank space):")
    for i in range(4):
        while True:
            row = input(f"Enter row {i + 1} (4 numbers separated by spaces): ")
            row_numbers = list(map(int, row.split()))
            if len(row_numbers) == 4 and all(0 <= num <= 15 for num in row_numbers) and len(set(row_numbers)) == 4:
                if numbers.isdisjoint(row_numbers):  # Check for duplicates across rows
                    state.extend(row_numbers)
                    numbers.update(row_numbers)
                    break
                else:
                    print("Invalid numbers. Make sure to enter numbers from 0 to 15 without duplicates.")
            else:
                print("Invalid input. Please enter exactly 4 numbers from 0 to 15.")

    return tuple(state)

if __name__ == "__main__":
    initial_state = get_user_input()
    moves_needed, move_sequence = dijkstra(initial_state)

    if moves_needed != -1:
        print(f"Solution found in {moves_needed} moves: {move_sequence}")
    else:
        print("No solution exists for the given puzzle configuration.")
