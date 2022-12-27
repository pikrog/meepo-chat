const emojiMap: [RegExp, string][] = [
  [/:ok:/gm, "✅"],
  [/:P/gm, "😛"],
];

export const addEmojisToString = (string: string) => {
  let value = string;

  emojiMap.forEach(([regexp, result]) => {
    value = value.replace(regexp, result);
  });

  return value;
};
