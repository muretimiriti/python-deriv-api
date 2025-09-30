#!/usr/bin/env python3
"""
Simple connection test for Python Deriv API
Run this to verify your setup is working correctly
"""

import asyncio
import os
import sys
from deriv_api import DerivAPI, APIError, ResponseError

async def test_connection():
    """Test basic connection and authentication"""
    print("🚀 Testing Python Deriv API Connection...")
    
    # Check for token
    api_token = os.getenv('DERIV_TOKEN')
    if not api_token:
        print("❌ Error: DERIV_TOKEN environment variable not set")
        print("   Please set your token: export DERIV_TOKEN=your_token_here")
        return False
    
    try:
        # Create API instance
        print("📡 Creating API connection...")
        api = DerivAPI(app_id=1089)
        
        # Test ping
        print("🏓 Testing ping...")
        response = await api.ping({'ping': 1})
        if response.get('ping'):
            print(f"✅ Ping successful: {response['ping']}")
        else:
            print("❌ Ping failed")
            return False
        
        # Authorize
        print("🔐 Authorizing...")
        auth = await api.authorize(api_token)
        if auth.get('authorize'):
            print(f"✅ Authorization successful: {auth['authorize']['loginid']}")
            print(f"   Account: {auth['authorize']['fullname']}")
        else:
            print("❌ Authorization failed")
            return False
        
        # Get balance
        print("💰 Getting account balance...")
        balance = await api.balance()
        if balance.get('balance'):
            bal_data = balance['balance']
            print(f"✅ Balance: {bal_data['balance']} {bal_data['currency']}")
        else:
            print("❌ Failed to get balance")
            return False
        
        # Get active symbols
        print("📊 Getting active symbols...")
        symbols = await api.active_symbols({
            "active_symbols": "brief",
            "product_type": "basic"
        })
        if symbols.get('active_symbols'):
            print(f"✅ Found {len(symbols['active_symbols'])} active symbols")
        else:
            print("❌ Failed to get symbols")
            return False
        
        print("\n🎉 All tests passed! Your setup is working correctly.")
        return True
        
    except APIError as e:
        print(f"❌ API Error: {e}")
        return False
    except ResponseError as e:
        print(f"❌ Response Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False
    finally:
        # Clean up
        try:
            await api.clear()
            print("🧹 Cleaned up resources")
        except:
            pass

async def test_subscription():
    """Test real-time subscription"""
    print("\n📡 Testing real-time subscription...")
    
    api_token = os.getenv('DERIV_TOKEN')
    if not api_token:
        print("❌ No token available for subscription test")
        return False
    
    try:
        api = DerivAPI(app_id=1089)
        await api.authorize(api_token)
        
        # Subscribe to tick data
        print("📈 Subscribing to tick data...")
        tick_stream = await api.subscribe({'ticks': 'R_50'})
        
        if tick_stream:
            print("✅ Subscription successful")
            
            # Set up tick handler
            tick_count = 0
            def on_tick(tick):
                nonlocal tick_count
                tick_count += 1
                if tick_count <= 3:  # Show first 3 ticks
                    print(f"   Tick {tick_count}: {tick['tick']['quote']}")
            
            tick_stream.subscribe(on_tick)
            
            # Wait for ticks
            print("⏳ Waiting for tick data (5 seconds)...")
            await asyncio.sleep(5)
            
            if tick_count > 0:
                print(f"✅ Received {tick_count} ticks")
            else:
                print("⚠️  No ticks received (this might be normal)")
            
            await api.clear()
            return True
        else:
            print("❌ Subscription failed")
            return False
            
    except Exception as e:
        print(f"❌ Subscription test failed: {e}")
        return False
    finally:
        try:
            await api.clear()
        except:
            pass

async def main():
    """Main test function"""
    print("=" * 50)
    print("Python Deriv API - Connection Test")
    print("=" * 50)
    
    # Test basic connection
    success = await test_connection()
    
    if success:
        # Test subscription
        await test_subscription()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Setup verification complete!")
        print("   You can now start building your trading bot!")
        print("   Check examples/ directory for more examples.")
    else:
        print("❌ Setup verification failed!")
        print("   Please check your token and network connection.")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
