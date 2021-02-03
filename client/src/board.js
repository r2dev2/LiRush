import { CPiece } from './piece.js';
import { Chess } from 'chess.js';

export class CBoard {
  constructor(fen) {
    this.fen = fen;
    const parts = fen.split(' ');
    const ranks = parts[0].split('/');
    const pieces = [];
    ranks.forEach((rank, i) => {
      let file = 0;
      Array.from(rank).forEach((s, j) => {
        if (/[1234567]/.exec(s)) {
          file += parseInt(s);
        } else if (s !== '8') {
          const piece = new CPiece(s);
          pieces.push({ piece, rank: 7 - i, file, pieceL: s });
          file++;
        }
      })
    });
    const otherInfo = parts.slice(1).join('');
    this.turn = /w/.exec(otherInfo) ? true: false;
    this.pieces = pieces;
    this.chess = new Chess(fen);
  }

  validate(move) {
    const from = `${'abcdefgh'[move.from.file]}${move.from.rank + 1}`
    const to = `${'abcdefgh'[move.to.file]}${move.to.rank + 1}`
    return this.chess.moves({ square: from, verbose: true})
      .map(({ to }) => to)
      .includes(to);
  }

  move(m) {
    const from = `${'abcdefgh'[m.from.file]}${m.from.rank + 1}`;
    const to = `${'abcdefgh'[m.to.file]}${m.to.rank + 1}`;
    const newChess = new Chess(this.chess.fen());
    newChess.move({ from, to });
    return new CBoard(newChess.fen());
  }

  move_uci(uci) {
    const newChess = new Chess(this.chess.fen());
    newChess.move(uci, { sloppy: true });
    return new CBoard(newChess.fen());
  }
}
