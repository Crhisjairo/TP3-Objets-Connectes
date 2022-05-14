import { Component, OnInit } from '@angular/core';
import { DoorSystemService } from 'src/doorSystemService/doorSystemData.service';
import { DoorSystemModel } from 'src/doorSystemService/models/doorSystemModel.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'door-system-front-end';

  data: DoorSystemModel[] | undefined;

  constructor(
    private doorDataService: DoorSystemService,
  ){
    
  }
  ngOnInit(): void {
    this.fetchData();
  }



  fetchData(){
    this.doorDataService.getAllData().subscribe((data) => {
      console.log(data);
      
      this.data = [...data];

      console.log(this.data);
    
    });
  }
}
  
