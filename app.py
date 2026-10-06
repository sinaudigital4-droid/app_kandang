import streamlit as st

# Menyembunyikan header, menu, dan footer bawaan Streamlit
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)





from license_manager import validate_license

# Pengaturan Halaman Utama
st.set_page_config(
    page_title="Master Prompt AI Studio",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Master Prompt AI Generator Studio")
st.caption("Aplikasi pembuat prompt otomatis sesuai sintaks resmi Seedance 2.5, Veo 3, Nano Banana, & Commercial Ads.")

# ===== LICENSE HYBRID SYSTEM =====
if 'license_valid' not in st.session_state:
    st.session_state.license_valid = False
    st.session_state.license_info = None
    st.session_state.license_key = ""

st.sidebar.title("🔐 Aktivasi Lisensi")

# Status lisensi
if st.session_state.license_valid and st.session_state.license_info:
    expiry = st.session_state.license_info['expiry']
    user = st.session_state.license_info['user']
    st.sidebar.success(f"✅ Lisensi aktif untuk {user}")
    st.sidebar.info(f"Berlaku sampai: {expiry}")
    if st.sidebar.button("🔄 Ganti Lisensi"):
        st.session_state.license_valid = False
        st.session_state.license_info = None
        st.session_state.license_key = ""
        st.rerun()
else:
    st.sidebar.warning("⚠️ Lisensi belum diaktifkan")
    license_key_input = st.sidebar.text_area(
        "Paste License Key",
        value=st.session_state.license_key,
        height=120,
        placeholder="Tempel license key Anda di sini..."
    )
    if st.sidebar.button("Aktifkan Lisensi"):
        if license_key_input.strip():
            st.session_state.license_key = license_key_input.strip()
            result = validate_license(license_key_input.strip())
            if result['valid']:
                st.session_state.license_valid = True
                st.session_state.license_info = result
                st.sidebar.success("Lisensi berhasil diaktifkan!")
                st.rerun()
            else:
                st.sidebar.error(f"Gagal: {result['message']}")
        else:
            st.sidebar.error("License key tidak boleh kosong")

# Blokir akses jika belum valid
if not st.session_state.license_valid:
    st.warning("🔒 Aplikasi ini dilindungi lisensi. Silakan aktifkan lisensi di sidebar untuk melanjutkan.")
    st.info("💡 Anda menerima license key dari penjual. Tempelkan di sidebar untuk mengakses generator.")
    st.stop()

# Sidebar Pilihan Kategori Model
model_choice = st.sidebar.selectbox(
    "Pilih Kategori Model AI",
    [
        "Seedance 2.5 (Multimodal & Audio)",
        "Veo 3 (Cinematic Video)",
        "Nano Banana (Aset Gambar 8K)",
        "Commercial Product (Orbit 360 & Slow-Mo)",
        "UGC Video Ad (10s Vertikal)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tips Cara Pakai:** Hasil prompt yang dibuat siap dicopy dan digunakan langsung di platform AI generatif.")

# ==========================================
# 1. SEEDANCE 2.5 GENERATOR
# ==========================================
if model_choice == "Seedance 2.5 (Multimodal & Audio)":
    st.header("⚡ Seedance 2.5 Master Prompt Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input("Subjek / Karakter", "seorang wanita muda berpakaian kasual")
        product = st.text_input("Objek / Produk", "botol serum skincare pink pastel")
        pet = st.text_input("Hewan Pendamping (Opsional)", "kucing oranye fluffy")
        env = st.text_input("Latar Tempat & Pencahayaan", "kamar tidur estetis berlimpah sinar matahari")
    
    with col2:
        vo_hook = st.text_input("Voiceover Hook (0-3s)", "Kucing gue aja sampai heran ngeliat muka gue makin glowing!")
        vo_demo = st.text_input("Voiceover Penjelasan (3-7s)", "Serum ini ringan banget dan bikin kulit lembap seharian.")
        vo_cta = st.text_input("Voiceover Call to Action (7-10s)", "Yuk cobain sekarang, klik keranjang di bawah!")
        bgm = st.text_input("Musik Latar (BGM)", "upbeat acoustic pop music plays softly")
        sfx = st.text_input("Efek Suara (SFX)", "clean bottle placement click sound")
        
    if st.button("Hasilkan Prompt Seedance 2.5"):
        prompt_output = f"""[Generation goal]
Authentic vertical 9:16 UGC video ad, 10 seconds duration, 24fps.

[Reference roles]
@Image 1 defines the {subject}'s face, hair, and clothing only.
@Image 2 defines the {pet}'s appearance and species only.
@Image 3 defines the {product}'s exact packaging, shape, and label only.

[Timeline & Scene Plan]
0-3s (VISUAL HOOK): Close-up handheld selfie tracking shot at eye level. The {subject} holds the {product} while the {pet} sits right next to her, looking curiously at the camera lens. Soft natural ambient sunlight in a {env}.
Spoken language: Indonesian. She says in an energetic, authentic UGC voice: {{{vo_hook}}} <soft room ambience>

3-7s (DEMO): Medium shot with dynamic handheld camera tracking. The {subject} applies a drop of product on her cheek with high energy, while the {pet} reacts playfully in frame.
Spoken language: Indonesian. She says in a warm friendly tone: {{{vo_demo}}} ( {bgm} )

7-10s (CTA & HERO SHOT): Fast whip-pan transition to a close-up hero shot of the {product} placed on a wooden surface, with the woman and {pet} smiling softly in the background.
Spoken language: Indonesian. She says enthusiastically: {{{vo_cta}}} <{sfx}> 【Diskon Khusus Hari Ini!】

[Maintain consistency]
Exactly one {subject}, one {pet}, and one {product}. Preserve character facial identity, animal features, product label typography, and natural lighting across all 10 seconds. No extra characters, no warped packaging, no unwanted watermarks or logos."""
        
        st.subheader("📋 Hasil Master Prompt Seedance 2.5:")
        st.code(prompt_output, language="text")

# ==========================================
# 2. VEO 3 GENERATOR
# ==========================================
elif model_choice == "Veo 3 (Cinematic Video)":
    st.header("🎥 Veo 3 Cinematic Video Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        veo_subject = st.text_input("Subjek Utama", "A vintage chronograph mechanical watch")
        veo_action = st.text_input("Pergerakan / Aksi Subjek", "internal gears turning smoothly with precision movement")
        veo_surface = st.text_input("Alas / Permukaan", "dark polished mahogany wood desk")
    
    with col2:
        veo_camera = st.selectbox("Gerakan Kamera", ["Slow 360-degree orbit shot", "Cinematic dolly zoom in", "Smooth tracking pan shot", "Low-angle crane shot"])
        veo_lighting = st.text_input("Pencahayaan", "Volumetric golden spotlight with soft moody studio shadows")
        
    if st.button("Hasilkan Prompt Veo 3"):
        veo_output = f"""Cinematic 10-second ultra-realistic video of {veo_subject}, 24fps.

Subject: {veo_subject} positioned elegantly on a {veo_surface}. The subject shows {veo_action}, remaining sharp and visually dominant.

Camera Movement: {veo_camera} around the subject with steady, fluid motion and shallow depth of field.

Lighting & Atmosphere: {veo_lighting}, crisp surface highlights, physical material reflections, subtle atmospheric haze, high-end commercial aesthetic.

Quality & Constraints: Photorealistic 8K render, physically accurate motion and lighting, professional color grading, continuous smooth movement, no motion blur artifacts, no extra objects."""
        
        st.subheader("📋 Hasil Master Prompt Veo 3:")
        st.code(veo_output, language="text")

# ==========================================
# 3. NANO BANANA GENERATOR
# ==========================================
elif model_choice == "Nano Banana (Aset Gambar 8K)":
    st.header("🖼️ Nano Banana Image Asset Generator")
    
    asset_type = st.selectbox("Tipe Aset Gambar", ["Karakter Portrait", "Hewan Pendamping", "Produk Comercial"])
    detail_desc = st.text_area("Deskripsi Detail Visual", "cheerful young Indonesian woman in her 20s, warm authentic smile, wearing a casual pastel beige t-shirt")
    lens_style = st.selectbox("Gaya Lensa & Kamera", ["85mm lens, soft bokeh, studio rim lighting", "50mm macro lens, hyper-detailed texture", "35mm street photography lens, natural daylight"])
    
    if st.button("Hasilkan Prompt Nano Banana"):
        nano_output = f"""Photorealistic hero shot of {detail_desc}, {lens_style}, crisp skin and material texture details, clean aesthetic composition, realistic physical reflections, volumetric ambient lighting, 8k resolution, ultra-detailed render."""
        
        st.subheader("📋 Hasil Master Prompt Nano Banana:")
        st.code(nano_output, language="text")

# ==========================================
# 4. COMMERCIAL PRODUCT GENERATOR
# ==========================================
elif model_choice == "Commercial Product (Orbit 360 & Slow-Mo)":
    st.header("💎 Commercial Luxury Product Generator")
    
    prod_category = st.text_input("Kategori Produk", "Luxury Timepiece / Perfume / Canned Beverage / Belt")
    brand_name = st.text_input("Nama Brand / Logo", "MUTU ORA")
    prod_detail = st.text_area("Deskripsi Fisik Produk", "A premium rose-gold chronograph watch with a dark alligator leather strap")
    surface = st.text_input("Alas Permukaan", "wet dark obsidian stone")
    effect_part = st.text_input("Efek Partikel Tambahan", "glowing golden dust motes floating in slow-motion catching lens flares")
    
    if st.button("Hasilkan Prompt Commercial Product"):
        comm_output = f"""[Generation goal]
Cinematic 10-second luxury commercial for {prod_category}, slow-motion 60fps presentation, high-end brand advertising quality.

[Hero Subject & Placement]
{prod_detail} with clean, readable branding labeled "{brand_name}" is elegantly positioned on {surface}. The product is the central hero subject, remaining perfectly sharp, realistic, and visually dominant throughout the entire shot.

[Camera Motion - Fixed Orbit & Slow Motion]
The camera performs a smooth, continuous slow-motion 360-degree cinematic orbit around the product, executing a refined 180° to 360° reveal. The movement is steady, controlled, and fluid. Subtle parallax creates a strong sense of depth and three-dimensional realism.

[Lighting & Dynamic Visual Effects]
Warm golden spotlight sweeps gently across the product surface, revealing authentic material textures, crisp highlights, and fine craftsmanship. 

[ADDITIONAL DRAMATIC EFFECTS]: 
1. Slow-motion atmospheric {effect_part}.
2. Dynamic hyper-detailed macro reflections sliding across the product surface.

[Branding & Quality Constraints]
The "{brand_name}" text remains clean, perfectly readable, correctly spelled, and physically integrated into the product material. No deformation, no morphing logo, no extra floating objects. Photorealistic 8K visual quality, physically accurate lighting and reflections, rich contrast, professional color grading."""
        
        st.subheader("📋 Hasil Master Prompt Commercial:")
        st.code(comm_output, language="text")

# ==========================================
# 5. UGC VIDEO AD GENERATOR
# ==========================================
else:
    st.header("📱 UGC Video Ad 10s Generator")
    
    ugc_char = st.text_input("Karakter", "young energetic guy in a hoodie")
    ugc_prod = st.text_input("Produk", "wireless bluetooth earbuds")
    ugc_vo = st.text_input("Voiceover", "Sumpah, earbud ini bass-nya mantap banget dan gak gampang lepas!")
    
    if st.button("Hasilkan Prompt UGC Ad"):
        ugc_output = f"""Vertical format 9:16, 10 seconds duration, authentic UGC video style, 24fps.

0s-3s (HOOK): Close-up handheld camera shot. A cheerful {ugc_char} holds and shows {ugc_prod} to the camera with natural lighting.
3s-7s (DEMO): Medium shot, selfie-style dynamic handheld motion. The {ugc_char} wears and tests {ugc_prod} with high energy.
7-10s (CTA): Quick pan to a close-up hero shot of {ugc_prod} on a desk.

VO Direction: Energetic, friendly, authentic Indonesian UGC voiceover.
Script: "{ugc_vo}"

Negative Prompt: over-edited, professional studio lighting, cinematic glossy filter, static camera, blurry texture, watermark."""
        
        st.subheader("📋 Hasil Master Prompt UGC Ad:")
        st.code(ugc_output, language="text")
