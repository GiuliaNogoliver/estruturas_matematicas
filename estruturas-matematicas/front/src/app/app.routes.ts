import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './components/home-component/home-component.component';
import { EditComponent } from './components/edit-component/edit-component.component';
import { AboutUsComponent } from './components/about-us-component/about-us-component.component';

export const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'edit', component: EditComponent},
  {path: 'about-us', component: AboutUsComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutes {}
