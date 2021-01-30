const WHITE = 1;
const BLACK = 0;
const imgroot = 'https://raw.githubusercontent.com/r2dev2/WayChess/master/img/';

export class CPiece {
  constructor(fenValue) {
    this.name = {
      p: 'pawn',
      n: 'knight',
      b: 'bishop',
      r: 'rook',
      q: 'queen',
      k: 'king'
    }[fenValue.toLowerCase()];
    this.colorNum = /[a-z]/.exec(fenValue) ? BLACK : WHITE;
    this.color = this.colorNum ? 'white' : 'black';
  }

  getClass() {
    return `${this.color} ${this.name}`;
  }

  getImg() {
    return `${imgroot}${this.color}/${this.name}.png`;
  }
}
