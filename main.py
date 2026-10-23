import csv
from datetime import date, datetime
import json


def muat_profil():
    try:
        with open("profil.json", "r") as dataProfil:
            return json.load(dataProfil)
    except FileNotFoundError:
        return None


def simpan_profil(profil):
    with open("profil.json", "w") as dataProfil:
        json.dump(profil, dataProfil, indent=2)


def buat_profil_baru():
    profil_lama = muat_profil()

    if profil_lama is not None:
        print("Data Profil Anda Saat Ini:")
        print(f"- Gender    : {profil_lama['gender']}")
        print(f"- Umur      : {profil_lama['umur']} tahun")
        print(f"- Berat     : {profil_lama['berat']} kg")
        print(f"- Tinggi    : {profil_lama['tinggi']} cm")
        print(f"- Aktivitas : {profil_lama['aktivitas']}")
        print(f"- Tujuan    : {profil_lama['tujuan']}")
        print("---------------------------------")
        print("Masukkan data baru di bawah ini:")

    while True:
        gender = input("Gender (pria / wanita): ").strip().lower()
        if gender in ["pria", "wanita"]:
            break
        print('Ketik "pria" atau "wanita" yaah')

    while True:
        try:
            umur = int(input("Umur (10 - 100 tahun): "))
            if 10 <= umur <= 100:
                break
            print("Umur tidak valid! Masukkan antara 10 sampai 100 tahun")
        except ValueError:
            print("Umur harus berupa angka bulat!")

    while True:
        try:
            berat = float(input("Berat badan (20 - 300 kg): ").replace(",", "."))
            if 20 <= berat <= 300:
                break
            print("Berat badan harus antara 20 sampai 300 kg.")
        except ValueError:
            print("Berat badan harus berupa angka!")

    while True:
        try:
            tinggi = float(input("Tinggi badan (100 - 250 cm): ").replace(",", "."))
            if 100 <= tinggi <= 250:
                break
            print("Tinggi badan harus antara 100 sampai 250 cm.")
        except ValueError:
            print("Tinggi badan harus berupa angka!")

    print("\nBagaimana aktivitas keseharianmu?")
    print("1. Sangat ringan")
    print("2. Ringan")
    print("3. Sedang")
    print("4. Berat")
    print("5. Sangat berat")

    while True:
        aktivitas = input("Pilih jenis aktivitas (1-5): ").strip()
        if aktivitas in ["1", "2", "3", "4", "5"]:
            break
        print("Pilih aktivitasmu dengan memilih antara 1-5!")

    while True:
        tujuan = (
            input("Tujuan terhadap kalorimu apa? (turun/tetap/naik): ").strip().lower()
        )
        if tujuan in ["turun", "tetap", "naik"]:
            break
        print("Ketik turun/tetap/naik!")

    profil = {
        "gender": gender,
        "umur": umur,
        "berat": berat,
        "tinggi": tinggi,
        "aktivitas": aktivitas,
        "tujuan": tujuan,
    }

    simpan_profil(profil)
    print("Profil berhasil tersimpan")
    return profil


def baca_makanan_csv():
    daftar = []
    try:
        with open(
            "makanan.csv", "r", encoding="utf-8", newline=""
        ) as dataMakananMinuman:
            data_makanan_minuman = csv.DictReader(dataMakananMinuman)
            for baris in data_makanan_minuman:
                daftar.append(
                    {
                        "nama": baris["nama"].strip(),
                        "kategori": baris["kategori"].strip(),
                        "porsi": baris["porsi"].strip(),
                        "gram": baris["gram_perporsi"],
                        "kalori": float(baris["kcal_perporsi"]),
                    }
                )
    except FileNotFoundError:
        pass
    return daftar


def hitung_bmr(gender, berat, tinggi, umur):
    if gender == "pria":
        return (10 * berat) + (6.25 * tinggi) - (5 * umur) + 5.0
    else:
        return (10 * berat) + (6.25 * tinggi) - (5 * umur) - 161.0


def hitung_target(profil):
    bmr = hitung_bmr(
        profil["gender"], profil["berat"], profil["tinggi"], profil["umur"]
    )

    if profil["aktivitas"] == "sangat_ringan":
        tdee = bmr * 1.2
    elif profil["aktivitas"] == "ringan":
        tdee = bmr * 1.375
    elif profil["aktivitas"] == "sedang":
        tdee = bmr * 1.55
    elif profil["aktivitas"] == "berat":
        tdee = bmr * 1.725
    else:
        tdee = bmr * 1.9

    if profil["tujuan"] == "turun":
        target = tdee - 500
    elif profil["tujuan"] == "naik":
        target = tdee + 500
    else:
        target = tdee

    if target < bmr:
        target = bmr

    return round(target)


