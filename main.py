import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Helper Functions (Tidak Berubah) ---
def setup_driver():
    print("Mencoba memulai browser Chrome...")
    try:
        service = Service()
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        print("Browser berhasil dimulai.")
        return driver
    except Exception as e:
        print(f"Gagal memulai Chrome. Error: {e}")
        return None

# --- Fungsi Handler (Dengan Penambahan Jeda) ---

def handle_text_input(driver, config, data_row):
    """Mengisi field isian singkat atau paragraf."""
    time.sleep(1) # Jeda 1 detik sebelum mengisi
    try:
        if config['mode'] == 'tetap':
            data_to_fill = config['fixed_text']
        else: # Mode dari file
            data_to_fill = data_row[config['data_column']]
        
        print(f"   - Mengisi '{config['name']}': {data_to_fill}")
        input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config['xpath'])))
        input_field.clear()
        input_field.send_keys(data_to_fill)
    except Exception as e:
        print(f"   - GAGAL mengisi '{config['name']}'. Error: {e}")

def handle_multiple_choice(driver, config):
    """Menangani Pilihan Ganda (Radio Button)."""
    time.sleep(1) # Jeda 1 detik sebelum mengisi
    try:
        if config['mode'] == '1': # Mode Tetap
            print(f"   - Memilih Opsi Tetap untuk '{config['name']}'")
            option_to_click = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config['xpath'])))
            option_to_click.click()
        elif config['mode'] == '2': # Mode Acak
            print(f"   - Memilih Opsi Acak untuk '{config['name']}'")
            all_options = driver.find_elements(By.XPATH, config['xpath'])
            if all_options:
                random.choice(all_options).click()
            else:
                print(f"   - GAGAL: Tidak ada opsi yang ditemukan untuk '{config['name']}'")
    except Exception as e:
        print(f"   - GAGAL menangani pilihan ganda '{config['name']}'. Error: {e}")

def handle_checkbox(driver, config):
    """Menangani Kotak Centang (Checkbox)."""
    time.sleep(1) # Jeda 1 detik sebelum mengisi
    try:
        all_checkboxes = driver.find_elements(By.XPATH, config['xpath'])
        if not all_checkboxes:
            print(f"   - GAGAL: Tidak ada checkbox yang ditemukan untuk '{config['name']}'")
            return

        if config['mode'] == '1': # Mode Tetap
            print(f"   - Memilih Opsi Tetap {config['options_to_select']} untuk '{config['name']}'")
            for checkbox in all_checkboxes:
                try:
                    label = checkbox.find_element(By.XPATH, ".//ancestor::div[contains(@class, 'exportLabel')]").text
                    if label in config['options_to_select']:
                        checkbox.click()
                except:
                    # Fallback jika struktur label berbeda
                    pass
        elif config['mode'] == '2': # Mode Acak
            print(f"   - Memilih Opsi Acak untuk '{config['name']}'")
            num_to_select = random.randint(1, len(all_checkboxes))
            selected_checkboxes = random.sample(all_checkboxes, num_to_select)
            for checkbox in selected_checkboxes:
                checkbox.click()
    except Exception as e:
        print(f"   - GAGAL menangani checkbox '{config['name']}'. Error: {e}")

def handle_dropdown(driver, config):
    """Menangani Dropdown."""
    time.sleep(1) # Jeda 1 detik sebelum mengisi
    try:
        print(f"   - Menangani Dropdown '{config['name']}'")
        dropdown_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config['xpath_main'])))
        dropdown_button.click()
        time.sleep(1)

        if config['mode'] == '1': # Mode Tetap
            print(f"   - Memilih Opsi Tetap dari dropdown")
            option_to_click = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config['xpath_option'])))
            option_to_click.click()
        elif config['mode'] == '2': # Mode Acak
            print(f"   - Memilih Opsi Acak dari dropdown")
            all_options = driver.find_elements(By.XPATH, "//div[@role='option' and not(@aria-disabled='true')]")
            if all_options:
                random.choice(all_options).click()
            else:
                print(f"   - GAGAL: Tidak ada opsi ditemukan di dropdown '{config['name']}'")
    except Exception as e:
        print(f"   - GAGAL menangani dropdown '{config['name']}'. Error: {e}")

