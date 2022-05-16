import { Component, OnInit } from '@angular/core';
import { DoorSystemService } from 'src/doorSystemService/doorSystemData.service';
import { DoorSystemModel } from 'src/doorSystemService/models/doorSystemModel.model';
import { interval } from 'rxjs';
import { switchMap } from 'rxjs/operators'
import {MatCardModule} from '@angular/material/card';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'door-system-front-end';

  allData: DoorSystemModel[] | undefined;

  percentageValue: number = 0;

  //lastData est supossé contenir les dernieres entrées de la DB.
  //Pourtant, à cause que j'ai plus accès aux services Azure (À cause du manque du crédit),
  //les données vont être hardcodés
  //lastData: DoorSystemModel | undefined;
  lastData: DoorSystemModel = {
    deviceId: 'Raspberry Pi Device',
    temperature: 30,
    openDoorPercentage: 80,
    mode: 'auto'
  };

  constructor(
    private doorDataService: DoorSystemService,
  ){}
  ngOnInit(): void {
    //this.startFetchingData();
    this.fetchData();
  }

  /**
   * Recupère les données à chaque interval de temps.
   */
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

  /**
   * Recupère une fois les donneés de la DB.
   */
  fetchData(){
    this.doorDataService.getAllData().subscribe((data) => {
      this.allData = data.value as DoorSystemModel[];
      console.log(this.allData)
      this.lastData = this.allData[this.allData.length - 1];
      
      console.log(this.lastData);
    });
  }

  async sendMessage(mode: string, openDoorPercentage: string = "", action:string = ""){
    const message = {Mode: mode, OpenDoorPercentage: openDoorPercentage, Action: action };
    try {     
      const response = await fetch('https://process-data-function.azurewebsites.net/api/SendMessage?code=aGE7LF4NelxDXsYY_eIbTYmz6acRVGoycc1f1D-cF-CPAzFu-5oIiQ==', {
        method: 'post',
        body: JSON.stringify(message),
      });
      console.log('Completed!', response);
    } catch(err) {
      console.error(`Error: ${err}`);
    }
  }

  formatLabel(value: number) {
    if (value >= 100) {
      return 'Max';
    }

    return value;
  }
}
  
