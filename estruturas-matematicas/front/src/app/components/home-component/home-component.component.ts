import { Component } from '@angular/core';
import { ButtonComponentComponent } from "../button-component/button-component.component";
import { NavbarComponent } from '../navbar-component/navbar-component.component';


@Component({
  selector: 'app-home-component',
  standalone: true,
  imports: [ButtonComponentComponent, NavbarComponent],
  templateUrl: './home-component.component.html',
  styleUrl: './home-component.component.scss'
})
export class HomeComponent{

}
