import flet as ft
import easyocr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
from tkinter import filedialog, Tk

def main(page: ft.Page):
    page.title = "AI Real-time Translator"
    page.window_width = 390
    page.window_height = 844
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def proses_pilih_dan_scan(e):
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        jalur_foto_terpilih = filedialog.askopenfilename(
            title="Pilih Foto yang Mau Di-scan",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
        )
        root.destroy()

        if not jalur_foto_terpilih:
            indikator_status.value = "Pemilihan foto dibatalkan."
            page.update()
            return

        tombol_scan.content.value = "⏳ Sedang Membaca..."
        indikator_status.value = "Mata AI sedang memuat bahasa pilihanmu..."
        page.update()

        # FITUR DINAMIS: Mengambil kode bahasa yang diketik user di kolom input
        # Menghapus spasi dan memecahnya menjadi bentuk list/daftar
        bahasa_user = [lang.strip() for lang in kolom_bahasa.value.split(",")]

        try:
            # AI membaca kamus sesuai yang diketik secara real-time!
            reader = easyocr.Reader(bahasa_user)
        except Exception as err:
            indikator_status.value = "Error: Kombinasi kode bahasa tidak cocok!"
            tombol_scan.content.value = "📸 SCAN PHOTO / SELECT IMAGE"
            page.update()
            return

        if os.path.exists(jalur_foto_terpilih):
            # 1. AI Membaca Gambar
            hasil_ocr = reader.readtext(jalur_foto_terpilih, detail=0)
            teks_asli = " ".join(hasil_ocr)
            
            if not teks_asli.strip():
                indikator_status.value = "AI tidak menemukan teks dalam foto!"
                tombol_scan.content.value = "📸 SCAN PHOTO / SELECT IMAGE"
                page.update()
                return

            # 2. FITUR AUTO: Terjemahkan otomatis dari bahasa apapun ke Indonesia
            tombol_scan.content.value = "🌐 Sedang Menerjemahkan..."
            page.update()
            teks_terjemahan = GoogleTranslator(source='auto', target='id').translate(teks_asli)
            
            # 3. Bikin Suara AI otomatis
            tombol_scan.content.value = "🎙️ Membikin Suara AI..."
            page.update()
            suara_ai = gTTS(text=teks_terjemahan, lang='id', slow=False)
            suara_ai.save("suara_ai.mp3")
            
            # 4. Tampilkan Hasil Final
            hasil_teks.value = teks_terjemahan
            tombol_suara.disabled = False
            indikator_status.value = f"Berhasil scan bahasa [{kolom_bahasa.value}]! Putar suara."
        else:
            indikator_status.value = "Error: File foto tidak ditemukan!"

        tombol_scan.content.value = "📸 SCAN PHOTO / SELECT IMAGE"
        page.update()

    def putar_suara(e):
        os.system("start suara_ai.mp3")

    # --- Komponen Tampilan Utama ---
    
    judul_text = ft.Text("AI Camera Translator", size=24, weight=ft.FontWeight.BOLD, color="blue")
    judul = ft.Container(
        content=judul_text,
        padding=15
    )
    
    # KOMPONEN BARU: Kolom input teks untuk ganti bahasa langsung dari aplikasi
    kolom_bahasa = ft.TextField(
        value="en,ar", # Default awal diset Inggris dan Arab, tinggal hapus/ganti sesuka hati
        label="Kode Bahasa Target (Pisahkan dengan koma)",
        width=330,
        hint_text="Contoh: en,ar atau en,ja atau en,fr,de"
    )
    
    tombol_scan = ft.ElevatedButton(
        content=ft.Text("📸 SCAN PHOTO / SELECT IMAGE", color="white", weight=ft.FontWeight.BOLD),
        bgcolor="blue",
        width=330,
        on_click=proses_pilih_dan_scan
    )
    
    indikator_status = ft.Text("Ketik kode bahasa di atas sebelum menekan tombol scan!", size=11, color="grey")

    tombol_suara = ft.ElevatedButton(
        content=ft.Text("🔊 LISTEN TO AI VOICE", color="white", weight=ft.FontWeight.BOLD),
        bgcolor="green",
        width=330,
        disabled=True, 
        on_click=putar_suara
    )

    hasil_teks = ft.Text(
        value="Hasil terjemahan akan muncul di sini...",
        size=15,
        color="black"
    )

    wadah_teks_estetik = ft.Container(
        content=hasil_teks,
        padding=15,
        bgcolor="#eeeeee"
    )

    area_hasil_scroll = ft.Column(
        [wadah_teks_estetik],
        scroll=ft.ScrollMode.AUTO,
        height=380, # Disesuaikan sedikit biar dapet space buat kolom teks baru
        width=350,
    )

    # Susun tata letak aplikasi
    page.add(
        judul,
        kolom_bahasa, # Dimasukkan ke layar aplikasi
        tombol_scan,
        indikator_status,
        ft.Text(""), 
        tombol_suara, 
        ft.Divider(), 
        area_hasil_scroll 
    )

ft.app(target=main)