def muat_catatan():
    try:
        with open("catatan.json", "r") as dataCatatan:
            return json.load(dataCatatan)
    except FileNotFoundError:
        return {}


def kategori_rekomendasi(item):
    kategori = item["kategori"].strip().lower()

    if kategori == "minuman":
        return "Minuman"
    if kategori in {"camilan", "jajanan"}:
        return "Junk food"
    if kategori in {"makanan pokok", "lauk hewani", "lauk nabati", "sayur", "buah"}:
        return "Makanan sehat"
    return "Lainnya"


def atur_urutan_rekomendasi(data_makanan):
    return data_makanan["selisih"], data_makanan["nama"].lower()


def cari_makanan(katakunci, daftar_makanan):
    katakunci = katakunci.strip().lower()
    hasil = []
    for data in daftar_makanan:
        if katakunci in data["nama"].lower():
            hasil.append(data)
    return hasil


def simpan_catatan_baru(nama, porsi, kalori):
    semua_data = muat_catatan()
    hari_ini = str(date.today())
    jam_sekarang = datetime.now().strftime("%H:%M")

    if hari_ini not in semua_data:
        semua_data[hari_ini] = []

    catatan_baru = {
        "nama": nama,
        "porsi": porsi,
        "kalori": kalori,
        "jam": jam_sekarang,
    }

    semua_data[hari_ini].append(catatan_baru)

    with open("catatan.json", "w") as f:
        json.dump(semua_data, f, indent=2)


def hapus_catatan_hari_ini(indeks):
    semua_data = muat_catatan()
    hari_ini = str(date.today())
    catatan_hari_ini = semua_data.get(hari_ini, [])
    if indeks < 0 or indeks >= len(catatan_hari_ini):
        return False

    catatan_hari_ini.pop(indeks)
    if catatan_hari_ini:
        semua_data[hari_ini] = catatan_hari_ini
    else:
        del semua_data[hari_ini]

    with open("catatan.json", "w") as dataCatatan:
        json.dump(semua_data, dataCatatan, indent=2)
    return True


