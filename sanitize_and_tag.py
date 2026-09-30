import os
import re
import json
import urllib.parse
import colorsys
from PIL import Image, ImageFilter, ImageStat

USER_METADATA_LIST = [
  {
    "id": 1,
    "file_name": "wallpaper_01_lord_vishnu_sheshanaga.jpg",
    "title": "Lord Vishnu and Sheshanaga in Cosmic Slumber",
    "device_compatibility": "Desktop / PC / Laptop",
    "aspect_ratio": "16:9 Landscape",
    "primary_category": "Mythology & Spiritual",
    "themes": ["God", "Spiritual", "Eternal Knowledge", "Hindu Mythology", "Cosmic Divinity", "Devotion"],
    "dominant_colors": ["Divine Blue", "Gold", "Cyan", "Deep Navy"],
    "hashtags": ["#desktop", "#desktopwallpaper", "#pcwallpaper", "#4kwallpaper", "#god", "#hindugod", "#lordvishnu", "#krishna", "#narayana", "#sheshanaga", "#adisesha", "#sanatandharma", "#mythology", "#spiritual", "#divineart", "#eternalknowledge", "#animated", "#graphical", "#bluewise", "#blueaesthetic", "#goldenaesthetic", "#cosmicart", "#themewise", "#bhakti", "#devotion"]
  },
  {
    "id": 2,
    "file_name": "wallpaper_02_minimalist_snow_mountain_peak.jpg",
    "title": "Chiseled Alpine Peak on Pitch Black",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Nature & Minimalism",
    "themes": ["Hills", "Mountains", "Summit", "Monochrome", "OLED Minimal"],
    "dominant_colors": ["Pitch Black", "Pure White", "Slate Gray"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#homescreen", "#nature", "#hills", "#mountainpeak", "#alpinemountain", "#summit", "#minimalist", "#graphical", "#real", "#blackandwhite", "#monochrome", "#amoled", "#oledwallpaper", "#darkmode", "#colourwise", "#darkaesthetic", "#themewise", "#cleanwallpaper", "#solitude"]
  },
  {
    "id": 3,
    "file_name": "wallpaper_03_minimalist_batman_dark_knight_logo.jpg",
    "title": "Minimalist Dark Knight Bat Symbol",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Movies & Comics",
    "themes": ["Movie Related", "DC Comics", "Batman", "Dark Knight", "Minimalist Logo"],
    "dominant_colors": ["True Black", "Matte White"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#batman", "#thedarkknight", "#brucewayne", "#dccomics", "#movierelated", "#superhero", "#batmanlogo", "#batsymbol", "#minimalist", "#graphical", "#amoled", "#oledwallpaper", "#blackandwhite", "#monochrome", "#darkaesthetic", "#colourwise", "#themewise"]
  },
  {
    "id": 4,
    "file_name": "wallpaper_04_starry_night_mountain_lake_reflection.jpg",
    "title": "Milky Way Over Alpine Summit and Glassy Lake",
    "device_compatibility": "Desktop / PC / Laptop",
    "aspect_ratio": "16:9 Landscape",
    "primary_category": "Nature & Astrophotography",
    "themes": ["Nature", "Real", "Rivers", "Hills", "Stars", "Night Sky", "Lake Reflection"],
    "dominant_colors": ["Midnight Blue", "Deep Teal", "Warm Amber", "Starlight White"],
    "hashtags": ["#desktop", "#desktopwallpaper", "#pcwallpaper", "#nature", "#real", "#astrophotography", "#nightsky", "#stars", "#milkyway", "#mountains", "#hills", "#rivers", "#lake", "#lakereflection", "#pineforest", "#tranquil", "#darkaesthetic", "#bluewise", "#colourwise", "#themewise", "#4kdesktop"]
  },
  {
    "id": 5,
    "file_name": "wallpaper_05_sunset_valley_layered_mountains.jpg",
    "title": "Dreamy Pastel Sunset Over Layered Peaks",
    "device_compatibility": "Desktop / PC / Laptop",
    "aspect_ratio": "16:9 Landscape",
    "primary_category": "Illustration & Graphic Landscape",
    "themes": ["Nature", "Graphical", "Animated", "Hills", "Sunset", "Vaporwave Horizon"],
    "dominant_colors": ["Pastel Purple", "Rose Pink", "Soft Peach", "Indigo"],
    "hashtags": ["#desktop", "#desktopwallpaper", "#pcwallpaper", "#nature", "#graphical", "#animated", "#vectorart", "#digitalillustration", "#mountains", "#hills", "#sunset", "#sunsetlandscape", "#purpleaesthetic", "#pinkaesthetic", "#colourwise", "#themewise", "#vaporwave", "#calming", "#flatdesign", "#4kwallpaper"]
  },
  {
    "id": 6,
    "file_name": "wallpaper_06_crimson_ring_portal_barren_forest.jpg",
    "title": "The Crimson Portal in the Twisted Forest",
    "device_compatibility": "Desktop / PC / Laptop",
    "aspect_ratio": "16:9 Landscape",
    "primary_category": "Dark Fantasy & Anime",
    "themes": ["Dark Fantasy", "Anime", "Alone", "Portal", "Eclipse", "Apocalyptic Wasteland"],
    "dominant_colors": ["Crimson Red", "Charcoal Black", "Stormy Gray"],
    "hashtags": ["#desktop", "#desktopwallpaper", "#pcwallpaper", "#darkfantasy", "#anime", "#animated", "#alone", "#lonewanderer", "#portal", "#redring", "#eclipse", "#redaesthetic", "#blackandred", "#colourwise", "#themewise", "#apocalyptic", "#darkaesthetic", "#surrealart", "#4kwallpaper", "#epicscenery"]
  },
  {
    "id": 7,
    "file_name": "wallpaper_07_samurai_cherry_blossom_red_katana.jpg",
    "title": "Ronin Under Blood-Red Sakura and Full Moon",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Samurai & Japanese Art",
    "themes": ["Samurai", "Anime", "Katana", "Cherry Blossom", "Full Moon", "Alone"],
    "dominant_colors": ["Blood Red", "Magenta", "Charcoal Gray", "Moonlit White"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#samurai", "#ronin", "#anime", "#animated", "#katana", "#redkatana", "#cherryblossom", "#sakura", "#fullmoon", "#alone", "#warrior", "#japanart", "#redaesthetic", "#darkaesthetic", "#colourwise", "#themewise", "#4kphone"]
  },
  {
    "id": 8,
    "file_name": "wallpaper_08_raiden_shogun_electric_purple_slash.jpg",
    "title": "Electric Violet Katana Slash Across the Stars",
    "device_compatibility": "Desktop / PC / Laptop",
    "aspect_ratio": "16:9 Landscape",
    "primary_category": "Anime & Gaming",
    "themes": ["Anime", "Genshin Impact", "Raiden Shogun", "Acheron", "Sword Slash", "Cosmic"],
    "dominant_colors": ["Electric Purple", "Neon Violet", "Magenta", "Starlight White"],
    "hashtags": ["#desktop", "#desktopwallpaper", "#pcwallpaper", "#anime", "#animated", "#raidenshogun", "#genshinimpact", "#acheron", "#honkaistarrail", "#katana", "#swordslash", "#purpleaesthetic", "#neonpurple", "#electroslash", "#cosmicart", "#colourwise", "#themewise", "#gamingwallpaper", "#4kgaming"]
  },
  {
    "id": 9,
    "file_name": "wallpaper_09_inosuke_torii_gate_bioluminescent_blossoms.jpg",
    "title": "Inosuke at the Bioluminescent Torii Gate",
    "device_compatibility": "Desktop / PC / Laptop",
    "aspect_ratio": "16:9 Landscape",
    "primary_category": "Anime & Series Related",
    "themes": ["Series Related", "Anime", "Demon Slayer", "Inosuke Hashibira", "Torii Gate", "Glowing Flora"],
    "dominant_colors": ["Electric Cyan", "Neon Blue", "Lantern Red", "Midnight Blue"],
    "hashtags": ["#desktop", "#desktopwallpaper", "#pcwallpaper", "#seriesrelated", "#anime", "#animated", "#demonslayer", "#kimetsunoyaiba", "#inosuke", "#inosukehashibira", "#toriigate", "#japanesescenery", "#bluecherryblossom", "#bioluminescent", "#blueaesthetic", "#bluewise", "#colourwise", "#themewise", "#4kanime"]
  },
  {
    "id": 10,
    "file_name": "wallpaper_10_roronoa_zoro_golden_autumn_forest.jpg",
    "title": "Roronoa Zoro Strolling Through Autumn Foliage",
    "device_compatibility": "Desktop / PC / Laptop",
    "aspect_ratio": "16:9 Landscape",
    "primary_category": "Anime & Series Related",
    "themes": ["Series Related", "Anime", "One Piece", "Roronoa Zoro", "Samurai", "Autumn Nature"],
    "dominant_colors": ["Golden Amber", "Warm Yellow", "Forest Green", "Earth Brown"],
    "hashtags": ["#desktop", "#desktopwallpaper", "#pcwallpaper", "#seriesrelated", "#anime", "#animated", "#onepiece", "#roronoazoro", "#zoro", "#samurai", "#swordsman", "#autumnleaves", "#fallfoliage", "#goldenaesthetic", "#nature", "#forestpath", "#strawhats", "#colourwise", "#themewise", "#4kanime"]
  },
  {
    "id": 11,
    "file_name": "wallpaper_11_byakuya_kuchiki_bankai_senbonzakura.jpg",
    "title": "Byakuya Kuchiki - Senbonzakura Kageyoshi Bankai",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Anime & Series Related",
    "themes": ["Series Related", "Anime", "Bleach", "Byakuya Kuchiki", "Bankai", "Sakura Blades"],
    "dominant_colors": ["Petal Pink", "Glowing Violet", "Deep Black", "Pure White"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#seriesrelated", "#anime", "#animated", "#bleach", "#byakuyakuchiki", "#byakuya", "#senbonzakura", "#bankai", "#shinigami", "#soulreaper", "#pinkaesthetic", "#katana", "#swords", "#cherryblossom", "#colourwise", "#themewise"]
  },
  {
    "id": 12,
    "file_name": "wallpaper_12_interstellar_van_gogh_cosmic_farmhouse.jpg",
    "title": "Interstellar Farmhouse Under Van Gogh Accretion Disk",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Movie Related & Fine Art",
    "themes": ["Movie Related", "Interstellar", "Van Gogh", "Black Hole", "House", "Cosmic Art"],
    "dominant_colors": ["Cobalt Blue", "Fiery Orange", "Golden Yellow", "Cornfield Ochre"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#movierelated", "#interstellar", "#christophernolan", "#vangoghstyle", "#starrynight", "#blackhole", "#gargantua", "#house", "#farmhouse", "#scifi", "#spaceart", "#oilpainting", "#postimpressionism", "#colourwise", "#themewise", "#colorfulart"]
  },
  {
    "id": 13,
    "file_name": "wallpaper_13_lost_in_thought_quote_minimalist.jpg",
    "title": "Lost in Thought - Don't Believe Everything You Think",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Quotes & Philosophy",
    "themes": ["Quotes", "With Quotes", "Philosophy", "Mindset", "Eternal Knowledge", "Minimalist"],
    "dominant_colors": ["Textured Off-White", "Charcoal Black"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#withquotes", "#quotes", "#lostinthought", "#dontbelieveeverythingyouthink", "#philosophy", "#eternalknowledge", "#mindset", "#mindfulness", "#mentalhealth", "#stoicism", "#minimalist", "#graphical", "#blackandwhite", "#monochrome", "#typography", "#themewise"]
  },
  {
    "id": 14,
    "file_name": "wallpaper_14_solitary_tree_colossal_cloud_reflection.jpg",
    "title": "Solitary Tree Mirrored Beneath Massive Cumulus",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Nature & Symmetry",
    "themes": ["Nature", "Real", "Alone", "Lone Tree", "Clouds", "Rivers", "Lake Reflection"],
    "dominant_colors": ["Deep Obsidian", "Cloud White", "Golden Wheat"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#nature", "#real", "#alone", "#lonetree", "#clouds", "#cumuluscloud", "#reflection", "#lakereflection", "#rivers", "#symmetry", "#minimalistnature", "#darkmode", "#amoled", "#oledwallpaper", "#tranquil", "#themewise"]
  },
  {
    "id": 15,
    "file_name": "wallpaper_15_bronze_botanical_foliage_amoled_black.jpg",
    "title": "Golden Bronze Leaves on Pure AMOLED Black",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Nature & AMOLED",
    "themes": ["Nature", "AMOLED", "OLED Black", "Botanical", "Minimalist Leaves"],
    "dominant_colors": ["Pure Black", "Warm Bronze", "Caramel Brown"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#nature", "#amoled", "#oledwallpaper", "#trueblack", "#leaves", "#botanical", "#autumnvibes", "#autumnleaves", "#bronzeaesthetic", "#brownwise", "#colourwise", "#minimalist", "#cleanwallpaper", "#darkmode", "#negativespace"]
  },
  {
    "id": 16,
    "file_name": "wallpaper_16_planet_earth_from_orbit_night_lights.jpg",
    "title": "Orbital View of Mediterranean City Lights at Night",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Space & Nature",
    "themes": ["Nature", "Real", "Space", "Earth", "City Lights", "Astronomy"],
    "dominant_colors": ["Deep Ocean Blue", "Desert Sand", "City Gold", "Space Black"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#nature", "#real", "#space", "#earth", "#planetearth", "#earthfromspace", "#orbit", "#citylights", "#mediterranean", "#astronomy", "#cosmos", "#darkmode", "#bluewise", "#colourwise", "#themewise"]
  },
  {
    "id": 17,
    "file_name": "wallpaper_17_lone_astronaut_cliff_deep_space_nebula.jpg",
    "title": "Lone Watcher on Asteroid Cliff Over Cosmic Void",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Space & Solitude",
    "themes": ["Alone", "Space", "Solitude", "Nebula", "Hills", "Cliff Edge"],
    "dominant_colors": ["Pitch Black", "Nebula Blue", "Starlight White"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#alone", "#solitude", "#space", "#outerspace", "#astronomy", "#nebula", "#stars", "#lonewanderer", "#cliff", "#hills", "#scifi", "#existential", "#darkaesthetic", "#bluewise", "#colourwise", "#themewise"]
  },
  {
    "id": 18,
    "file_name": "wallpaper_18_great_pyramid_giza_starry_night.jpg",
    "title": "Great Pyramid of Giza Beneath the Starry Cosmos",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "History & Astrophotography",
    "themes": ["Real", "Pyramids", "History", "Stars", "Dark Aesthetic", "Monochrome"],
    "dominant_colors": ["Charcoal Black", "Graphite Gray", "Starlight White"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#real", "#pyramids", "#giza", "#egypt", "#ancientwonders", "#nightsky", "#stars", "#milkyway", "#darkaesthetic", "#monochrome", "#blackandwhite", "#amoled", "#historicmonument", "#themewise"]
  },
  {
    "id": 19,
    "file_name": "wallpaper_19_stormy_palm_trees_windy_coastal_highway.jpg",
    "title": "Windblown Palm Trees in a Dark Twilight Storm",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Nature & Atmospheric",
    "themes": ["Nature", "Real", "Storm", "Palm Trees", "Moody", "Dark Aesthetic"],
    "dominant_colors": ["Thunderstorm Gray", "Muted Olive", "Warm Streetlight Amber"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#nature", "#real", "#palmtrees", "#tropicalstorm", "#stormclouds", "#moodyphotography", "#darkaesthetic", "#rainyvibes", "#gloomy", "#coastalroad", "#atmospheric", "#themewise", "#cleanwallpaper"]
  },
  {
    "id": 20,
    "file_name": "wallpaper_20_daenerys_targaryen_facing_drogon_snow.jpg",
    "title": "Daenerys in Crimson Cloak Staring Down Drogon",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Series Related & Dragon",
    "themes": ["Series Related", "Game of Thrones Related", "Dragon", "Daenerys Targaryen", "Drogon", "Winter"],
    "dominant_colors": ["Winter Gray", "Dragon Charcoal", "Crimson Velvet"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#seriesrelated", "#gameofthronesrelated", "#gameofthrones", "#got", "#dragon", "#dragons", "#daenerystargaryen", "#drogon", "#motherofdragons", "#targaryen", "#houseofthedragon", "#dracarys", "#winteriscoming", "#epicfantasy", "#redaesthetic", "#colourwise", "#themewise"]
  },
  {
    "id": 21,
    "file_name": "wallpaper_21_jon_snow_viserion_ice_dragon_crimson_smoke.jpg",
    "title": "Jon Snow and the Blue-Eyed Dragon with Red Smoke Plume",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Series Related & Dragon",
    "themes": ["Series Related", "Game of Thrones Related", "Dragon", "Jon Snow", "Ice Dragon", "Red Smoke"],
    "dominant_colors": ["Stark White", "Crimson Red", "Dragon Slate", "Cyan Blue"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#seriesrelated", "#gameofthronesrelated", "#gameofthrones", "#got", "#dragon", "#icedragon", "#viserion", "#jonsnow", "#kinginthenorth", "#redsmoke", "#targaryen", "#stark", "#redandwhite", "#colourwise", "#themewise", "#popart", "#fantasyart"]
  },
  {
    "id": 22,
    "file_name": "wallpaper_22_papercraft_layered_wolf_head.jpg",
    "title": "3D Layered Paper Relief Wolf Head",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Graphical & Paper Art",
    "themes": ["Graphical", "Papercraft", "Wolf", "Direwolf", "Game of Thrones Related", "Minimalist"],
    "dominant_colors": ["Paper White", "Denim Blue", "Soft Gray"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#graphical", "#papercraft", "#paperart", "#origami", "#wolf", "#direwolf", "#housestark", "#gameofthronesrelated", "#minimalist", "#3dart", "#blueandwhite", "#bluewise", "#colourwise", "#themewise", "#cleanwallpaper"]
  },
  {
    "id": 23,
    "file_name": "wallpaper_23_minimalist_smoke_dragon_white_backdrop.jpg",
    "title": "Vaporous Smoke Dragon Head on High-Key White",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Dragon & Minimalist",
    "themes": ["Dragon", "Smoke Art", "Minimalist", "High Key", "Mythology"],
    "dominant_colors": ["Pure White", "Smoky Navy", "Icy Blue"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#dragon", "#dragons", "#smokearteffect", "#minimalist", "#highkey", "#whiteaesthetic", "#whitebackground", "#gameofthronesrelated", "#icedragon", "#fantasycreature", "#graphical", "#cleanwallpaper", "#themewise"]
  },
  {
    "id": 24,
    "file_name": "wallpaper_24_ancient_pale_dragon_fog_close_up.jpg",
    "title": "Close-Up Gaze of an Ancient Horned Dragon in Fog",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Dragon & Series Related",
    "themes": ["Dragon", "Series Related", "Game of Thrones Related", "House of the Dragon", "Vhagar", "Close-Up"],
    "dominant_colors": ["Pale Bone", "Smoky Gray", "Glowing Amber"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#dragon", "#dragons", "#seriesrelated", "#gameofthronesrelated", "#houseofthedragon", "#vhagar", "#dragonface", "#closeupportrait", "#fantasybeast", "#cinematic", "#mist", "#fog", "#themewise"]
  },
  {
    "id": 25,
    "file_name": "wallpaper_25_iron_man_tell_none_motivational_quote.jpg",
    "title": "Iron Man on Donut Roof - Until It's Done, Tell None",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Marvel & Quotes",
    "themes": ["Marvel", "Iron Man", "Movie Related", "With Quotes", "Quotes", "Motivation"],
    "dominant_colors": ["Sky Blue", "Iron Man Red", "Gold", "Bold Black"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#marvel", "#ironman", "#tonystark", "#movierelated", "#withquotes", "#quotes", "#untilitsdonetellnone", "#motivation", "#hustle", "#sigmamindset", "#successquotes", "#mcu", "#avengers", "#colourwise", "#themewise"]
  },
  {
    "id": 26,
    "file_name": "wallpaper_26_tony_stark_im_chosen_quote.jpg",
    "title": "Tony Stark Jericho Demo - I Can't Lose, I'm Chosen",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Marvel & Quotes",
    "themes": ["Marvel", "Tony Stark", "Movie Related", "With Quotes", "Quotes", "Hills", "Confidence"],
    "dominant_colors": ["Clear Sky Blue", "Snowy Peak White", "Suit Navy"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#marvel", "#tonystark", "#ironman", "#movierelated", "#withquotes", "#quotes", "#imchosen", "#confidence", "#billionairemindset", "#jericho", "#hills", "#mountains", "#mcu", "#avengers", "#themewise"]
  },
  {
    "id": 27,
    "file_name": "wallpaper_27_the_batman_then_who_crimson_quote.jpg",
    "title": "The Batman Silhouette - If Not Me, Then Who?",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Movies & Quotes",
    "themes": ["Movie Related", "Batman", "DC Comics", "With Quotes", "Quotes", "Red Aesthetic"],
    "dominant_colors": ["Blood Red", "Silhouette Black"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#batman", "#thebatman", "#robertpattinson", "#dccomics", "#movierelated", "#withquotes", "#quotes", "#ifnotmethenwho", "#redaesthetic", "#darkaesthetic", "#redwise", "#colourwise", "#themewise", "#superhero", "#vengeance"]
  },
  {
    "id": 28,
    "file_name": "wallpaper_28_makima_samsung_galaxy_manga_art.jpg",
    "title": "Makima Chainsaw Man Samsung Galaxy Wallpaper",
    "device_compatibility": "Smartphone (Samsung Galaxy / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Anime & Samsung Galaxy",
    "themes": ["Samsung Galaxy", "Anime", "Chainsaw Man", "Makima", "Manga", "AMOLED"],
    "dominant_colors": ["Deep Black", "Manga White", "Fiery Orange-Red Eyes"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#samsunggalaxy", "#samsungwallpaper", "#chainsawman", "#makima", "#anime", "#animated", "#mangaart", "#redeyes", "#amoled", "#oledwallpaper", "#darkmode", "#colourwise", "#themewise"]
  },
  {
    "id": 29,
    "file_name": "wallpaper_29_anbu_sharingan_samsung_galaxy.jpg",
    "title": "ANBU Mask & Sharingan Eye Samsung Galaxy Wallpaper",
    "device_compatibility": "Smartphone (Samsung Galaxy / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Anime & Samsung Galaxy",
    "themes": ["Samsung Galaxy", "Anime", "Naruto", "Itachi Uchiha", "Kakashi", "Sharingan", "ANBU"],
    "dominant_colors": ["True Black", "Porcelain White", "Sharingan Red"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#samsunggalaxy", "#samsungwallpaper", "#naruto", "#itachi", "#itachiuchiha", "#kakashi", "#anbu", "#sharingan", "#anime", "#animated", "#amoled", "#oledwallpaper", "#darkmode", "#colourwise", "#themewise"]
  },
  {
    "id": 30,
    "file_name": "wallpaper_30_anime_maid_bmw_e30_samsung_galaxy.jpg",
    "title": "Anime Maid on BMW E30 M3 Samsung Galaxy Wallpaper",
    "device_compatibility": "Smartphone (Samsung Galaxy / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Anime & Automotive",
    "themes": ["Samsung Galaxy", "Anime", "Anime Maid", "BMW E30", "JDM & Car Culture", "AMOLED"],
    "dominant_colors": ["Obsidian Black", "Gloss Black", "Neon Red Trim"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#samsunggalaxy", "#samsungwallpaper", "#animemaid", "#anime", "#animated", "#bmw", "#bmwe30", "#e30m3", "#carculture", "#jdm", "#amoled", "#oledwallpaper", "#darkmode", "#themewise"]
  },
  {
    "id": 31,
    "file_name": "wallpaper_31_classy_tailored_suit_samsung_galaxy.jpg",
    "title": "Classy Black Suit Cufflinks Samsung Galaxy Wallpaper",
    "device_compatibility": "Smartphone (Samsung Galaxy / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Minimalist & Lifestyle",
    "themes": ["Samsung Galaxy", "Classy", "Suit", "Gentleman", "Menswear", "AMOLED Minimal"],
    "dominant_colors": ["Pure Black", "Crisp White", "Charcoal Gray"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#samsunggalaxy", "#samsungwallpaper", "#classy", "#gentleman", "#suitandtie", "#mensfashion", "#tailoredsuit", "#elegance", "#minimalist", "#amoled", "#oledwallpaper", "#darkmode", "#themewise", "#cleanwallpaper"]
  },
  {
    "id": 32,
    "file_name": "wallpaper_32_tanjiro_sun_breathing_samsung_galaxy.jpg",
    "title": "Tanjiro Hinokami Kagura Flame Blade Samsung Galaxy",
    "device_compatibility": "Smartphone (Samsung Galaxy / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Anime & Series Related",
    "themes": ["Samsung Galaxy", "Series Related", "Anime", "Demon Slayer", "Tanjiro", "Sun Breathing"],
    "dominant_colors": ["Pure Black", "Flame Amber", "Crimson Fire", "Haori Green"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#samsunggalaxy", "#samsungwallpaper", "#seriesrelated", "#demonslayer", "#kimetsunoyaiba", "#tanjiro", "#tanjirokamado", "#sunbreathing", "#hinokamikagura", "#fireblade", "#anime", "#animated", "#amoled", "#themewise"]
  },
  {
    "id": 33,
    "file_name": "wallpaper_33_cyberpunk_oni_samurai_samsung_galaxy.jpg",
    "title": "Cyberpunk Samurai Oni & Skull Collage Samsung Galaxy",
    "device_compatibility": "Smartphone (Samsung Galaxy / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Samurai & Cyberpunk",
    "themes": ["Samsung Galaxy", "Samurai", "Oni Mask", "Cyberpunk", "Japanese Streetwear", "Skull"],
    "dominant_colors": ["Onyx Black", "Blood Red", "Bone White"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#samsunggalaxy", "#samsungwallpaper", "#samurai", "#onimask", "#cyberpunk", "#skull", "#japanesestreetwear", "#anime", "#graphical", "#redandblack", "#darkart", "#redaesthetic", "#colourwise", "#themewise"]
  },
  {
    "id": 34,
    "file_name": "wallpaper_34_neon_purple_coiling_dragon_samsung_galaxy.jpg",
    "title": "Neon Violet Coiling Eastern Dragon Samsung Galaxy",
    "device_compatibility": "Smartphone (Samsung Galaxy / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Dragon & AMOLED",
    "themes": ["Samsung Galaxy", "Dragon", "Purple Aesthetic", "Neon Art", "Asian Mythical Beast"],
    "dominant_colors": ["Electric Purple", "Neon Violet", "AMOLED Black"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#samsunggalaxy", "#samsungwallpaper", "#dragon", "#dragons", "#purpledragon", "#neondragon", "#purpleaesthetic", "#asiandragon", "#mythicalbeast", "#amoled", "#oledwallpaper", "#purplewise", "#colourwise", "#themewise"]
  },
  {
    "id": 35,
    "file_name": "wallpaper_35_interstellar_rocket_launch_over_farmhouse.jpg",
    "title": "Interstellar Rocket Ascent Over the Cooper Homestead",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Movie Related & Space",
    "themes": ["Movie Related", "Interstellar", "Christopher Nolan", "Rocket Launch", "House", "Space"],
    "dominant_colors": ["Golden Amber", "Charcoal Slate", "Night Sky Black"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#movierelated", "#interstellar", "#christophernolan", "#rocketlaunch", "#spacetravel", "#spaceexploration", "#scifi", "#house", "#farmhouse", "#linocut", "#vintageillustration", "#goldenaesthetic", "#colourwise", "#themewise"]
  },
  {
    "id": 36,
    "file_name": "wallpaper_36_great_wave_dark_eternity_japanese_art.jpg",
    "title": "Great Wave off Kanagawa - Dark Eternity Edition",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Japanese Art & Minimalist",
    "themes": ["Japanese Art", "Great Wave", "Rivers", "Ocean", "Minimalist", "Eternity"],
    "dominant_colors": ["Textured Dark Slate", "Ocean Blue", "Seafoam White"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#japaneseart", "#ukiyoe", "#thegreatwave", "#kanagawa", "#hokusai", "#eternity", "#oceanwaves", "#rivers", "#minimalist", "#darkaesthetic", "#japanesetypography", "#bluewise", "#colourwise", "#themewise"]
  },
  {
    "id": 37,
    "file_name": "wallpaper_37_miles_morales_rooftop_perch_sunset.jpg",
    "title": "Miles Morales Perched Above Glowing Manhattan",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Marvel & Comics",
    "themes": ["Marvel", "Spider-Man", "Miles Morales", "Superheroes", "City Lights", "Sunset"],
    "dominant_colors": ["Dusky Violet", "Sunset Coral", "Glittering Gold", "Shadow Navy"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#marvel", "#spiderman", "#milesmorales", "#intothespiderverse", "#superhero", "#nyc", "#newyorkcity", "#skyline", "#citylights", "#sunset", "#comicart", "#colourwise", "#themewise"]
  },
  {
    "id": 38,
    "file_name": "wallpaper_38_spiderman_high_spire_golden_sunset.jpg",
    "title": "Spider-Man Standing on High Spire at Sunset",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Marvel & Comics",
    "themes": ["Marvel", "Spider-Man", "Peter Parker", "Golden Hour", "Clouds", "NYC Spire"],
    "dominant_colors": ["Fiery Orange", "Golden Peach", "Rose Clouds", "Urban Navy"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#marvel", "#spiderman", "#peterparker", "#superhero", "#sunset", "#goldenhour", "#clouds", "#nyc", "#manhattan", "#skyline", "#heroic", "#comicbookart", "#colourwise", "#themewise"]
  },
  {
    "id": 39,
    "file_name": "wallpaper_39_spiderman_into_the_spiderverse_inverted_dive.jpg",
    "title": "What's Up Danger - Inverted Manhattan Skyfall",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Marvel & Movie Related",
    "themes": ["Marvel", "Movie Related", "Spider-Man", "Miles Morales", "Leap of Faith", "Color Wise"],
    "dominant_colors": ["Cotton Candy Pink", "Sunset Coral", "Cyber Violet", "Skyline Amber"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#marvel", "#movierelated", "#spiderman", "#milesmorales", "#intothespiderverse", "#whatsupdanger", "#leapoffaith", "#invertedcity", "#pinkaesthetic", "#purplesky", "#cinematicart", "#superhero", "#colourwise", "#themewise"]
  },
  {
    "id": 40,
    "file_name": "wallpaper_40_miles_morales_leap_of_faith_jordans.jpg",
    "title": "Miles Morales Leap of Faith with Jordan 1s",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Marvel & Movie Related",
    "themes": ["Marvel", "Movie Related", "Spider-Man", "Miles Morales", "Streetwear", "Leap of Faith"],
    "dominant_colors": ["Electric Cyan", "Jacket Green", "Spider Red", "City Navy"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#marvel", "#movierelated", "#spiderman", "#milesmorales", "#intothespiderverse", "#leapoffaith", "#airjordan1", "#streetwear", "#superhero", "#blueaesthetic", "#bluewise", "#actionanime", "#colourwise", "#themewise"]
  },
  {
    "id": 41,
    "file_name": "wallpaper_41_spiderman_swinging_wet_street_yellow_cab.jpg",
    "title": "Spider-Man Swinging Low Across Wet Neon NYC Street",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Marvel & Cinematic",
    "themes": ["Marvel", "Spider-Man", "Miles Morales", "Rainy Night", "Yellow Cab", "Cyberpunk NYC"],
    "dominant_colors": ["Neon Red", "Cab Yellow", "Wet Asphalt Black", "Cyan Glow"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#marvel", "#spiderman", "#milesmorales", "#superhero", "#nyc", "#yellowcab", "#rainynight", "#neoncity", "#citystreet", "#reflections", "#cyberpunkvibes", "#urban", "#colourwise", "#themewise"]
  },
  {
    "id": 42,
    "file_name": "wallpaper_42_spiderman_in_bed_watching_city_burn.jpg",
    "title": "Spider-Man in Bed Watching the City Burn",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Marvel & Comics",
    "themes": ["Marvel", "Spider-Man", "Peter Parker", "Comic Art", "Burning City", "Tragedy"],
    "dominant_colors": ["Fire Orange", "Explosion Yellow", "Smoke Gray", "Costume Red & Blue"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#marvel", "#spiderman", "#peterparker", "#comicart", "#burningcity", "#fire", "#apocalypse", "#superhero", "#responsibility", "#dramatic", "#emotionalart", "#colourwise", "#themewise"]
  },
  {
    "id": 43,
    "file_name": "wallpaper_43_kendrick_lamar_damn_last_supper_red.jpg",
    "title": "Kendrick Lamar DAMN. - The Last Supper",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Music & Pop Culture",
    "themes": ["Music Related", "Kendrick Lamar", "DAMN.", "The Last Supper", "Red Aesthetic"],
    "dominant_colors": ["Fiery Crimson Red", "Matte Black", "Earthy Tones"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#musicrelated", "#kendricklamar", "#damn", "#humble", "#hiphop", "#rapmusic", "#albumart", "#lastsupper", "#redaesthetic", "#blackandred", "#redwise", "#colourwise", "#themewise", "#popculture"]
  },
  {
    "id": 44,
    "file_name": "wallpaper_44_traditional_japanese_gold_curling_waves.jpg",
    "title": "Traditional Japanese Gold Waves and Crimson Disks",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Japanese Art & Dark Aesthetic",
    "themes": ["Japanese Art", "Rivers", "Ocean Waves", "Blood Moon", "Gold Leaf Texture"],
    "dominant_colors": ["Textured Black", "Antique Gold", "Crimson Red"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#japaneseart", "#ukiyoe", "#goldwaves", "#bloodmoon", "#redandblack", "#goldenaesthetic", "#darkaesthetic", "#oceanwaves", "#traditionalart", "#zenart", "#colourwise", "#themewise"]
  },
  {
    "id": 45,
    "file_name": "wallpaper_45_spiderman_noir_detective_portrait.jpg",
    "title": "Spider-Man Noir 1930s Detective Close-Up",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Marvel & Film Noir",
    "themes": ["Marvel", "Spider-Man Noir", "Detective", "Monochrome", "Black and White"],
    "dominant_colors": ["Deep Shadows", "Charcoal Black", "Highlight White"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#marvel", "#spidermannoir", "#spiderman", "#superhero", "#detective", "#filmnoir", "#1930s", "#blackandwhite", "#monochrome", "#darkaesthetic", "#vintagecomics", "#fedora", "#themewise"]
  },
  {
    "id": 46,
    "file_name": "wallpaper_46_spiderman_noir_under_bridge_desktop.jpg",
    "title": "Spider-Man Noir Beneath the Misty Suspension Bridge",
    "device_compatibility": "Desktop / PC / Laptop",
    "aspect_ratio": "16:9 Landscape",
    "primary_category": "Marvel & Film Noir",
    "themes": ["Marvel", "Spider-Man Noir", "Bridge", "Monochrome", "Vintage NYC"],
    "dominant_colors": ["Grayscale", "Dark Charcoal", "Lantern White"],
    "hashtags": ["#desktop", "#desktopwallpaper", "#pcwallpaper", "#marvel", "#spidermannoir", "#spiderman", "#filmnoir", "#manhattanbridge", "#bridge", "#1930s", "#vintagecars", "#blackandwhite", "#monochrome", "#cinematic", "#superhero", "#themewise"]
  },
  {
    "id": 47,
    "file_name": "wallpaper_47_abstract_black_ink_wash_flowing_curls.jpg",
    "title": "Dynamic Sumi-e Black Ink Wash Swirl",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Abstract & Minimalist",
    "themes": ["Abstract", "Sumi-e", "Ink Wash", "Monochrome", "Fluid Dynamics"],
    "dominant_colors": ["Chinese Ink Black", "Washi Paper White"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#abstractart", "#inkwash", "#sumie", "#monochrome", "#blackandwhite", "#fluidart", "#minimalist", "#graphical", "#chinesepainting", "#fineart", "#cleanwallpaper", "#themewise"]
  },
  {
    "id": 48,
    "file_name": "wallpaper_48_grim_reaper_scythe_solar_eclipse_beam.jpg",
    "title": "Grim Reaper with Golden Scythe and Eclipse Ray",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Dark Fantasy & Occult",
    "themes": ["Dark Fantasy", "Grim Reaper", "Scythe", "Eclipse", "Red Clouds", "Neon Pink"],
    "dominant_colors": ["Void Black", "Blood Red", "Neon Magenta", "Burnished Gold"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#darkfantasy", "#grimreaper", "#death", "#scythe", "#eclipse", "#bloodred", "#redaesthetic", "#neonpink", "#magenta", "#gothicart", "#darkart", "#heavymetal", "#redwise", "#colourwise", "#themewise"]
  },
  {
    "id": 49,
    "file_name": "wallpaper_49_3d_carved_stone_river_canyon_relief.jpg",
    "title": "3D Topographic Slate Stone River Canyon",
    "device_compatibility": "Smartphone (iOS / Android)",
    "aspect_ratio": "9:16 Portrait",
    "primary_category": "Topography & Nature Art",
    "themes": ["Nature", "Rivers", "Topography", "3D Relief", "Chinese Calligraphy", "Slate Texture"],
    "dominant_colors": ["Steel Blue", "Slate Gray", "Gold Dust"],
    "hashtags": ["#phone", "#phonewallpaper", "#lockscreen", "#nature", "#topography", "#3drelief", "#rivers", "#canyon", "#slate", "#rocktexture", "#chinesecalligraphy", "#minimalist", "#bluewise", "#blueaesthetic", "#cleanwallpaper", "#graphical", "#themewise"]
  }
]

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def analyze_image_properties(img):
    img_rgb = img.convert('RGB')
    small_img = img_rgb.resize((60, 60))
    colors = small_img.getcolors(3600)
    
    if not colors:
        return "#6366f1", "blue", 128, 0.5, 0.5, 50.0

    colors.sort(key=lambda x: x[0], reverse=True)
    
    dom_rgb = colors[0][1]
    for count, (r, g, b) in colors[:15]:
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        if 0.15 < s < 0.95 and 0.15 < v < 0.95:
            dom_rgb = (r, g, b)
            break
            
    r, g, b = dom_rgb
    hex_color = rgb_to_hex(r, g, b)
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    hue_deg = h * 360.0

    if v < 0.20:
        color_family = "dark"
    elif s < 0.12:
        color_family = "white" if v > 0.8 else "dark"
    elif hue_deg >= 340 or hue_deg < 15:
        color_family = "red"
    elif 15 <= hue_deg < 45:
        color_family = "gold"
    elif 45 <= hue_deg < 70:
        color_family = "gold"
    elif 70 <= hue_deg < 165:
        color_family = "green"
    elif 165 <= hue_deg < 210:
        color_family = "cyan"
    elif 210 <= hue_deg < 255:
        color_family = "blue"
    elif 255 <= hue_deg < 290:
        color_family = "purple"
    elif 290 <= hue_deg < 340:
        color_family = "pink"
    else:
        color_family = "blue"

    gray = img.convert('L').resize((120, 120))
    edges = gray.filter(ImageFilter.FIND_EDGES)
    stat = ImageStat.Stat(edges)
    edge_std = stat.stddev[0]

    return hex_color, color_family, hue_deg, s, v, edge_std

def sanitize_filename(filename):
    name, ext = os.path.splitext(filename)
    clean = name.replace('#', '').replace(' ', '_').replace('-', '_')
    clean = re.sub(r'__+', '_', clean).strip('_')
    if not clean:
        clean = "wallpaper"
    return clean.lower() + ext.lower()

KEYWORD_MAP = {
    'vishnu': 1, 'sheshanaga': 1, 'narayana': 1,
    'mountain_peak': 2, 'alpine_peak': 2, 'chiseled_alpine': 2,
    'batman': 3, 'dark_knight': 3, 'bat_symbol': 3, 'batsymbol': 3,
    'lake_reflection': 4, 'starry_night_mountain': 4,
    'sunset_valley': 5, 'layered_mountains': 5, 'vaporwave_horizon': 5,
    'crimson_ring': 6, 'twisted_forest': 6, 'apocalyptic_wasteland': 6,
    'samurai': 7, 'red_katana': 7, 'ronin': 7, 'cherry_blossom_red': 7,
    'raiden_shogun': 8, 'genshin': 8, 'acheron': 8, 'purple_slash': 8,
    'inosuke': 9, 'torii_gate': 9, 'demon_slayer': 9,
    'zoro': 10, 'roronoa': 10, 'one_piece': 10,
    'byakuya': 11, 'senbonzakura': 11, 'bankai': 11, 'bleach': 11,
    'interstellar': 12, 'van_gogh': 12, 'accretion_disk': 12,
    'lost_in_thought': 13, 'quote': 13, 'dont_believe': 13,
    'solitary_tree': 14, 'cumulus': 14, 'lone_tree': 14,
    'bronze_botanical': 15, 'foliage': 15, 'golden_bronze': 15,
    'earth': 16, 'orbit': 16, 'mediterranean': 16,
    'astronaut': 17, 'asteroid_cliff': 17, 'nebula': 17,
    'pyramid': 18, 'giza': 18, 'egypt': 18,
    'palm_tree': 19, 'coastal_highway': 19, 'tropical_storm': 19,
    'daenerys': 20, 'drogon': 20, 'mother_of_dragons': 20,
    'jon_snow': 21, 'viserion': 21, 'ice_dragon': 21,
    'papercraft': 22, 'layered_wolf': 22, 'direwolf': 22,
    'smoke_dragon': 23, 'high_key_white': 23,
    'ancient_pale_dragon': 24, 'vhagar': 24, 'house_of_the_dragon': 24,
    'iron_man': 25, 'until_its_done': 25, 'tell_none': 25,
    'tony_stark': 26, 'im_chosen': 26, 'jericho': 26,
    'the_batman': 27, 'if_not_me': 27, 'then_who': 27,
    'makima': 28, 'chainsaw_man': 28,
    'anbu': 29, 'sharingan': 29, 'itachi': 29,
    'anime_maid': 30, 'bmw_e30': 30, 'e30_m3': 30,
    'classy': 31, 'tailored_suit': 31, 'cufflinks': 31,
    'tanjiro': 32, 'sun_breathing': 32, 'hinokami': 32,
    'oni_samurai': 33, 'cyberpunk_oni': 33, 'skull_collage': 33,
    'coiling_dragon': 34, 'neon_violet_dragon': 34,
    'cooper_homestead': 35, 'rocket_ascent': 35, 'rocket_launch': 35,
    'great_wave': 36, 'kanagawa': 36, 'hokusai': 36,
    'miles_morales': 37, 'spiderverse': 37, 'rooftop_perch': 37,
    'high_spire': 38, 'spiderman_golden_sunset': 38,
    'whats_up_danger': 39, 'inverted_dive': 39, 'inverted_manhattan': 39,
    'leap_of_faith': 40, 'jordan_1s': 40,
    'yellow_cab': 41, 'wet_street': 41, 'swinging_low': 41,
    'in_bed_watching': 42, 'city_burn': 42,
    'kendrick': 43, 'kendrick_lamar': 43, 'damn': 43, 'last_supper': 43,
    'gold_waves': 44, 'crimson_disks': 44,
    'spiderman_noir': 45, 'detective_portrait': 45, 'fedora': 45,
    'suspension_bridge': 46, 'under_bridge': 46,
    'ink_wash': 47, 'sumi_e': 47, 'black_ink': 47,
    'grim_reaper': 48, 'golden_scythe': 48, 'eclipse_ray': 48,
    'canyon_relief': 49, 'topographic_slate': 49, 'river_canyon': 49
}

def match_metadata(filename, index):
    lower_f = filename.lower()
    for meta in USER_METADATA_LIST:
        meta_fname = meta['file_name'].lower()
        if meta_fname in lower_f or lower_f in meta_fname:
            return meta
    
    # Keyword search
    for kw, meta_id in KEYWORD_MAP.items():
        if kw in lower_f:
            return USER_METADATA_LIST[meta_id - 1]

    # Index fallback if 1 <= index <= len(USER_METADATA_LIST)
    if 1 <= index <= len(USER_METADATA_LIST):
        return USER_METADATA_LIST[index - 1]

    return None

def determine_genres(filename, category, color_family, sat, val, edge_std, matched_meta=None):
    if matched_meta:
        cat_str = matched_meta.get('primary_category', '').lower()
        genres = set()
        if any(k in cat_str for k in ['movie', 'series', 'anime', 'marvel', 'comics']):
            genres.add('movies_series')
        if any(k in cat_str for k in ['spiritual', 'mythology', 'god', 'divine']):
            genres.add('spiritual_divine')
        if any(k in cat_str for k in ['nature', 'astrophotography', 'landscape', 'symmetry', 'atmospheric']):
            genres.add('nature_landscape')
        if any(k in cat_str for k in ['illustration', 'graphic', 'paper', 'abstract', 'topography']):
            genres.add('animated_graphical')
        if any(k in cat_str for k in ['dark', 'amoled', 'occult']):
            genres.add('dark_amoled')
        if any(k in cat_str for k in ['minimal', 'minimalism', 'quotes', 'lifestyle']):
            genres.add('light_minimal')

        if not genres:
            genres.add('animated_graphical')

        genre_priority = ['movies_series', 'spiritual_divine', 'nature_landscape', 'animated_graphical', 'dark_amoled', 'light_minimal']
        primary = 'animated_graphical'
        for p in genre_priority:
            if p in genres:
                primary = p
                break

        return primary, sorted(list(genres))

    lower_f = filename.lower()
    genres = set()

    movie_keywords = ['got', 'game_of_thrones', 'mentalist', 'cinema', 'movie', 'series', 'character', 'anime', 'hero', 'joker', 'batman', 'marvel', 'spiderman', 'zoro', 'inosuke', 'byakuya', 'makima', 'tanjiro', 'drogon', 'kendrick']
    if any(k in lower_f for k in movie_keywords):
        genres.add('movies_series')

    spiritual_keywords = ['krishna', 'radhe', 'buddha', 'god', 'divine', 'statue', 'spiritual', 'devotional', 'temple', 'sacred', 'vishnu', 'sheshanaga']
    if any(k in lower_f for k in spiritual_keywords):
        genres.add('spiritual_divine')

    nature_keywords = ['mountain', 'nature', 'sunset', 'landscape', 'tree', 'fuji', 'scenery', 'autumn', 'lake', 'sunrise', 'alpes', 'sea', 'sky', 'milky_way', 'stars', 'forest', 'river']
    if any(k in lower_f for k in nature_keywords) or color_family in ['green', 'gold'] and edge_std > 20:
        genres.add('nature_landscape')

    if 'generative_ai' in lower_f or 'abstract' in lower_f or 'vector' in lower_f or '3d' in lower_f or edge_std < 24:
        genres.add('animated_graphical')

    if val < 0.35 or color_family == 'dark':
        genres.add('dark_amoled')

    if val > 0.70 and sat < 0.25 or color_family == 'white':
        genres.add('light_minimal')

    if not genres:
        genres.add('animated_graphical')

    genre_priority = ['movies_series', 'spiritual_divine', 'nature_landscape', 'animated_graphical', 'dark_amoled', 'light_minimal']
    primary = 'animated_graphical'
    for p in genre_priority:
        if p in genres:
            primary = p
            break

    return primary, sorted(list(genres))

def generate_natural_title(filename, primary_genre, color_family, index, matched_meta=None):
    if matched_meta and matched_meta.get('title'):
        return matched_meta['title']

    name_stem = os.path.splitext(filename)[0]
    clean = re.sub(r'^\d+_', '', name_stem)
    clean = re.sub(r'img_\d+_\d+_\d+|\d+_\d+_\d+_\d+', '', clean, flags=re.IGNORECASE)
    clean = re.sub(r'[a-f0-9]{8}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{12}', '', clean, flags=re.IGNORECASE)
    clean = clean.replace('_', ' ').replace('-', ' ').strip()

    lower_f = filename.lower()
    if 'got' in lower_f or 'game_of_thrones' in lower_f:
        return f"Game of Thrones Artwork #{index}"
    if 'mentalist' in lower_f:
        return f"The Mentalist Art #{index}"
    if 'krishna' in lower_f or 'radhe' in lower_f:
        return f"Radhe Krishna Divine Art #{index}"
    if 'fuji' in lower_f:
        return f"Mount Fuji Landscape #{index}"
    if 'joker' in lower_f:
        return f"The Joker Cyber Art #{index}"
    if 'batman' in lower_f:
        return f"Dark Knight Batman #{index}"

    words = clean.split()
    valid_words = [w.capitalize() for w in words if not w.isdigit() and len(w) > 2 and w.lower() not in ['img', 'picjumbo', 'com', 'jpeg', 'jpg', 'png', 'webp', 'px', 'hd', 'wallpaper', 'wallpapers', 'pinterest', 'download']]

    if valid_words and len(" ".join(valid_words)) >= 4:
        title = " ".join(valid_words)
        if len(title) > 36:
            title = title[:34] + '...'
        return title

    color_descriptors = {
        'dark': ['Obsidian', 'Midnight', 'Shadow', 'Eclipse', 'Onyx', 'Dark Cyber'],
        'cyan': ['Neon Cyan', 'Electric Cyan', 'Aqua Horizon', 'Cyan Cyber', 'Azure Stream'],
        'blue': ['Deep Cobalt', 'Celestial Blue', 'Oceanic Depth', 'Sapphire', 'Cosmic Blue'],
        'purple': ['Mystic Violet', 'Cosmic Purple', 'Amethyst Glow', 'Nebula Purple', 'Velvet Dusk'],
        'pink': ['Vibrant Magenta', 'Neon Pink', 'Cyberpunk Pink', 'Rose Glow', 'Sakura Pulse'],
        'gold': ['Solar Amber', 'Golden Horizon', 'Autumn Gold', 'Gilded Sun', 'Radiant Dawn'],
        'green': ['Emerald Nature', 'Verdant Forest', 'Jade Horizon', 'Bio Green', 'Forest mist'],
        'red': ['Crimson Flare', 'Scarlet Cyber', 'Inferno Red', 'Ruby Ember', 'Magma Glow'],
        'white': ['Minimalist Ivory', 'Pure Monolith', 'Crystal White', 'Snow Apex', 'Luminous Frost']
    }

    genre_descriptors = {
        'movies_series': 'Cinematic Artwork',
        'spiritual_divine': 'Sacred Devotional',
        'nature_landscape': 'Nature Horizon',
        'animated_graphical': 'Abstract Render',
        'reality_photo': 'Scenic Photograph',
        'dark_amoled': 'AMOLED Edition',
        'light_minimal': 'Minimal Aesthetic'
    }

    colors_list = color_descriptors.get(color_family, ['Chroma', 'Lumina', 'Vivid'])
    color_prefix = colors_list[(index - 1) % len(colors_list)]
    genre_suffix = genre_descriptors.get(primary_genre, 'Visual Art')

    return f"{color_prefix} {genre_suffix} #{index}"

def run_sanitization_and_tagging():
    pictures_dir = os.path.join(os.path.dirname(__file__), 'Pictures')
    if not os.path.exists(pictures_dir):
        print(f"Pictures directory missing at {pictures_dir}")
        return

    files = sorted(os.listdir(pictures_dir))
    wallpapers = []
    id_counter = 1

    for f in files:
        fp = os.path.join(pictures_dir, f)
        if not os.path.isfile(fp):
            continue

        ext = os.path.splitext(f)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            continue

        # Sanitize filename if needed
        clean_f = sanitize_filename(f)
        if clean_f != f.lower() and not os.path.exists(os.path.join(pictures_dir, clean_f)):
            new_fp = os.path.join(pictures_dir, clean_f)
            try:
                os.rename(fp, new_fp)
                fp = new_fp
                f = clean_f
            except Exception as e:
                pass

        size_bytes = os.path.getsize(fp)

        try:
            with Image.open(fp) as img:
                w, h = img.size
                ratio = round(w / h, 2)
                hex_color, color_family, hue, sat, val, edge_std = analyze_image_properties(img)
        except Exception as e:
            w, h = 1080, 1920
            ratio = 0.56
            hex_color, color_family, sat, val, edge_std = "#6366f1", "blue", 0.5, 0.5, 30.0

        if ratio >= 1.25:
            category = 'desktop'
        elif ratio <= 0.85:
            category = 'phone'
        else:
            category = 'both'

        matched_meta = match_metadata(f, id_counter)

        primary_genre, genre_list = determine_genres(f, category, color_family, sat, val, edge_std, matched_meta)

        tags = set(genre_list)
        tags.add(color_family)
        
        if category == 'phone':
            tags.update(['mobile', 'portrait', 'phone'])
        elif category == 'desktop':
            tags.update(['desktop', 'landscape', 'monitor', 'pc'])
        else:
            tags.update(['universal', 'square'])

        if w >= 2500 or h >= 2500:
            tags.update(['4k', 'ultra_hd'])

        if matched_meta:
            for tag in matched_meta.get('hashtags', []):
                tags.add(tag.lstrip('#').lower())
            for theme in matched_meta.get('themes', []):
                tags.add(theme.lower().replace(' ', '_'))
            for col in matched_meta.get('dominant_colors', []):
                tags.add(col.lower().replace(' ', '_'))
            if matched_meta.get('primary_category'):
                tags.add(matched_meta['primary_category'].lower().replace(' ', '_'))

        lower_name = f.lower()
        if any(k in lower_name for k in ['krishna', 'radhe', 'god', 'divine', 'vishnu']):
            tags.update(['krishna', 'radheradhe', 'spiritual', 'devotional', 'vishnu', 'sheshanaga'])
        if any(k in lower_name for k in ['mountain', 'nature', 'sunset', 'landscape']):
            tags.update(['nature', 'mountains', 'sunset'])

        display_title = generate_natural_title(f, primary_genre, color_family, id_counter, matched_meta)

        if size_bytes > 1024 * 1024:
            size_str = f'{size_bytes / (1024 * 1024):.2f} MB'
        else:
            size_str = f'{size_bytes / 1024:.1f} KB'

        rel_path = f'Pictures/{f}'
        encoded_path = f'Pictures/{urllib.parse.quote(f)}'

        # Generate low-quality optimized preview thumbnail for ultra-fast page loading
        thumb_dir = os.path.join(os.path.dirname(__file__), 'Thumbnails')
        os.makedirs(thumb_dir, exist_ok=True)
        base_name, _ = os.path.splitext(f)
        safe_base = re.sub(r'[^a-zA-Z0-9_-]', '_', base_name)
        thumb_filename = f"thumb_{id_counter}_{safe_base}.jpg"
        thumb_fp = os.path.join(thumb_dir, thumb_filename)

        if not os.path.exists(thumb_fp) or (os.path.exists(fp) and os.path.getmtime(fp) > os.path.getmtime(thumb_fp)):
            try:
                with Image.open(fp) as img_thumb:
                    img_copy = img_thumb.copy()
                    if img_copy.mode in ('RGBA', 'LA', 'P'):
                        img_copy = img_copy.convert('RGB')
                    img_copy.thumbnail((450, 450), Image.Resampling.LANCZOS)
                    img_copy.save(thumb_fp, 'JPEG', quality=65, optimize=True)
            except Exception as thumb_err:
                print(f"Warning: Failed to thumbnail {f}: {thumb_err}")

        rel_thumb = f'Thumbnails/{thumb_filename}'
        encoded_thumb = f'Thumbnails/{urllib.parse.quote(thumb_filename)}'

        wallpapers.append({
            'id': id_counter,
            'filename': f,
            'title': display_title,
            'path': rel_path,
            'encodedPath': encoded_path,
            'thumbnail': rel_thumb,
            'encodedThumbnail': encoded_thumb,
            'width': w,
            'height': h,
            'aspectRatio': ratio,
            'category': category,
            'primaryGenre': primary_genre,
            'genres': genre_list,
            'hexColor': hex_color,
            'colorFamily': color_family,
            'size': size_str,
            'sizeBytes': size_bytes,
            'tags': sorted(list(tags))
        })
        id_counter += 1

    json_path = os.path.join(os.path.dirname(__file__), 'wallpapers.json')
    with open(json_path, 'w', encoding='utf-8') as out_f:
        json.dump(wallpapers, out_f, indent=2)

    js_path = os.path.join(os.path.dirname(__file__), 'wallpapers.js')
    with open(js_path, 'w', encoding='utf-8') as out_f:
        out_f.write('window.WALLPAPERS_DATA = ' + json.dumps(wallpapers, indent=2) + ';')

    print(f"Successfully generated wallpapers.json and wallpapers.js ({len(wallpapers)} items with rich metadata)")

if __name__ == '__main__':
    run_sanitization_and_tagging()
