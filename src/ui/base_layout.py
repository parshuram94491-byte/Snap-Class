import streamlit as st


def style_background_home():
    st.markdown(
        """<style>
/* App Canvas Gradient */
.stApp:has(.snap-home-page) {
    background: radial-gradient(circle at 50% 12%, #385DF8 0%, #294DF2 30%, #2540D8 60%, #462DE0 100%) !important;
    min-height: 100vh !important;
    overflow-x: hidden !important;
}

/* Decorative Background Layer via ::before on .stApp */
.stApp:has(.snap-home-page)::before {
    content: '' !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    pointer-events: none !important;
    z-index: 0 !important;
    background-image: url("data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20viewBox%3D%270%200%201440%20900%27%20preserveAspectRatio%3D%27none%27%3E%0A%20%20%3Cdefs%3E%0A%20%20%20%20%3CradialGradient%20id%3D%27glow-tl%27%20cx%3D%278%25%27%20cy%3D%2715%25%27%20r%3D%2735%25%27%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%270%25%27%20stop-color%3D%27%234F75FF%27%20stop-opacity%3D%270.38%27/%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%27100%25%27%20stop-color%3D%27%234F75FF%27%20stop-opacity%3D%270%27/%3E%0A%20%20%20%20%3C/radialGradient%3E%0A%20%20%20%20%3CradialGradient%20id%3D%27glow-bl%27%20cx%3D%275%25%27%20cy%3D%2785%25%27%20r%3D%2735%25%27%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%270%25%27%20stop-color%3D%27%233B5BDB%27%20stop-opacity%3D%270.32%27/%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%27100%25%27%20stop-color%3D%27%233B5BDB%27%20stop-opacity%3D%270%27/%3E%0A%20%20%20%20%3C/radialGradient%3E%0A%20%20%20%20%3CradialGradient%20id%3D%27glow-br%27%20cx%3D%2795%25%27%20cy%3D%2785%25%27%20r%3D%2735%25%27%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%270%25%27%20stop-color%3D%27%235B3BE8%27%20stop-opacity%3D%270.38%27/%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%27100%25%27%20stop-color%3D%27%235B3BE8%27%20stop-opacity%3D%270%27/%3E%0A%20%20%20%20%3C/radialGradient%3E%0A%20%20%3C/defs%3E%0A%20%20%3Crect%20width%3D%27100%25%27%20height%3D%27100%25%27%20fill%3D%27url%28%23glow-tl%29%27/%3E%0A%20%20%3Crect%20width%3D%27100%25%27%20height%3D%27100%25%27%20fill%3D%27url%28%23glow-bl%29%27/%3E%0A%20%20%3Crect%20width%3D%27100%25%27%20height%3D%27100%25%27%20fill%3D%27url%28%23glow-br%29%27/%3E%0A%20%20%3Ccircle%20cx%3D%270%27%20cy%3D%27900%27%20r%3D%27160%27%20fill%3D%27none%27%20stroke%3D%27%23FFFFFF%27%20stroke-opacity%3D%270.08%27%20stroke-width%3D%271.5%27/%3E%0A%20%20%3Ccircle%20cx%3D%270%27%20cy%3D%27900%27%20r%3D%27240%27%20fill%3D%27none%27%20stroke%3D%27%23FFFFFF%27%20stroke-opacity%3D%270.08%27%20stroke-width%3D%271.5%27/%3E%0A%20%20%3Ccircle%20cx%3D%270%27%20cy%3D%27900%27%20r%3D%27320%27%20fill%3D%27none%27%20stroke%3D%27%23FFFFFF%27%20stroke-opacity%3D%270.08%27%20stroke-width%3D%271.5%27/%3E%0A%20%20%3Ccircle%20cx%3D%271440%27%20cy%3D%27900%27%20r%3D%27180%27%20fill%3D%27none%27%20stroke%3D%27%23FFFFFF%27%20stroke-opacity%3D%270.08%27%20stroke-width%3D%271.5%27/%3E%0A%20%20%3Ccircle%20cx%3D%271440%27%20cy%3D%27900%27%20r%3D%27280%27%20fill%3D%27none%27%20stroke%3D%27%23FFFFFF%27%20stroke-opacity%3D%270.08%27%20stroke-width%3D%271.5%27/%3E%0A%20%20%3Cg%20transform%3D%27translate%28180%2C%20140%29%20rotate%28-12%29%27%20stroke%3D%27%23FFFFFF%27%20stroke-width%3D%272%27%20fill%3D%27none%27%20stroke-linecap%3D%27round%27%20stroke-linejoin%3D%27round%27%20opacity%3D%270.32%27%3E%0A%20%20%20%20%3Cpolygon%20points%3D%2750%2C15%2095%2C0%2050%2C-15%205%2C0%27/%3E%0A%20%20%20%20%3Cpath%20d%3D%27M22%2C6%20L22%2C24%20C22%2C32%2078%2C32%2078%2C24%20L78%2C6%27/%3E%0A%20%20%20%20%3Ccircle%20cx%3D%2750%27%20cy%3D%270%27%20r%3D%272%27%20fill%3D%27%23FFFFFF%27/%3E%0A%20%20%20%20%3Cpath%20d%3D%27M50%2C0%20C38%2C12%2025%2C22%2025%2C36%27/%3E%0A%20%20%20%20%3Crect%20x%3D%2723%27%20y%3D%2736%27%20width%3D%274%27%20height%3D%2712%27%20rx%3D%271%27%20fill%3D%27%23FFFFFF%27/%3E%0A%20%20%3C/g%3E%0A%20%20%3Cg%20fill%3D%27%23FFFFFF%27%20opacity%3D%270.32%27%3E%0A%20%20%20%20%3Cpath%20d%3D%27M165%2C195%20Q165%2C203%20173%2C203%20Q165%2C203%20165%2C211%20Q165%2C203%20157%2C203%20Q165%2C203%20165%2C195%20Z%27/%3E%0A%20%20%20%20%3Cpath%20d%3D%27M305%2C130%20Q305%2C136%20311%2C136%20Q305%2C136%20305%2C142%20Q305%2C136%20299%2C136%20Q305%2C136%20305%2C130%20Z%27/%3E%0A%20%20%3C/g%3E%0A%20%20%3Cg%20fill%3D%27%23FFFFFF%27%20opacity%3D%270.3%27%3E%0A%20%20%20%20%3Ccircle%20cx%3D%2780%27%20cy%3D%27280%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%2798%27%20cy%3D%27280%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%27116%27%20cy%3D%27280%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%27134%27%20cy%3D%27280%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%27152%27%20cy%3D%27280%27%20r%3D%272.5%27/%3E%0A%20%20%20%20%3Ccircle%20cx%3D%2780%27%20cy%3D%27298%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%2798%27%20cy%3D%27298%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%27116%27%20cy%3D%27298%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%27134%27%20cy%3D%27298%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%27152%27%20cy%3D%27298%27%20r%3D%272.5%27/%3E%0A%20%20%20%20%3Ccircle%20cx%3D%2780%27%20cy%3D%27316%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%2798%27%20cy%3D%27316%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%27116%27%20cy%3D%27316%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%27134%27%20cy%3D%27316%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%27152%27%20cy%3D%27316%27%20r%3D%272.5%27/%3E%0A%20%20%3C/g%3E%0A%20%20%3Cg%20transform%3D%27translate%2870%2C%20540%29%20rotate%28-6%29%27%20stroke%3D%27%23FFFFFF%27%20stroke-width%3D%272%27%20fill%3D%27none%27%20stroke-linecap%3D%27round%27%20stroke-linejoin%3D%27round%27%20opacity%3D%270.32%27%3E%0A%20%20%20%20%3Cpath%20d%3D%27M55%2C20%20C40%2C12%2018%2C16%204%2C22%20L4%2C76%20C18%2C70%2040%2C66%2055%2C74%20Z%27/%3E%0A%20%20%20%20%3Cpath%20d%3D%27M55%2C20%20C70%2C12%2092%2C16%20106%2C22%20L106%2C76%20C92%2C70%2070%2C66%2055%2C74%20Z%27/%3E%0A%20%20%20%20%3Cline%20x1%3D%2755%27%20y1%3D%2720%27%20x2%3D%2755%27%20y2%3D%2774%27/%3E%0A%20%20%20%20%3Cline%20x1%3D%2714%27%20y1%3D%2736%27%20x2%3D%2745%27%20y2%3D%2732%27/%3E%0A%20%20%20%20%3Cline%20x1%3D%2714%27%20y1%3D%2748%27%20x2%3D%2745%27%20y2%3D%2744%27/%3E%0A%20%20%20%20%3Cline%20x1%3D%2714%27%20y1%3D%2760%27%20x2%3D%2745%27%20y2%3D%2756%27/%3E%0A%20%20%20%20%3Cline%20x1%3D%2765%27%20y1%3D%2732%27%20x2%3D%2796%27%20y2%3D%2736%27/%3E%0A%20%20%20%20%3Cline%20x1%3D%2765%27%20y1%3D%2744%27%20x2%3D%2796%27%20y2%3D%2748%27/%3E%0A%20%20%20%20%3Cline%20x1%3D%2765%27%20y1%3D%2756%27%20x2%3D%2796%27%20y2%3D%2760%27/%3E%0A%20%20%3C/g%3E%0A%20%20%3Cg%20fill%3D%27%23FFFFFF%27%20opacity%3D%270.32%27%3E%0A%20%20%20%20%3Ccircle%20cx%3D%271280%27%20cy%3D%2740%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%271300%27%20cy%3D%2740%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%271320%27%20cy%3D%2740%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%271340%27%20cy%3D%2740%27%20r%3D%272.5%27/%3E%0A%20%20%20%20%3Ccircle%20cx%3D%271280%27%20cy%3D%2760%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%271300%27%20cy%3D%2760%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%271320%27%20cy%3D%2760%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%271340%27%20cy%3D%2760%27%20r%3D%272.5%27/%3E%0A%20%20%20%20%3Ccircle%20cx%3D%271280%27%20cy%3D%2780%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%271300%27%20cy%3D%2780%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%271320%27%20cy%3D%2780%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%271340%27%20cy%3D%2780%27%20r%3D%272.5%27/%3E%0A%20%20%20%20%3Ccircle%20cx%3D%271280%27%20cy%3D%27100%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%271300%27%20cy%3D%27100%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%271320%27%20cy%3D%27100%27%20r%3D%272.5%27/%3E%3Ccircle%20cx%3D%271340%27%20cy%3D%27100%27%20r%3D%272.5%27/%3E%0A%20%20%20%20%3Cpath%20d%3D%27M1355%2C30%20Q1355%2C36%201361%2C36%20Q1355%2C36%201355%2C42%20Q1355%2C36%201349%2C36%20Q1355%2C36%201355%2C30%20Z%27/%3E%0A%20%20%3C/g%3E%0A%20%20%3Cg%20stroke%3D%27%23FFFFFF%27%20stroke-width%3D%272%27%20fill%3D%27none%27%20opacity%3D%270.32%27%3E%0A%20%20%20%20%3Cpath%20d%3D%27M1170%2C390%20C1220%2C380%201260%2C330%201280%2C265%27%20stroke-dasharray%3D%275%205%27%20stroke-linecap%3D%27round%27/%3E%0A%20%20%20%20%3Cg%20transform%3D%27translate%281260%2C%20215%29%20rotate%2815%29%27%20stroke-linecap%3D%27round%27%20stroke-linejoin%3D%27round%27%3E%0A%20%20%20%20%20%20%3Cpolygon%20points%3D%2710%2C48%2078%2C8%2048%2C72%2038%2C52%27/%3E%0A%20%20%20%20%20%20%3Cline%20x1%3D%2778%27%20y1%3D%278%27%20x2%3D%2738%27%20y2%3D%2752%27/%3E%0A%20%20%20%20%3C/g%3E%0A%20%20%3C/g%3E%0A%3C/svg%3E") !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
}

/* Main Content Container Restyling */
.block-container {
    width: min(100%, 960px) !important;
    max-width: 960px !important;
    margin: 0 auto !important;
    padding: 2.2rem 1.5rem 1rem !important;
    position: relative !important;
    z-index: 1 !important;
}

/* Branding Header */
.snap-brand-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-bottom: 2.2rem;
    position: relative;
    z-index: 2;
}

.snap-brand-logo-badge {
    width: 82px;
    height: 82px;
    border-radius: 20px;
    box-shadow: 0 10px 28px rgba(252, 207, 53, 0.45);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.8rem;
    transition: transform 0.25s ease;
}

.snap-brand-logo-badge:hover {
    transform: scale(1.05);
}

.snap-brand-logo-badge img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 20px;
}

.snap-brand-wordmark {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 900 !important;
    font-size: clamp(2.4rem, 5.2vw, 3.4rem) !important;
    line-height: 0.92 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    text-align: center !important;
    margin: 0 0 0.75rem 0 !important;
    text-shadow: 0 4px 14px rgba(0, 0, 0, 0.18) !important;
}

.snap-brand-wordmark .word-snap {
    color: #FFFFFF !important;
    display: block;
}

.snap-brand-wordmark .word-class {
    color: #FCCF35 !important;
    display: block;
}

.snap-brand-tagline {
    font-family: 'Outfit', sans-serif !important;
    font-size: clamp(0.95rem, 1.8vw, 1.12rem) !important;
    font-weight: 500 !important;
    color: rgba(255, 255, 255, 0.95) !important;
    margin: 0 0 0.65rem 0 !important;
    letter-spacing: 0.01em !important;
}

.snap-brand-indicator {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 2px;
}

.snap-brand-indicator .snap-pill {
    width: 32px;
    height: 4.5px;
    background: rgba(255, 255, 255, 0.85);
    border-radius: 9999px;
}

.snap-brand-indicator .snap-dot {
    width: 4.5px;
    height: 4.5px;
    background: rgba(255, 255, 255, 0.45);
    border-radius: 50%;
}

/* Landing-page portal cards only; regular dashboard columns remain unstyled */
.portal-card {
    background: #FFFFFF !important;
    border-radius: 30px !important;
    box-shadow: 0 20px 45px rgba(10, 20, 70, 0.22), 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    padding: 2.2rem 2.2rem 1.8rem !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    position: relative !important;
    overflow: hidden !important;
    transition: transform 0.25s cubic-bezier(0.2, 0, 0, 1), box-shadow 0.25s cubic-bezier(0.2, 0, 0, 1) !important;
    min-height: 260px !important;
}

.portal-card:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 28px 55px rgba(10, 20, 70, 0.28), 0 4px 14px rgba(0, 0, 0, 0.06) !important;
}

.portal-card.student-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 150px;
    height: 150px;
    background: radial-gradient(circle at 0% 0%, #D8E7FF 0%, #EBF2FE 60%, transparent 100%);
    border-radius: 30px 0 100% 0;
    pointer-events: none;
    z-index: 0;
}

.portal-card.teacher-card::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 150px;
    height: 150px;
    background: radial-gradient(circle at 100% 0%, #FDD7EB 0%, #FEEBF5 60%, transparent 100%);
    border-radius: 0 30px 0 100%;
    pointer-events: none;
    z-index: 0;
}

/* Card Content Layout */
.card-inner-content {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    position: relative;
    z-index: 1;
    min-height: 170px;
    margin-bottom: 1.5rem;
}

.card-text-col {
    flex: 1;
    padding-right: 0.5rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    z-index: 2;
}

.card-role-im {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.5rem;
    font-weight: 800;
    color: #111318;
    line-height: 1.1;
}

.card-role-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 2.1rem;
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 0.8rem;
}

.role-student {
    color: #2554F6 !important;
}

.role-teacher {
    color: #EC369B !important;
}

.card-desc {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.88rem;
    line-height: 1.45;
    color: #64748B;
    font-weight: 500;
    max-width: 190px;
    margin: 0;
}

/* Mascot Box and Sparks */
.card-mascot-box {
    position: relative;
    width: 150px;
    height: 165px;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    flex-shrink: 0;
    z-index: 2;
}

.mascot-sparks {
    position: absolute;
    top: -6px;
    left: 50%;
    transform: translateX(-50%);
    width: 44px;
    height: 26px;
    pointer-events: none;
}

.mascot-img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.12));
    transition: transform 0.25s ease;
}

.portal-card:hover .mascot-img {
    transform: scale(1.04);
}

/* Student Portal Button (Column 1) */
.portal-card.student-card .st-key-btn_student_portal button,
.portal-card.student-card [data-testid="stButton"] button {
    width: 100% !important;
    min-height: 52px !important;
    height: 52px !important;
    border-radius: 9999px !important;
    border: none !important;
    background: linear-gradient(90deg, #375EF8 0%, #466DF8 100%) !important;
    color: #FFFFFF !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 22px rgba(55, 94, 248, 0.4) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    cursor: pointer !important;
    position: relative !important;
    z-index: 2 !important;
}

.portal-card.student-card .st-key-btn_student_portal button:hover,
.portal-card.student-card [data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 28px rgba(55, 94, 248, 0.55) !important;
}

.portal-card.student-card .st-key-btn_student_portal button:focus-visible,
.portal-card.student-card [data-testid="stButton"] button:focus-visible {
    outline: 3px solid #FCCF35 !important;
    outline-offset: 3px !important;
}

/* Teacher Portal Button (Column 2) */
.portal-card.teacher-card .st-key-btn_teacher_portal button,
.portal-card.teacher-card [data-testid="stButton"] button {
    width: 100% !important;
    min-height: 52px !important;
    height: 52px !important;
    border-radius: 9999px !important;
    border: none !important;
    background: linear-gradient(90deg, #E62A7D 0%, #FA4B97 100%) !important;
    color: #FFFFFF !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 22px rgba(230, 42, 125, 0.4) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    cursor: pointer !important;
    position: relative !important;
    z-index: 2 !important;
}

.portal-card.teacher-card .st-key-btn_teacher_portal button:hover,
.portal-card.teacher-card [data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 28px rgba(230, 42, 125, 0.55) !important;
}

.portal-card.teacher-card .st-key-btn_teacher_portal button:focus-visible,
.portal-card.teacher-card [data-testid="stButton"] button:focus-visible {
    outline: 3px solid #FCCF35 !important;
    outline-offset: 3px !important;
}

/* Footer Styling */
.snap-footer-home {
    width: 100%;
    margin-top: 2.8rem;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    position: relative;
    z-index: 2;
}

.snap-footer-text {
    font-family: 'Outfit', sans-serif !important;
    font-size: clamp(0.85rem, 1.5vw, 1.02rem) !important;
    font-weight: 600 !important;
    color: #FFFFFF !important;
    letter-spacing: 0.01em !important;
    margin: 0 !important;
}

.snap-footer-author {
    color: #FCCF35 !important;
    font-weight: 700 !important;
}

/* Responsive Queries */
@media (max-width: 768px) {
    .stApp:has(.snap-home-page) .block-container {
        padding: 1.5rem 1rem !important;
    }

    .stApp:has(.snap-home-page) div[data-testid="stHorizontalBlock"]:has(.portal-card) {
        flex-direction: column !important;
        gap: 1.5rem !important;
    }

    .stApp:has(.snap-home-page) .portal-card {
        width: 100% !important;
        min-width: 100% !important;
        padding: 1.8rem 1.6rem 1.5rem !important;
        margin-bottom: 1rem !important;
    }

    .stApp:has(.snap-home-page) .card-inner-content {
        min-height: 140px;
        margin-bottom: 1.2rem;
    }

    .stApp:has(.snap-home-page) .card-mascot-box {
        width: 120px;
        height: 140px;
    }
}

/* Landing page refinements. These selectors only apply while the portal is rendered. */
.stApp:has(.snap-home-page) {
    background: radial-gradient(ellipse at 50% 12%, #3971FF 0%, #2852F3 43%, #2639D5 100%) !important;
    min-height: 100vh;
    overflow-x: hidden;
}

.stApp:has(.snap-home-page)::before {
    opacity: 0.72;
}

.stApp:has(.snap-home-page) [data-testid="stMainBlockContainer"] {
    position: relative;
    z-index: 1;
    width: min(100%, 1120px);
    padding: 0.75rem 1.5rem 0.5rem !important;
}

.stApp:has(.snap-home-page) [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
    gap: 0.75rem;
}

.stApp:has(.snap-home-page) [data-testid="stMain"] {
    align-items: stretch !important;
}

.stApp:has(.snap-home-page) [data-testid="stElementContainer"]:has(.snap-home-page) {
    display: none !important;
}

.stApp:has(.snap-home-page) .snap-brand-header {
    margin: 0 auto 0.75rem;
}

.stApp:has(.snap-home-page) .snap-brand-logo-badge {
    width: 78px;
    height: 78px;
    position: relative;
    background: #FFD51E;
    border-radius: 19px;
    box-shadow: 0 10px 28px rgba(252, 207, 53, 0.45), 0 0 26px rgba(255, 213, 30, 0.3);
}

.stApp:has(.snap-home-page) .snap-brand-logo-badge svg {
    position: absolute;
    inset: 14%;
    width: 72%;
    height: 72%;
}

.stApp:has(.snap-home-page) .snap-brand-logo-badge img {
    position: absolute;
    inset: 0;
}

.stApp:has(.snap-home-page) .snap-brand-wordmark {
    font-size: clamp(2.7rem, 5.2vw, 3.65rem) !important;
    line-height: 0.9 !important;
    padding: 0 !important;
    margin-bottom: 0.7rem !important;
}

.stApp:has(.snap-home-page) [data-testid="stColumn"]:has(.portal-card) {
    position: relative;
    isolation: isolate;
    display: flex;
    flex-direction: column;
    min-width: 0;
    min-height: 330px;
    overflow: hidden;
    border-radius: 27px;
    background: #FFFFFF;
    box-shadow: 0 20px 45px rgba(10, 20, 70, 0.22), 0 2px 8px rgba(0, 0, 0, 0.04);
    transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.stApp:has(.snap-home-page) [data-testid="stColumn"]:has(.portal-card):hover {
    transform: translateY(-4px);
    box-shadow: 0 27px 52px rgba(10, 20, 70, 0.27), 0 4px 14px rgba(0, 0, 0, 0.06);
}

.stApp:has(.snap-home-page) [data-testid="stColumn"]:has(.portal-card) > div {
    height: 100%;
}

.stApp:has(.snap-home-page) .portal-card {
    min-height: 250px !important;
    padding: 1.35rem 1.4rem 0.25rem !important;
    background: transparent !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

.stApp:has(.snap-home-page) .portal-card.student-card::before {
    top: 0;
    right: 0;
    left: auto;
    width: 58%;
    height: 78%;
    border-radius: 0 0 0 90%;
    background: radial-gradient(circle at 100% 0%, #D8E7FF 0%, #EBF2FE 62%, transparent 100%);
}

.stApp:has(.snap-home-page) .portal-card.teacher-card::before {
    width: 58%;
    height: 78%;
}

.stApp:has(.snap-home-page) .card-inner-content {
    min-height: 225px;
    margin-bottom: 0;
    align-items: center;
    gap: 0.25rem;
}

.stApp:has(.snap-home-page) .card-text-col {
    flex: 1 1 52%;
    min-width: 0;
    padding-right: 0.15rem;
}

.stApp:has(.snap-home-page) .card-role-title {
    font-size: clamp(1.7rem, 2.4vw, 2.1rem);
    margin-bottom: 0.6rem;
}

.stApp:has(.snap-home-page) .card-desc {
    max-width: 205px;
    font-size: 0.91rem;
    line-height: 1.5;
}

.stApp:has(.snap-home-page) .card-mascot-box {
    width: 46%;
    height: 215px;
}

.stApp:has(.snap-home-page) .mascot-img {
    display: block;
    width: 100%;
    height: 100%;
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

.stApp:has(.snap-home-page) [data-testid="stColumn"]:has(.portal-card) [data-testid="stButton"] {
    width: calc(100% - 2.8rem);
    margin: auto 1.4rem 1.1rem;
}

.stApp:has(.snap-home-page) [data-testid="stColumn"]:has(.portal-card) [data-testid="stButton"] button {
    width: 100%;
    min-height: 52px;
    height: 52px;
    border: 2px solid rgba(255, 255, 255, 0.92) !important;
    border-radius: 999px !important;
    background: linear-gradient(90deg, #F72CB0 0%, #EE269F 100%) !important;
    box-shadow: 0 8px 22px rgba(230, 42, 125, 0.28) !important;
    font-size: 1rem !important;
}

.stApp:has(.snap-home-page) [data-testid="stColumn"]:has(.portal-card) [data-testid="stButton"] button:hover {
    box-shadow: 0 12px 28px rgba(230, 42, 125, 0.42) !important;
}

.stApp:has(.snap-home-page) [data-testid="stColumn"]:has(.portal-card) [data-testid="stButton"] button:focus-visible {
    outline: 3px solid #FCCF35 !important;
    outline-offset: 3px !important;
}

.stApp:has(.snap-home-page) [data-testid="stColumn"]:has(.portal-card) [data-testid="stButton"] button p {
    margin: 0 !important;
}

.stApp:has(.snap-home-page) .snap-footer-home {
    margin-top: 0.65rem;
    margin-bottom: 0.15rem;
}

@media (max-width: 768px) {
    .stApp:has(.snap-home-page) [data-testid="stMainBlockContainer"] {
        padding: 0.75rem 1rem 1rem !important;
    }

    .stApp:has(.snap-home-page) [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
        gap: 0.8rem;
    }

    .stApp:has(.snap-home-page) [data-testid="stHorizontalBlock"]:has(.portal-card) {
        flex-direction: column !important;
        gap: 1.15rem !important;
    }

    .stApp:has(.snap-home-page) [data-testid="stColumn"]:has(.portal-card) {
        width: 100% !important;
        min-width: 0 !important;
        min-height: 320px;
    }

    .stApp:has(.snap-home-page) .portal-card {
        min-height: 240px !important;
        padding: 1.2rem 1.3rem 0.2rem !important;
    }

    .stApp:has(.snap-home-page) .card-inner-content {
        min-height: 210px;
    }

    .stApp:has(.snap-home-page) .card-mascot-box {
        width: 45%;
        height: 205px;
    }

    .stApp:has(.snap-home-page) .snap-brand-header {
        margin-bottom: 0.75rem;
    }

    .stApp:has(.snap-home-page) .snap-footer-home {
        margin-top: 1.15rem;
    }
}

@media (max-width: 480px) {
    .stApp:has(.snap-home-page) [data-testid="stMainBlockContainer"] {
        padding: 1rem 0.85rem 1.2rem !important;
    }

    .stApp:has(.snap-home-page) .snap-brand-logo-badge {
        width: 66px;
        height: 66px;
        border-radius: 17px;
    }

    .stApp:has(.snap-home-page) .snap-brand-wordmark {
        font-size: clamp(2.35rem, 13vw, 3rem) !important;
    }

    .stApp:has(.snap-home-page) .snap-brand-tagline {
        font-size: 0.94rem !important;
    }

    .stApp:has(.snap-home-page) [data-testid="stColumn"]:has(.portal-card) {
        min-height: 302px;
        border-radius: 23px;
    }

    .stApp:has(.snap-home-page) .portal-card {
        min-height: 220px !important;
        padding: 1rem 1rem 0.1rem !important;
    }

    .stApp:has(.snap-home-page) .card-inner-content {
        min-height: 190px;
    }

    .stApp:has(.snap-home-page) .card-role-title {
        font-size: clamp(1.5rem, 8vw, 1.85rem);
    }

    .stApp:has(.snap-home-page) .card-desc {
        max-width: 155px;
        font-size: 0.83rem;
    }

    .stApp:has(.snap-home-page) .card-mascot-box {
        width: 42%;
        height: 185px;
    }

    .stApp:has(.snap-home-page) [data-testid="stColumn"]:has(.portal-card) [data-testid="stButton"] {
        width: calc(100% - 2rem);
        margin: auto 1rem 0.95rem;
    }

    .stApp:has(.snap-home-page) .snap-footer-text {
        font-size: 0.82rem !important;
    }
}
</style>""",
        unsafe_allow_html=True,
    )


