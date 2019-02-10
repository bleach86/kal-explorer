import { Component } from '@angular/core';
import {Router} from "@angular/router";
import { AddressService } from './address.service';
import { environment } from '../environments/environment';
import { Title }  from '@angular/platform-browser';


@Component({
  templateUrl: './richlist.component.html',
//   styleUrls: ['./home.component.scss']
})
export class RichListComponent {
  title = 'Rich List';
  richlist : any [];
  distribution : object;
  environment = environment;

  constructor(private router : Router, private addressService : AddressService, private titleService : Title) {
    titleService.setTitle('Rich List');
    this.addressService.getRichList().then(data => {
        this.richlist = data;
    });

    this.addressService.getDistribution().then(data => {
      this.distribution = data;
    });
  }

  goAddress(addr : String) {
    this.router.navigate(['address', addr]);
  }
};

