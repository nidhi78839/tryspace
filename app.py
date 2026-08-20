import streamlit as st
from pathlib import Path
from PIL import Image
import base64
import io

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TrySpace — Visualize Before You Buy",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).parent
ASSETS = BASE_DIR / "assets"

CLOTHING = ASSETS / "clothing"
JEWELLERY = ASSETS / "jewellery"
FURNITURE = ASSETS / "furniture"

# =========================================================
# PRODUCT DATA
# =========================================================

products = {
    "Clothing": [
        {
            "name": "Lemon Glow Dress",
            "file": CLOTHING / "lemon_glow.jpg",
            "description": "Soft lemon evening dress",
            "colours": ["Lemon", "Cream", "Sage", "Blush"]
        },
        {
            "name": "Rosé Blush Palazzo Set",
            "file": CLOTHING / "rose_blush.jpg",
            "description": "Elegant blush pink palazzo set",
            "colours": ["Rose", "Blush", "Dusty Pink", "Nude"]
        },
        {
            "name": "Sky Flare Jeans",
            "file": CLOTHING / "sky_flare.jpg",
            "description": "Relaxed wide-leg denim",
            "colours": ["Sky Blue", "Denim", "Ice Blue", "Grey"]
        },
        {
            "name": "Pastel Pink Sharara Set",
            "file": CLOTHING / "pastel_pink.jpg",
            "description": "Soft festive pink sharara set",
            "colours": ["Pink", "Rose", "Peach", "Champagne"]
        }
    ],

    "Jewellery": [
        {
            "name": "Emerald Kundan Earrings",
            "file": JEWELLERY / "emerald_kundan.jpg",
            "description": "Traditional kundan earrings with green stones",
            "colours": ["Emerald", "Gold", "Pearl"]
        },
        {
            "name": "Golden Pearl Layers",
            "file": JEWELLERY / "golden_pearl_layers.jpg",
            "description": "Layered golden pearl necklace",
            "colours": ["Gold", "Pearl", "Ivory"]
        },
        {
            "name": "Lavender Bloom Necklace",
            "file": JEWELLERY / "lavender_bloom.jpg",
            "description": "Delicate lavender stone necklace",
            "colours": ["Lavender", "Silver", "Rose"]
        },
        {
            "name": "Lilac Kundan Earrings",
            "file": JEWELLERY / "lilac_kundan.jpg",
            "description": "Pearl and lilac kundan earrings",
            "colours": ["Lilac", "Pearl", "Gold"]
        }
    ],

    "Room & Furniture": [
        {
            "name": "Petal Glow Table Lamp",
            "file": FURNITURE / "petal_glow_lamp.jpg",
            "description": "Warm floral bedside lamp",
            "colours": ["Warm White", "Gold", "Wood"]
        },
        {
            "name": "Bamboo Curve Side Table",
            "file": FURNITURE / "bamboo_curve_table.jpg",
            "description": "Minimal bamboo storage table",
            "colours": ["Natural Wood", "Beige", "Cream"]
        },
        {
            "name": "Cloud Lounge Bean Bag",
            "file": FURNITURE / "cloud_lounge_bag.jpg",
            "description": "Soft cream lounge seating",
            "colours": ["Cream", "Ivory", "Beige"]
        },
        {
            "name": "Walnut Cozy Accent Chair",
            "file": FURNITURE / "walnut_accent_chair.jpg",
            "description": "Warm walnut and cream accent chair",
            "colours": ["Walnut", "Cream", "Brown"]
        }
    ]
}

# =========================================================
# SESSION STATE
# =========================================================

if "selected_category" not in st.session_state:
    st.session_state.selected_category = "Clothing"

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