def style_background_dashboard():
    st.markdown(
        """
        <style>
            .stApp {
                background: #E6E9FF !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_base_layout():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

            :root {
                color-scheme: light;
                --snap-background: #E6E9FF;
                --snap-text: #111318;
                --snap-muted: #4B5563;
                --snap-blue: #4F5FF5;
                --snap-pink: #EC369B;
                --snap-dark: #111318;
            }

            #MainMenu,
            footer,
            header {
                visibility: hidden;
            }

            .block-container {
                width: min(100%, 1120px);
                padding: 1.5rem 1.5rem 2rem !important;
            }

            .snap-footer-dashboard {
                width: 100%;
                margin: 2rem auto 1.25rem;
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
            }

            .snap-footer-dashboard-text {
                max-width: 100%;
                font-family: 'Outfit', sans-serif !important;
                font-size: clamp(0.82rem, 1.4vw, 0.98rem) !important;
                font-weight: 600 !important;
                color: #334155 !important;
                letter-spacing: 0.01em !important;
                line-height: 1.5 !important;
                margin: 0 !important;
                overflow-wrap: anywhere;
            }

            .snap-footer-dashboard-author {
                color: #4F5FF5 !important;
                font-weight: 700 !important;
            }

            .stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stMain"],
            [data-testid="stMainBlockContainer"] {
                color: var(--snap-text);
            }

            [data-testid="stMarkdownContainer"],
            [data-testid="stMarkdownContainer"] p,
            [data-testid="stMarkdownContainer"] li,
            [data-testid="stCaptionContainer"],
            [data-testid="stWidgetLabel"],
            [data-testid="stWidgetLabel"] p,
            [data-testid="stHeader"],
            [data-testid="stSubheader"],
            [data-testid="stText"],
            [data-testid="stAlert"] p {
                color: var(--snap-text);
                font-family: 'Outfit', sans-serif;
            }

            h1,
            h2,
            h3,
            h4,
            [data-testid="stHeading"] h1,
            [data-testid="stHeading"] h2,
            [data-testid="stHeading"] h3,
            [data-testid="stSubheader"] {
                color: var(--snap-text) !important;
                font-family: 'Climate Crisis', sans-serif !important;
                line-height: 1.15 !important;
                margin-bottom: 0.35rem !important;
            }

            h1,
            [data-testid="stHeading"] h1 {
                font-size: clamp(2rem, 4vw, 3.5rem) !important;
            }

            h2,
            [data-testid="stHeading"] h2,
            [data-testid="stSubheader"] {
                font-size: clamp(1.45rem, 2.4vw, 2rem) !important;
            }

            h3,
            h4,
            p,
            label,
            [data-testid="stCaptionContainer"] {
                font-family: 'Outfit', sans-serif;
            }

            .teacher-welcome {
                margin: 0 0 0.7rem;
                color: var(--snap-text) !important;
                font-family: 'Outfit', sans-serif;
                font-size: clamp(1.25rem, 2vw, 1.7rem);
                font-weight: 750;
                line-height: 1.2;
            }

            .teacher-welcome span,
            .dashboard-page-title span {
                color: var(--snap-blue) !important;
            }

            .dashboard-page-title {
                margin: 0 0 1.25rem !important;
                color: var(--snap-text) !important;
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: clamp(2rem, 4vw, 3.5rem) !important;
                line-height: 1.12 !important;
            }

            [data-testid="stCaptionContainer"] {
                color: var(--snap-muted) !important;
            }

            [data-testid="stDivider"] {
                border-color: rgba(17, 19, 24, 0.14);
            }

            [data-testid="stButton"] button,
            [data-testid="stFormSubmitButton"] button {
                min-height: 2.75rem;
                padding: 0.65rem 1.15rem !important;
                border: 1px solid transparent !important;
                border-radius: 999px !important;
                background: var(--snap-blue) !important;
                color: #fff !important;
                font-family: 'Outfit', sans-serif;
                font-weight: 600;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }

            [data-testid="stButton"] button[kind="secondary"],
            [data-testid="stFormSubmitButton"] button[kind="secondary"] {
                background: var(--snap-pink) !important;
                color: #fff !important;
            }

            [data-testid="stButton"] button[kind="tertiary"],
            [data-testid="stFormSubmitButton"] button[kind="tertiary"] {
                background: var(--snap-dark) !important;
                color: #fff !important;
            }

            [data-testid="stButton"] button *,
            [data-testid="stFormSubmitButton"] button *,
            [data-testid="stButton"] button [data-testid="stMarkdownContainer"],
            [data-testid="stFormSubmitButton"] button [data-testid="stMarkdownContainer"] {
                color: #fff !important;
                fill: currentColor;
            }

            [data-testid="stButton"] button:hover,
            [data-testid="stFormSubmitButton"] button:hover {
                transform: translateY(-1px);
                box-shadow: 0 5px 14px rgba(17, 19, 24, 0.16);
            }

            [data-testid="stButton"] button:focus-visible,
            [data-testid="stFormSubmitButton"] button:focus-visible,
            [data-baseweb="select"]:focus-within,
            input:focus-visible,
            textarea:focus-visible {
                outline: 3px solid #111318 !important;
                outline-offset: 3px;
            }

            [data-testid="stButton"] button:disabled,
            [data-testid="stFormSubmitButton"] button:disabled {
                opacity: 0.55;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }

            [data-baseweb="select"] > div,
            [data-baseweb="input"] > div,
            [data-baseweb="textarea"] > div {
                border: 1px solid rgba(255, 255, 255, 0.16) !important;
                border-radius: 0.75rem !important;
                background: #202127 !important;
                color: #fff !important;
            }

            [data-baseweb="select"] input,
            [data-baseweb="input"] input,
            [data-baseweb="textarea"] textarea,
            [data-baseweb="select"] [role="combobox"] {
                color: #fff !important;
                -webkit-text-fill-color: #fff !important;
                font-family: 'Outfit', sans-serif;
            }

            [data-baseweb="select"] input::placeholder,
            [data-baseweb="input"] input::placeholder,
            [data-baseweb="textarea"] textarea::placeholder {
                color: #C4C7D0 !important;
                -webkit-text-fill-color: #C4C7D0 !important;
                opacity: 1;
            }

            [data-baseweb="popover"],
            [data-baseweb="menu"],
            [role="listbox"] {
                background: #202127 !important;
                color: #fff !important;
            }

            [role="option"] {
                color: #fff !important;
            }

            [role="option"]:hover,
            [role="option"][aria-selected="true"] {
                background: #343746 !important;
                color: #fff !important;
            }

            [data-testid="stDataFrame"],
            [data-testid="stTable"] {
                color: var(--snap-text);
            }

            /* Keep the Streamlit overlay transparent and only paint the actual dialog panel. */
            [data-testid="stDialog"] {
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                padding: 12px !important;
                overflow: hidden !important;
            }

            [data-testid="stDialog"] > div {
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                width: auto !important;
                max-width: 100% !important;
                max-height: 100% !important;
                margin: 0 !important;
            }

            [data-testid="stDialog"] [role="dialog"] {
                box-sizing: border-box !important;
                width: min(680px, calc(100vw - 40px)) !important;
                max-width: min(680px, calc(100vw - 40px)) !important;
                max-height: calc(100vh - 40px) !important;
                max-height: calc(100dvh - 40px) !important;
                overflow-y: auto !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 16px !important;
                background: transparent !important;
                color: #0F172A !important;
                box-shadow: none !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.create-subject-dialog),
            [data-testid="stDialog"] [role="dialog"]:has(.voice-attendance-dialog),
            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog),
            [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container) {
                background: #FFFFFF !important;
                border: 1px solid #E2E8F0 !important;
                box-shadow: 0 20px 50px rgba(15, 23, 42, 0.2) !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container) {
                display: flex !important;
                flex-direction: column !important;
                width: min(920px, calc(100vw - 32px)) !important;
                max-width: min(920px, calc(100vw - 32px)) !important;
                max-height: min(760px, calc(100vh - 32px)) !important;
                max-height: min(760px, calc(100dvh - 32px)) !important;
                min-height: 0 !important;
                overflow: hidden !important;
                border-radius: 16px !important;
                box-shadow: 0 16px 40px rgba(15, 23, 42, 0.16) !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container),
            [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container) *,
            [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container) *::before,
            [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container) *::after {
                box-sizing: border-box !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) {
                max-width: min(94vw, 680px) !important;
                width: min(94vw, 680px) !important;
            }

            [data-testid="stDialog"] [data-testid="stDialogContent"] {
                box-sizing: border-box !important;
                border: 0 !important;
                border-radius: 0 !important;
                background: transparent !important;
                color: #0F172A !important;
                padding: 1.1rem 1.5rem 1.25rem !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container) [data-testid="stDialogContent"] {
                display: flex !important;
                flex: 1 1 auto !important;
                flex-direction: column !important;
                min-height: 0 !important;
                overflow: hidden !important;
                padding: 0.5rem 1.375rem 0 !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container) > div {
                display: flex !important;
                flex: 1 1 auto !important;
                flex-direction: column !important;
                width: 100% !important;
                min-width: 0 !important;
                min-height: 0 !important;
                overflow: hidden !important;
                padding: 0.5rem 1.375rem 0 !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container) > div > [data-testid="stVerticalBlock"] {
                display: flex !important;
                flex: 1 1 auto !important;
                flex-direction: column !important;
                height: 100% !important;
                min-height: 0 !important;
                overflow: hidden !important;
                gap: 0.4rem !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container) [data-testid="stVerticalBlock"]:has(> [data-testid="stLayoutWrapper"] .st-key-attendance-review-list) {
                display: flex !important;
                flex: 1 1 auto !important;
                flex-direction: column !important;
                height: 100% !important;
                min-height: 0 !important;
                overflow: hidden !important;
                gap: 0.4rem !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container) [data-testid="stDialogContent"] > [data-testid="stVerticalBlock"] {
                display: flex !important;
                flex: 1 1 auto !important;
                flex-direction: column !important;
                height: 100% !important;
                min-height: 0 !important;
                gap: 0.4rem !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) [data-testid="stSegmentedControl"] {
                width: 100% !important;
                margin: 0.25rem 0 0.75rem !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) [data-testid="stSegmentedControl"] button {
                min-height: 2.5rem !important;
                border: 1px solid #D9DDF2 !important;
                border-radius: 0.65rem !important;
                background: #F5F6FF !important;
                color: #334155 !important;
                font-weight: 600 !important;
                box-shadow: none !important;
                transform: none !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) [data-testid="stSegmentedControl"] button[aria-pressed="true"] {
                border-color: #4F5FF5 !important;
                background: #4F5FF5 !important;
                color: #FFFFFF !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) [data-testid="stFileUploader"],
            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) .st-key-dialog_cam,
            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) [data-testid="stCameraInput"] {
                width: 100% !important;
                min-width: 0 !important;
                max-width: 100% !important;
                box-sizing: border-box !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) .st-key-dialog_cam,
            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) .st-key-dialog_cam > div,
            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) [data-testid="stCameraInput"],
            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) [data-testid="stCameraInput"] div {
                width: 100% !important;
                min-width: 0 !important;
                max-width: 100% !important;
                box-sizing: border-box !important;
                overflow: hidden !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) .st-key-dialog_cam,
            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) .st-key-dialog_cam > div,
            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) [data-testid="stCameraInput"] {
                overflow: hidden !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) [data-testid="stFileUploader"] section {
                width: 100% !important;
                min-width: 0 !important;
                border: 1px dashed #B8C0E8 !important;
                border-radius: 0.9rem !important;
                background: #F7F8FF !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) [data-testid="stFileUploader"] section button {
                border: 1px solid #4F5FF5 !important;
                border-radius: 0.65rem !important;
                background: #4F5FF5 !important;
                color: #FFFFFF !important;
                white-space: nowrap !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) .st-key-dialog_cam video,
            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) .st-key-dialog_cam img,
            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) [data-testid="stCameraInput"] video,
            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) [data-testid="stCameraInput"] img {
                display: block !important;
                width: 100% !important;
                max-width: 100% !important;
                max-height: min(38vh, 300px) !important;
                min-width: 0 !important;
                height: auto !important;
                aspect-ratio: auto !important;
                object-fit: contain !important;
                margin-inline: auto !important;
            }

            /* Keep the live camera in natural orientation; snapshots remain untransformed. */
            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) .st-key-dialog_cam video,
            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) [data-testid="stCameraInput"] video {
                transform: none !important;
                -webkit-transform: none !important;
            }

            [data-testid="stDialog"] [data-testid="stMarkdownContainer"],
            [data-testid="stDialog"] [data-testid="stWidgetLabel"] {
                color: #0F172A !important;
                font-family: 'Outfit', sans-serif !important;
            }

            [data-testid="stDialog"] h2,
            [data-testid="stDialog"] [data-testid="stHeading"] h2 {
                color: #0F172A !important;
                font-family: 'Outfit', sans-serif !important;
                font-size: 1.5rem !important;
                font-weight: 700 !important;
                letter-spacing: -0.01em !important;
                margin: 0 !important;
            }

            [data-testid="stDialog"] button[aria-label="Close"] {
                color: #64748B !important;
                border-radius: 8px !important;
                transition: all 0.2s ease !important;
            }

            [data-testid="stDialog"] button[aria-label="Close"]:hover {
                background: #F1F5F9 !important;
                color: #0F172A !important;
            }

            /* Attendance Review Header & Subtitle */
            .attendance-review-subtitle {
                font-family: 'Outfit', sans-serif !important;
                color: #64748B !important;
                font-size: 0.88rem !important;
                margin: 0 0 0.5rem 0 !important;
            }

            /* Dynamic Summary Cards */
            .attendance-summary-cards {
                display: grid !important;
                grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
                gap: 8px !important;
                margin-bottom: 0.25rem !important;
            }

            .summary-card {
                border-radius: 10px !important;
                padding: 8px 12px !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: center !important;
                min-height: 50px !important;
            }

            .card-total {
                background: #F8FAFC !important;
                border: 1px solid #E2E8F0 !important;
            }

            .card-total .summary-card-label {
                color: #64748B !important;
                font-size: 0.75rem !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.05em !important;
                font-family: 'Outfit', sans-serif !important;
            }

            .card-total .summary-card-value {
                color: #0F172A !important;
                font-size: 1.35rem !important;
                font-weight: 800 !important;
                line-height: 1.1 !important;
                margin-top: 4px !important;
                font-family: 'Outfit', sans-serif !important;
            }

            .card-present {
                background: #F0FDF4 !important;
                border: 1px solid #BBF7D0 !important;
            }

            .card-present .summary-card-label {
                color: #166534 !important;
                font-size: 0.75rem !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.05em !important;
                font-family: 'Outfit', sans-serif !important;
            }

            .card-present .summary-card-value {
                color: #15803D !important;
                font-size: 1.35rem !important;
                font-weight: 800 !important;
                line-height: 1.1 !important;
                margin-top: 4px !important;
                font-family: 'Outfit', sans-serif !important;
            }

            .card-absent {
                background: #FEF2F2 !important;
                border: 1px solid #FECACA !important;
            }

            .card-absent .summary-card-label {
                color: #991B1B !important;
                font-size: 0.75rem !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.05em !important;
                font-family: 'Outfit', sans-serif !important;
            }

            .card-absent .summary-card-value {
                color: #B91C1C !important;
                font-size: 1.35rem !important;
                font-weight: 800 !important;
                line-height: 1.1 !important;
                margin-top: 4px !important;
                font-family: 'Outfit', sans-serif !important;
            }

            /* Search Field within Dialog */
            [data-testid="stDialog"] [data-baseweb="input"] > div {
                border: 1px solid #E2E8F0 !important;
                border-radius: 8px !important;
                background: #F8FAFC !important;
                min-height: 40px !important;
                height: 40px !important;
            }

            [data-testid="stDialog"] [data-baseweb="input"] input {
                color: #0F172A !important;
                -webkit-text-fill-color: #0F172A !important;
                font-size: 0.88rem !important;
                font-family: 'Outfit', sans-serif !important;
            }

            [data-testid="stDialog"] [data-baseweb="input"] input::placeholder {
                color: #94A3B8 !important;
                -webkit-text-fill-color: #94A3B8 !important;
            }

            /* Table Header & Rows in Dialog */
            .table-header-cell {
                font-family: 'Outfit', sans-serif !important;
                font-size: 0.74rem !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.05em !important;
                color: #64748B !important;
                display: block !important;
                padding-bottom: 4px !important;
            }

            .student-name-cell {
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                font-size: 0.92rem !important;
                color: #0F172A !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
                display: block !important;
            }

            [data-testid="stDialog"] .st-key-attendance-review-list {
                box-sizing: border-box !important;
                flex: 1 1 0% !important;
                height: 0 !important;
                min-height: 0 !important;
                overflow-x: hidden !important;
                overflow-y: auto !important;
                scrollbar-gutter: stable;
            }

            [data-testid="stDialog"] [data-testid="stLayoutWrapper"]:has(.st-key-attendance-review-list) {
                box-sizing: border-box !important;
                flex: 1 1 0% !important;
                height: 0 !important;
                min-height: 0 !important;
                max-height: 100% !important;
                overflow: hidden !important;
            }

            [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stHorizontalBlock"] {
                gap: 0.5rem !important;
                align-items: center !important;
                padding: 0.2rem 0 !important;
                border-bottom: 1px solid #EEF0F5 !important;
            }

            [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stHorizontalBlock"] [data-testid="stColumn"] {
                min-width: 0 !important;
            }

            [data-testid="stDialog"] .st-key-attendance-review-header {
                position: sticky !important;
                top: 0 !important;
                z-index: 2 !important;
                background: #FFFFFF !important;
                border-bottom: 1px solid #E2E8F0 !important;
            }

            [data-testid="stDialog"] .st-key-attendance-review-header [data-testid="stHorizontalBlock"] {
                gap: 0.5rem !important;
                align-items: center !important;
                padding: 0.2rem 0 !important;
            }

            [data-testid="stDialog"] .st-key-attendance-review-list [data-baseweb="select"] > div {
                background: #F5F6FF !important;
                border-color: #D9DDF2 !important;
                border-radius: 8px !important;
                min-height: 42px !important;
                height: 42px !important;
            }

            [data-testid="stDialog"] .st-key-attendance-review-list [data-testid="stMarkdownContainer"] p {
                margin: 0 !important;
            }

            .student-id-cell {
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
                font-size: 0.78rem !important;
                color: #475569 !important;
                background: #F1F5F9 !important;
                padding: 2px 7px !important;
                border-radius: 4px !important;
                display: inline-block !important;
                white-space: nowrap !important;
            }

            .badge-source {
                font-size: 0.76rem !important;
                color: #475569 !important;
                background: #F8FAFC !important;
                border: 1px solid #E2E8F0 !important;
                padding: 2px 8px !important;
                border-radius: 6px !important;
                font-weight: 500 !important;
                display: inline-block !important;
                white-space: nowrap !important;
            }

            .badge-status {
                font-size: 0.76rem !important;
                font-weight: 600 !important;
                padding: 3px 9px !important;
                border-radius: 9999px !important;
                display: inline-flex !important;
                align-items: center !important;
                gap: 4px !important;
                white-space: nowrap !important;
            }

            .badge-present {
                background: #DCFCE7 !important;
                color: #15803D !important;
            }

            .badge-absent {
                background: #F1F5F9 !important;
                color: #64748B !important;
            }

            .badge-override {
                font-size: 0.68rem !important;
                font-weight: 700 !important;
                background: #FEF3C7 !important;
                color: #B45309 !important;
                padding: 2px 6px !important;
                border-radius: 4px !important;
                display: inline-block !important;
                margin-top: 2px !important;
            }

            /* Selectbox inside Dialog */
            [data-testid="stDialog"] [data-baseweb="select"] > div {
                border: 1px solid #CBD5E1 !important;
                border-radius: 8px !important;
                background: #FFFFFF !important;
                min-height: 38px !important;
                height: 38px !important;
            }

            [data-testid="stDialog"] [data-baseweb="select"] [role="combobox"],
            [data-testid="stDialog"] [data-baseweb="select"] input {
                color: #0F172A !important;
                -webkit-text-fill-color: #0F172A !important;
                font-size: 0.88rem !important;
                font-weight: 600 !important;
                font-family: 'Outfit', sans-serif !important;
            }

            [data-testid="stDialog"] [data-baseweb="popover"],
            [data-testid="stDialog"] [role="listbox"] {
                background: #FFFFFF !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 8px !important;
                box-shadow: 0 10px 25px rgba(15, 23, 42, 0.12) !important;
            }

            [data-testid="stDialog"] [role="option"] {
                color: #0F172A !important;
                font-family: 'Outfit', sans-serif !important;
                font-size: 0.88rem !important;
            }

            [data-testid="stDialog"] [role="option"]:hover,
            [data-testid="stDialog"] [role="option"][aria-selected="true"] {
                background: #F1F5F9 !important;
                color: #4F46E5 !important;
            }

            /* Footer Divider */
            [data-testid="stDialog"] .st-key-attendance-review-footer {
                box-sizing: border-box !important;
                flex: 0 0 auto !important;
                padding: 0.55rem 0 0.65rem !important;
                border-top: 1px solid #E2E8F0 !important;
                background: #FFFFFF !important;
            }

            /* Dialog Footer Action Buttons */
            [data-testid="stDialog"] .st-key-attendance-review-footer div[data-testid="stColumn"]:first-child button {
                background: #FFFFFF !important;
                border: 1px solid #CBD5E1 !important;
                color: #334155 !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                min-height: 2.75rem !important;
                transition: all 0.2s ease !important;
            }

            [data-testid="stDialog"] .st-key-attendance-review-footer div[data-testid="stColumn"]:first-child button p,
            [data-testid="stDialog"] .st-key-attendance-review-footer div[data-testid="stColumn"]:first-child button [data-testid="stMarkdownContainer"] {
                color: #334155 !important;
                -webkit-text-fill-color: #334155 !important;
            }

            [data-testid="stDialog"] .st-key-attendance-review-footer div[data-testid="stColumn"]:first-child button:hover {
                background: #F8FAFC !important;
                border-color: #94A3B8 !important;
                color: #0F172A !important;
            }

            [data-testid="stDialog"] .st-key-attendance-review-footer div[data-testid="stColumn"]:last-child button {
                background: #4F46E5 !important;
                border: 1px solid #4F46E5 !important;
                color: #FFFFFF !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                min-height: 2.75rem !important;
                box-shadow: 0 4px 14px rgba(79, 70, 229, 0.28) !important;
                transition: all 0.2s ease !important;
            }

            [data-testid="stDialog"] .st-key-attendance-review-footer div[data-testid="stColumn"]:last-child button p,
            [data-testid="stDialog"] .st-key-attendance-review-footer div[data-testid="stColumn"]:last-child button [data-testid="stMarkdownContainer"] {
                color: #FFFFFF !important;
                -webkit-text-fill-color: #FFFFFF !important;
            }

            [data-testid="stDialog"] .st-key-attendance-review-footer div[data-testid="stColumn"]:last-child button:hover {
                background: #4338CA !important;
                border-color: #4338CA !important;
                box-shadow: 0 6px 18px rgba(79, 70, 229, 0.38) !important;
            }

            [data-testid="stDialog"] [data-testid="stMarkdownContainer"],
            [data-testid="stDialog"] [data-testid="stWidgetLabel"],
            [data-testid="stDialog"] [data-testid="stHeading"] {
                color: var(--snap-text) !important;
            }

            @media (max-width: 640px) {
                .block-container {
                    padding: 1rem 0.85rem 1.5rem !important;
                }

                .snap-footer-dashboard {
                    margin: 1.25rem auto 0.75rem;
                    padding-inline: 0.5rem;
                }

                [data-testid="stButton"] button,
                [data-testid="stFormSubmitButton"] button {
                    width: 100%;
                    padding-inline: 0.8rem !important;
                }

                [data-testid="stDialog"] [data-testid="stDialogContent"] {
                    padding: 0.5rem 0.75rem 0 !important;
                }

                [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container) [data-testid="stDialogContent"] {
                    padding: 0.5rem 0.75rem 0 !important;
                }

                [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container) > div {
                    padding: 0.5rem 0.75rem 0 !important;
                }

                [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) {
                    max-width: 96vw !important;
                    width: 96vw !important;
                }

                [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) .st-key-dialog_cam video,
                [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) .st-key-dialog_cam img,
                [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) [data-testid="stCameraInput"] video,
                [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) [data-testid="stCameraInput"] img {
                    max-height: min(34vh, 240px) !important;
                }

                [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container) {
                    width: calc(100vw - 24px) !important;
                    max-width: 920px !important;
                    max-height: calc(100vh - 24px) !important;
                    max-height: calc(100dvh - 24px) !important;
                    margin: auto !important;
                    overflow: hidden !important;
                }

                [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container) [data-testid="stDialogContent"],
                [data-testid="stDialog"] .st-key-attendance-review-list,
                [data-testid="stDialog"] .st-key-attendance-review-footer {
                    box-sizing: border-box !important;
                    min-width: 0 !important;
                    max-width: 100% !important;
                }

                [data-testid="stDialog"] .st-key-attendance-review-list {
                    flex: 1 1 0% !important;
                    height: 0 !important;
                    min-height: 8rem !important;
                    overflow-x: hidden !important;
                    overflow-y: auto !important;
                    overscroll-behavior: contain !important;
                }

                .attendance-summary-cards {
                    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
                    gap: 6px !important;
                    margin-bottom: 0.25rem !important;
                }

                .summary-card {
                    min-height: 0 !important;
                    padding: 6px 8px !important;
                    overflow: hidden !important;
                }

                .summary-card-label {
                    font-size: 0.64rem !important;
                    line-height: 1.15 !important;
                    letter-spacing: 0.02em !important;
                }

                .summary-card-value {
                    font-size: 1.05rem !important;
                    margin-top: 2px !important;
                }

                @media (max-width: 350px) {
                    .attendance-summary-cards {
                        grid-template-columns: 1fr !important;
                    }
                }

                [data-testid="stDialog"] .st-key-attendance-review-header {
                    display: none !important;
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] {
                    display: block !important;
                    width: 100% !important;
                    min-width: 0 !important;
                    max-width: 100% !important;
                    margin: 0.35rem 0 !important;
                    padding: 0.45rem 0.65rem !important;
                    border: 1px solid #E2E8F0 !important;
                    border-radius: 10px !important;
                    background: #FFFFFF !important;
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] > div,
                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stVerticalBlock"] {
                    width: 100% !important;
                    min-width: 0 !important;
                    max-width: 100% !important;
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stHorizontalBlock"] {
                    display: block !important;
                    width: 100% !important;
                    min-width: 0 !important;
                    max-width: 100% !important;
                    padding: 0 !important;
                    border: 0 !important;
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stColumn"] {
                    display: grid !important;
                    width: 100% !important;
                    min-width: 0 !important;
                    max-width: 100% !important;
                    grid-template-columns: minmax(6rem, 34%) minmax(0, 1fr) !important;
                    align-items: center !important;
                    gap: 0.5rem !important;
                    padding: 0.2rem 0 !important;
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stColumn"]::before {
                    white-space: nowrap !important;
                    overflow: hidden !important;
                    text-overflow: ellipsis !important;
                    line-height: 1.2 !important;
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stMarkdownContainer"],
                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stMarkdownContainer"] > *,
                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] .student-name-cell,
                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] .student-id-cell,
                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] .badge-source,
                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] .badge-status {
                    min-width: 0 !important;
                    max-width: 100% !important;
                    white-space: nowrap !important;
                    word-break: normal !important;
                    overflow-wrap: normal !important;
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] .student-name-cell,
                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] .badge-source {
                    overflow: hidden !important;
                    text-overflow: ellipsis !important;
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] .student-id-cell {
                    justify-self: start !important;
                    overflow: visible !important;
                    text-overflow: clip !important;
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-baseweb="select"],
                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-baseweb="select"] > div {
                    width: 100% !important;
                    min-width: 0 !important;
                    max-width: 100% !important;
                    min-height: 44px !important;
                    height: 44px !important;
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stSelectbox"],
                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stSelectbox"] [role="group"] {
                    width: 100% !important;
                    min-width: 0 !important;
                    max-width: 100% !important;
                    min-height: 44px !important;
                    height: 44px !important;
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stSelectbox"] [role="combobox"] {
                    min-height: 42px !important;
                    height: 42px !important;
                    white-space: nowrap !important;
                    word-break: normal !important;
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stColumn"]:nth-child(1)::before {
                    content: "Student";
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stColumn"]:nth-child(2)::before {
                    content: "Student ID";
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stColumn"]:nth-child(3)::before {
                    content: "Source";
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stColumn"]:nth-child(4)::before {
                    content: "Detected";
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stColumn"]:nth-child(5)::before {
                    content: "Final status";
                }

                [data-testid="stDialog"] [class*="st-key-attendance-review-row-"] [data-testid="stColumn"]::before {
                    color: #64748B !important;
                    font-size: 0.75rem !important;
                    font-weight: 600 !important;
                }

                [data-testid="stDialog"] .st-key-attendance-review-footer button {
                    color: #334155 !important;
                }

                [data-testid="stDialog"] .st-key-attendance-review-footer div[data-testid="stColumn"]:last-child button {
                    color: #FFFFFF !important;
                }

                [data-testid="stDialog"] .st-key-attendance-review-footer {
                    padding: 0.65rem 0 0.75rem !important;
                }

                [data-testid="stDialog"] .st-key-attendance-review-footer [data-testid="stHorizontalBlock"] {
                    display: flex !important;
                    flex-direction: row !important;
                    gap: 8px !important;
                }

                [data-testid="stDialog"] .st-key-attendance-review-footer [data-testid="stColumn"] {
                    width: 50% !important;
                    min-width: 0 !important;
                    max-width: 50% !important;
                }
            }

            @media (prefers-reduced-motion: reduce) {
                *,
                *::before,
                *::after {
                    scroll-behavior: auto !important;
                    transition-duration: 0.01ms !important;
                    animation-duration: 0.01ms !important;
                }
            }

            /* Dialog sizing and layout override */
            [data-testid="stDialog"] {
                position: fixed !important;
                inset: 0 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                padding: 0 !important;
                overflow: visible !important;
                background: transparent !important;
            }

            [data-testid="stDialog"] > div {
                width: auto !important;
                display: block !important;
                background: transparent !important;
                margin: 0 auto !important;
            }

            [data-testid="stDialog"] [role="dialog"] {
                position: relative !important;
                box-sizing: border-box !important;
                width: min(560px, calc(100vw - 32px)) !important;
                max-width: calc(100vw - 32px) !important;
                max-height: calc(100dvh - 32px) !important;
                border-radius: 24px !important;
                border: 1px solid rgba(148, 163, 184, 0.22) !important;
                background: #FFFFFF !important;
                color: #0F172A !important;
                box-shadow: 0 24px 48px rgba(15, 23, 42, 0.18) !important;
                overflow: hidden !important;
                margin: 0 auto !important;
                display: flex !important;
                flex-direction: column !important;
            }

            [data-testid="stDialog"] [data-testid="stDialogContent"] {
                box-sizing: border-box !important;
                width: 100% !important;
                max-width: 100% !important;
                padding: 1rem 1.25rem 1.25rem !important;
                background: transparent !important;
                overflow: auto !important;
            }

            [data-testid="stDialog"] [role="dialog"] > div,
            [data-testid="stDialog"] [role="dialog"] [data-testid="stVerticalBlock"],
            [data-testid="stDialog"] [role="dialog"] [data-testid="stHorizontalBlock"],
            [data-testid="stDialog"] [role="dialog"] .stForm {
                width: 100% !important;
                max-width: 100% !important;
                box-sizing: border-box !important;
                min-width: 0 !important;
            }

            [data-testid="stDialog"] [role="dialog"] * {
                box-sizing: border-box !important;
            }

            [data-testid="stDialog"] [role="dialog"] p,
            [data-testid="stDialog"] [role="dialog"] .stMarkdown,
            [data-testid="stDialog"] [role="dialog"] label,
            [data-testid="stDialog"] [role="dialog"] .stTextInput,
            [data-testid="stDialog"] [role="dialog"] .stSelectbox,
            [data-testid="stDialog"] [role="dialog"] .stButton {
                max-width: 100% !important;
                min-width: 0 !important;
                overflow-wrap: anywhere !important;
                word-break: break-word !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.create-subject-dialog) {
                width: min(520px, calc(100vw - 32px)) !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.voice-attendance-dialog) {
                width: min(560px, calc(100vw - 32px)) !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.photo-upload-dialog) {
                width: min(760px, calc(100vw - 32px)) !important;
                max-width: calc(100vw - 32px) !important;
            }

            [data-testid="stDialog"] [role="dialog"]:has(.attendance-review-container) {
                width: min(900px, calc(100vw - 32px)) !important;
                max-width: calc(100vw - 32px) !important;
            }

            [data-testid="stDialog"] button[aria-label="Close"] {
                position: absolute !important;
                top: 12px !important;
                right: 12px !important;
                width: 32px !important;
                height: 32px !important;
                border-radius: 999px !important;
                border: 0 !important;
                background: transparent !important;
                color: #0F172A !important;
                font-size: 1.35rem !important;
                line-height: 1 !important;
                z-index: 2 !important;
            }

            [data-testid="stDialog"] button[aria-label="Close"]:hover {
                background: rgba(148, 163, 184, 0.12) !important;
            }

            [data-testid="stDialog"] [role="dialog"] .stButton button,
            [data-testid="stDialog"] [role="dialog"] [data-testid="stFormSubmitButton"] button {
                width: 100% !important;
                max-width: 100% !important;
            }

            @media (max-width: 640px) {
                [data-testid="stDialog"] {
                    padding: 14px !important;
                }

                [data-testid="stDialog"] [role="dialog"] {
                    width: min(100%, calc(100vw - 20px)) !important;
                    max-width: calc(100vw - 20px) !important;
                    max-height: calc(100dvh - 20px) !important;
                    border-radius: 18px !important;
                }

                [data-testid="stDialog"] [data-testid="stDialogContent"] {
                    padding: 0.75rem 0.85rem 1rem !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
