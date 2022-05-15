import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { DoorSystemModel } from './models/doorSystemModel.model';

const GET_DATA_URL = 'https://process-data-function.azurewebsites.net/api/GetData?code=x4Msd7v173A2OD77aLd-7ktRAMuNFwCd8lmTwxRI0DEXAzFuC14duw==';


@Injectable({
  providedIn:'root',
})
export class DoorSystemService {

  constructor(private http: HttpClient) { }

  getLastEntry() {
    return this.http.get<any>(GET_DATA_URL);
  }

  getAllData(){
    return this.http.get<any>(GET_DATA_URL);
  }
}