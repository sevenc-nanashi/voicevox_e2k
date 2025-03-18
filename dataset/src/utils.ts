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

// 半角カタカナ、ひらがなを全角カタカナに変換し、長音っぽい文字を長音に変換する
const normalizeKana = (text: string) => {
  return text
    .replace(/[\uFF65-\uFF9F]/g, (s) =>
      String.fromCharCode(s.charCodeAt(0) - 0x60),
    )
    .replace(/[\u3041-\u3096]/g, (s) =>
      String.fromCharCode(s.charCodeAt(0) + 0x60),
    )
    .replace(/[ｰ―－ー]/g, "ー");
};

const normalizeOrNull = (pronunciation: string) => {
  const normalized = normalizeKana(pronunciation.trim());
  if (!normalized.match(/^[\p{Script=Katakana}ー]+$/u)) {
    return null;
  }
  return normalized;
};

export const filterPronunciations = (pronunciations: Record<string, string>) => {
  const filtered: Record<string, string> = {};
  for (const [word, pronunciation] of Object.entries(pronunciations)) {
    const normalized = normalizeOrNull(pronunciation);
    if (normalized == null) {
      console.error(`Invalid pronunciation: ${word} -> ${pronunciation}`);
      continue;
    }
    filtered[word] = normalized;
  }
  return filtered;
};

export class ExhaustiveError extends Error {
  constructor(value: never, message?: string) {
    super(message ?? `Unexpected value: ${JSON.stringify(value, null, 2)}`);
  }
}
