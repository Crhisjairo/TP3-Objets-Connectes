import { Component, OnInit } from '@angular/core';
import { DoorSystemService } from 'src/doorSystemService/doorSystemData.service';
import { DoorSystemModel } from 'src/doorSystemService/models/doorSystemModel.model';
import { interval } from 'rxjs';
import { switchMap } from 'rxjs/operators'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'door-system-front-end';

  allData: DoorSystemModel[] | undefined;
  lastData: DoorSystemModel | undefined;

  constructor(
    private doorDataService: DoorSystemService,
  ){
    
  }
  ngOnInit(): void {
    //this.startFetchingData();
    this.fetchData();
  }

  startFetchingData(){
    interval(5000).pipe(
      switchMap(() => this.doorDataService.getAllData())
    ).subscribe(data => {
      this.allData = [...data];
      this.lastData = this.allData[this.allData.length - 1];
      console.log(this.lastData);
      console.log(this.allData);
    });;
  }

  fetchData(){
    this.doorDataService.getAllData().subscribe((data) => {
      this.allData = [...data];
      this.lastData = this.allData[this.allData.length - 1];
      console.log(data);
      console.log(this.lastData);
    });
  }
}
  
