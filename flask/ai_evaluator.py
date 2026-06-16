import difflib
import speech_recognition as sr
import google.generativeai as genai

class AdaptEdAI:
    def __init__(self, gemini_api_key=None):
        # Konfigurasi LLM untuk Evaluasi Writing (Grammar/Vocab)
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
            self.llm_model = genai.GenerativeModel('gemini-pro')
        
        # Inisialisasi Speech-to-Text untuk Speaking
        self.recognizer = sr.Recognizer()

    # ==========================================
    # 1. READING EVALUATOR (Kecepatan & Pemahaman)
    # ==========================================
    def evaluate_reading(self, teks_soal, durasi_detik, jawaban_benar, jawaban_siswa):
        skor_jawaban = 100 if jawaban_benar.lower() == jawaban_siswa.lower() else 0
        
        # Menghitung WPM (Words Per Minute)
        jumlah_kata = len(teks_soal.split())
        wpm = (jumlah_kata / max(durasi_detik, 1)) * 60
        
        feedback = ""
        if skor_jawaban == 100:
            if wpm < 50: # Standar batas bawah membaca (bisa disesuaikan)
                feedback = "Jawaban benar, namun kecepatan membacamu masih lambat. Terus berlatih membaca Hangeul ya!"
            else:
                feedback = "Sempurna! Pemahaman dan kecepatan membacamu sangat baik."
        else:
            feedback = "Jawaban kurang tepat. Coba baca ulang teksnya dengan lebih teliti."
            
        return skor_jawaban, feedback

    # ==========================================
    # 2. LISTENING EVALUATOR (Fuzzy Semantic Match)
    # ==========================================
    def evaluate_listening(self, transkrip_asli, jawaban_siswa):
        # Menggunakan SequenceMatcher untuk menilai kemiripan teks (Akurasi pendengaran)
        similarity = difflib.SequenceMatcher(None, transkrip_asli.lower(), jawaban_siswa.lower()).ratio()
        skor_ai = int(similarity * 100)
        
        if skor_ai >= 90:
            feedback = "Luar biasa! Pendengaranmu sangat tajam."
        elif skor_ai >= 70:
            feedback = "Cukup baik, ada sedikit typo/kesalahan ejaan dari yang kamu dengar."
        else:
            feedback = f"Masih kurang tepat. Transkrip aslinya adalah: '{transkrip_asli}'"
            
        return skor_ai, feedback

    # ==========================================
    # 3. SPEAKING EVALUATOR (Speech-to-Text)
    # ==========================================
    def evaluate_speaking(self, file_audio_path, teks_target):
        try:
            with sr.AudioFile(file_audio_path) as source:
                audio_data = self.recognizer.record(source)
                # Menggunakan Google Web Speech API (Gratis) untuk mendeteksi bahasa Korea (ko-KR)
                teks_terdeteksi = self.recognizer.recognize_google(audio_data, language="ko-KR")
                
            # Bandingkan hasil deteksi suara dengan teks yang seharusnya dibaca
            similarity = difflib.SequenceMatcher(None, teks_target.lower(), teks_terdeteksi.lower()).ratio()
            skor_ai = int(similarity * 100)
            
            feedback = f"AI mendeteksi kamu mengucapkan: '{teks_terdeteksi}'."
            if skor_ai >= 85:
                feedback += " Pelafalan (Pronunciation) kamu sangat natural!"
            else:
                feedback += " Perhatikan lagi intonasi dan pelafalan suku katanya."
                
            return skor_ai, feedback
            
        except sr.UnknownValueError:
            return 0, "AI tidak dapat mendengar suaramu dengan jelas. Coba rekam di tempat yang lebih sepi."
        except Exception as e:
            return 0, f"Error pemrosesan audio: {str(e)}"

    # ==========================================
    # 4. WRITING EVALUATOR (LLM Grammar Check)
    # ==========================================
    def evaluate_writing(self, jawaban_siswa, topik="Membahas kegiatan sehari-hari"):
        prompt = f"""
        Kamu adalah pengajar bahasa Korea yang ketat namun suportif.
        Evaluasi tulisan bahasa Korea siswa ini dengan topik: {topik}.
        Jawaban siswa: "{jawaban_siswa}"
        
        Berikan format balasan seperti ini:
        SKOR: [berikan nilai 0-100 berdasarkan grammar, kosakata, dan relevansi]
        FEEDBACK: [Berikan penjelasan singkat dalam bahasa Indonesia letak kesalahannya dan bagaimana kalimat yang benarnya]
        """
        try:
            response = self.llm_model.generate_content(prompt)
            hasil = response.text
            
            # Parsing sederhana untuk memisahkan SKOR dan FEEDBACK
            baris = hasil.split('\n')
            skor = 0
            feedback = "Koreksi AI belum tersedia."
            
            for b in baris:
                if b.startswith('SKOR:'):
                    # Ekstrak angka saja
                    skor = int(''.join(filter(str.isdigit, b)))
                elif b.startswith('FEEDBACK:'):
                    feedback = b.replace('FEEDBACK:', '').strip()
                    
            return min(skor, 100), feedback
        except Exception as e:
            return 0, "Gagal terhubung ke model analisis bahasa."