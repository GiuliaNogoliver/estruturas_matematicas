import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-edit-component',
  templateUrl: './edit-component.component.html',
  styleUrls: ['./edit-component.component.scss']
})
export class EditComponent {
  imageUrl: string | null = null;
  image: boolean = false;

  constructor(private http: HttpClient) { }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = (e: any) => {
      this.imageUrl = e.target.result as string;
      this.image = true;
    };

    reader.readAsDataURL(file);
  }

  convertToMonochrome() {
    if (this.imageUrl) {
      // corta a parte que tava estragando e deixa só a base 64
      const base64Data = this.imageUrl.split(',')[1];
      // chama o back e manda somente a imagem em base64
      this.http.post<string>('http://127.0.0.1:5000/monochrome', { image_data: base64Data })
        .subscribe((response: any) => {
          // tira a imagem de base64 e coloca no lugar da colorida
          this.imageUrl = 'data:image/jpeg;base64,' + response.monochrome_data;
        });
    }
  }
}
