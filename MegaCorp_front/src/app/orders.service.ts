import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Token } from './models';

@Injectable({
  providedIn: 'root'
})
export class OrdersService {
  private apiUrl = 'http://localhost:8000/orders';

  constructor(private http: HttpClient) { }

  login(username: string, password: string): Observable<Token> {
    return this.http.post<Token>(
      `${this.apiUrl}/login/`,
      {username, password}
    )
  }

  register(username: string, password: string, role: string): Observable<any> {
    return this.http.post<any>(
      `${this.apiUrl}/register/`,
      { username, password, role }
    );
  }

  getOrders(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/`);
  }

  createOrder(order: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': 'Bearer ' + localStorage.getItem('access')
    });
    return this.http.post(`${this.apiUrl}/`, order, { headers: headers });
  }

  getCategories(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl + '/categories');
  }

  takeOrder(orderId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${orderId}/take/`, {});
  }

  getCurrentUserRole(): string {
    return localStorage.getItem('role') || ''; 
  }

  declineOrder(orderId: number): Observable<any> {
    return this.http.post(`/${orderId}/decline/`, {});
  }
  completeOrder(orderId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${orderId}/complete/`, {});
  }
}
