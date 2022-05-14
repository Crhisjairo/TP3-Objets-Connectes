import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { DoorSystemModel } from './models/doorSystemModel.model';

const urlPrefix = 'https://localhost:44337/';

@Injectable({
  providedIn:'root',
})
export class DoorSystemService {

  constructor(private http: HttpClient) { }

  getLastEntry() {
    return this.http.get<DoorSystemModel>(urlPrefix + 'api/DoorSystemModels');
  }

  getAllData(){
    return this.http.get<DoorSystemModel[]>(urlPrefix + 'api/DoorSystemModels');
  }
}