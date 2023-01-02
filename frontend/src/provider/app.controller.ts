import { Controller, Get } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

@Controller('api')
export class AppController {
  constructor(private readonly configService: ConfigService) {}

  @Get('master')
  getAddress() {
    return {
      masterServerAddress: this.configService.get('MASTER_SERVER_ADDRESS'),
    };
  }
}
