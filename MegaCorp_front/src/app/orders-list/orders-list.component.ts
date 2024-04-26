import { Component, OnInit } from '@angular/core';
import { OrdersService } from '../orders.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-orders-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './orders-list.component.html',
  styleUrl: './orders-list.component.css'
})
export class OrdersListComponent implements OnInit {
  orders: any[] = [];
  isExecutor: boolean = false;
  constructor(private ordersService: OrdersService) {}

  ngOnInit(): void {
    this.checkUserRole();
    this.ordersService.getOrders().subscribe(data => {
      this.orders = data.filter(order => !order.executor); 
    });
    this.ordersService.getOrders().subscribe(data => {
      this.orders = data;
    });
  }

  checkUserRole() {
    this.isExecutor = this.ordersService.getCurrentUserRole() === 'executor'; 
  }

  takeOrder(orderId: number) {
    this.ordersService.takeOrder(orderId).subscribe({
        next: () => {
            console.log('Order taken successfully');
        },
        error: (error) => console.error('Failed to take order', error)
    });
  }


}
