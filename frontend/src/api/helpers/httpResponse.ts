export class HTTPResponse<T> {
    private _data: T;
    private _status: number;
    private _url: string;
    public constructor(url: string, data: T, status: number) {
      this._url = url;
      this._data = data;
      this._status = status;
    }
  
    public get url(): string {
      return this._url;
    }
  
    public get data(): T {
      return this._data;
    }
  
    public get status(): number {
      return this._status;
    }
  }
  