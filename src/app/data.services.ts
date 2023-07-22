import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  private apiUrl = 'http://localhost:5000/api/run_notebook'; // Replace with your Flask API URL

  constructor(private http: HttpClient) { }

  runNotebook() {
    return this.http.get<any[]>(this.apiUrl);
  }
}
