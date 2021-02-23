# Botnance

Botnance is a simple bot trading based on Crypto Trading Bot Project created by Larry.

## Requirements

- Docker
- Docker Compose
- Binance API key

## Prepare
Copy .env.example to .env and replace all values according to your trading criteria

```env
API_KEY=binanceapikey
API_SECRET=binancesecretkey
TRADE_SYMBOL=symbol
TRADE_QUANTITY=0.5
WS_URL=wss://stream.binance.com:9443/ws/dogebusd@kline_1m
```
For more information, you can watch this video https://www.youtube.com/watch?v=GdlFhF6gjKo

## Usage

```bash
docker-compose up
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Apache-2.0 License](http://www.apache.org/licenses/LICENSE-2.0)
