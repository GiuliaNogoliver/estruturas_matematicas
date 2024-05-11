import { Component } from '@angular/core';
import { UploadService } from '../../upload.service';

@Component({
  selector: 'app-edit-component',
  standalone: true,
  imports: [],
  templateUrl: './edit-component.component.html',
  styleUrls: ['./edit-component.component.scss'] // Use styleUrls for styles
})
export class EditComponent {
  imageUrl: string | null = null; // Initialize imageUrl to null
  image: boolean = false;

  constructor(private uploadService: UploadService) { }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = (e: any) => {
      this.imageUrl = e.target.result as string;
      this.image = true;
    };

    this.uploadService.uploadFile(formData).subscribe(
      response => {
        console.log('Arquivo enviado com sucesso:', response);
      },
      error => {
        console.error('Erro ao enviar arquivo:', error);
      }
    );
  }
}
