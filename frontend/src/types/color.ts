export type Color = `#${string}`;
export const isValidColor = (color: string): color is Color => {
    const hexColorRegex = /^#[0-9A-Fa-f]{3}([0-9A-Fa-f]{3})?$/;
    return hexColorRegex.test(color);
};
