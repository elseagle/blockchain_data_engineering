import requests
from datetime import datetime, timedelta


def check_date_validity(upcoming_nft_sale):
    if "Sale Date" not in upcoming_nft_sale:
        return True

    try:
        x = (
            datetime.fromisoformat(
                upcoming_nft_sale["Sale Date"].lower().replace("z", "")
            ).date()
            >= datetime.now().date()
        )
        y = datetime.now() - datetime.fromisoformat(
            upcoming_nft_sale["Listed Date"].lower().replace("z", "")
        )
        y = y.days <= 7
        return x and y

    except:
        return True


def get_initial_data():
    res = requests.get("https://collections.rarity.tools/upcoming2")
    if res.status_code != 200:
        print(f"Error making request to rarity.tools")
        exit()
    res = list(filter(check_date_validity, res.json()))
    print("Upcoming nfts data gotten from rarity.tools")
    return res


if __name__ == "__main__":
    print(get_initial_data())
