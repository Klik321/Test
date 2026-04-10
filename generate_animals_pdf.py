#!/usr/bin/env python3
"""Generate Hebrew PDF: Top 10 Rarest Animals on Earth."""

import base64
from PIL import Image, ImageDraw
from io import BytesIO
from weasyprint import HTML

ANIMALS = [
    {
        "rank": 1,
        "name": "וואקיטה",
        "latin": "Vaquita (Phocoena sinus)",
        "count": "כ-10 פרטים בלבד",
        "color": "#1a1a2e",
        "accent": "#e94560",
        "description": (
            "וואקיטה היא חיית הים הנדירה ביותר בעולם — דולפינון זעיר שחי אך ורק "
            "במפרץ קליפורניה שבמקסיקו. אורכה כ-1.5 מטר בלבד והיא מוכרת בזכות "
            "הכתמים הכהים סביב העיניים והפה. הסיבה המרכזית להכחדתה היא דיג בלתי "
            "חוקי ברשתות זימים, שבהן היא נלכדת בטעות. למרות מאמצי שימור בינלאומיים, "
            "מספר הפרטים ממשיך לרדת בקצב מדאיג."
        ),
        "silhouette": "dolphin",
    },
    {
        "rank": 2,
        "name": "צב רך ענק של הינגצה",
        "latin": "Yangtze Giant Softshell Turtle (Rafetus swinhoei)",
        "count": "כ-3 פרטים ידועים",
        "color": "#16213e",
        "accent": "#0f3460",
        "description": (
            "צב הינגצה הענק הוא צב המים המתוקים הגדול ביותר בעולם, במשקל של עד "
            "100 ק\"ג. מינו נמצא על סף הכחדה מוחלטת — נותרו רק מספר בודד של פרטים "
            "בטבע ובשבי. בית גידולו ההיסטורי היה בנהרות ובאגמים של סין ווייטנאם. "
            "ציד, זיהום מים ואובדן בתי גידול הביאו אותו למצבו הנוכחי. ניסיונות רבייה "
            "מלאכותית טרם צלחו."
        ),
        "silhouette": "turtle",
    },
    {
        "rank": 3,
        "name": "קרנף ג'אווה",
        "latin": "Javan Rhinoceros (Rhinoceros sondaicus)",
        "count": "כ-72 פרטים",
        "color": "#1b262c",
        "accent": "#3282b8",
        "description": (
            "קרנף ג'אווה הוא אחד מיונקי היבשה הנדירים ביותר על פני כדור הארץ. "
            "כל הפרטים הנותרים חיים באזור מוגן אחד בלבד — הפארק הלאומי אוג'ונג קולון "
            "שבאינדונזיה. בעבר הוא התפרס ברחבי דרום-מזרח אסיה, אך ציד בלתי חוקי "
            "לצורך קרנו (המשמשת ברפואה מסורתית) וכריתת יערות צמצמו את אוכלוסייתו "
            "באופן קטסטרופלי."
        ),
        "silhouette": "rhino",
    },
    {
        "rank": 4,
        "name": "קרנף סומטרה",
        "latin": "Sumatran Rhinoceros (Dicerorhinus sumatrensis)",
        "count": "כ-80 פרטים",
        "color": "#2c3333",
        "accent": "#395B64",
        "description": (
            "קרנף סומטרה הוא הקרנף הקטן ביותר והיחיד בעל שתי קרניים באסיה. גופו "
            "מכוסה שיער חום-אדמדם, מה שמבדיל אותו משאר הקרנפים. הוא חי ביערות "
            "הגשם הטרופיים של סומטרה ובורנאו. אובדן בתי גידול, ציד וקושי ברבייה "
            "בשבי הפכו את שימורו לאתגר עצום. תוכניות רבייה מלאכותיות פועלות "
            "באינדונזיה בניסיון להציל את המין."
        ),
        "silhouette": "rhino",
    },
    {
        "rank": 5,
        "name": "נמר אמור",
        "latin": "Amur Leopard (Panthera pardus orientalis)",
        "count": "כ-100 פרטים",
        "color": "#2b2d42",
        "accent": "#8d99ae",
        "description": (
            "נמר אמור הוא תת-מין של הנמר המצוי, החי באזור הגבול בין רוסיה לסין. "
            "הוא מותאם לחיים בתנאי קור קיצוניים, עם פרווה עבה וארוכה במיוחד. "
            "ציד פרוות, אובדן בתי גידול ומחלות צמצמו את אוכלוסייתו עד לסף הכחדה. "
            "בזכות מאמצי שימור אינטנסיביים ברוסיה, מספר הפרטים בטבע עלה לאחרונה "
            "מכ-30 לכ-100, אך הוא עדיין בסכנת הכחדה חמורה."
        ),
        "silhouette": "leopard",
    },
    {
        "rank": 6,
        "name": "סאולה",
        "latin": "Saola (Pseudoryx nghetinhensis)",
        "count": "לא ידוע — עשרות בודדות",
        "color": "#3c1642",
        "accent": "#7b2d8e",
        "description": (
            "הסאולה, המכונה גם \"חד-קרן אסיה\", התגלתה לראשונה רק בשנת 1992 "
            "ביערות האנאם שבווייטנאם. היא אחת מגילויי היונקים הגדולים המשמעותיים "
            "ביותר של המאה ה-20. עם קרניים ארוכות וישרות ופנים ייחודיות, היא מעולם "
            "לא נצפתה בצורה מהימנה בטבע על ידי חוקרים. ציד במלכודות ופגיעה ביערות "
            "מאיימים על קיומה."
        ),
        "silhouette": "antelope",
    },
    {
        "rank": 7,
        "name": "גורילת קרוס ריבר",
        "latin": "Cross River Gorilla (Gorilla gorilla diehli)",
        "count": "כ-300 פרטים",
        "color": "#1e3d59",
        "accent": "#f5f0e1",
        "description": (
            "גורילת קרוס ריבר היא תת-המין הנדיר ביותר של הגורילה, והיא חיה באזור "
            "הגבול בין ניגריה לקמרון. היא ביישנית במיוחד ונמנעת ממגע עם בני אדם, "
            "מה שמקשה על חקירתה. אובדן יערות, ציד וקונפליקטים עם חקלאים מאיימים "
            "על אוכלוסייתה. פרויקטים קהילתיים לשימור יערות באזור מנסים להבטיח "
            "את המשך קיומה."
        ),
        "silhouette": "gorilla",
    },
    {
        "rank": 8,
        "name": "קקאפו",
        "latin": "Kakapo (Strigops habroptilus)",
        "count": "כ-250 פרטים",
        "color": "#004643",
        "accent": "#f9bc60",
        "description": (
            "הקקאפו הוא תוכי לילי שאינו מסוגל לעוף — היחיד מסוגו בעולם. בית גידולו "
            "הטבעי הוא ניו זילנד, שם הוא חי על הקרקע. הכנסת טורפים כמו חתולים "
            "וחולדות על ידי מתיישבים אירופיים כמעט חיסלה את המין. תוכנית שימור "
            "ניו-זילנדית אינטנסיבית, הכוללת ניטור כל פרט בנפרד, הצליחה להעלות "
            "את מספרו בהדרגה."
        ),
        "silhouette": "parrot",
    },
    {
        "rank": 9,
        "name": "אקסולוטל",
        "latin": "Axolotl (Ambystoma mexicanum)",
        "count": "כ-50-1,000 פרטים בטבע",
        "color": "#212529",
        "accent": "#f72585",
        "description": (
            "האקסולוטל הוא דו-חיים מרתק שמקורו באגם סוצ'ימילקו שבמקסיקו סיטי. "
            "הוא ייחודי ביכולתו לחדש איברים שלמים — כולל לב, מוח וגפיים. בטבע הוא "
            "נמצא בסכנת הכחדה חמורה עקב זיהום מים, מינים פולשים ועיור. למרות שהוא "
            "נפוץ מאוד במעבדות מחקר ובחנויות חיות, האוכלוסייה הפראית כמעט נעלמה."
        ),
        "silhouette": "axolotl",
    },
    {
        "rank": 10,
        "name": "קונדור קליפורני",
        "latin": "California Condor (Gymnogyps californianus)",
        "count": "כ-500 פרטים",
        "color": "#353535",
        "accent": "#d4a373",
        "description": (
            "הקונדור הקליפורני הוא ציפור הדורסים הגדולה ביותר בצפון אמריקה, עם מוטת "
            "כנפיים של עד 3 מטרים. בשנות ה-80 נותרו רק 22 פרטים, והמין הוכרז ככחוד "
            "בטבע. תוכנית רבייה בשבי שאפתנית הצליחה להגדיל את מספרם לכ-500. "
            "הרעלת עופרת מכדורי ציד נותרה האיום המרכזי עליו כיום. סיפור השימור שלו "
            "נחשב לאחד ההצלחות הגדולות בתחום."
        ),
        "silhouette": "condor",
    },
]