if "user_photo" not in st.session_state:
    st.session_state.user_photo = None

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@500;600;700&display=swap');

    .stApp {
        background: #fcf9f7;
        color: #302b2d;
    }

    [data-testid="stSidebar"] {
        background: #fffdfc;
        border-right: 1px solid #eadfe0;
    }

    [data-testid="stSidebar"] * {
        color: #302b2d !important;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', Georgia, serif !important;
        color: #302b2d !important;
    }

    p, div, label, span {
        font-family: 'DM Sans', sans-serif;
    }

    .brand {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2rem;
        font-weight: 700;
        color: #302b2d;
        margin-bottom: 0;
    }

    .brand span {
        color: #c87891;
    }

    .tagline {
        color: #8d777d;
        font-size: 0.9rem;
        margin-top: -5px;
        margin-bottom: 30px;
    }

    .hero {
        background: linear-gradient(
            135deg,
            #fff7f7 0%,
            #f8eff5 100%
        );
        border: 1px solid #eadfe3;
        border-radius: 28px;
        padding: 55px;
        margin-bottom: 30px;
    }

    .eyebrow {
        color: #bd7188;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hero-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 3.4rem;
        line-height: 1.08;
        color: #302b2d;
        margin: 12px 0 18px 0;
    }

    .hero-text {
        color: #6f6266;
        font-size: 1.05rem;
        max-width: 800px;
        line-height: 1.7;
    }

    .section-card {
        background: #ffffff;
        border: 1px solid #eadfe3;
        border-radius: 22px;
        padding: 28px;
        margin-bottom: 25px;
    }

    .section-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.65rem;
        color: #302b2d;
        margin-bottom: 20px;
    }

    .product-card {
        background: #fff;
        border: 1px solid #eadfe3;
        border-radius: 18px;
        overflow: hidden;
        margin-bottom: 10px;
        transition: 0.2s;
    }

    .product-name {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.15rem;
        color: #302b2d;
        font-weight: 600;
        padding: 12px 14px 3px 14px;
    }

    .product-description {
        color: #817277;
        font-size: 0.82rem;
        padding: 0 14px 10px 14px;
    }

    .colour-dot {
        display: inline-block;
        width: 13px;
        height: 13px;
        border-radius: 50%;
        margin-right: 5px;
        border: 1px solid #ddd;
    }

    .upload-box {
        background: #fff8fa;
        border: 1.5px dashed #dfabbc;
        border-radius: 18px;
        padding: 25px;
        text-align: center;
    }

    .info-box {
        background: #f9f1f5;
        border-radius: 16px;
        padding: 20px;
        color: #685c61;
        line-height: 1.6;
    }

    .score {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2.4rem;
        color: #bd7188;
        font-weight: 600;
    }

    .footer {
        text-align: center;
        color: #a18d93;
        padding: 35px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">✦ Try<span>Space</span></div>
        <div class="tagline">Visualize Before You Buy</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✦ Explore")

    category = st.radio(
        "Choose experience",
        ["Home", "Clothing", "Jewellery", "Room & Furniture"],
        index=["Home", "Clothing", "Jewellery", "Room & Furniture"].index(
            st.session_state.selected_category
            if st.session_state.selected_category in
            ["Home", "Clothing", "Jewellery", "Room & Furniture"]
            else "Clothing"
        ),
        label_visibility="collapsed"
    )

    st.session_state.selected_category = category

    st.markdown("---")

    st.markdown(
        """
        <div class="info-box">
        ✦ <b>AI Style Assistant</b><br><br>
        Understand colours, style and product compatibility before you decide what to buy.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# HOME
# =========================================================

if category == "Home":

    st.markdown(
        """
        <div class="hero">

        <div class="eyebrow">AI-POWERED VIRTUAL SHOPPING</div>

        <div class="hero-title">
        Find the look.<br>
        See it before you buy. ✦
        </div>

        <div class="hero-text">
        TrySpace helps you visualize fashion, jewellery and furniture
        in your own context before making a purchase.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-card"><div class="section-title">How TrySpace works</div></div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="section-card">
            <small>01</small>
            <h3>Upload your photo</h3>
            <p>Upload one clear photo of yourself or your room.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="section-card">
            <small>02</small>
            <h3>Choose a product</h3>
            <p>Browse our ready-to-try collection.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            """
            <div class="section-card">
            <small>03</small>
            <h3>Visualize & decide</h3>
            <p>See the product in your context before buying.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# CATEGORY PAGE
# =========================================================

else:

    category_icon = {
        "Clothing": "👗",
        "Jewellery": "💎",
        "Room & Furniture": "🛋️"
    }

    st.markdown(
        f"""
        <div class="hero">

        <div class="eyebrow">TRYSPACE COLLECTION</div>

        <div class="hero-title">
        {category_icon[category]} Find your perfect {category.lower()}.
        </div>

        <div class="hero-text">
        Choose a product from our collection and visualize it before you buy.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # STEP 1 - UPLOAD
    # =====================================================

    st.markdown(
        """
        <div class="section-card">
        <div class="section-title">1. Upload Your Photo</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if category == "Room & Furniture":
        upload_text = "Upload a clear photo of your room"
    else:
        upload_text = "Upload a clear full-body photo"

    uploaded = st.file_uploader(
        upload_text,
        type=["jpg", "jpeg", "png"],
        key=f"upload_{category}"
    )

    if uploaded:
        st.session_state.user_photo = uploaded

        image = Image.open(uploaded)

        st.image(
            image,
            caption="Your uploaded photo",
            width=350
        )

    # =====================================================
    # STEP 2 - PRODUCTS
    # =====================================================

    st.markdown(
        """
        <div class="section-card">
        <div class="section-title">2. Choose a Product</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    current_products = products[category]

    cols = st.columns(4)

    for i, product in enumerate(current_products):

        with cols[i]:

            image_path = product["file"]

            if image_path.exists():

                st.image(
                    str(image_path),
                    use_container_width=True
                )

            else:

                st.error(
                    f"Missing image:\n{image_path.name}"
                )

            st.markdown(
                f"""
                <div class="product-name">
                {product["name"]}
                </div>

                <div class="product-description">
                {product["description"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "Try This ✦",
                key=f"product_{category}_{i}",
                use_container_width=True
            ):
                st.session_state.selected_product = product

    # =====================================================
    # SELECTED PRODUCT
    # =====================================================

    if st.session_state.selected_product:

        product = st.session_state.selected_product

        st.markdown("---")

        st.markdown(
            f"""
            <div class="section-card">
            <div class="section-title">
            3. Your Selection
            </div>
            <b>{product["name"]}</b><br>
            {product["description"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        selected_col1, selected_col2 = st.columns(2)

        with selected_col1:

            st.image(
                str(product["file"]),
                caption=product["name"],
                use_container_width=True
            )

        with selected_col2:

            st.markdown("### ✦ Product Details")

            st.write(
                f"**Style:** {product['description']}"
            )

            st.write(
                "**Available palette:** "
                + ", ".join(product["colours"])
            )

            st.markdown("### Compatibility Preview")

            st.markdown(
                """
                <div class="score">92%</div>
                <small>Initial style compatibility</small>
                """,
                unsafe_allow_html=True
            )

            st.info(
                "AI visualization will use your uploaded photo "
                "and this selected product."
            )

            if st.button(
                "✨ ANALYSE & VISUALIZE ON ME",
                use_container_width=True,
                type="primary"
            ):

                if not st.session_state.user_photo:

                    st.warning(
                        "Please upload your photo first."
                    )

                else:

                    st.success(
                        "Product and photo are ready for AI visualization."
                    )

                    st.info(
                        "Next step: connect the Gemini image-generation "
                        "model to create the actual virtual try-on."
                    )

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
    ✦ TrySpace<br>
    Visualize Before You Buy
    </div>
    """,
    unsafe_allow_html=True
)