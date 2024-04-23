import chess


piece_material = {
    'P': 1,
    'N': 3,
    'B': 3,
    'R': 5,
    'Q': 9,
}

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8']

class Heuristics:
    def __init__(self):
        pass

    def legal_move_manipulation(self, board: chess.Board, uci_translator):
        coordinate_legal_moves = []
        capture_legal_moves = []
        uci_legal_moves = []
        for move in board.legal_moves:
            uci_legal_moves.append((str(move)[:2], str(move)[2:]))
            coord_move = uci_translator(str(move))
            coordinate_legal_moves.append(coord_move) # these are flipped
            end_square = coord_move[1]
            if board.piece_at(chess.parse_square(str(move)[2:])):
                capture_legal_moves.append(coord_move)
        return coordinate_legal_moves, capture_legal_moves, uci_legal_moves

    def piece_values(self, board: chess.Board):
        material = 0
        for letter in letters:
            for number in numbers:
                square = letter + number
                piece = str(board.piece_at(chess.parse_square(square)))
                if piece.lower() != 'k' and piece != 'None':
                    if piece.isupper():
                        material += piece_material[piece]
                    else:
                        material -= piece_material[piece.upper()]
        return material
    