def create_animal_image(animal, width=400, height=260):
    """Create a stylized placeholder image for each animal."""
    img = Image.new("RGB", (width, height), animal["accent"])
    draw = ImageDraw.Draw(img)

    # Decorative circle in center
    cx, cy = width // 2, height // 2
    r = 80
    draw.ellipse(
        [cx - r, cy - r, cx + r, cy + r],
        fill=animal["color"],
        outline="#ffffff",
        width=3,
    )

    # Rank number in circle
    try:
        from PIL import ImageFont
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except Exception:
        font = ImageFont.load_default()

    rank_text = f"#{animal['rank']}"
    bbox = draw.textbbox((0, 0), rank_text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 5), rank_text, fill="#ffffff", font=font)

    # Latin name at bottom
    try:
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except Exception:
        small_font = ImageFont.load_default()

    latin = animal["latin"].split("(")[0].strip()
    bbox2 = draw.textbbox((0, 0), latin, font=small_font)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((cx - tw2 // 2, height - 35), latin, fill="#ffffff", font=small_font)

    # Corner decorations
    for corner in [(0, 0, 30, 30), (width-30, 0, width, 30),
                   (0, height-30, 30, height), (width-30, height-30, width, height)]:
        draw.rectangle(corner, fill=animal["color"])

    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def build_html():
    cards = ""
    for animal in ANIMALS:
        img_b64 = create_animal_image(animal)
        cards += f"""
        <div class="animal-card">
            <div class="card-header" style="background: {animal['color']};">
                <span class="rank">{animal['rank']}</span>
                <div class="header-text">
                    <h2>{animal['name']}</h2>
                    <span class="latin">{animal['latin']}</span>
                </div>
            </div>
            <div class="card-body">
                <div class="image-section">
                    <img src="data:image/png;base64,{img_b64}" alt="{animal['name']}" />
                    <div class="count" style="background: {animal['accent']}; color: {animal['color']};">
                        {animal['count']}
                    </div>
                </div>
                <div class="description">
                    <p>{animal['description']}</p>
                </div>
            </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<style>
    @page {{
        size: A4;
        margin: 15mm;
    }}

    body {{
        font-family: 'FreeSans', 'DejaVu Sans', sans-serif;
        direction: rtl;
        font-size: 11pt;
        line-height: 1.7;
        color: #1a1a1a;
        margin: 0;
        padding: 0;
    }}

    .cover {{
        page-break-after: always;
        text-align: center;
        padding-top: 60mm;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: white;
        margin: -15mm;
        padding: 60mm 15mm 15mm 15mm;
        height: 257mm;
        box-sizing: border-box;
    }}

    .cover h1 {{
        font-size: 32pt;
        margin-bottom: 10mm;
        line-height: 1.4;
    }}

    .cover .subtitle {{
        font-size: 16pt;
        opacity: 0.85;
        margin-bottom: 20mm;
    }}

    .cover .divider {{
        width: 60mm;
        height: 2px;
        background: #e94560;
        margin: 10mm auto;
    }}

    .cover .meta {{
        font-size: 11pt;
        opacity: 0.7;
        margin-top: 40mm;
    }}

    .toc {{
        page-break-after: always;
        padding-top: 10mm;
    }}

    .toc h2 {{
        font-size: 22pt;
        color: #1a1a2e;
        border-bottom: 3px solid #e94560;
        padding-bottom: 5mm;
        margin-bottom: 8mm;
    }}

    .toc-item {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 3mm 2mm;
        border-bottom: 1px dashed #ccc;
        font-size: 12pt;
    }}

    .toc-item .toc-rank {{
        display: inline-block;
        width: 8mm;
        height: 8mm;
        line-height: 8mm;
        text-align: center;
        background: #1a1a2e;
        color: white;
        border-radius: 50%;
        font-size: 9pt;
        font-weight: bold;
        margin-left: 3mm;
    }}

    .toc-item .toc-count {{
        font-size: 9pt;
        color: #666;
    }}

    .animal-card {{
        page-break-inside: avoid;
        page-break-after: always;
        border: 1px solid #e0e0e0;
        border-radius: 4mm;
        overflow: hidden;
        margin-bottom: 8mm;
    }}

    .card-header {{
        color: white;
        padding: 6mm 8mm;
        display: flex;
        align-items: center;
        gap: 5mm;
    }}

    .card-header .rank {{
        font-size: 28pt;
        font-weight: bold;
        opacity: 0.5;
        min-width: 15mm;
        text-align: center;
    }}

    .card-header h2 {{
        margin: 0;
        font-size: 20pt;
    }}

    .card-header .latin {{
        font-size: 10pt;
        opacity: 0.75;
        font-style: italic;
        direction: ltr;
        unicode-bidi: isolate;
    }}

    .card-body {{
        padding: 6mm 8mm;
    }}

    .image-section {{
        text-align: center;
        margin-bottom: 5mm;
    }}

    .image-section img {{
        max-width: 100%;
        height: auto;
        border-radius: 3mm;
    }}

    .count {{
        display: inline-block;
        padding: 2mm 6mm;
        border-radius: 3mm;
        font-size: 12pt;
        font-weight: bold;
        margin-top: 3mm;
    }}

    .description {{
        font-size: 12pt;
        line-height: 1.9;
        text-align: justify;
    }}

    .footer-page {{
        page-break-before: always;
        text-align: center;
        padding-top: 80mm;
        color: #555;
    }}

    .footer-page h2 {{
        font-size: 20pt;
        color: #1a1a2e;
        margin-bottom: 10mm;
    }}

    .footer-page p {{
        font-size: 11pt;
        line-height: 2;
    }}
</style>
</head>
<body>

<div class="cover">
    <h1>10 החיות הנדירות ביותר<br>בכדור הארץ</h1>
    <div class="divider"></div>
    <div class="subtitle">מדריך מאויר — מהנדירה ביותר ועד הפחות נדירה</div>
    <div class="meta">2026 | נתונים עדכניים מארגוני שימור בינלאומיים</div>
</div>

<div class="toc">
    <h2>תוכן עניינים</h2>
    {"".join(f'''
    <div class="toc-item">
        <div>
            <span class="toc-rank">{a['rank']}</span>
            {a['name']}
            <span style="font-style:italic; font-size:9pt; color:#888; direction:ltr; unicode-bidi:isolate;"> — {a['latin'].split('(')[0].strip()}</span>
        </div>
        <div class="toc-count">{a['count']}</div>
    </div>''' for a in ANIMALS)}
</div>

{cards}

<div class="footer-page">
    <h2>על השימור</h2>
    <p>
        כל החיות ברשימה זו נמצאות בסכנת הכחדה חמורה.<br>
        שימור מגוון ביולוגי הוא אחריות משותפת לכולנו.<br>
        ניתן לתרום לארגונים כמו WWF, IUCN ושמורות טבע מקומיות.<br><br>
        <strong>כל יצור חי הוא עולם ומלואו.</strong>
    </p>
</div>

</body>
</html>"""


if __name__ == "__main__":
    html = build_html()
    output = "top10_rarest_animals_he.pdf"
    HTML(string=html).write_pdf(output)
    print(f"PDF created: {output}")
