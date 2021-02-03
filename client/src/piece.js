const WHITE = 1;
const BLACK = 0;
const imgroot = "/public/extimg/";

export class CPiece {
  constructor(fenValue) {
    this.fenValue = fenValue;
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
