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

export const shuffle = <T>(array: T[]) => {
  const keys = Array.from({ length: array.length }, () => Math.random());

  return array
    .map((value, index) => ({ value, key: keys[index] }))
    .sort((a, b) => a.key - b.key)
    .map(({ value }) => value);
};
