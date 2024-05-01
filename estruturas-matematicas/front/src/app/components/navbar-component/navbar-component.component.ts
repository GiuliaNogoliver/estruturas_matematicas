import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ButtonComponentComponent } from "../button-component/button-component.component";

@Component({
    selector: 'app-navbar-component',
    standalone: true,
    templateUrl: './navbar-component.component.html',
    styleUrl: './navbar-component.component.scss',
    imports: [CommonModule, ButtonComponentComponent]
})
export class NavbarComponent{

}