def main():
    print("=============================================")
    print("   Auto Form Filler v6.0 - Multi-Halaman    ")
    print("=============================================\n")
    
    form_url = input("➡️  Masukkan link Google Form yang akan diisi: \n")
    pages = []
    data_files = {}
    page_number = 1

    # --- Konfigurasi Per Halaman ---
    while True:
        print(f"\n{'='*10} Mengkonfigurasi Halaman {page_number} {'='*10}")
        elements_on_page = []
        while True:
            print("\nPilih tipe elemen untuk Halaman ini:")
            print("1. Isian Singkat / Paragraf")
            print("2. Pilihan Ganda (Pilih Satu)")
            print("3. Kotak Centang (Pilih Banyak)")
            print("4. Dropdown")
            print("0. Selesai untuk Halaman ini")
            
            choice = input("Pilihan Anda (angka): ")
            element_config = {}

            if choice == '0':
                break
            
            field_name = input("Beri nama untuk field ini: ")
            element_config['name'] = field_name
            
            # --- Tipe 1: Isian ---
            if choice == '1':
                element_config['type'] = 'isian'
                mode = input("Pilih mode jawaban: [1] Jawaban Tetap, [2] Dari File .txt : ")
                element_config['mode'] = 'tetap' if mode == '1' else 'file'
                element_config['xpath'] = input("Masukkan XPath untuk kolom input: ")
                if mode == '1':
                    element_config['fixed_text'] = input("Masukkan teks jawaban yang akan selalu digunakan: ")
                else:
                    file_path = input("Masukkan nama file .txt untuk data ini: ")
                    element_config['data_column'] = file_path
                    if file_path not in data_files:
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data_files[file_path] = [line.strip() for line in f if line.strip()]
                            print(f"✅ Berhasil memuat data dari '{file_path}'.")
                        except FileNotFoundError:
                            print(f"❌ ERROR: File '{file_path}' tidak ditemukan!")
                            continue
            
            # --- Tipe 2, 3, 4 ---
            elif choice in ['2', '3', '4']:
                type_map = {'2': 'pilgan', '3': 'checkbox', '4': 'dropdown'}
                element_config['type'] = type_map[choice]
                mode = input("Pilih mode jawaban: [1] Jawaban Tetap, [2] Jawaban Acak : ")
                element_config['mode'] = mode
                
                if mode not in ['1', '2']:
                    print("Mode tidak valid. Silakan coba lagi.")
                    continue

                if element_config['type'] == 'pilgan':
                    if mode == '1': # Tetap
                        element_config['xpath'] = input(f"Masukkan XPath untuk radio button spesifik yang dipilih: ")
                    else: # Acak
                        element_config['xpath'] = input("Masukkan XPath untuk menemukan SEMUA radio button: ")
                
                elif element_config['type'] == 'checkbox':
                    element_config['xpath'] = input("Masukkan XPath untuk menemukan SEMUA checkbox: ")
                    if mode == '1': # Tetap
                        options = input("Masukkan teks opsi (pisahkan dengan koma): ")
                        element_config['options_to_select'] = [opt.strip() for opt in options.split(',')]

                elif element_config['type'] == 'dropdown':
                    element_config['xpath_main'] = input("Masukkan XPath untuk membuka dropdown: ")
                    if mode == '1': # Tetap
                        element_config['xpath_option'] = input("Masukkan XPath untuk opsi spesifik dari daftar: ")
            else:
                print("Pilihan tidak valid.")
                continue
                
            elements_on_page.append(element_config)
            print(f"✅ Field '{field_name}' berhasil dikonfigurasi.")
        
        # --- Aksi di Akhir Halaman ---
        print("\nSetelah mengisi Halaman ini, tombol apa yang akan ditekan?")
        action_choice = input("[1] Berikutnya (Next), [2] Kirim (Submit): ")
        if action_choice == '1':
            action_button_xpath = input("Masukkan XPath untuk tombol 'Berikutnya': ")
            pages.append({'elements': elements_on_page, 'action_xpath': action_button_xpath})
            page_number += 1
        else:
            action_button_xpath = input("Masukkan XPath untuk tombol 'Kirim': ")
            pages.append({'elements': elements_on_page, 'action_xpath': action_button_xpath})
            break # Selesai konfigurasi
    
    # --- Konfigurasi Iterasi ---
    data_lengths = [len(data) for data in data_files.values()]
    if not data_lengths:
        num_iterations = int(input("\nMasukkan jumlah total pengisian: "))
    else:
        max_iter = min(data_lengths)
        num_iterations = int(input(f"\nBerapa kali form akan diisi? (Maksimal dari file: {max_iter}): "))
        num_iterations = min(num_iterations, max_iter)

    # --- Proses Eksekusi ---
    driver = setup_driver()
    if not driver: return

    for i in range(num_iterations):
        print(f"\n--- 🚀 Memulai Iterasi ke-{i + 1} dari {num_iterations} ---")
        driver.get(form_url)
        time.sleep(2)
        
        current_data_row = {key: values[i] for key, values in data_files.items() if i < len(values)}

        for page_config in pages:
            print(f"   -> Mengisi elemen di Halaman...")
            for config in page_config['elements']:
                elem_type = config['type']
                if elem_type == 'isian': handle_text_input(driver, config, current_data_row)
                elif elem_type == 'pilgan': handle_multiple_choice(driver, config)
                elif elem_type == 'checkbox': handle_checkbox(driver, config)
                elif elem_type == 'dropdown': handle_dropdown(driver, config)
            
            # Klik tombol aksi (Next atau Submit)
            print("   -> Menekan tombol aksi halaman...")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, page_config['action_xpath']))).click()
            time.sleep(2) # Tunggu halaman berikutnya memuat
            
        print("   - Formulir terkirim.")
    
    driver.quit()
    print("\n🎉 Semua proses telah selesai! 🎉")

if __name__ == "__main__":
    main()