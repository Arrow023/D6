import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { ClientService} from '../client.service';
@Component({
  selector: 'app-chartlist',
  templateUrl: './chartlist.component.html',
  styleUrls: ['./chartlist.component.css']
})
export class ChartlistComponent implements OnInit {
  url = environment.SERVER_URL;
  list:any[] =[];
  
  constructor(private http:HttpClient, private route:Router, private client:ClientService) {
      this.http.get(this.url+"charts").subscribe((data)=>{
        this.list = data['List'];
      })
   }

  ngOnInit(): void {
  }

  viewCharts(i)
  {
    console.log(i);
    // this.client.selected_charts.next(i);
    this.route.navigate(['charts'],{queryParams:{file:i}});
  }

}
