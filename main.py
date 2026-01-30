import re
import random
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import colorsys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def preprocess(text:str)->str:
    text=text.strip().lower()
    text=re.sub(r'\s+',' ',text)
    return text

def detect_mood_vader(text:str)->tuple:
    sia=SentimentIntensityAnalyzer()
    scores=sia.polarity_scores(text)
    compound=scores['compound']

    if compound>=0.05:
        mood="happy"
    elif compound<=-0.05:
        mood="sad"
    else:
        mood="calm"
    
    keywords={
        "birthday": "birthday",
        "wedding": "wedding",
        "party": "party",
        "love": "romantic",
        "romantic": "romantic",
        "study": "focus",
        "aesthetic": "aesthetic",
        "dark": "dark",
        "light": "light",
    }

    theme=None
    for k,v in keywords.items():
        if k in text:
            theme=v
            break

    if theme in ("wedding","birthday"):
        if mood=="calm":
            return f"happy_{theme}"
        else:
         return f"{mood}_{theme}"
    elif theme =="party":
        if mood in("happy","calm"):
            return f"excited"
        else:
            return f"disappointed"
    elif theme:
        return f"{theme}"
    else:
        return mood


mood_palettes = {
    "happy": (45, 1.0, 1.0),
    "sad": (210, 0.4, 0.5),
    "calm": (200, 0.2, 0.8),
    "birthday": (320, 0.7, 1.0),
    "wedding": (30, 0.2, 1.0),
    "excited": (270, 1.0, 0.8),
    "romantic": (350, 0.7, 0.9),
    "focus": (180, 0.3, 0.7),
    "aesthetic": (250, 0.3, 0.7),
    "dark": (0, 0.0, 0.2),
    "light": (50, 0.1, 1.0),

    # Combined variations 
    "sad_birthday": (210, 0.3, 0.6),
    "happy_birthday": (320, 0.8, 1.0),
    "sad_wedding": (220, 0.2, 0.8),
    "happy_wedding": (35, 0.3, 1.0),
    "disappointed": (200, 0.3, 0.5),
    "excited": (280, 1.0, 0.8),
}

mood_messages={
    "happy": ("💛 Bright & joyful vibes ahead!", "A burst of sunshine and cheer!"),
    "sad": ("💙 Soft hues for gentle comfort.", "Even on cloudy days, color heals."),
    "calm": ("🤍 Peaceful tones to relax your mind.", "Tranquil and balanced energy."),
    "birthday": ("🎂 Celebration mode!", "A playful palette for happy moments."),
    "happy_birthday": ("🎉 Happy birthday vibes!", "Colorful and full of life."),
    "sad_birthday": ("💔 Gentle birthday tones.", "A soft comfort palette for the heart."),
    "wedding": ("💍 Elegant wedding hues.", "Pure, timeless, and graceful."),
    "happy_wedding": ("💫 Radiant wedding glow!", "Golden ivory shades of love."),
    "sad_wedding": ("🌧 Calm wedding tones.", "Graceful blues for a tender mood."),
    "excited": ("🎊 Let's dance!", "Vibrant energy and neon charm."),
    "disappointed": ("🌙 Quiet celebration.", "Muted lights and peaceful hues."),
    "romantic": ("💖 Sweet romantic vibes.", "Soft roses and gentle warmth."),
    "focus": ("📘 Study focus mode.", "Cool tones for deep concentration."),
    "aesthetic": ("🔮Aesthetic mode on.", "Dusty purples and balanced hues."),
    "dark": ("🖤 Moody elegance.", "Deep, mysterious contrasts."),
    "light": ("🤍 Soft minimal glow.", "Pastel and pure harmony."),

}

