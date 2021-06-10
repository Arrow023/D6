import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private route:Router) { }

  renderSamaritan()
  {
    let video = document.createElement('video');
    let full = document.getElementById('full');
    video.src = '../assets/samaritan2.mp4';
    video.autoplay = true;
    // video.muted = true;
    video.loop = true;
    video.style.position = 'absolute';
    video.style.right = '0';
    video.style.bottom = '0';
    video.style.top='0';
    video.style.left = '0';
    video.style.marginTop = '-80px';
    video.style.maxWidth = '100%';
    video.style.maxHeight = '120%';
    full.append(video);
    setTimeout(() => {
      full.removeChild(video);
      this.route.navigate(['trainer']);
  
    }, 17000);
  }

  ngOnInit(): void {
  }

}
