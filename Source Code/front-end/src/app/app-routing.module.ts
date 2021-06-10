import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ChartlistComponent } from './chartlist/chartlist.component';
import { ChartsComponent } from './charts/charts.component';
import { HomeComponent } from './home/home.component';
import { ResourcesComponent } from './resources/resources.component';
import { TrainerComponent } from './trainer/trainer.component';

const routes: Routes = [
  { path :'', component:HomeComponent},
  { path:'trainer', component:TrainerComponent},
  { path:'resources', component:ResourcesComponent},
  { path:'plots', component:ChartlistComponent},
  { path:'charts', component:ChartsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
