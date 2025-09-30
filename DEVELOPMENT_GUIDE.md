# Python Deriv API - Development Guide

## Project Overview

This is a Python client library for the Deriv WebSocket API, enabling developers to:
- Connect to Deriv's trading platform
- Execute trades and manage accounts
- Subscribe to real-time market data
- Build trading bots and applications

## Project Structure

```
python-deriv-api/
├── deriv_api/                 # Main package
│   ├── __init__.py           # Package initialization
│   ├── deriv_api.py          # Core API class
│   ├── deriv_api_calls.py    # Auto-generated API methods
│   ├── subscription_manager.py # Real-time subscriptions
│   ├── cache.py              # Caching system
│   ├── errors.py             # Error handling
│   ├── middlewares.py        # Middleware hooks
│   ├── utils.py              # Utility functions
│   ├── easy_future.py        # Future wrapper
│   ├── in_memory.py          # In-memory storage
│   └── streams_list.py       # Stream management
├── examples/                 # Usage examples
│   ├── simple_bot1.py        # Basic trading bot
│   ├── simple_bot2.py        # Advanced bot
│   ├── simple_bot3.py        # Subscription example
│   └── simple_bot4.py        # Error handling
├── tests/                    # Test suite
├── docs/                     # Documentation
├── scripts/                  # Build scripts
├── setup.py                  # Package setup
├── pyproject.toml           # Modern Python packaging
├── Pipfile                  # Pipenv dependencies
└── Makefile                 # Build commands
```

## Development Environment Setup

### Prerequisites
- Python 3.9.6+ (3.9.7 excluded due to websockets bug)
- pip3

### Setup Steps

1. **Clone and navigate to project:**
   ```bash
   cd "/home/mureti/Desktop/Mureti code projects/python-deriv-api"
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install websockets==10.3 reactivex==4.0.*
   pip install -e .
   ```

4. **Install development dependencies:**
   ```bash
   pip install pytest pytest-asyncio pytest-mock
   ```

5. **Run tests:**
   ```bash
   python -m pytest tests/ -v
   ```

## Key Features

### 1. WebSocket Connection Management
- Automatic connection handling
- Reconnection support
- Connection state management

### 2. Real-time Data Subscriptions
- Market data streams (ticks, candles)
- Account updates
- Contract monitoring
- Reactive programming with RxPY

### 3. Caching System
- In-memory caching
- Persistent storage support
- Automatic cache management

### 4. Error Handling
- Comprehensive error types
- Connection error recovery
- API error handling

### 5. Middleware Support
- Request/response interceptors
- Custom processing hooks
- Logging and monitoring

## Core Classes

### DerivAPI
Main API class providing:
- WebSocket connection management
- API call execution
- Subscription management
- Caching integration

### SubscriptionManager
Handles real-time subscriptions:
- Stream management
- Subscription lifecycle
- Memory optimization

### Cache
Caching system with:
- In-memory storage
- Persistent storage support
- Automatic invalidation

## Usage Examples

### Basic Connection
```python
from deriv_api import DerivAPI

# Create API instance
api = DerivAPI(app_id=1089)

# Test connection
response = await api.ping({'ping': 1})
print(response)
```

### Authentication
```python
# Authorize with token
authorize = await api.authorize(api_token)
print(authorize)

# Get account balance
balance = await api.balance()
print(f"Balance: {balance['balance']['balance']} {balance['balance']['currency']}")
```

### Trading Operations
```python
# Get proposal
proposal = await api.proposal({
    "proposal": 1,
    "amount": 100,
    "barrier": "+0.1",
    "basis": "payout",
    "contract_type": "CALL",
    "currency": "USD",
    "duration": 60,
    "duration_unit": "s",
    "symbol": "R_100"
})

# Execute trade
buy_response = await api.buy({
    "buy": proposal['proposal']['id'],
    "price": 100
})
```

### Real-time Subscriptions
```python
# Subscribe to tick data
tick_stream = await api.subscribe({'ticks': 'R_50'})
tick_stream.subscribe(lambda tick: print(f"Tick: {tick}"))

# Subscribe to contract updates
contract_stream = await api.subscribe({
    "proposal_open_contract": 1,
    "contract_id": contract_id
})
contract_stream.subscribe(lambda update: print(f"Contract: {update}"))
```

## Development Workflow

### Running Examples
```bash
# Set your Deriv token
export DERIV_TOKEN=your_token_here

# Run example
PYTHONPATH=. python3 examples/simple_bot1.py
```

### Testing
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_deriv_api.py -v

# Run with coverage
pip install coverage
coverage run -m pytest
coverage report
```

### Building
```bash
# Build package
python -m build

# Install from source
pip install -e .
```

## API Methods

The library provides access to all Deriv API methods including:

### Account Management
- `authorize()` - Authenticate user
- `balance()` - Get account balance
- `statement()` - Get transaction history
- `profit_table()` - Get profit/loss data

### Trading
- `proposal()` - Get trade proposal
- `buy()` - Execute trade
- `sell()` - Close position
- `proposal_open_contract()` - Get contract details

### Market Data
- `active_symbols()` - Get available symbols
- `asset_index()` - Get asset information
- `ticks()` - Get tick data
- `candles()` - Get candle data

### Subscriptions
- `subscribe()` - Subscribe to real-time data
- `forget()` - Unsubscribe from stream
- `forget_all()` - Unsubscribe from all streams

## Error Handling

```python
from deriv_api import APIError, ResponseError

try:
    response = await api.buy(buy_request)
except APIError as e:
    print(f"API Error: {e}")
except ResponseError as e:
    print(f"Response Error: {e}")
```

## Best Practices

1. **Always use async/await** for API calls
2. **Handle errors gracefully** with try-catch blocks
3. **Manage subscriptions** properly to avoid memory leaks
4. **Use caching** for frequently accessed data
5. **Monitor connection state** for reliability
6. **Clean up resources** when done

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Check network connectivity
   - Verify app_id is correct
   - Ensure token is valid

2. **Subscription Issues**
   - Check subscription parameters
   - Verify symbol availability
   - Monitor memory usage

3. **Authentication Errors**
   - Verify token format
   - Check token expiration
   - Ensure proper authorization

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Monitor API events
api.events.subscribe(lambda event: print(f"Event: {event}"))
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## Resources

- [Deriv API Documentation](https://api.deriv.com/)
- [Python Deriv API Docs](https://deriv-com.github.io/python-deriv-api/)
- [GitHub Repository](https://github.com/deriv-com/python-deriv-api)
- [PyPI Package](https://pypi.org/project/python_deriv_api/)

## Next Steps

1. **Explore Examples**: Start with `examples/simple_bot1.py`
2. **Read Documentation**: Check `docs/usage_examples.md`
3. **Run Tests**: Verify everything works with `pytest`
4. **Build Your Bot**: Create your own trading application
5. **Contribute**: Help improve the library

## Support

For issues and questions:
- Check the [GitHub Issues](https://github.com/deriv-com/python-deriv-api/issues)
- Review the [API Documentation](https://api.deriv.com/)
- Join the [Deriv Community](https://community.deriv.com/)
