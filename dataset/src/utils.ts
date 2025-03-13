import Rand from "rand-seed";

export const bisectMax = async (
  min: number,
  max: number,
  predicate: (mid: number) => boolean | Promise<boolean>,
) => {
  let currentMin = min;
  let currentMax = max;
  while (currentMin < currentMax) {
    const mid = Math.floor((currentMin + currentMax) / 2);

    if (await predicate(mid)) {
      currentMin = mid + 1;
    } else {
      currentMax = mid;
    }
  }

  return currentMin;
};

export const createRandom = (seed: number) => {
  const rand = new Rand(String(seed));
  return () => rand.next();
}

export const shuffle = <T>(array: T[], random: () => number) => {
  const keys = Array.from({ length: array.length }, () => random());

  return array
    .map((value, index) => ({ value, key: keys[index] }))
    .sort((a, b) => a.key - b.key)
    .map(({ value }) => value);
};

// 半角カタカナ、ひらがなを全角カタカナに変換し、長音っぽい文字を長音に変換する
export const normalizeKana = (text: string) => {
  return text
    .replace(/[\uFF65-\uFF9F]/g, (s) =>
      String.fromCharCode(s.charCodeAt(0) - 0x60),
    )
    .replace(/[\u3041-\u3096]/g, (s) =>
      String.fromCharCode(s.charCodeAt(0) + 0x60),
    )
    .replace(/[ｰ－ー]/g, "ー");
};

export class ExhaustiveError extends Error {
  constructor(value: never, message?: string) {
    super(message ?? `Unexpected value: ${JSON.stringify(value, null, 2)}`);
  }
}
