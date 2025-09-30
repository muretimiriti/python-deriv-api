# Quick Start Guide - Python Deriv API

## 🚀 Get Started in 5 Minutes

### 1. Setup Environment
```bash
# Navigate to project
cd "/home/mureti/Desktop/Mureti code projects/python-deriv-api"

# Activate virtual environment
source venv/bin/activate

# Verify installation
python -c "from deriv_api import DerivAPI; print('✅ Installation successful!')"
```

### 2. Get Your Deriv Token
1. Go to [Deriv.com](https://deriv.com) and create an account
2. Navigate to [API Token](https://app.deriv.com/account/api-token)
3. Generate a new token
4. Copy the token for use in your code

### 3. Basic Connection Test
```python
# test_connection.py
import asyncio
import os
from deriv_api import DerivAPI

async def test_connection():
    # Set your token
    api_token = os.getenv('DERIV_TOKEN', 'your_token_here')
    
    # Create API instance
    api = DerivAPI(app_id=1089)
    
    # Test ping
    response = await api.ping({'ping': 1})
    print(f"✅ Ping successful: {response}")
    
    # Authorize
    auth = await api.authorize(api_token)
    print(f"✅ Authorization successful: {auth['authorize']['loginid']}")
    
    # Get balance
    balance = await api.balance()
    print(f"✅ Balance: {balance['balance']['balance']} {balance['balance']['currency']}")
    
    # Clean up
    await api.clear()

# Run the test
if __name__ == "__main__":
    asyncio.run(test_connection())
```

### 4. Run Your First Test
```bash
# Set your token
export DERIV_TOKEN=your_actual_token_here

# Run the test
python test_connection.py
```

### 5. Explore Examples
```bash
# Run the simple bot example
PYTHONPATH=. python3 examples/simple_bot1.py

# Run other examples
PYTHONPATH=. python3 examples/simple_bot2.py
PYTHONPATH=. python3 examples/simple_bot3.py
PYTHONPATH=. python3 examples/simple_bot4.py
```

## 📊 Common Use Cases

### Get Market Data
```python
async def get_market_data():
    api = DerivAPI(app_id=1089)
    
    # Get active symbols
    symbols = await api.active_symbols({
        "active_symbols": "brief",
        "product_type": "basic"
    })
    print(f"Available symbols: {len(symbols['active_symbols'])}")
    
    # Get asset information
    assets = await api.asset_index({"asset_index": 1})
    print(f"Available assets: {len(assets['asset_index'])}")
    
    await api.clear()
```

### Subscribe to Real-time Data
```python
async def subscribe_to_ticks():
    api = DerivAPI(app_id=1089)
    
    # Subscribe to tick data
    tick_stream = await api.subscribe({'ticks': 'R_50'})
    
    # Handle incoming ticks
    def on_tick(tick):
        print(f"Tick: {tick['tick']['quote']}")
    
    tick_stream.subscribe(on_tick)
    
    # Keep running for 10 seconds
    await asyncio.sleep(10)
    
    await api.clear()
```

### Place a Trade
```python
async def place_trade():
    api = DerivAPI(app_id=1089)
    api_token = os.getenv('DERIV_TOKEN')
    
    # Authorize
    await api.authorize(api_token)
    
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
    
    print(f"Proposal: {proposal}")
    
    # Execute trade
    buy_response = await api.buy({
        "buy": proposal['proposal']['id'],
        "price": 100
    })
    
    print(f"Trade executed: {buy_response}")
    
    await api.clear()
```

## 🔧 Development Commands

### Testing
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_deriv_api.py::test_deriv_api -v

# Run with coverage
pip install coverage
coverage run -m pytest
coverage report
```

### Building
```bash
# Build package
python -m build

# Install in development mode
pip install -e .
```

### Documentation
```bash
# Generate documentation
pip install pdoc3
pdoc3 deriv_api --html -o docs/html
```

## 🐛 Troubleshooting

### Common Issues

**1. Connection Failed**
```python
# Check your app_id and endpoint
api = DerivAPI(app_id=1089, endpoint='wss://ws.derivws.com')
```

**2. Authentication Error**
```python
# Verify your token
api_token = os.getenv('DERIV_TOKEN')
if not api_token:
    print("❌ DERIV_TOKEN environment variable not set")
```

**3. Subscription Not Working**
```python
# Check subscription parameters
tick_stream = await api.subscribe({'ticks': 'R_50'})
if not tick_stream:
    print("❌ Subscription failed")
```

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Monitor API events
api.events.subscribe(lambda event: print(f"Event: {event}"))
```

## 📚 Next Steps

1. **Read the Full Documentation**: Check `DEVELOPMENT_GUIDE.md`
2. **Explore Examples**: Study the code in `examples/` directory
3. **Build Your Bot**: Create your own trading application
4. **Join the Community**: [Deriv Community](https://community.deriv.com/)

## 🆘 Need Help?

- **Documentation**: [API Docs](https://api.deriv.com/)
- **GitHub**: [Repository](https://github.com/deriv-com/python-deriv-api)
- **Issues**: [GitHub Issues](https://github.com/deriv-com/python-deriv-api/issues)
- **Community**: [Deriv Community](https://community.deriv.com/)

## 🎯 Quick Reference

### Essential Imports
```python
from deriv_api import DerivAPI, APIError, ResponseError
import asyncio
import os
```

### Basic API Setup
```python
api = DerivAPI(app_id=1089)
await api.authorize(os.getenv('DERIV_TOKEN'))
```

### Clean Up
```python
await api.clear()  # Always clean up when done
```

### Error Handling
```python
try:
    response = await api.some_method()
except APIError as e:
    print(f"API Error: {e}")
except ResponseError as e:
    print(f"Response Error: {e}")
```

Happy trading! 🚀
