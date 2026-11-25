# מחולל דו״ח חברתי – התחדשות עירונית

כלי עזר (לא רשמי) לכתיבת דו״ח חברתי לפי מדריך 3.0 של הרשות הממשלתית להתחדשות עירונית.
אתר חי: https://romangash-star.github.io/social-report/ (GitHub Pages, ענף main, שורש המאגר).

## מצב נוכחי
- `index.html` בתיקייה הזו הוא **גרסה 3.1** – עדיין לא נדחף. באתר החי רצה גרסה 3.0.
- המשימה הראשונה: `git add index.html && git commit && git push origin main`, לחכות דקה ל-Pages, ולהריץ בדיקה חיה (ראו למטה).

## ארכיטקטורה
- קובץ יחיד `index.html`: CSS + JS inline, בלי build. ספריות: Leaflet 1.9.4 (cdnjs), גופן Rubik.
- מצב: אובייקט `S` (ראו `blank()`), נשמר ב-localStorage (`srb3_index`, `srb3_p_<id>`). אין שרת.
- 14 שלבים ב-`STEPS`; כל שלב הוא `VIEWS.<id>()` שמחזיר HTML; `go(id)` מרנדר. שדות נקשרים ב-`data-p="path.in.S"`.
- `buildReport(type)` מפיק 3 תוצרים: מצב קיים / הערכת חלופות / מלא. חוסרים מסומנים `[להשלמה]`. `CHECKS` = רשימת השלמות.
- `autoFill()` = מילוי אוטומטי; `initPicker()/pickCompound()` = מפת המתחמים בשלב 1.
- עברית RTL בלבד. צבעים: #0C3058, #50B0A0, #206070. לא להשתמש בלוגו הרשות; להשאיר את השורה "כלי עזר עצמאי".

## מקורות נתונים (כולם CORS פתוח, נבדקו 25.11.2026)
- מתחמים מוכרזים (פוליגונים): services6.arcgis.com/I08Ekaykft5ELucH/.../GIS_UrbanRenewal/FeatureServer/1 – מעל 1000 רשומות, חובה pagination.
- data.gov.il CKAN datastore: מתחמים `f65a0daf-…` (SemelYeshuv), מפקד 2022 לפי א״ס `9a9e085f-…` (LocalityCode), מוסדות חינוך `2055063b-…` (SEMEL_ISHUV_PNIM, X/Y ב-ITM), גני ילדים `75d2d6a7-…` (SETL_CODE), תחנות `e873e6a2-…` (CityCode), דיור ציבורי (package `diurtziburi`, לפי שם בלבד).
- **לסנן תמיד לפי סמל יישוב** (`filters=`), לא לפי שם עיר – האיות שונה בין מאגרים. לשמות: `normCity()`.
- למ״ס ArcGIS (services2.arcgis.com/xMRYm7cNgdR5RN6F): Statistical__Areas_2022/0, SOEC_Stat11_2021/27.
- מינהל התכנון: ags.iplan.gov.il/.../Xplan/MapServer/1 (קווים כחולים).
- Nominatim (1 בקשה/שנייה), OSRM routed-foot, Overpass (מרוץ בין מראות; overpass-api.de לרוב תקוע).
- לא נגישים מדפדפן: GovMap, API של gov.il/apps/moch.

## בדיקות
- `tests/*.py` – Playwright (להחליף `{ROOT}` בנתיב המלא לתיקייה; דורש Chrome ועותק מקומי של Leaflet ב-pk.py/mob.py).
- בדיקה חיה חובה אחרי כל שינוי ב-autoFill: לבחור מתחם ולהריץ מילוי אוטומטי לפחות ב: חולון "ההסתדרות 197-207", תל אביב, ירושלים, פתח תקווה, ומתחם בלי מספרי בית בשם (למשל חיפה "המלך אמציה").

## פתוחים / רעיונות
- 3.1 לא נבדקה מקצה לקצה באתר החי (רק השאילתות בנפרד + רגרסיה מקומית).
- "הטבלה לניהול מידע חברתי במתחם" מהמדריך – עוד לא נבנתה.
- מחירי שכירות/דירות: אין מקור פתוח אמין; היום הזנה ידנית (נתוני שמאי).
- הכנסות לפי עשירון קבועות בקוד (`INCOME_REF`, למ״ס 2024) – לעדכן שנתית.
- כיוון מוצר בתשלום + דף נחיתה ליועצים חברתיים (בבחינה).
