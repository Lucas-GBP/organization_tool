import { UUID } from "crypto";

export function arrayToMap<T extends { uuid: UUID }>(arr: T[]): Map<UUID, T> {
    return new Map(arr.map((item) => [item.uuid, item]));
}

export function mapToMap<T>(map: Map<UUID, T>): T[] {
    return Array.from(map.values());
}
