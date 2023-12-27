import requests
import time

# Replace these values with your actual Discord webhook URL and Roblox limited item ID
webhook_url = "https://YOUR_DISCORD_WEBHOOK_URL_HERE"
limited_item_id = 1234567689  # Replace with your actual item ID

previous_price = None

while True:
    try:
        url = f"https://catalog.roblox.com/v1/catalog/items/{limited_item_id}/details?itemType=Asset"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        current_price = data["lowestResalePrice"]
        name = data["name"]

        if previous_price is None:
            print(f"Tracking {name}. Initial price: {current_price}")
        else:
            if current_price != previous_price:  
                if current_price > previous_price:
                    message = f"**Price increased!** {name} is now {current_price} (was {previous_price})"
                    color = 0x00FF00  
                else:
                    message = f"**Price decreased!** {name} is now {current_price} (was {previous_price})"
                    color = 0xFF0000  

                requests.post(
                    webhook_url,
                    json={"content": message, "embeds": [{"color": color}]},
                )

        previous_price = current_price

        time.sleep(300)  

    except requests.exceptions.RequestException as e:
        print(f"Error fetching price: {e}")
        time.sleep(300)  

