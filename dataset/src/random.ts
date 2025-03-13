import Rand from "rand-seed";

export class Random {
  private rand: Rand;

  constructor(seed: number) {
    this.rand = new Rand(String(seed));
  }

  random() {
    return this.rand.next();
  }

  shuffle<T>(array: T[]) {
    const keys = Array.from({ length: array.length }, () => this.random());

    return array
      .map((value, index) => ({ value, key: keys[index] }))
      .sort((a, b) => a.key - b.key)
      .map(({ value }) => value);
  }
}
