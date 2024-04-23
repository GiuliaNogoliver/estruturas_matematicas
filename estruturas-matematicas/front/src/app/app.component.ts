import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './components/navbar-component/navbar-component.component';
import { FooterComponent } from './components/footer-component/footer-component.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule, NavbarComponent],
  // templateUrl: './app.component.html',
  template: `
    <app-navbar-component />
    <router-outlet> </router-outlet>

  `,
  // styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'estruturas-matematicas';
}