def main():
    print("==== KALKULATOR KALORI =====")

    profil = muat_profil()
    if profil is None:
        print("Belum ada profil.. Silahkan membuat terlebih dahulu!")
        profil = buat_profil_baru()

    daftar_makanan = baca_makanan_csv()

    while True:
        target = hitung_target(profil)

        semua_data = muat_catatan()
        hari_ini = str(date.today())
        catatan_hari_ini = semua_data.get(hari_ini, [])

        total_kalori = 0
        for data in catatan_hari_ini:
            total_kalori = total_kalori + data["kalori"]

        print("\n----------------------------------")
        print(f"Tanggal  : {date.today().strftime('%d-%m-%Y')}")
        print(f"Target   : {target} kkal")
        print(f"Tercatat : {total_kalori} kkal")
        print("----------------------------------")
        print("1. Catat Makanan")
        print("2. Lihat Catatan Hari Ini")
        print("3. Cek Kecukupan Kalori")
        print("4. Hapus Catatan Hari Ini")
        print("5. Ubah Data Profil")
        print("0. Keluar")

        pilihan = input("Pilih menu (0-5): ").strip()

        if pilihan == "1":
            print("\n--- CATAT MAKANAN ---")
            cari = input("Cari nama makanan: ").strip()
            hasil = cari_makanan(cari, daftar_makanan)

            item_terpilih = None
            kalori_final = 0
            porsi_final = 1.0

            if hasil:
                print("\nHasil Pencarian:")
                i = 1
                for data in hasil:
                    print(
                        f"{i}. {data['nama']} ({data['gram']}g / {data['porsi']}) - {data['kalori']} kkal"
                    )
                    i = i + 1

                try:
                    pilih_no = int(input("Pilih makanan/minuman no: "))
                    if pilih_no > 0:
                        indeks = pilih_no - 1
                        if indeks < len(hasil):
                            pilih_makanan = hasil[indeks]
                            try:
                                porsi_final = float(
                                    input(
                                        "Jumlah porsi (1 atau 0.5 atau berapapun): "
                                    ).replace(",", ".")
                                )
                            except ValueError:
                                porsi_final = 1.0

                            kalori_final = pilih_makanan["kalori"] * porsi_final
                            item_terpilih = pilih_makanan["nama"]
                except ValueError:
                    print("Nomor tidak valid.")

            if item_terpilih is None:
                print("\nInput Manual Kalori:")
                item_terpilih = input("Nama makanan/minuman: ").strip()
                try:
                    kalori_final = float(
                        input("Total kalori (kkal): ").replace(",", ".")
                    )
                except ValueError:
                    print("Kalori tidak valid! Batal dicatat.")
                    continue

            if item_terpilih and kalori_final > 0:
                simpan_catatan_baru(item_terpilih, porsi_final, kalori_final)
                print(f"Berhasil mencatat: {item_terpilih} ({kalori_final} kkal)")

        elif pilihan == "2":
            print("\n--- CATATAN HARI INI ---")
            if not catatan_hari_ini:
                print("Belum ada catatan hari ini")
            else:
                print("Jam   Nama Makanan            Porsi    Kalori")
                for data in catatan_hari_ini:
                    print(
                        f"{data['jam']}   {data['nama']} ({data['porsi']} porsi) = {data['kalori']} kkal"
                    )
                print(f"\nTotal: {total_kalori} kkal")

        elif pilihan == "3":
            print("\n--- CEK KECUKUPAN ---")
            sisa = target - total_kalori
            print(f"Target : {target} kkal")
            print(f"Masuk  : {total_kalori} kkal")
            if sisa <= 0:
                print(f"Status : CUKUP (Kelebihan {-sisa} kkal)")
            else:
                print(f"Status : BELUM CUKUP (Sisa kurang {sisa} kkal)")

            if daftar_makanan:
                print("\nPilih kategori rekomendasi:")
                print("1. Makanan sehat")
                print("2. Junk food")
                print("3. Minuman")
                print("4. Makanan lainnya")
                print("5. Semua kategori")
                pilihan_kategori = input("Pilih kategori (1-5): ").strip()

                if pilihan_kategori not in ("1", "2", "3", "4", "5"):
                    print("Pilihan kategori tidak valid.")
                    continue

                kategori_dipilih = {
                    "1": "Makanan sehat",
                    "2": "Junk food",
                    "3": "Minuman",
                    "4": "Lainnya",
                    "5": None,
                }.get(pilihan_kategori)

                print("\nRekomendasi yang muat di sisa kalorimu:")
                cocok = []
                for m in daftar_makanan:
                    kategori_item = kategori_rekomendasi(m)
                    if m["kalori"] <= sisa + 50 and (
                        kategori_dipilih is None or kategori_item == kategori_dipilih
                    ):
                        item_baru = {
                            "nama": m["nama"],
                            "kategori": kategori_item,
                            "kategori_asli": m["kategori"],
                            "porsi": m["porsi"],
                            "kalori": m["kalori"],
                            "selisih": abs(sisa - m["kalori"]),
                        }
                        cocok.append(item_baru)

                cocok.sort(key=atur_urutan_rekomendasi)

                if not cocok:
                    print(
                        "Belum ada rekomendasi pada kategori ini yang sesuai sisa kalori."
                    )
                else:
                    i = 0
                    for r in cocok:
                        if i < 3:
                            print(
                                f"- {r['nama']} [{r['kategori']} / {r['kategori_asli']}] "
                                f"({r['porsi']}) = {r['kalori']} kkal"
                            )
                            i = i + 1
                        else:
                            break

        elif pilihan == "4":
            print("\n--- HAPUS CATATAN ---")
            if not catatan_hari_ini:
                print("Tidak ada catatan hari ini untuk dihapus.")
            else:
                i = 1
                for c in catatan_hari_ini:
                    print(f"{i}. {c['jam']} - {c['nama']} ({c['kalori']} kkal)")
                    i = i + 1

                try:
                    n = int(input("Nomor yang mau dihapus (0 batal): "))
                    if n > 0 and hapus_catatan_hari_ini(n - 1):
                        print("Catatan berhasil dihapus!")
                    else:
                        print("Dibatalkan atau nomor salah")
                except ValueError:
                    print("Masukkan angka yang benar!")

        elif pilihan == "5":
            profil = buat_profil_baru()

        elif pilihan == "0":
            print("Program berhenti")
            break
        else:
            print("Pilihan menu tidak valid, masukkan angka 0 sampai 5!")


if __name__ == "__main__":
    main()
