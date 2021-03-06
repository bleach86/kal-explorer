import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AddressService } from './address.service';
import { TransactionService } from './transactions.service';
import { environment } from '../environments/environment';
import * as moment from 'moment';
import { Observable } from 'rxjs';
import { Title }  from '@angular/platform-browser';


@Component({
    selector: 'address',
    templateUrl: './address.component.html',
    styleUrls: ['./address.component.scss']
})
export class AddressComponent implements OnInit {
    balance: Number;
    sent : Number;
    received : Number;
    sub: any;
    address: string;
    txs : any[] = [];

    sum = 100;
    throttle = 300;
    scrollDistance = 1;
    scrollUpDistance = 2;

    lastTime : Number;

    constructor(private router: Router, 
        private route: ActivatedRoute, 
        private addressService: AddressService, 
        private txService: TransactionService,
        private titleService : Title) {

    }

    onScrollDown() {
        console.log('add more');
        this.moreTxs();
    }

    ngOnInit() {
        this.route.params.subscribe(params => {
            this.address = params['address'];
            this.titleService.setTitle(this.address);
            this.addressService.getBalance(this.address).then(data => {
                this.balance = data.balance / environment.coin.division;
                this.sent = data.sent / environment.coin.division;
                this.received = data.received / environment.coin.division;
            });
            this.txs = [];
            this.moreTxs();
        });
    }

    moreTxs() {
        this.txService.getTransactions(this.address, this.lastTime).then(data => {
            if(data.length === 0){
                return;
            }
            for(let tx of data.txs){
                this.txs.push(tx);
            }
            this.lastTime = data.lastTime;
        });
    }

};

