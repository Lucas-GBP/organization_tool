export type ApiDateTime = `${number}-${number}-${number}T${number}:${number}:${number}.${number}Z`;
export const HexExpression = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/;
/**
 * Converte uma ApiDateTime em um objeto Date.
 * @param apiDate - A string no formato ApiDateTime.
 * @returns Um objeto Date.
 * @throws Error se a string não estiver no formato esperado.
 */
export function apiDateToDate(apiDate: ApiDateTime): Date {
    if (!HexExpression.test(apiDate)) {
      throw new Error("Invalid ApiDateTime format");
    }
    return new Date(apiDate);
  }

/**
 * Converte um Date para uma string no formato de ApiDateTime.
 * @param date - um objeto Date.
 * @returns string no formato ApiDateTime.
 */
export function dateToApiDate(date: Date): ApiDateTime {
  return date.toUTCString() as ApiDateTime;
}