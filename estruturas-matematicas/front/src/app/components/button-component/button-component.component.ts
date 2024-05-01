import { Component, Input, input } from '@angular/core';

@Component({
  selector: 'app-button-component',
  standalone: true,
  imports: [],
  templateUrl: './button-component.component.html',
  styleUrl: './button-component.component.scss'
})
export class ButtonComponentComponent {
  @Input() label="";
  @Input() url="";
}
