import os
import re

FRONTEND_SRC = "frontend/src"

REPLACEMENTS = [
    # 1. Fix the "SHIVA / MEN" and "SHAKTI / WOMEN" in english and translations
    (re.compile(r"SHIVA\s*/\s*MEN", re.IGNORECASE), "MEN"),
    (re.compile(r"SHAKTI\s*/\s*WOMEN", re.IGNORECASE), "WOMEN"),
    (re.compile(r"SHIVA\s*/\s*[^\"]+"), "MEN"), # For other languages like "SHIVA / HOMBRE"
    (re.compile(r"SHAKTI\s*/\s*[^\"]+"), "WOMEN"),
    
    # 2. Fix the specific translation keys and URLs
    (re.compile(r"/shop/shiva"), "/shop/men"),
    (re.compile(r"/shop/shakti"), "/shop/women"),
    (re.compile(r"nav\.shiva"), "nav.men"),
    (re.compile(r"nav\.shakti"), "nav.women"),
    (re.compile(r"home\.shivaMen"), "home.men"),
    (re.compile(r"home\.shaktiWomen"), "home.women"),
    (re.compile(r"home\.shivaDeconstructed"), "home.menDeconstructed"),
    (re.compile(r"home\.shaktiSilhouettes"), "home.womenSilhouettes"),
    (re.compile(r"home\.shivaDesc"), "home.menDesc"),
    (re.compile(r"home\.shaktiDesc"), "home.womenDesc"),
    (re.compile(r"home\.exploreShiva"), "home.exploreMen"),
    (re.compile(r"home\.exploreShakti"), "home.exploreWomen"),
    (re.compile(r"footer\.shiva"), "footer.men"),
    (re.compile(r"footer\.shakti"), "footer.women"),
    (re.compile(r"shop\.shivaCollection"), "shop.menCollection"),
    (re.compile(r"shop\.shaktiCollection"), "shop.womenCollection"),
    (re.compile(r"shop\.shivaDesc"), "shop.menDesc"),
    (re.compile(r"shop\.shaktiDesc"), "shop.womenDesc"),

    # 3. Code state variables and general strings
    (re.compile(r"\"shiva\""), "\"men\""),
    (re.compile(r"\"shakti\""), "\"women\""),
    (re.compile(r"'shiva'"), "'men'"),
    (re.compile(r"'shakti'"), "'women'"),
    (re.compile(r"=== \"shiva\""), "=== \"men\""),
    (re.compile(r"=== \"shakti\""), "=== \"women\""),
    (re.compile(r"isShiva"), "isMen"),
    (re.compile(r"isShakti"), "isWomen"),
    
    # 4. Display text
    (re.compile(r"\"SHIVA\""), "\"MEN\""),
    (re.compile(r"\"SHAKTI\""), "\"WOMEN\""),
    (re.compile(r"\"Shiva\""), "\"Men\""),
    (re.compile(r"\"Shakti\""), "\"Women\""),
    
    # 5. Catch any stray Shiva/Shakti in English texts (like "Shiva Avant-Garde")
    (re.compile(r"\bShiva\b"), "Men"),
    (re.compile(r"\bShakti\b"), "Women"),
    (re.compile(r"\bSHIVA\b"), "MEN"),
    (re.compile(r"\bSHAKTI\b"), "WOMEN"),
]

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    original = content
    for pattern, replacement in REPLACEMENTS:
        content = pattern.sub(replacement, content)
        
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {filepath}")

for root, _, files in os.walk(FRONTEND_SRC):
    for file in files:
        if file.endswith((".ts", ".tsx", ".css")):
            process_file(os.path.join(root, file))

print("Done renaming categories in frontend!")
