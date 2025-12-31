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
        "Mystic Flour Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/d/d2/Mystic_flour_head.png",
        "Burning Spice Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/7d/Burning_spice_head.png",
        "Shadow Milk Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/5/53/Shadow_milk_head.png",
        "Eternal Sugar Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/70/Eternal_sugar_head.png",
        "Silent Salt Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/a/ad/Silent_salt_head.png",

        # Ancients
        "Pure Vanilla Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/78/Pure_vanilla_head.png",
        "Hollyberry Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/a/a2/Hollyberry_head.png",
        "Dark Cacao Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/84/Dark_cacao_head.png",
        "Golden Cheese Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/b/b9/Golden_cheese_head.png",
        "White Lily Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/2/23/White_lily_head.png",

        # Ascended versions use different portraits
        "Pure Vanilla Cookie (Ascended)": "https://static.wikia.nocookie.net/cookierunkingdom/images/f/ff/Awakened_pure_vanilla_head.png",
        "Hollyberry Cookie (Ascended)": "https://static.wikia.nocookie.net/cookierunkingdom/images/a/ae/Awakened_hollyberry_head.png",
        "Dark Cacao Cookie (Ascended)": "https://static.wikia.nocookie.net/cookierunkingdom/images/f/f8/Awakened_dark_cacao_head.png",
        "Golden Cheese Cookie (Ascended)": "https://static.wikia.nocookie.net/cookierunkingdom/images/d/db/Awakened_golden_cheese_head.png",
        "White Lily Cookie (Ascended)": "https://static.wikia.nocookie.net/cookierunkingdom/images/4/4b/Awakened_white_lily_head.png",

        # Legendary
        "Fire Spirit Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/1/11/Fire_spirit_head.png",
        "Wind Archer": "https://static.wikia.nocookie.net/cookierunkingdom/images/2/21/Wind_archer_head.png",
        "Stormbringer Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/77/Stormbringer_head.png",
        "Moonlight Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/0/04/Moonlight_head.png",
        "Black Pearl Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/8a/Black_pearl_head.png",
        "Frost Queen Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/d/d7/Frost_queen_head.png",
        "Sea Fairy Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/b/b3/Sea_fairy_head.png",
        "Millennial Tree Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/c/ce/Millennial_tree_head.png",

        # Super Epic
        "Camellia Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/0/0d/Camellia_head.png",
        "Capsaicin Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/2/21/Capsaicin_head.png",
        "Clotted Cream Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/9/99/Clotted_cream_head.png",
        "Crimson Coral Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/0/03/Crimson_coral_head.png",
        "Doughael": "https://static.wikia.nocookie.net/cookierunkingdom/images/e/e4/Doughael_head.png",
        "Elder Faerie Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/c/ce/Elder_faerie_head.png",
        "Oyster Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/4/48/Oyster_head.png",
        "Sherbet Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/f/fc/Sherbet_head.png",
        "Shining Glitter Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/a/a5/Shining_glitter_head.png",
        "Stardust Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/1/15/Stardust_head.png",

        # Epic cookies
        "Espresso Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/74/Espresso_head.png",
        "Madeleine Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/2/2f/Madeleine_head.png",
        "Latte Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/c/c2/Latte_head.png",
        "Almond Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/4/4a/Almond_head.png",
        "Black Raisin Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/f/f0/Black_raisin_head.png",
        "Vampire Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/78/Vampire_head.png",
        "Licorice Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/86/Licorice_head.png",
        "Poison Mushroom Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/3/33/Poison_mushroom_head.png",
        "Herb Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/8a/Herb_head.png",
        "Sparkling Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/b/b5/Sparkling_head.png",
        "Dark Choco Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/9/9d/Dark_choco_head.png",
        "Milk Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/8d/Milk_head.png",
        "Purple Yam Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/a/a4/Purple_yam_head.png",
        "Werewolf Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/6/69/Werewolf_head.png",
        "Snow Sugar Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/77/Snow_sugar_head.png",
        "Mint Choco Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/73/Mint_choco_head.png",
        "Pomegranate Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/2/27/Pomegranate_head.png",
        "Chili Pepper Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/6/65/Chili_pepper_head.png",
        "Rye Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/3/36/Rye_head.png",
        "Kumiho Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/1/1f/Kumiho_head.png",
        "Fig Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/f/f3/Fig_head.png",
        "Pastry Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/3/3f/Pastry_head.png",
        "Red Velvet Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/1/15/Red_velvet_head.png",
        "Mango Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/9/97/Mango_head.png",
        "Lilac Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/0/04/Lilac_head.png",
        "Squid Ink Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/0/00/Squid_ink_head.png",
        "Sorbet Shark Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/89/Sorbet_shark_head.png",
        "Parfait Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/5/58/Parfait_head.png",
        "Raspberry Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/0/08/Raspberry_head.png",
        "Moon Rabbit Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/f/f5/Moon_rabbit_head.png",
        "Mala Sauce Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/4/49/Mala_sauce_head.png",
        "Twizzly Gummy Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/83/Twizzly_gummy_head.png",
        "Pumpkin Pie Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/0/03/Pumpkin_pie_head.png",
        "Cotton Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/f/fe/Cotton_head.png",
        "Cocoa Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/1/17/Cocoa_head.png",
        "Éclair Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/8a/Eclair_head.png",
        "Tea Knight Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/4/44/Tea_knight_head.png",
        "Affogato Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/9/99/Affogato_head.png",
        "Caramel Arrow Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/d/d5/Caramel_arrow_head.png",
        "Cherry Blossom Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/0/0a/Cherry_blossom_head.png",
        "Wildberry Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/8f/Wildberry_head.png",
        "Crunchy Chip Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/3/37/Crunchy_chip_head.png",
        "Financier Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/9/95/Financier_head.png",
        "Cream Unicorn Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/5/5a/Cream_unicorn_head.png",
        "Captain Caviar Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/85/Captain_caviar_head.png",
        "Candy Diver Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/7a/Candy_diver_head.png",
        "Schwarzwalder": "https://static.wikia.nocookie.net/cookierunkingdom/images/5/50/Schwarzwalder_head.png",
        "Macaron Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/7d/Macaron_head.png",
        "Carol Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/b/b0/Carol_head.png",
        "Pinecone Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/5/5b/Pinecone_head.png",
        "Agar Agar Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/e/ed/Agar_agar_head.png",
        "Black Forest Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/a/a3/Black_forest_head.png",
        "Black Lemonade Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/0/04/Black_lemonade_head.png",
        "Black Sapphire Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/72/Black_sapphire_head.png",
        "Blueberry Pie Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/3/3c/Blueberry_pie_head.png",
        "Burnt Cheese Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/6/65/Burnt_cheese_head.png",
        "Butter Roll Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/3/30/Butter_roll_head.png",
        "Candy Apple Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/1/12/Candy_apple_head.png",
        "Caramel Choux Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/5/53/Caramel_choux_head.png",
        "Charcoal Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/c/c7/Charcoal_head.png",
        "Choco Drizzle Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/0/09/Choco_drizzle_head.png",
        "Cloud Haetae Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/0/04/Cloud_haetae_head.png",
        "Cream Puff Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/b/b3/Cream_puff_head.png",
        "Cream Soda Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/3/30/Cream_soda_head.png",
        "Crème Brulee Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/5/5c/Creme_brulee_head.png",
        "Fettuccine Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/c/cf/Fettuccine_head.png",
        "Frilled Jellyfish Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/0/04/Frilled_jellyfish_head.png",
        "Golden Osmanthus Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/4/4f/Golden_osmanthus_head.png",
        "Grapefruit Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/5/53/Grapefruit_head.png",
        "Green Tea Mousse Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/82/Green_tea_mousse_head.png",
        "Jagae Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/1/1f/Jagae_head.png",
        "Kouign-Amann Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/6/6d/Kouign_amann_head.png",
        "Lemon Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/8d/Lemon_head.png",
        "Lime Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/5/50/Lime_head.png",
        "Linzer Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/83/Linzer_head.png",
        "Manju Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/4/46/Manju_head.png",
        "Matcha Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/7a/Matcha_head.png",
        "Menthol Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/1/1c/Menthol_head.png",
        "Mercurial Knight Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/b/b5/Mercurial_knight_head.png",
        "Milky Way Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/2/2f/Milky_way_head.png",
        "Mozzarella Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/1/1c/Mozzarella_head.png",
        "Nutmeg Tiger Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/b/bc/Nutmeg_tiger_head.png",
        "Okchun Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/3/39/Okchun_head.png",
        "Olive Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/9/9d/Olive_head.png",
        "Orange Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/f/f8/Orange_head.png",
        "Pavlova Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/4/4f/Pavlova_head.png",
        "Peach Blossom Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/3/39/Peach_blossom_head.png",
        "Peppermint Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/4/45/Peppermint_head.png",
        "Prophet Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/b/b6/Prophet_head.png",
        "Prune Juice Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/9/97/Prune_juice_head.png",
        "Pudding a la Mode Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/a/a8/Pudding_a_la_mode_head.png",
        "Rebel Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/8f/Rebel_head.png",
        "Red Osmanthus Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/e/e3/Red_osmanthus_head.png",
        "Rockstar Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/0/08/Rockstar_head.png",
        "Royal Margarine Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/e/e3/Royal_margarine_head.png",
        "Salt Cellar Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/73/Salt_cellar_head.png",
        "Seltzer Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/c/cf/Seltzer_head.png",
        "Silverbell Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/2/25/Silverbell_head.png",
        "Smoked Cheese Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/9/97/Smoked_cheese_head.png",
        "Space Doughnut": "https://static.wikia.nocookie.net/cookierunkingdom/images/d/d6/Space_doughnut_head.png",
        "Star Coral Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/d/d3/Star_coral_head.png",
        "Strawberry Crepe Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/5/50/Strawberry_crepe_head.png",
        "Street Urchin Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/b/b7/Street_urchin_head.png",
        "Sugarfly Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/9/92/Sugarfly_head.png",
        "Tarte Tatin Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/73/Tarte_tatin_head.png",
        "Tiger Lily Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/3/30/Tiger_lily_head.png",
        "Wedding Cake Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/2/28/Wedding_cake_head.png",

        # Dragon
        "Pitaya Dragon Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/f/f9/Pitaya_dragon_head.png",

        # Rare
        "Adventurer Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/e/ed/Adventurer_head.png",
        "Alchemist Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/7b/Alchemist_head.png",
        "Avocado Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/f/f5/Avocado_head.png",
        "Blackberry Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/6/68/Blackberry_head.png",
        "Carrot Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/8b/Carrot_head.png",
        "Cherry Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/b/b2/Cherry_head.png",
        "Clover Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/e/e8/Clover_head.png",
        "Custard Cookie III": "https://static.wikia.nocookie.net/cookierunkingdom/images/2/2c/Custard_iii_head.png",
        "Devil Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/d/dc/Devil_head.png",
        "Gumball Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/a/aa/Gumball_head.png",
        "Knight Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/0/0b/Knight_head.png",
        "Onion Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/a/a3/Onion_head.png",
        "Pancake Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/1/1f/Pancake_head.png",
        "Princess Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/83/Princess_head.png",

        # Common
        "Angel Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/d/d7/Angel_head.png",
        "Beet Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/8/8a/Beet_head.png",
        "GingerBrave": "https://static.wikia.nocookie.net/cookierunkingdom/images/3/3f/Gingerbrave_head.png",
        "Muscle Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/b/b0/Muscle_head.png",
        "Ninja Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/2/2f/Ninja_head.png",
        "Strawberry Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/77/Strawberry_head.png",
        "Wizard Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/3/3c/Wizard_head.png",

        # Special
        "Cream Ferret Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/e/ed/Cream_ferret_head.png",
        "Elphaba Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/1/14/Elphaba_head.png",
        "Glinda Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/6/64/Glinda_head.png",
        "Icicle Yeti Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/9/9c/Icicle_yeti_head.png",
        "Jimin Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/7f/Jimin_head.png",
        "Jin Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/5/54/Jin_head.png",
        "Jungkook Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/0/01/Jung_kook_head.png",
        "Marshmallow Bunny Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/9/9d/Marshmallow_bunny_head.png",
        "RM Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/b/ba/Rm_head.png",
        "SUGA Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/7d/Suga_head.png",
        "Snapdragon Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/3/3b/Snapdragon_head.png",
        "Sonic Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/9/9e/Sonic_head.png",
        "Tails Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/f/fc/Tails_head.png",
        "V Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/3/3f/V_head.png",
        "j-hope Cookie": "https://static.wikia.nocookie.net/cookierunkingdom/images/7/78/J-hope_head.png",
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
