import { Component, OnInit, Renderer2, Inject } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Router } from '@angular/router';
declare var $ : any;
@Component({
  selector: 'app-trainer',
  templateUrl: './trainer.component.html',
  styleUrls: ['./trainer.component.css']
})
export class TrainerComponent implements OnInit {
  url = environment.SERVER_URL;
  timer :number;
  remaining : any;
  constructor( private _renderer2: Renderer2,
    private http:HttpClient,
    private route:Router,
    @Inject(DOCUMENT) private _document: Document) {
    
   }

  
  ngOnInit(): void {
    let script = this._renderer2.createElement('script');
    script.src = 'https://www.gstatic.com/charts/loader.js';
    this._renderer2.appendChild(this._document.body, script);
    script = this._renderer2.createElement('script');
    script.src = '../assets/charts.js';
    this._renderer2.appendChild(this._document.body, script);
  }

  trainModel(iteration, epochs)
  {
    $('#exampleModalCenter').modal('show');
    this.timer =24+((5 * iteration) * 1000);
    this.remaining = Math.floor(this.timer / 1000);
    this.http.get(`${this.url}/run?iteration=${iteration}&epoch=${epochs}`)
    .subscribe((response)=>{
          console.log(response);  
      })
      
    console.log(this.timer,this.remaining);
    setTimeout(() => {
      $('#exampleModalCenter').modal('hide');
      this.route.navigate(['plots']);
    }, this.timer);

    setInterval(()=>{
      this.remaining = this.remaining - 1;
    },1000)
    return false;
  }
  
}
