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
      // Extract base64 data from the URL
      const base64Data = this.imageUrl.split(',')[1]; // Split at the comma and take the second part
      // Send only the base64 encoded image data to the server
      this.http.post<string>('http://127.0.0.1:5000/monochrome', { image_data: base64Data })
        .subscribe((response: any) => {
          // Update imageUrl with the base64 encoded monochrome image data
          this.imageUrl = 'data:image/jpeg;base64,' + response.monochrome_data;
        });
    }
  }
}
