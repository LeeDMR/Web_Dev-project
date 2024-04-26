import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms'
import { OrdersService } from '../orders.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-create-order',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './create-order.component.html',
  styleUrl: './create-order.component.css'
})
export class CreateOrderComponent {
  order = { title: '', description: '', category: null, reward: null };
  categories: any[] = [];

  constructor(private ordersService: OrdersService) {}

  onSubmit(): void {
    this.ordersService.createOrder(this.order).subscribe(result => {
      console.log('Order created', result);
    });
  }
  
  ngOnInit() {
    this.ordersService.getCategories().subscribe(data => {
      this.categories = data;
    });
  }
}
