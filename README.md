# 🎬 Film Bot — O'rnatish va Ishlatish

## Fayllar tuzilmasi
```
film_bot/
├── bot.py           # Asosiy bot kodi
├── database.py      # SQLite ma'lumot bazasi
├── add_film.py      # Film qo'shish uchun skript
├── requirements.txt # Kerakli kutubxonalar
└── films.db         # Avtomatik yaratiladi
```

---

## 1. O'rnatish

```bash
pip install -r requirements.txt
```

---

## 2. Botni sozlash

`bot.py` faylini oching va quyidagilarni o'zgartiring:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"   # @BotFather dan olingan token
ADMIN_IDS = [123456789]             # Sizning Telegram ID raqamingiz
```

### Token olish:
1. Telegramda **@BotFather** ga yozing
2. `/newbot` buyrug'ini yuboring
3. Bot nomi va username bering
4. Token nusxalang

### Telegram ID olish:
- **@userinfobot** ga `/start` yuboring — u sizning ID raqamingizni ko'rsatadi

---

## 3. Botni ishga tushirish

```bash
python bot.py
```

---

## 4. Film qo'shish

### Usul 1 — Bot orqali (tavsiya etiladi)
1. Botga `/add` yuboring
2. Kod kiriting (masalan: `F001`)
3. Film nomini kiriting
4. Video faylni yuboring
5. Tavsif kiriting (ixtiyoriy)

### Usul 2 — Terminal orqali
```bash
python add_film.py
```

---

## 5. Foydalanuvchi uchun buyruqlar

| Buyruq | Ta'rif |
|--------|--------|
| Film kodi (masalan `F001`) | Filmni olish |
| `/start` | Botni ishga tushirish |
| `/help` | Yordam |

## 6. Admin buyruqlari

| Buyruq | Ta'rif |
|--------|--------|
| `/add` | Yangi film qo'shish |
| `/delete` | Film o'chirish |
| `/list` | Barcha filmlar ro'yxati |
| `/stats` | Statistika |

---

## 7. Izohlar

- Film kodlari **katta harfga** avtomatik o'giriladi (`f001` → `F001`)
- Filmlar Telegram serverida saqlanadi (`file_id` orqali)
- SQLite bazasi `films.db` faylida saqlanadi
