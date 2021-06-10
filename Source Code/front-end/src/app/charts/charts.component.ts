import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { DomSanitizer } from '@angular/platform-browser';
@Component({
  selector: 'app-charts',
  templateUrl: './charts.component.html',
  styleUrls: ['./charts.component.css']
})
export class ChartsComponent implements OnInit {
  file_data ;
  url = environment.SERVER_URL;
  selected_charts;
  mse:any;
  ssim:any;
  psnr:any;
  pcc:any;
  training:any;
  iterations : any;
  epochs : any;
  xtrain : any;
  xtest: any;
  x_reconstructed_train : any;
  x_reconstructed_test : any;
  svm:any;
  random : any;
  xgboost: any;
  configuration = {'displayModeBar': false, 'scrollZoom':true};

  
  constructor(private http:HttpClient,private activated: ActivatedRoute,  private sanitizer: DomSanitizer) { 
    this.activated.queryParams.subscribe((data)=>{
      this.selected_charts = data.file;
    });   
  }

  fetchFile()
  {
    this.http.get(this.url+'/charts/'+this.selected_charts).subscribe((result)=>{
      this.iterations = result['Iterations'];
      this.epochs = result['Epochs'];
      this.mse = {
        data: [
            { x: result['MSE'].Models, y: result['MSE'].Accuracy, type: 'bar' }
        ],
        layout: {height:380,width:380,title: 'Mean Squared Error',paper_bgcolor:"black", plot_bgcolor:'black',
        font: {
          family: 'Sitka Text',
          size: 12,
          color: 'white'
        }}
      };
      this.ssim = {
        data: [
            { x: result['SSIM'].Models, y: result['SSIM'].Accuracy, type: 'bar' }
        ],
        layout: {height:380,width:380,title: 'Structured Similarity Index',paper_bgcolor:"black", plot_bgcolor:'black',
        font: {
          family: 'Sitka Text',
          size: 12,
          color: 'white'
        }}
      };
      this.psnr = {
        data: [
            { x: result['PSNR'].Models, y: result['PSNR'].Accuracy, type: 'bar' }
        ],
        layout: {height:380,width:380,title: 'Peak Signal Noise Ratio',paper_bgcolor:"black", plot_bgcolor:'black',font: {
          family: 'Sitka Text',
          size: 12,
          color: 'white'
        }}
      };
      this.pcc = {
        data: [
            { x: result['PCC'].Models, y: result['PCC'].Accuracy, type: 'bar' }
        ],
        layout: {height:380,width:380,title: 'Pearson Correlation Coefficient',paper_bgcolor:"black", plot_bgcolor:'black',font: {
          family: 'Sitka Text',
          size: 12,
          color: 'white'
        }}
      };
      this.training = {
        data: [
            { x: result['Training'].Models, y: result['Training'].Accuracy, type: 'bar' }
        ],
        layout: {height:380,width:380,title: 'Comparison of Metrics during Training',paper_bgcolor:"black", plot_bgcolor:'black', 
                  font: {
          family: 'Sitka Text',
          size: 12,
          color: 'white'
        }}
      };

    })

    this.getImage('X_train.png').subscribe((baseImage : any) => {
      let objectURL = URL.createObjectURL(baseImage);
       this.xtrain = this.sanitizer.bypassSecurityTrustUrl(objectURL);
    });
    this.getImage('X_test.png').subscribe((baseImage : any) => {
      let objectURL = URL.createObjectURL(baseImage);
       this.xtest = this.sanitizer.bypassSecurityTrustUrl(objectURL);
    });
    this.getImage('X_reconstructed_train.png').subscribe((baseImage : any) => {
      let objectURL = URL.createObjectURL(baseImage);
       this.x_reconstructed_train = this.sanitizer.bypassSecurityTrustUrl(objectURL);
    });
    this.getImage('X_reconstructed_test.png').subscribe((baseImage : any) => {
      let objectURL = URL.createObjectURL(baseImage);
       this.x_reconstructed_test = this.sanitizer.bypassSecurityTrustUrl(objectURL);
    });

    this.fetchClassificationScores('random').subscribe((response)=>{
      this.random = response;
    })

    this.fetchClassificationScores('svm').subscribe((response)=>{
      this.svm = response;
    })

    this.fetchClassificationScores('xgboost').subscribe((response)=>{
      this.xgboost = response;
    })


  }

  ngOnInit(): void {
    this.fetchFile();
  }

  fetchClassificationScores(classifier)
  {
    return this.http.get(this.url+'/classification/'+classifier);
  }

  fetchPlots(file:string)
  {
    return this.http.get(this.url+'/plot/'+file);
  }

  getImage(imageUrl: string): Observable<Blob> {
    return this.http.get(this.url+'/plot/'+imageUrl, { responseType: 'blob' });
  }


}
