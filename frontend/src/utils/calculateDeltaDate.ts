export type DeltaDateType = {
    miliseconds: number,
    centiseconds: number,
    seconds: number,
    minutes: number,
    hours: number,
    days: number
}
export function calculateDeltaDate(start:Date, end?:Date):DeltaDateType {
    const calculate_thingy = (delta:number, factor:number) => {
        if(factor > delta){
            return 0
        }
        return Math.floor(delta/factor)
    }
    const delta_miliseconds = (end?end:new Date()).getTime() - start.getTime();

    const delta_centiseconds = calculate_thingy(delta_miliseconds, 10);
    const delta_seconds = calculate_thingy(delta_centiseconds, 100);
    const delta_minutes = calculate_thingy(delta_seconds, 60);
    const delta_hours = calculate_thingy(delta_minutes, 60);
    const delta_days = calculate_thingy(delta_hours, 24);

    const miliseconds = delta_miliseconds%1000;
    const centiseconds = delta_centiseconds%100;
    const seconds = delta_seconds%60;
    const minutes = delta_minutes%60;
    const hours = delta_hours%24;
    const days = delta_days;

    return {
        miliseconds,
        centiseconds,
        seconds,
        minutes,
        hours,
        days
    }
}

