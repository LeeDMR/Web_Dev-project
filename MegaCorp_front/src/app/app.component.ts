import { HttpClientModule } from '@angular/common/http';
import { Component, Inject, OnInit, PLATFORM_ID } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { OrdersListComponent } from './orders-list/orders-list.component';
import { CreateOrderComponent } from './create-order/create-order.component';
import { OrdersService } from './orders.service';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ProfileComponent } from './profile/profile.component';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, OrdersListComponent, CreateOrderComponent, HttpClientModule, CommonModule, FormsModule, ProfileComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  providers: [OrdersService]
})
export class AppComponent{

  title = 'MegaCorp_front'
  showRegistrationForm = false;;
  logged: boolean = false;
  username: string = "";
  password: string = "";
  usernameReg: string = "";
  passwordReg: string = "";
  role: string = 'client';


  constructor(@Inject(PLATFORM_ID) private platformId: Object, private orderService: OrdersService, private router: Router) {
  }

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      const access = localStorage.getItem("access");
      if (access) {
        this.logged = true;
      }
    }
  }

  login() {
    if (isPlatformBrowser(this.platformId)) {
      this.orderService
        .login(this.username, this.password)
        .subscribe((data) => {
          this.logged = true;
          localStorage.setItem("access", data.access);
          localStorage.setItem("refresh", data.refresh);
        });
    }
  }
  register(): void {
    this.orderService.register(this.usernameReg, this.passwordReg, this.role).subscribe({
      next: (response) => {
        console.log('Registration successful', response);
      },
      error: (error) => {
        console.error('Registration failed', error);
      }
    });
  }

  logout() {
    if (isPlatformBrowser(this.platformId)) {
      this.logged = false;
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
    }
  }
  goToCreateOrder() {
    this.router.navigate(['/create-order']);
  }

}