predefined_themes = {
    "happy_birthday": [
        ["#FF9CEE", "#B5EAD7", "#C7CEEA", "#FFDAC1", "#E2F0CB"],
        ["#FFD6E0", "#E7C6FF", "#B8E0D2", "#FFB6B9", "#FAE3D9"],
        ["#FFB5E8", "#FF9CEE", "#B28DFF", "#B5EAD7", "#FFDAC1"],
        ["#FFC1CC", "#FFF5E1", "#FFDAE9", "#C8E7FF", "#E2F0CB"],
    ],
    "happy_wedding": [
        ["#FDF5E6", "#E6D5B8", "#B6A28E", "#D4C2B0", "#F1E8E6"],
        ["#FAF3F3", "#E1CEB5", "#C7B198", "#A68B75", "#EFE5DC"],
        ["#FFF0E5", "#FFE8D6", "#E8D5C4", "#D0B8A8", "#F7EDE2"],
        ["#F7E7CE", "#E8C5D8", "#FDECEF", "#FFF7F0", "#D6E5FA"],
        ["#F2F0EB", "#E3E8D8", "#C9D6C5", "#A8B8A5", "#8FA391"],
        ["#F6F4F0", "#EDE7DD", "#DCCFC3", "#C0B2A0", "#A68D7C"],
        ["#FFF0E5", "#F8E5D0", "#E6D2BE", "#D1B8A1", "#C7A27A"],
        ["#FFC1CC", "#FFDDE2", "#E4BAD4", "#C4A69F", "#F6E3D4"],
        ["#E29578", "#FFDDD2", "#FFB5A7", "#FEC5BB", "#FCD5CE"],
        ["#FDECEC", "#F7CACA", "#E8A8A8", "#D98888", "#C46A6A"],
        ["#FFE5EC", "#FFC2D1", "#FFB3C6", "#FF8FAB", "#FB6F92"],
        ["#FAD4D4", "#EFA7A7", "#E26D6D", "#C84747", "#A83232"],
    ],

    "excited": [
        ["#FF00C8", "#7A00FF", "#00FFE0", "#FFF600", "#FF006E"],
        ["#FFB5E8", "#FF9CEE", "#B28DFF", "#B5EAD7", "#FFDAC1"],
        ["#FCE77D", "#F96167", "#F9C5D5", "#6DC5D1", "#41B3A3"],
        ["#FEC8D8", "#F9F1F0", "#D8E2DC", "#FFE5D9", "#FFCAD4"],
        ["#FFD93D", "#FF6F91", "#FF9671", "#FFC75F", "#F9F871"],
        ["#FFE082", "#FFAB91", "#F48FB1", "#81D4FA", "#A5D6A7"],
    ],
    "romantic": [
        ["#FFC1CC", "#FFDDE2", "#E4BAD4", "#C4A69F", "#F6E3D4"],
        ["#E29578", "#FFDDD2", "#FFB5A7", "#FEC5BB", "#FCD5CE"],
        ["#FDECEC", "#F7CACA", "#E8A8A8", "#D98888", "#C46A6A"],
        ["#FFE5EC", "#FFC2D1", "#FFB3C6", "#FF8FAB", "#FB6F92"],
        ["#FAD4D4", "#EFA7A7", "#E26D6D", "#C84747", "#A83232"],
    ]
}


def generate_palette(mood_type):
    if mood_type in predefined_themes:
        return random.choice(predefined_themes[mood_type])
    if mood_type not in mood_palettes:
        mood_type="calm"
    base_hue,base_sat,base_val=mood_palettes[mood_type]
    colors=[]

    for i in range(5):
        hue=(base_hue+random.uniform(-20,20))%360
        sat=min(1,max(0,base_sat+random.uniform(-0.2,0.2)))
        val=min(1,max(0,base_val+random.uniform(-0.2,0.2)))

        rgb=colorsys.hsv_to_rgb(hue/360,sat,val)
        hex_color="#{:02x}{:02x}{:02x}".format(int(rgb[0]*255),int(rgb[1]*255),int(rgb[2]*255))
        colors.append(hex_color)
    random.shuffle(colors)
    return colors

def display_palette(colors,title="Your Palette"):
    fig,ax=plt.subplots(figsize=(12,3))
    ax.set_aspect("equal")
    plt.axis("off")
    plt.title(title,fontsize=17,fontweight="bold",pad=20,color="#442")
    
    card_width=1
    card_space=0.25
    start_x=0.5

    for i,color in enumerate(colors):
        x=start_x+i*(card_width+card_space)
        rect=patches.FancyBboxPatch(
            (x,0),
            card_width,
            1.6,
            boxstyle="round,pad=0.07,rounding_size=0.15",
            linewidth=2,
            facecolor=color,
            edgecolor="white"
        )
        ax.add_patch(rect)
        plt.text(
            x+card_width/2,
            -0.25,
            color.upper(),
            fontsize=9,
            ha="center",
            color="#442"
        )

    plt.xlim(0,start_x+len(colors)*(card_width+card_space)+0.5)
    plt.ylim(-0.5,2)

    plt.savefig("generated_palette.png",dpi=300)
    plt.show()


if __name__ == "__main__":
    print("WELCOME TO MOOD PALETTE GENERATOR")
    mood_input = input("Enter your current mood or theme: ")

    text = preprocess(mood_input)
    mood_type = detect_mood_vader(text)
    palette=generate_palette(mood_type)

    print(f"\nDetected mood: {mood_type}")
    print(f"Colors:{palette}")

    emoji,message=mood_messages.get(mood_type,("🎨", "A lovely color mood just for you."))
    print(f"\n{emoji} {message}\n")

    display_palette(palette,f"Palette for: {mood_type}")