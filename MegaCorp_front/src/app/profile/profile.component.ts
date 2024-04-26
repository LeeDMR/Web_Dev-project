// profile.component.ts
import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';
import { OrdersService } from '../orders.service';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  imports: [CommonModule],
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  balance: number | undefined;
  orders: any[] = [];
  reviews: any[] = [];

  constructor(private userService: UserService, private ordersService: OrdersService) { }

  ngOnInit() {
    this.userService.getBalance().subscribe(data => this.balance = data.balance);
    this.userService.getOrders().subscribe(data => this.orders = data);
    this.userService.getReviews().subscribe(data => this.reviews = data);
  }

  completeOrder(orderId: number) {
    this.ordersService.completeOrder(orderId).subscribe({
      next: (response) => {
        console.log(response.message);
        this.orders = this.orders.filter(order => order.id !== orderId);
      },
      error: (error) => {
        console.error('Error completing the order', error);
      }
    });
  }
}
