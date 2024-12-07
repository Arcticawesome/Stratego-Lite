import random

# Board Setup
board = [
    ['EB1', 'EF1', 'EB2', 'EM1'],
    ['EM2', 'EB3', 'ES1', 'ES2'],
    [' . ', ' . ', ' . ', ' . '],
    [' . ', ' . ', ' . ', ' . '],
    ['M1 ', 'S1 ', 'B1 ', 'M2 '],
    ['S2 ', 'B2 ', 'F1 ', 'B3 ']
    ]

Enemy_troops = {
    'EF1': 0, 'EB1': 10, 'EB2': 12, 'EB3': 12,
    'ES1': 1, 'ES2': 1, "EM1": 11, "EM2": 11
}

your_troops = {
    'F1': 0, 'B1': 12, 'B2': 12, 'B3': 12,
    'S1': 1, 'S2': 1, 'M1': 11, 'M2': 11
}

game_over = False

while not game_over:

    def print_board(board): # Prints the board
        for i in range(len(board)):
            if i == 0:
                print("+---------------------+")
            print(f"{board[i][0]} | {board[i][1]} | {board[i][2]} | {board[i][3]} |")
            if i < 6:
                if i == 5:
                    print("+---------------------+")
                else:
                    print("+---+-----+-----+-----+")

    # Get index of a troop
    def getIndex(board, selected_troop):
        selected_troop = selected_troop.strip()
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell.strip() == selected_troop:
                    return i, j
        return None

    def move_troop(board, x, y, new_x, new_y):
        board[new_x][new_y] = board[x][y]
        board[x][y] = ' . '

    def combat_situation(attacker, defender, attacker_index, defender_index):
        if attacker in ['S1', 'S2'] and defender in ['EB1', 'EB2', 'EB3']:
            print(f"\n{attacker} defuses {defender}!")
            board[defender_index[0]][defender_index[1]] = attacker 
            board[attacker_index[0]][attacker_index[1]] = ' . '
           # print_board(board)
            return True

        if attacker in ['ES1', 'ES2'] and defender in ['B1', 'B2', 'B3']:
            print(f"\n{attacker} defuses {defender}!")
            board[defender_index[0]][defender_index[1]] = attacker 
            board[attacker_index[0]][attacker_index[1]] = ' . '
           # print_board(board)
            return True
         
        if attacker in your_troops and defender in ['EF1']:
            game_over = True

        if attacker in Enemy_troops and defender in ['F1']:
            game_over = True

        attacker_value = your_troops.get(attacker, Enemy_troops.get(attacker, 0))
        defender_value = your_troops.get(defender, Enemy_troops.get(defender, 0))

        if attacker_value > defender_value:
            print(f"\n{attacker} defeats {defender}")
            board[defender_index[0]][defender_index[1]] = attacker
            board[attacker_index[0]][attacker_index[1]] = ' . '
        elif attacker_value == defender_value:
            print(f"\n{attacker} and {defender} destroy each other.")
            board[defender_index[0]][defender_index[1]] = ' . '
            board[attacker_index[0]][attacker_index[1]] = ' . '
        else:
            print(f"\n{defender} defeats {attacker}!")
            board[attacker_index[0]][attacker_index[1]] = ' . '
        return False
    
    def check_flag_capture(selected_troop, new_x, new_y, board):
        global game_over
        target_cell = board[new_x][new_y].strip()

        if selected_troop in your_troops:
            if target_cell == 'EF1':
                index = getIndex(board, selected_troop)
                x, y = index
                board[x][y] = ' . '
                board[new_x][new_y] = selected_troop
                print(f"You have captured the enemy flag (EF1). You win!")
                print_board(board)
                game_over = True
                return True
        elif selected_troop in Enemy_troops:
            if target_cell == 'F1':
                index = getIndex(board, selected_troop)
                x, y = index
                board[x][y] = ' . '
                board[new_x][new_y] = selected_troop
                print(f"AI has captured your flag (F1). You lose!")
                print_board(board)
                game_over = True
                return True
        return False


    def player_move(board, your_troops):
        immovable_troops = {'F1', 'B1', 'B2', 'B3'}
        while True:
            selected_troop = input("Select a troop: ").strip()
            if selected_troop in your_troops:
                if selected_troop in immovable_troops:
                    print(f"The troop {selected_troop} cannot be moved.")
                    continue

                print(f'{selected_troop} is selected.')
                index = getIndex(board, selected_troop)
                if not index:
                    print(f"Troop {selected_troop} not found on the board.")
                    continue

                x, y = index
                print(f"The troop {selected_troop} is at: {index}")
                direction = input("Where do you want to move it? (Up, Down, Left, Right): ").strip().lower()

                new_x, new_y = x, y
                if direction == 'up' and x > 0:
                    new_x -= 1
                elif direction == 'down' and x < len(board) - 1:
                    new_x += 1
                elif direction == 'left' and y > 0:
                    new_y -= 1
                elif direction == 'right' and y < len(board[0]) - 1:
                    new_y += 1
                else:
                    print("Invalid move. Try again.")
                    continue

                target_cell = board[new_x][new_y].strip()

                if check_flag_capture(selected_troop, new_x, new_y, board):
                    return 

                if target_cell == '.':
                    move_troop(board, x, y, new_x, new_y)
                    print("\nMove is successful.")
                 #   print_board(board)
                    return
                elif target_cell in Enemy_troops:
                    combat_situation(selected_troop, target_cell, (x, y), (new_x, new_y))
                 #   print_board(board)
                    return
                elif target_cell in your_troops:
                    print("Cannot move there. Position is taken by your own troop.")
                else:
                    print("Invalid move.")
            else:
                print("Select a valid troop")
        
    def ai_move(board):
        print("\nAI Player's move.\n")
        immovable_troops = {'EF1', 'EB1', 'EB2', 'EB3'}
        ai_troops = []
        directions = ['up', 'down', 'left', 'right']

        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell.strip() in Enemy_troops and cell.strip() not in immovable_troops:
                    ai_troops.append((cell.strip(), i, j))

        while ai_troops:
            troop, x, y = random.choice(ai_troops)
            random.shuffle(directions)
            for direction in directions:
                new_x, new_y = x, y
                if direction == 'up' and x > 0:
                    new_x -= 1
                elif direction == 'down' and x <  len(board) - 1:
                    new_x += 1
                elif direction == 'left' and y > 0:
                    new_y -= 1
                elif direction == 'right' and y < len(board[0]) - 1:
                    new_y += 1
                else:
                    continue

                target_cell = board[new_x][new_y].strip()

                if check_flag_capture(troop, new_x, new_y, board):
                    return

                if target_cell == '.':
                    move_troop(board, x, y, new_x, new_y)
                    print(f"The AI moved {troop} from ({x}, {y}) to ({new_x}, {new_y}).")
               #     print_board(board)
                    return troop, new_x, new_y

                if target_cell in your_troops:
                    combat_situation(troop, target_cell, (x, y), (new_x, new_y))
                #    print_board(board)
                    return troop, new_x, new_y
                    

            ai_troops.remove((troop, x, y))

        print("Computer has no valid moves left")
        return None, None, None

    def has_movable_troops(board, troops, immovable_troops):
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell.strip() in troops and cell.strip() not in immovable_troops:
                    directions = ['up', 'down', 'left', 'right']
                    for direction in directions:
                        new_x, new_y = i, j
                        if direction == 'up' and i > 0:
                            new_x -= 1
                        elif direction == 'down' and i < len(board) - 1:
                            new_x += 1
                        elif direction == 'left' and j > 0:
                            new_y -= 1
                        elif direction == 'right' and j < len(board[0]) - 1:
                            new_y += 1
                        else:
                            continue

                        target_cell = board[new_x][new_y].strip()
                        if target_cell == '.' or target_cell in (your_troops if troops == Enemy_troops else Enemy_troops):
                            return True
        return False


    print_board(board)
    
    if game_over:
        break
        
 

    player_can_move = has_movable_troops(board, your_troops, {'F1', 'B1', 'B2', 'B3'})
    if player_can_move:
        player_move(board, your_troops)
    else:
        print("You have no valid moves. Skipping your turn...")

    if game_over:
        break

    ai_can_move = has_movable_troops(board, Enemy_troops, {'EF1', 'EB1', 'EB2', 'EB3'})
    if ai_can_move:
        result_check = ai_move(board)
        if result_check and result_check[0]:
            troop, new_x, new_y = result_check
            if troop and check_flag_capture(troop, new_x, new_y, board):
                break
        if game_over:
            break
    else:
        print("The AI has no valid moves. Skipping its turn...")

    if not player_can_move and not ai_can_move:
        print("Neither player can move. It's a draw!")
        game_over = True
        break
        
            
