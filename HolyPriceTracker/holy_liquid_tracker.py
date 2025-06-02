import requests
import time
import random
import os
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_mcap(mcap):
    if mcap >= 1_000_000:
        return f"${mcap/1_000_000:.2f}M"
    elif mcap >= 1_000:
        return f"${mcap/1_000:.2f}K"
    else:
        return f"${mcap:.2f}"

def get_hype_price():
    """Fetch HYPE price from DexScreener API"""
    try:
        url = "https://api.dexscreener.com/latest/dex/pairs/hyperliquid/0x13ba5fea7078ab3798fbce53b4d0721c"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data and 'pair' in data and data['pair']:
            pair = data['pair']
            price = float(pair.get('priceUsd', 0))
            return price
    except:
        return None

def get_holy_liquid_data():
    """Fetch Holy Liquid data from DexScreener API"""
    try:
        url = "https://api.dexscreener.com/latest/dex/tokens/0x738dD55C272b0B686382F62DD4a590056839F4F6"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data and 'pairs' in data and data['pairs'] and len(data['pairs']) > 0:
            pair = data['pairs'][0]
            price = float(pair.get('priceUsd', 0))
            mcap = float(pair.get('fdv', 0)) if pair.get('fdv') else 0
            volume_24h = float(pair.get('volume', {}).get('h24', 0))
            change_24h = float(pair.get('priceChange', {}).get('h24', 0)) if pair.get('priceChange') and pair.get('priceChange').get('h24') else 0
            change_6h = float(pair.get('priceChange', {}).get('h6', 0)) if pair.get('priceChange') and pair.get('priceChange').get('h6') else 0
            change_1h = float(pair.get('priceChange', {}).get('h1', 0)) if pair.get('priceChange') and pair.get('priceChange').get('h1') else 0
            change_5m = float(pair.get('priceChange', {}).get('m5', 0)) if pair.get('priceChange') and pair.get('priceChange').get('m5') else 0
            
            return {
                'price': price,
                'mcap': mcap,
                'volume_24h': volume_24h,
                'change_24h': change_24h,
                'change_6h': change_6h,
                'change_1h': change_1h,
                'change_5m': change_5m,
                'success': True
            }
        else:
            return {'success': False, 'error': 'No pairs data found'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def display_ascii_art():
    art = """
    ██╗  ██╗ ██████╗ ██╗  ██╗   ██╗    ██╗     ██╗ ██████╗ ██╗   ██╗██╗██████╗       ██
    ██║  ██║██╔═══██╗██║  ╚██╗ ██╔╝    ██║     ██║██╔═══██╗██║   ██║██║██╔══██╗      ██
    ███████║██║   ██║██║   ╚████╔╝     ██║     ██║██║   ██║██║   ██║██║██║  ██║ ████████████
    ██╔══██║██║   ██║██║    ╚██╔╝      ██║     ██║██║▄▄ ██║██║   ██║██║██║  ██║      ██
    ██║  ██║╚██████╔╝███████╗██║       ███████╗██║╚██████╔╝╚██████╔╝██║██████╔╝      ██
    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝       ╚══════╝╚═╝ ╚══▀▀═╝  ╚═════╝ ╚═╝╚═════╝       ██
                                                                                     ██
                                                             Created by @infidel.hl
    """
    return art

def main():
    print("Holy Liquid Market Cap Tracker Starting...")
    time.sleep(2)
    
    previous_mcap = None
    
    while True:
        try:
            clear_screen()
            
            # Display ASCII art
            print(Fore.CYAN + display_ascii_art())
            print("=" * 80)
            
            # Fetch data
            hl_data = get_holy_liquid_data()
            hype_price = get_hype_price()
            
            if hl_data['success']:
                current_mcap = hl_data['mcap']
                price = hl_data['price']
                volume_24h = hl_data['volume_24h']
                change_24h = hl_data['change_24h']
                change_6h = hl_data['change_6h']
                change_1h = hl_data['change_1h']
                change_5m = hl_data['change_5m']
                
                # Determine color based on previous mcap
                if previous_mcap is None:
                    mcap_color = Fore.WHITE
                    trend = "●"
                elif current_mcap > previous_mcap:
                    mcap_color = Fore.GREEN
                    trend = "▲"
                else:
                    mcap_color = Fore.RED
                    trend = "▼"
                
                # Display data
                print(f"{mcap_color}Market Cap: {format_mcap(current_mcap)} {trend}")
                print(f"Price: ${price:.8f}")
                if hype_price:
                    print(f"HYPE Price: ${hype_price:.2f}")
                print(f"Volume 24h: {format_mcap(volume_24h)}")
                print()
                
                # Time period changes with colors
                print("Price Changes:")
                change_color_5m = Fore.GREEN if change_5m >= 0 else Fore.RED
                change_color_1h = Fore.GREEN if change_1h >= 0 else Fore.RED
                change_color_6h = Fore.GREEN if change_6h >= 0 else Fore.RED
                change_color_24h = Fore.GREEN if change_24h >= 0 else Fore.RED
                
                print(f"{change_color_5m}  5m: {'+' if change_5m >= 0 else ''}{change_5m:.2f}%")
                print(f"{change_color_1h}  1h: {'+' if change_1h >= 0 else ''}{change_1h:.2f}%")
                print(f"{change_color_6h}  6h: {'+' if change_6h >= 0 else ''}{change_6h:.2f}%")
                print(f"{change_color_24h} 24h: {'+' if change_24h >= 0 else ''}{change_24h:.2f}%")
                
                previous_mcap = current_mcap
                
            else:
                print(f"{Fore.RED}Error fetching data: {hl_data.get('error', 'Unknown error')}")
            
            # Random wait time between 15-35 seconds
            wait_time = random.randint(15, 35)
            time.sleep(wait_time)
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Tracker stopped. Holy liquid to the moon! 🚀")
            break
        except Exception as e:
            print(f"{Fore.RED}Unexpected error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()