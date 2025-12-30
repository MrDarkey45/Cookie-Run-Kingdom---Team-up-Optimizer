"""
Cookie image URL mapping for Cookie Run: Kingdom.
Maps cookie names to their portrait images from external sources.
"""

def get_cookie_image_url(cookie_name: str) -> str:
    """
    Get the image URL for a cookie.

    Args:
        cookie_name: The full name of the cookie (e.g., "Shadow Milk Cookie")

    Returns:
        str: URL to the cookie's portrait image
    """
    # Convert to PascalCase Icon format
    # "Shadow Milk Cookie" -> "ShadowMilkCookieIcon"
    icon_name = cookie_name.replace(" ", "").replace("(", "").replace(")", "") + "Icon"

    # Cookie Run Wiki uses this URL pattern for cookie portraits
    # Using the fandom wiki which has consistent image URLs
    base_url = "https://static.wikia.nocookie.net/cookierun/images"

    # Map specific cookies to their wiki image hashes
    # This is a curated list - we'll use a fallback for unmapped cookies
    cookie_image_map = {
        # Beasts
        "Mystic Flour Cookie": "c/c4/Mystic_Flour_Cookie.png",
        "Burning Spice Cookie": "8/8a/Burning_Spice_Cookie.png",
        "Shadow Milk Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/5/53/Shadow_milk_head.png",
        "Eternal Sugar Cookie": "7/7b/Eternal_Sugar_Cookie.png",
        "Silent Salt Cookie": "a/a5/Silent_Salt_Cookie.png",

        # Ancients
        "Pure Vanilla Cookie": "9/9d/Pure_Vanilla_Cookie.png",
        "Hollyberry Cookie": "4/49/Hollyberry_Cookie.png",
        "Dark Cacao Cookie": "3/34/Dark_Cacao_Cookie.png",
        "Golden Cheese Cookie": "e/e3/Golden_Cheese_Cookie.png",
        "White Lily Cookie": "0/05/White_Lily_Cookie.png",

        # Ascended versions use same portraits
        "Pure Vanilla Cookie (Ascended)": "9/9d/Pure_Vanilla_Cookie.png",
        "Hollyberry Cookie (Ascended)": "4/49/Hollyberry_Cookie.png",
        "Dark Cacao Cookie (Ascended)": "3/34/Dark_Cacao_Cookie.png",
        "Golden Cheese Cookie (Ascended)": "e/e3/Golden_Cheese_Cookie.png",
        "White Lily Cookie (Ascended)": "0/05/White_Lily_Cookie.png",

        # Legendary
        "Fire Spirit Cookie": "8/81/Fire_Spirit_Cookie.png",
        "Wind Archer": "d/d4/Wind_Archer_Cookie.png",
        "Stormbringer Cookie": "5/52/Stormbringer_Cookie.png",
        "Moonlight Cookie": "b/b5/Moonlight_Cookie.png",
        "Black Pearl Cookie": "c/c7/Black_Pearl_Cookie.png",
        "Frost Queen Cookie": "f/f5/Frost_Queen_Cookie.png",
        "Sea Fairy Cookie": "a/a0/Sea_Fairy_Cookie.png",
        "Millennial Tree Cookie": "2/2f/Millennial_Tree_Cookie.png",

        # Super Epic
        "Clotted Cream Cookie": "1/15/Clotted_Cream_Cookie.png",
        "Oyster Cookie": "6/60/Oyster_Cookie.png",
        "Sherbet Cookie": "5/59/Sherbet_Cookie.png",
        "Stardust Cookie": "e/e8/Stardust_Cookie.png",
        "Capsaicin Cookie": "a/a9/Capsaicin_Cookie.png",
        "Shining Glitter Cookie": "7/75/Shining_Glitter_Cookie.png",
        "Crimson Coral Cookie": "2/2c/Crimson_Coral_Cookie.png",
        "Elder Faerie Cookie": "1/1c/Elder_Faerie_Cookie.png",
        "Camellia Cookie": "f/f0/Camellia_Cookie.png",

        # Popular Epic cookies
        "Espresso Cookie": "b/b5/Espresso_Cookie.png",
        "Madeleine Cookie": "5/5f/Madeleine_Cookie.png",
        "Latte Cookie": "c/c1/Latte_Cookie.png",
        "Almond Cookie": "8/82/Almond_Cookie.png",
        "Black Raisin Cookie": "0/07/Black_Raisin_Cookie.png",
        "Vampire Cookie": "d/d0/Vampire_Cookie.png",
        "Licorice Cookie": "9/9e/Licorice_Cookie.png",
        "Poison Mushroom Cookie": "a/a3/Poison_Mushroom_Cookie.png",
        "Herb Cookie": "6/69/Herb_Cookie.png",
        "Sparkling Cookie": "e/e7/Sparkling_Cookie.png",
        "Dark Choco Cookie": "5/59/Dark_Choco_Cookie.png",
        "Milk Cookie": "f/f2/Milk_Cookie.png",
        "Purple Yam Cookie": "7/7e/Purple_Yam_Cookie.png",
        "Werewolf Cookie": "c/c0/Werewolf_Cookie.png",
        "Snow Sugar Cookie": "4/47/Snow_Sugar_Cookie.png",
        "Mint Choco Cookie": "9/9a/Mint_Choco_Cookie.png",
        "Pomegranate Cookie": "d/dc/Pomegranate_Cookie.png",
        "Chili Pepper Cookie": "a/ab/Chili_Pepper_Cookie.png",
        "Rye Cookie": "9/93/Rye_Cookie.png",
        "Kumiho Cookie": "e/eb/Kumiho_Cookie.png",
        "Fig Cookie": "2/25/Fig_Cookie.png",
        "Pastry Cookie": "f/f3/Pastry_Cookie.png",
        "Red Velvet Cookie": "3/38/Red_Velvet_Cookie.png",
        "Mango Cookie": "5/51/Mango_Cookie.png",
        "Lilac Cookie": "a/a0/Lilac_Cookie.png",
        "Squid Ink Cookie": "7/7f/Squid_Ink_Cookie.png",
        "Sorbet Shark Cookie": "4/4a/Sorbet_Shark_Cookie.png",
        "Parfait Cookie": "8/87/Parfait_Cookie.png",
        "Raspberry Cookie": "f/f6/Raspberry_Cookie.png",
        "Moon Rabbit Cookie": "2/2d/Moon_Rabbit_Cookie.png",
        "Mala Sauce Cookie": "0/0b/Mala_Sauce_Cookie.png",
        "Twizzly Gummy Cookie": "7/7c/Twizzly_Gummy_Cookie.png",
        "Pumpkin Pie Cookie": "9/95/Pumpkin_Pie_Cookie.png",
        "Cotton Cookie": "5/59/Cotton_Cookie.png",
        "Cocoa Cookie": "8/8a/Cocoa_Cookie.png",
        "Éclair Cookie": "c/c5/Eclair_Cookie.png",
        "Tea Knight Cookie": "e/e4/Tea_Knight_Cookie.png",
        "Affogato Cookie": "f/f2/Affogato_Cookie.png",
        "Caramel Arrow Cookie": "4/4b/Caramel_Arrow_Cookie.png",
        "Cherry Blossom Cookie": "3/3a/Cherry_Blossom_Cookie.png",
        "Wildberry Cookie": "6/62/Wildberry_Cookie.png",
        "Crunchy Chip Cookie": "a/a4/Crunchy_Chip_Cookie.png",
        "Financier Cookie": "5/57/Financier_Cookie.png",
        "Cream Unicorn Cookie": "9/95/Cream_Unicorn_Cookie.png",
        "Captain Caviar Cookie": "f/f5/Captain_Caviar_Cookie.png",
        "Candy Diver Cookie": "c/c8/Candy_Diver_Cookie.png",
        "Schwarzwalder": "2/2e/Schwarzwalder_Cookie.png",
        "Macaron Cookie": "d/d3/Macaron_Cookie.png",
        "Carol Cookie": "6/6f/Carol_Cookie.png",
        "Pinecone Cookie": "a/a6/Pinecone_Cookie.png",

        # Common/Rare
        "GingerBrave": "https://static.wikia.nocookie.net/cookierunkingdom/images/3/3f/Gingerbrave_head.png",
        "Strawberry Cookie": "c/c9/Strawberry_Cookie.png",
        "Wizard Cookie": "f/fc/Wizard_Cookie.png",
        "Ninja Cookie": "5/57/Ninja_Cookie.png",

        # Special BTS
        "RM Cookie": "8/8c/RM_Cookie.png",
        "Jin Cookie": "e/e5/Jin_Cookie.png",
        "SUGA Cookie": "4/46/SUGA_Cookie.png",
        "j-hope Cookie": "2/2f/J-Hope_Cookie.png",
        "Jimin Cookie": "7/79/Jimin_Cookie.png",
        "V Cookie": "b/bb/V_Cookie.png",
        "Jungkook Cookie": "0/04/Jungkook_Cookie.png",
    }

    # Check if we have a specific mapping
    if cookie_name in cookie_image_map:
        image_value = cookie_image_map[cookie_name]
        # If it's already a full URL, return as-is
        if image_value.startswith("http"):
            return image_value
        # Otherwise, prepend the base URL
        return f"{base_url}/{image_value}"

    # Fallback: construct a generic URL pattern
    # Convert "Shadow Milk Cookie" -> "Shadow_Milk_Cookie.png"
    safe_name = cookie_name.replace(" (Ascended)", "").replace(" ", "_")
    return f"{base_url}/thumb/{safe_name}.png"


def get_all_cookie_images(cookies_list):
    """
    Generate a mapping of all cookie names to their image URLs.

    Args:
        cookies_list: List of cookie dictionaries with 'name' field

    Returns:
        dict: Mapping of cookie name to image URL
    """
    return {
        cookie['name']: get_cookie_image_url(cookie['name'])
        for cookie in cookies_list
    }
