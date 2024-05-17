import { Component, Renderer2 } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import download from 'downloadjs';

@Component({
  selector: 'app-edit-component',
  templateUrl: './edit-component.component.html',
  styleUrls: ['./edit-component.component.scss']
})

export class EditComponent {
  imageUrl: string | null = null;
  ogImageUrl: string | null = null;
  image: boolean = false;
  loading = document.getElementsByClassName('loading') as HTMLCollectionOf<HTMLElement>;
  altText = document.getElementsByClassName('alt-text') as HTMLCollectionOf<HTMLElement>;
  selectedImage = document.getElementsByClassName('selected-image') as HTMLCollectionOf<HTMLElement>;
  scale = document.getElementsByClassName('escala') as HTMLCollectionOf<HTMLElement>;
  brightness = document.getElementsByClassName('brilho') as HTMLCollectionOf<HTMLElement>;
  rotation = document.getElementsByClassName('rotacao') as HTMLCollectionOf<HTMLElement>;
  ranges = document.getElementsByTagName('range')  as HTMLCollectionOf<HTMLElement>;

  constructor(private http: HttpClient) {
  }

  scaleValue(event: any){
    console.log(event.target.value)
    this.scale[0].innerHTML = event.target.value
  }
  brightnessValue(event: any){
    console.log(event.target.value)
    this.brightness[0].innerHTML = event.target.value
  }
  rotationValue(event: any){
    console.log(event.target.value)
    this.rotation[0].innerHTML = event.target.value
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = (e: any) => {
      this.imageUrl = e.target.result as string;
      this.ogImageUrl = e.target.result as string;
      // this.canva[0].style.width = this.selectedImage[0].style.width
      // this.canva[0].style.height = this.selectedImage[0].style.height
      this.image = true;
      this.selectedImage[0].style.visibility = 'visible'
      this.altText[0].style.visibility = 'hidden'
    };

    reader.readAsDataURL(file);
  }

  applyChanges() {
    if (this.imageUrl) {
      this.loading[0].style.visibility = "visible";
      // corta a parte que tava estragando e deixa só a base 64
      const base64Data = this.imageUrl.split(',')[1];
      const scaleNum = this.scale[0].innerHTML;
      const brightnessNum = this.brightness[0].innerHTML; 
      const rotationNum = this.rotation[0].innerHTML;
      // chama o back e manda somente a imagem em base64
      this.http.post<string>('http://127.0.0.1:5000/apply', { image_data: base64Data, scale_data: scaleNum, brightness_data: brightnessNum, rotation_data: rotationNum})
        .subscribe((response: any) => {
          // tira a imagem de base64 e coloca no lugar da colorida
          this.imageUrl = 'data:image/jpeg;base64,' + response.monochrome_data;
          this.loading[0].style.visibility = "hidden";
        });
    }
  }

  convertToMonochrome() {
    if (this.imageUrl) {
      this.loading[0].style.visibility = "visible";
      // corta a parte que tava estragando e deixa só a base 64
      const base64Data = this.imageUrl.split(',')[1];
      // chama o back e manda somente a imagem em base64
      this.http.post<string>('http://127.0.0.1:5000/monochrome', { image_data: base64Data })
        .subscribe((response: any) => {
          // tira a imagem de base64 e coloca no lugar da colorida
          this.imageUrl = 'data:image/jpeg;base64,' + response.monochrome_data;
          this.loading[0].style.visibility = "hidden";
        });
    }
  }

  convertToNormal() {
    if (this.imageUrl) {
      // substitui o link alterado pelo original
      this.imageUrl = this.ogImageUrl;
    }
  }

  convertToSepia() {
    if (this.imageUrl) {
      this.loading[0].style.visibility = "visible";
      // corta a parte que tava estragando e deixa só a base 64
      const base64Data = this.imageUrl.split(',')[1];
      // chama o back e manda somente a imagem em base64
      this.http.post<string>('http://127.0.0.1:5000/sepia', { image_data: base64Data })
        .subscribe((response: any) => {
          // tira a imagem de base64 e coloca no lugar da colorida
          this.imageUrl = 'data:image/jpeg;base64,' + response.sepia_data;
          this.loading[0].style.visibility = "hidden";
        });
    }
  }

  convertToNegative() {
    if (this.imageUrl) {
      this.loading[0].style.visibility = "visible";
      // corta a parte que tava estragando e deixa só a base 64
      const base64Data = this.imageUrl.split(',')[1];
      // chama o back e manda somente a imagem em base64
      this.http.post<string>('http://127.0.0.1:5000/negative', { image_data: base64Data })
        .subscribe((response: any) => {
          // tira a imagem de base64 e coloca no lugar da colorida
          this.imageUrl = 'data:image/jpeg;base64,' + response.negative_data;
          this.loading[0].style.visibility = "hidden";
        });
    }
  }

  convertToBlue() {
    if (this.imageUrl) {
      this.loading[0].style.visibility = "visible";
      // corta a parte que tava estragando e deixa só a base 64
      const base64Data = this.imageUrl.split(',')[1];
      // chama o back e manda somente a imagem em base64
      this.http.post<string>('http://127.0.0.1:5000/blue', { image_data: base64Data })
        .subscribe((response: any) => {
          // tira a imagem de base64 e coloca no lugar da colorida
          this.imageUrl = 'data:image/jpeg;base64,' + response.blue_data;
          this.loading[0].style.visibility = "hidden";
        });
    }
  }

  convertToRed() {
    if (this.imageUrl) {
      this.loading[0].style.visibility = "visible";
      // corta a parte que tava estragando e deixa só a base 64
      const base64Data = this.imageUrl.split(',')[1];
      // chama o back e manda somente a imagem em base64
      this.http.post<string>('http://127.0.0.1:5000/red', { image_data: base64Data })
        .subscribe((response: any) => {
          // tira a imagem de base64 e coloca no lugar da colorida
          this.imageUrl = 'data:image/jpeg;base64,' + response.red_data;
          this.loading[0].style.visibility = "hidden";
        });
    }
  }

  convertToGreen() {
    if (this.imageUrl) {
      this.loading[0].style.visibility = "visible";
      // corta a parte que tava estragando e deixa só a base 64
      const base64Data = this.imageUrl.split(',')[1];
      // chama o back e manda somente a imagem em base64
      this.http.post<string>('http://127.0.0.1:5000/green', { image_data: base64Data })
        .subscribe((response: any) => {
          // tira a imagem de base64 e coloca no lugar da colorida
          this.imageUrl = 'data:image/jpeg;base64,' + response.green_data;
          this.loading[0].style.visibility = "hidden";
        });
    }
  }

  exportImage(){
    if(this.image){
      download((this.imageUrl as string), "image.jpg", "text/plain")
    }

  }
}
