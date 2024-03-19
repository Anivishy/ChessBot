import chess
import pygame
import time
from ui import UI
from pgn_translator import Translator
from Movemaker import Movemaker
pygame.init()
written_board = chess.Board()
size = 800
square_size = size / 8
movemaker = Movemaker()
all_moves = 'e4 e5 Nf3 Nc6 d4 exd4 c3 Nf6 e5 Qe7 cxd4 Qb4+ Bd2 Qxb2 exf6 Qxa1 Bc3 Qxa2 Bb5 Qe6+ Kd2 gxf6 Re1 Ne5 dxe5 fxe5 Rxe5 Qxe5 Nxe5 Be7 Qh5 Rf8 Bc4 d6 Nxf7 Kd7 Qf5+ Ke8 Qh5 Kd7 f4 c5 Qf5+ Kc6 Qxh7 b5 Qg6 bxc4 Ne5+ Kb7 Nxc4 Rxf4 Na5+ Kb8 Qg7 Rf2+ Ke3 Rxg2 Nc6+ Kb7 Qxe7+ Kxc6 Qe4+ Kc7 Qxg2 Kb8 Qg7 Bb7 Be5 Kc8 Bxd6 Bc6 Qc7#'
translator = Translator(all_moves)

#print(chess.Move.from_uci("e2e5") in written_board.legal_moves)
#print(written_board.san(chess.Move.from_uci("g1f3")))
#print(written_board.parse_san('e4'))

def automated_move(turn, moves, game_ui):
    if turn < len(moves):
        move = moves[turn]
        uci = translator.pgn_to_uci(move, written_board)
        chess_move = chess.Move.from_uci(uci)
        first_coord, second_coord = translator.uci_to_coordinates(uci)
        screen_move, promotion, castle_detection = translator.get_move_from_screen(first_coord, second_coord, game_ui.board)
        if chess_move in written_board.legal_moves:
            game_ui.selected_piece_movement(second_coord, first_coord, promotion, castle_detection)
            written_board.push(chess_move)
        time.sleep(1)

def game_loop():
    pgn_moves = []
    turn = 0
    game_ui = UI(size)
    game_over = False
    selected_piece = None
    moves = all_moves.split(' ')
    print(translator.uci_to_coordinates('e2e4'))
    #for move in moves:
        #uci = translator.pgn_to_uci(move, written_board)
        #print(uci)
        #written_board.push(chess.Move.from_uci(uci))
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if movemaker.get_state() == 0:
                    selected_piece = movemaker.get_current_piece_pos(pygame.mouse.get_pos(), game_ui.board, square_size)
                    game_ui.set_selected_square([selected_piece[0], (selected_piece[1])]) # needs to be converted to indices
                    movemaker.change_state()
                    print(selected_piece)
                else:
                    new_pos = movemaker.get_current_piece_pos(pygame.mouse.get_pos(), game_ui.board, square_size)
                    screen_move, promotion, castle_detection = translator.get_move_from_screen(game_ui.get_seleceted_square(), new_pos, game_ui.board)
                    print(screen_move)
                    chess_move = chess.Move.from_uci(screen_move)
                    if chess_move in written_board.legal_moves:
                        game_ui.selected_piece_movement(new_pos, selected_piece, promotion, castle_detection)
                        pgn_moves.append(written_board.san(chess_move))
                        written_board.push(chess_move)
                    game_ui.set_selected_square(None)
                    movemaker.change_state()
                    print(pgn_moves)
        '''
        if turn < len(moves):
            move = moves[turn]
            uci = translator.pgn_to_uci(move, written_board)
        '''
        automated_move(turn, moves, game_ui)
        game_ui.draw_grid()
        game_ui.draw_pieces()
        pygame.display.update()
        turn += 1
        

if __name__ == '__main__':
    game_loop()
