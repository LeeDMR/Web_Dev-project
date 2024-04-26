// user.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = 'http://localhost:8000/orders';

  constructor(private http: HttpClient) { }

  getBalance(): Observable<{balance: number}> {
    return this.http.get<{balance: number}>(`${this.apiUrl}/user/balance`);
  }

  getOrders() {
    return this.http.get<any[]>(`${this.apiUrl}/user/orders`);
  }

  getReviews() {
    return this.http.get<any[]>(`${this.apiUrl}/user/reviews`);
  }
}
