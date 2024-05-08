import { Component } from '@angular/core';
import { UploadService } from '../../upload.service';

@Component({
  selector: 'app-edit-component',
  standalone: true,
  imports: [],
  templateUrl: './edit-component.component.html',
  styleUrl: './edit-component.component.scss'
})
export class EditComponent {

  constructor(private uploadService: UploadService) { }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

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
