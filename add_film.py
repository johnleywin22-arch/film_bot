"""
Bu skript orqali bazaga film qo'shishingiz mumkin.
Foydalanish: python add_film.py

Eslatma: file_id ni olish uchun botga video yuboring va
/getid buyrug'ini ishlatgan holda yoki botga video
yuborganingizda file_id ni konsolda ko'rishingiz mumkin.
"""

from database import create_table, add_film, get_all_films, delete_film

def main():
    create_table()
    print("=" * 40)
    print("   Film Boshqaruv Paneli")
    print("=" * 40)

    while True:
        print("\n1. Film qo'shish")
        print("2. Barcha filmlarni ko'rish")
        print("3. Film o'chirish")
        print("4. Chiqish")
        choice = input("\nTanlang (1-4): ").strip()

        if choice == "1":
            code = input("Film kodi (masalan F001): ").strip().upper()
            title = input("Film nomi: ").strip()
            file_id = input("Telegram file_id: ").strip()
            description = input("Tavsif (bo'sh qoldirish mumkin): ").strip()

            success = add_film(code, title, file_id, description)
            if success:
                print(f"✅ '{title}' ({code}) muvaffaqiyatli qo'shildi!")
            else:
                print(f"❌ '{code}' kodi allaqachon mavjud!")

        elif choice == "2":
            films = get_all_films()
            if films:
                print(f"\n{'Kod':<10} {'Nomi':<30} {'Tavsif'}")
                print("-" * 60)
                for film in films:
                    print(f"{film['code']:<10} {film['title']:<30} {film['description'] or '-'}")
            else:
                print("Bazada film yo'q.")

        elif choice == "3":
            code = input("O'chirmoqchi bo'lgan film kodi: ").strip().upper()
            success = delete_film(code)
            if success:
                print(f"✅ '{code}' o'chirildi!")
            else:
                print(f"❌ '{code}' topilmadi.")

        elif choice == "4":
            print("Chiqildi.")
            break
        else:
            print("Noto'g'ri tanlov.")

if __name__ == "__main__":
    main()
