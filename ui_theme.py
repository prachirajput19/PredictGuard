import html
import random
import streamlit as st
import streamlit.components.v1 as components
def _star_field(
    count: int,
    seed: int,
    max_x: int = 2400,
    max_y: int = 2400
) -> str:
    rng = random.Random(seed)
    return ", ".join(
        f"{rng.randint(0, max_x)}px {rng.randint(0, max_y)}px #FFF"
        for _ in range(count)
    )

_STARS_SMALL = _star_field(420, seed=50)
_STARS_MEDIUM = _star_field(110, seed=42)
_STARS_LARGE = _star_field(45, seed=53)
_STARS_TWINKLE = _star_field(70, seed=44)

# ============================================================
# MUCH MORE ACTIVE DEEP SPACE BACKGROUND
# ============================================================

_STARS_SMALL = _star_field(
    1000,
    seed=50,
    max_x=3000,
    max_y=3000
)

_STARS_MEDIUM = _star_field(
    260,
    seed=42,
    max_x=3000,
    max_y=3000
)

_STARS_LARGE = _star_field(
    100,
    seed=53,
    max_x=3000,
    max_y=3000
)

_STARS_TWINKLE = _star_field(
    150,
    seed=44,
    max_x=3000,
    max_y=3000
)


_COSMIC_BG_CSS = """

/* ============================================================
   DEEP SPACE INTELLIGENCE
   ULTRA ACTIVE COSMIC ENVIRONMENT
   ============================================================ */

.pg-cosmic-bg {

    position: fixed;
    inset: 0;

    z-index: 0;

    overflow: hidden;

    pointer-events: none;

    background:

        /* Purple nebula */
        radial-gradient(
            ellipse 80% 65%
            at 10% 10%,
            rgba(124, 58, 237, 0.22)
            0%,
            transparent 55%
        ),

        /* Cyan nebula */
        radial-gradient(
            ellipse 75% 60%
            at 90% 15%,
            rgba(56, 189, 248, 0.16)
            0%,
            transparent 55%
        ),

        /* Violet lower nebula */
        radial-gradient(
            ellipse 90% 70%
            at 50% 100%,
            rgba(139, 92, 246, 0.14)
            0%,
            transparent 60%
        ),

        /* Blue lower-right glow */
        radial-gradient(
            ellipse 60% 50%
            at 95% 90%,
            rgba(56, 189, 248, 0.10)
            0%,
            transparent 55%
        ),

        linear-gradient(
            180deg,
            #03050f 0%,
            #050816 35%,
            #080B1F 70%,
            #0B1026 100%
        );

}


/* ============================================================
   MOVING NEBULA
   ============================================================ */

.pg-nebula {

    position: absolute;

    inset: -25%;

    background:

        radial-gradient(
            circle at 18% 20%,
            rgba(124, 58, 237, 0.25)
            0%,
            transparent 35%
        ),

        radial-gradient(
            circle at 82% 18%,
            rgba(56, 189, 248, 0.20)
            0%,
            transparent 38%
        ),

        radial-gradient(
            circle at 48% 75%,
            rgba(139, 92, 246, 0.20)
            0%,
            transparent 40%
        ),

        radial-gradient(
            circle at 75% 65%,
            rgba(14, 165, 233, 0.10)
            0%,
            transparent 35%
        );

    filter:
        blur(30px);

    animation:
        pg-nebula-drift
        55s
        ease-in-out
        infinite
        alternate;

    will-change:
        transform;
}


@keyframes pg-nebula-drift {

    0% {

        transform:
            translate3d(
                -2%,
                -1%,
                0
            )
            scale(1);
    }

    25% {

        transform:
            translate3d(
                2%,
                1.5%,
                0
            )
            scale(1.04);
    }

    50% {

        transform:
            translate3d(
                -1%,
                3%,
                0
            )
            scale(1.07);
    }

    75% {

        transform:
            translate3d(
                3%,
                -2%,
                0
            )
            scale(1.03);
    }

    100% {

        transform:
            translate3d(
                -2%,
                2%,
                0
            )
            scale(1.06);
    }

}


/* ============================================================
   SECOND NEBULA MOTION LAYER
   ============================================================ */

.pg-nebula::after {

    content: "";

    position: absolute;

    inset: 5%;

    background:

        radial-gradient(
            ellipse at 30% 40%,
            rgba(99, 102, 241, 0.14),
            transparent 45%
        ),

        radial-gradient(
            ellipse at 70% 60%,
            rgba(14, 165, 233, 0.12),
            transparent 45%
        );

    filter:
        blur(45px);

    animation:
        pg-nebula-secondary
        80s
        ease-in-out
        infinite
        alternate;
}


@keyframes pg-nebula-secondary {

    0% {

        transform:
            translate(
                -4%,
                3%
            )
            rotate(0deg);
    }

    100% {

        transform:
            translate(
                5%,
                -4%
            )
            rotate(8deg);
    }

}


/* ============================================================
   STAR SYSTEM
   ============================================================ */

.pg-stars,
.pg-stars::after {

    position: absolute;

    width: 3px;

    height: 3px;

    background:
        transparent;

    border-radius:
        50%;
}


.pg-stars::after {

    content: "";

    top: 3000px;

}


/* ============================================================
   SMALL DISTANT STARS
   ============================================================ */

.pg-stars-small {

    box-shadow:
        __STARS_SMALL__;

    opacity:
        0.48;

    animation:
        pg-star-fall-small
        180s
        linear
        infinite;
}


.pg-stars-small::after {

    box-shadow:
        __STARS_SMALL__;
}


@keyframes pg-star-fall-small {

    from {

        transform:
            translate3d(
                0,
                0,
                0
            );
    }

    to {

        transform:
            translate3d(
                -120px,
                -3000px,
                0
            );
    }

}


/* ============================================================
   MEDIUM STARS
   ============================================================ */

.pg-stars-medium {

    box-shadow:
        __STARS_MEDIUM__;

    opacity:
        0.68;

    animation:
        pg-star-fall-medium
        125s
        linear
        infinite;
}


.pg-stars-medium::after {

    box-shadow:
        __STARS_MEDIUM__;
}


@keyframes pg-star-fall-medium {

    from {

        transform:
            translate3d(
                0,
                0,
                0
            );
    }

    to {

        transform:
            translate3d(
                160px,
                -3000px,
                0
            );
    }

}


/* ============================================================
   LARGE NEAR STARS
   ============================================================ */

.pg-stars-large {

    width: 4px;

    height: 4px;

    box-shadow:
        __STARS_LARGE__;

    opacity:
        0.90;

    animation:
        pg-star-fall-large
        85s
        linear
        infinite;
}


.pg-stars-large::after {

    box-shadow:
        __STARS_LARGE__;
}


@keyframes pg-star-fall-large {

    from {

        transform:
            translate3d(
                0,
                0,
                0
            )
            scale(1);
    }

    50% {

        transform:
            translate3d(
                -80px,
                -1500px,
                0
            )
            scale(1.08);
    }

    to {

        transform:
            translate3d(
                100px,
                -3000px,
                0
            )
            scale(1);
    }

}


/* ============================================================
   TWINKLING STARS
   ============================================================ */

.pg-stars-twinkle {

    width: 3px;

    height: 3px;

    box-shadow:
        __STARS_TWINKLE__;

    opacity:
        0.25;

    animation:
        pg-twinkle
        3.5s
        ease-in-out
        infinite;
}


.pg-stars-twinkle::after {

    box-shadow:
        __STARS_TWINKLE__;
}


@keyframes pg-twinkle {

    0% {

        opacity:
            0.08;

        transform:
            scale(0.7);
    }

    25% {

        opacity:
            0.35;
    }

    50% {

        opacity:
            0.85;

        transform:
            scale(1.35);
    }

    75% {

        opacity:
            0.30;
    }

    100% {

        opacity:
            0.08;

        transform:
            scale(0.7);
    }

}


/* ============================================================
   ORBITAL RINGS
   ============================================================ */

.pg-orbit {

    position: absolute;

    border:
        1px solid
        rgba(139, 92, 246, 0.10);

    border-radius:
        50%;

    will-change:
        transform;
}


.pg-orbit-1 {

    width:
        900px;

    height:
        900px;

    top:
        -320px;

    right:
        -280px;

    border-color:
        rgba(56, 189, 248, 0.10);

    animation:
        pg-orbit-spin
        160s
        linear
        infinite;
}


.pg-orbit-2 {

    width:
        1300px;

    height:
        1300px;

    bottom:
        -520px;

    left:
        -420px;

    border-color:
        rgba(139, 92, 246, 0.09);

    animation:
        pg-orbit-spin
        240s
        linear
        infinite
        reverse;
}


.pg-orbit-3 {

    width:
        650px;

    height:
        650px;

    top:
        15%;

    left:
        -280px;

    border-color:
        rgba(56, 189, 248, 0.07);

    animation:
        pg-orbit-spin
        130s
        linear
        infinite;
}


.pg-orbit-4 {

    width:
        1050px;

    height:
        1050px;

    right:
        -350px;

    bottom:
        5%;

    border-color:
        rgba(167, 139, 250, 0.07);

    animation:
        pg-orbit-spin
        190s
        linear
        infinite
        reverse;
}


@keyframes pg-orbit-spin {

    from {

        transform:
            rotate(0deg);
    }

    to {

        transform:
            rotate(360deg);
    }

}


/* ============================================================
   SHOOTING STARS
   ============================================================ */

.pg-shoot {

    position:
        absolute;

    width:
        3px;

    height:
        3px;

    border-radius:
        50%;

    background:
        #ffffff;

    box-shadow:
        0 0 5px
        rgba(255,255,255,0.95),

        0 0 12px
        rgba(56,189,248,0.85),

        0 0 22px
        rgba(139,92,246,0.55);

    opacity:
        0;

    will-change:
        transform,
        opacity;
}


/* Shooting star trail */

.pg-shoot::before {

    content:
        "";

    position:
        absolute;

    right:
        0;

    top:
        50%;

    width:
        140px;

    height:
        2px;

    transform:
        translateY(-50%);

    transform-origin:
        right center;

    background:
        linear-gradient(
            90deg,
            rgba(255,255,255,0.95),
            rgba(56,189,248,0.45),
            transparent
        );

    filter:
        blur(0.3px);
}


/* ============================================================
   SHOOTING STAR 1
   ============================================================ */

.pg-shoot-1 {

    top:
        8%;

    left:
        5%;

    animation:
        pg-shoot-1
        7s
        linear
        infinite;

    animation-delay:
        0s;
}


@keyframes pg-shoot-1 {

    0% {

        opacity:
            0;

        transform:
            translate(
                0,
                0
            )
            rotate(-35deg);
    }

    4% {

        opacity:
            1;
    }

    14% {

        opacity:
            0;

        transform:
            translate(
                500px,
                330px
            )
            rotate(-35deg);
    }

    100% {

        opacity:
            0;
    }

}


/* ============================================================
   SHOOTING STAR 2
   ============================================================ */

.pg-shoot-2 {

    top:
        20%;

    left:
        55%;

    animation:
        pg-shoot-2
        9s
        linear
        infinite;

    animation-delay:
        2s;
}


@keyframes pg-shoot-2 {

    0% {

        opacity:
            0;

        transform:
            translate(
                0,
                0
            )
            rotate(-40deg);
    }

    3% {

        opacity:
            1;
    }

    12% {

        opacity:
            0;

        transform:
            translate(
                600px,
                380px
            )
            rotate(-40deg);
    }

    100% {

        opacity:
            0;
    }

}


/* ============================================================
   SHOOTING STAR 3
   ============================================================ */

.pg-shoot-3 {

    top:
        42%;

    left:
        15%;

    animation:
        pg-shoot-3
        11s
        linear
        infinite;

    animation-delay:
        1s;
}


@keyframes pg-shoot-3 {

    0% {

        opacity:
            0;

        transform:
            translate(
                0,
                0
            )
            rotate(-32deg);
    }

    3% {

        opacity:
            1;
    }

    11% {

        opacity:
            0;

        transform:
            translate(
                450px,
                300px
            )
            rotate(-32deg);
    }

    100% {

        opacity:
            0;
    }

}


/* ============================================================
   SHOOTING STAR 4
   ============================================================ */

.pg-shoot-4 {

    top:
        65%;

    left:
        70%;

    animation:
        pg-shoot-4
        8s
        linear
        infinite;

    animation-delay:
        4s;
}


@keyframes pg-shoot-4 {

    0% {

        opacity:
            0;

        transform:
            translate(
                0,
                0
            )
            rotate(-42deg);
    }

    4% {

        opacity:
            1;
    }

    13% {

        opacity:
            0;

        transform:
            translate(
                520px,
                350px
            )
            rotate(-42deg);
    }

    100% {

        opacity:
            0;
    }

}


/* ============================================================
   SHOOTING STAR 5
   ============================================================ */

.pg-shoot-5 {

    top:
        32%;

    left:
        82%;

    animation:
        pg-shoot-5
        13s
        linear
        infinite;

    animation-delay:
        7s;
}


@keyframes pg-shoot-5 {

    0% {

        opacity:
            0;

        transform:
            translate(
                0,
                0
            )
            rotate(-35deg);
    }

    2% {

        opacity:
            1;
    }

    10% {

        opacity:
            0;

        transform:
            translate(
                480px,
                320px
            )
            rotate(-35deg);
    }

    100% {

        opacity:
            0;
    }

}


/* ============================================================
   SHOOTING STAR 6
   ============================================================ */

.pg-shoot-6 {

    top:
        78%;

    left:
        8%;

    animation:
        pg-shoot-6
        15s
        linear
        infinite;

    animation-delay:
        5s;
}


@keyframes pg-shoot-6 {

    0% {

        opacity:
            0;

        transform:
            translate(
                0,
                0
            )
            rotate(-30deg);
    }

    3% {

        opacity:
            1;
    }

    12% {

        opacity:
            0;

        transform:
            translate(
                520px,
                350px
            )
            rotate(-30deg);
    }

    100% {

        opacity:
            0;
    }

}


/* ============================================================
   SHOOTING STAR 7
   ============================================================ */

.pg-shoot-7 {

    top:
        12%;

    left:
        38%;

    animation:
        pg-shoot-7
        10s
        linear
        infinite;

    animation-delay:
        3s;
}


@keyframes pg-shoot-7 {

    0% {

        opacity:
            0;

        transform:
            translate(
                0,
                0
            )
            rotate(-45deg);
    }

    3% {

        opacity:
            1;
    }

    11% {

        opacity:
            0;

        transform:
            translate(
                430px,
                330px
            )
            rotate(-45deg);
    }

    100% {

        opacity:
            0;
    }

}


/* ============================================================
   SHOOTING STAR 8
   ============================================================ */

.pg-shoot-8 {

    top:
        55%;

    left:
        48%;

    animation:
        pg-shoot-8
        12s
        linear
        infinite;

    animation-delay:
        8s;
}


@keyframes pg-shoot-8 {

    0% {

        opacity:
            0;

        transform:
            translate(
                0,
                0
            )
            rotate(-38deg);
    }

    3% {

        opacity:
            1;
    }

    12% {

        opacity:
            0;

        transform:
            translate(
                550px,
                360px
            )
            rotate(-38deg);
    }

    100% {

        opacity:
            0;
    }

}


/* ============================================================
   SHOOTING STAR 9
   ============================================================ */

.pg-shoot-9 {

    top:
        88%;

    left:
        60%;

    animation:
        pg-shoot-9
        16s
        linear
        infinite;

    animation-delay:
        10s;
}


@keyframes pg-shoot-9 {

    0% {

        opacity:
            0;

        transform:
            translate(
                0,
                0
            )
            rotate(-33deg);
    }

    3% {

        opacity:
            1;
    }

    13% {

        opacity:
            0;

        transform:
            translate(
                500px,
                320px
            )
            rotate(-33deg);
    }

    100% {

        opacity:
            0;
    }

}


/* ============================================================
   SHOOTING STAR 10
   ============================================================ */

.pg-shoot-10 {

    top:
        72%;

    left:
        35%;

    animation:
        pg-shoot-10
        14s
        linear
        infinite;

    animation-delay:
        6s;
}


@keyframes pg-shoot-10 {

    0% {

        opacity:
            0;

        transform:
            translate(
                0,
                0
            )
            rotate(-40deg);
    }

    3% {

        opacity:
            1;
    }

    12% {

        opacity:
            0;

        transform:
            translate(
                570px,
                390px
            )
            rotate(-40deg);
    }

    100% {

        opacity:
            0;
    }

}


/* ============================================================
   SHOOTING STAR 11
   ============================================================ */

.pg-shoot-11 {

    top:
        25%;

    left:
        25%;

    animation:
        pg-shoot-11
        18s
        linear
        infinite;

    animation-delay:
        11s;
}


@keyframes pg-shoot-11 {

    0% {

        opacity:
            0;

        transform:
            translate(
                0,
                0
            )
            rotate(-37deg);
    }

    3% {

        opacity:
            1;
    }

    11% {

        opacity:
            0;

        transform:
            translate(
                620px,
                400px
            )
            rotate(-37deg);
    }

    100% {

        opacity:
            0;
    }

}


/* ============================================================
   SHOOTING STAR 12
   ============================================================ */

.pg-shoot-12 {

    top:
        48%;

    left:
        88%;

    animation:
        pg-shoot-12
        20s
        linear
        infinite;

    animation-delay:
        13s;
}


@keyframes pg-shoot-12 {

    0% {

        opacity:
            0;

        transform:
            translate(
                0,
                0
            )
            rotate(-43deg);
    }

    3% {

        opacity:
            1;
    }

    12% {

        opacity:
            0;

        transform:
            translate(
                520px,
                350px
            )
            rotate(-43deg);
    }

    100% {

        opacity:
            0;
    }

}


/* ============================================================
   FLOATING COSMIC PARTICLE GLOW
   ============================================================ */

.pg-cosmic-bg::before {

    content:
        "";

    position:
        absolute;

    width:
        500px;

    height:
        500px;

    border-radius:
        50%;

    background:
        radial-gradient(
            circle,
            rgba(56,189,248,0.07)
            0%,
            transparent 70%
        );

    top:
        20%;

    left:
        40%;

    filter:
        blur(20px);

    animation:
        pg-floating-glow
        25s
        ease-in-out
        infinite
        alternate;
}


@keyframes pg-floating-glow {

    0% {

        transform:
            translate(
                -150px,
                -80px
            )
            scale(0.8);

        opacity:
            0.3;
    }

    50% {

        transform:
            translate(
                100px,
                120px
            )
            scale(1.2);

        opacity:
            0.65;
    }

    100% {

        transform:
            translate(
                -80px,
                180px
            )
            scale(0.9);

        opacity:
            0.4;
    }

}


/* ============================================================
   ACCESSIBILITY
   ============================================================ */

@media (prefers-reduced-motion: reduce) {

    .pg-cosmic-bg *,
    .pg-cosmic-bg::before {

        animation:
            none !important;
    }

}


/* ============================================================
   MOBILE PERFORMANCE
   ============================================================ */

@media (max-width: 900px) {

    .pg-nebula {

        filter:
            blur(18px);
    }

    .pg-orbit {

        opacity:
            0.45;
    }

    .pg-shoot {

        opacity:
            0.7;
    }

}

"""

def render_cosmic_background():
    st.markdown(
        """<div class="pg-cosmic-bg" aria-hidden="true"><div class="pg-nebula"></div><div class="pg-stars pg-stars-small"></div><div class="pg-stars pg-stars-medium"></div><div class="pg-stars pg-stars-large"></div><div class="pg-stars pg-stars-twinkle"></div><div class="pg-orbit pg-orbit-1"></div><div class="pg-orbit pg-orbit-2"></div><div class="pg-orbit pg-orbit-3"></div><div class="pg-orbit pg-orbit-4"></div><div class="pg-shoot pg-shoot-1"></div><div class="pg-shoot pg-shoot-2"></div><div class="pg-shoot pg-shoot-3"></div><div class="pg-shoot pg-shoot-4"></div><div class="pg-shoot pg-shoot-5"></div><div class="pg-shoot pg-shoot-6"></div><div class="pg-shoot pg-shoot-7"></div><div class="pg-shoot pg-shoot-8"></div><div class="pg-shoot pg-shoot-9"></div><div class="pg-shoot pg-shoot-10"></div><div class="pg-shoot pg-shoot-11"></div><div class="pg-shoot pg-shoot-12"></div></div>
        """,
        unsafe_allow_html=True,
    )

def apply_custom_css():
    css = """
    <style>

    /* ============================================================
       PREDICTGUARD :: DEEP SPACE INTELLIGENCE
       COMPLETE UI + COSMIC ANIMATION THEME
       ============================================================ */

    /* =========================
       GOOGLE FONTS
       ========================= */

    @import url('https://fonts.googleapis.com/css2?family=Cactus+Classical+Serif&family=Playfair+Display:ital,wght@0,536;1,536&family=Sansation:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&display=swap');


    /* =========================
       GLOBAL VARIABLES
       ========================= */

    :root {

        --pg-bg: #050816;
        --pg-bg-alt: #080B1F;
        --pg-bg-deep: #0B1026;

        --pg-panel: rgba(11, 16, 38, 0.55);
        --pg-panel-strong: rgba(11, 16, 38, 0.78);
        --pg-panel-solid: #0B1026;

        --pg-border: rgba(139, 92, 246, 0.20);
        --pg-border-strong: rgba(56, 189, 248, 0.35);

        --pg-accent: #8B5CF6;
        --pg-accent-deep: #7C3AED;

        --pg-accent-2: #38BDF8;
        --pg-accent-2-deep: #60A5FA;

        --pg-text: #F8FAFC;
        --pg-text-dim: #94A3B8;
        --pg-text-muted: #64748B;

        /* Professional display font */
        --pg-font-display: 'Cactus Classical Serif', serif;

        /* Professional body font */
        --pg-font-body: 'Sansation', sans-serif;

        /* Elegant italic accent */
        --pg-font-elegant: 'Playfair Display', serif;
    }


    /* ============================================================
       GLOBAL PAGE
       ============================================================ */

    html,
    body {
        scroll-behavior: smooth;
        background: var(--pg-bg) !important;
    }

    .stApp {

        background: var(--pg-bg) !important;

        color: var(--pg-text);

        font-family: var(--pg-font-body);

        min-height: 100vh;
    }


    /* Remove unnecessary Streamlit backgrounds */

    [data-testid="stAppViewContainer"] {

        background: transparent !important;

        position: relative;

        z-index: 1;
    }

    [data-testid="stHeader"] {

        background: transparent !important;

        position: relative;

        z-index: 100;
    }

    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {

        position: relative;

        z-index: 100;
    }


    /* ============================================================
       MAIN CONTENT
       ============================================================ */

    .main .block-container {

        position: relative;

        z-index: 5;

        padding-top: 2rem;
        padding-bottom: 3rem;

        max-width: 1450px;
    }


    /* ============================================================
       TYPOGRAPHY
       ============================================================ */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6,

    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3,
    .stMarkdown h4,
    .stMarkdown h5,
    .stMarkdown h6 {

        font-family: var(--pg-font-display) !important;

        color: var(--pg-text) !important;

        letter-spacing: 0.02em;

        font-weight: 700;
    }


    /* Main body */

    p,
    span,
    div,
    label,
    li,
    td,
    th {

        font-family: var(--pg-font-body);
    }


    /* Elegant slightly-cursive text */

    .pg-cursive-accent {

        font-family: var(--pg-font-elegant) !important;

        font-style: italic !important;

        font-weight: 500;

        letter-spacing: 0.01em;
    }


    /* ============================================================
       SCROLLBAR
       ============================================================ */

    ::-webkit-scrollbar {

        width: 9px;
        height: 9px;
    }

    ::-webkit-scrollbar-track {

        background: var(--pg-bg);
    }

    ::-webkit-scrollbar-thumb {

        background: linear-gradient(
            180deg,
            #4c3d80,
            #263b62
        );

        border-radius: 20px;

        border: 2px solid var(--pg-bg);
    }

    ::-webkit-scrollbar-thumb:hover {

        background: linear-gradient(
            180deg,
            #7C3AED,
            #38BDF8
        );
    }

    * {

        scrollbar-width: thin;

        scrollbar-color:
            #3b2f63
            var(--pg-bg);
    }


    /* ============================================================
       STREAMLIT HEADER
       ============================================================ */

    header[data-testid="stHeader"] {

        background:
            rgba(5, 8, 22, 0.45) !important;

        backdrop-filter: blur(14px);

        -webkit-backdrop-filter: blur(14px);

        border-bottom:
            1px solid
            rgba(139, 92, 246, 0.15);

        box-shadow:
            0 4px 25px
            rgba(0, 0, 0, 0.25);
    }


    /* ============================================================
       SIDEBAR
       ============================================================ */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                rgba(8, 11, 31, 0.92),
                rgba(5, 8, 22, 0.88)
            );

        border-right:
            1px solid
            rgba(139, 92, 246, 0.22);

        backdrop-filter: blur(18px);

        -webkit-backdrop-filter: blur(18px);

        box-shadow:
            8px 0 35px
            rgba(0, 0, 0, 0.28);
    }


    section[data-testid="stSidebar"] .block-container {

        padding-top: 1.5rem;

        position: relative;

        z-index: 10;
    }


    /* Sidebar text */

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {

        color: #CBD5E1 !important;

        font-family: var(--pg-font-body) !important;
    }


    /* ============================================================
       METRIC CARDS
       ============================================================ */

    div[data-testid="stMetric"] {

        background:
            linear-gradient(
                135deg,
                rgba(17, 24, 50, 0.72),
                rgba(10, 15, 35, 0.58)
            );

        backdrop-filter: blur(15px) saturate(140%);

        -webkit-backdrop-filter: blur(15px) saturate(140%);

        border:
            1px solid
            var(--pg-border);

        border-radius: 14px;

        padding: 15px 18px;

        box-shadow:
            0 5px 22px
            rgba(0, 0, 0, 0.40);

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease;

        position: relative;

        overflow: hidden;
    }


    /* Animated light sweep */

    div[data-testid="stMetric"]::before {

        content: "";

        position: absolute;

        top: 0;
        left: -120%;

        width: 80%;
        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(56, 189, 248, 0.8),
                transparent
            );

        animation:
            pg-card-sweep 6s linear infinite;
    }


    @keyframes pg-card-sweep {

        0% {
            left: -120%;
        }

        45% {
            left: 130%;
        }

        100% {
            left: 130%;
        }
    }


    div[data-testid="stMetric"]:hover {

        transform:
            translateY(-4px)
            scale(1.01);

        border-color:
            rgba(56, 189, 248, 0.48);

        box-shadow:
            0 15px 35px
            rgba(56, 189, 248, 0.12),
            0 0 25px
            rgba(139, 92, 246, 0.14);
    }


    div[data-testid="stMetricLabel"] p {

        color: var(--pg-text-dim) !important;

        font-size: 0.76rem !important;

        font-weight: 700 !important;

        text-transform: uppercase;

        letter-spacing: 0.08em;

        font-family:
            var(--pg-font-body) !important;
    }


    div[data-testid="stMetricValue"] div {

        color: #F8FAFC !important;

        font-size: 1.65rem !important;

        font-weight: 700 !important;

        font-family:
            var(--pg-font-display) !important;

        text-shadow:
            0 0 14px
            rgba(56, 189, 248, 0.12);
    }


    /* ============================================================
       TABS
       ============================================================ */

    .stTabs [data-baseweb="tab-list"] {

        gap: 8px;

        border-bottom:
            1px solid
            var(--pg-border);

        padding-bottom: 5px;

        background: transparent;
    }


    .stTabs [data-baseweb="tab"] {

        background:
            rgba(11, 16, 38, 0.60);

        border:
            1px solid
            rgba(139, 92, 246, 0.18);

        border-radius: 9px;

        padding: 9px 18px;

        color: var(--pg-text-dim);

        font-weight: 600;

        font-size: 0.82rem;

        font-family:
            var(--pg-font-body);

        letter-spacing: 0.03em;

        transition:
            all 0.25s ease;

        backdrop-filter: blur(10px);
    }


    .stTabs [data-baseweb="tab"]:hover {

        background:
            rgba(139, 92, 246, 0.13);

        color: #F1F5F9;

        border-color:
            rgba(56, 189, 248, 0.55);

        transform:
            translateY(-1px);
    }


    .stTabs [aria-selected="true"] {

        background:
            linear-gradient(
                135deg,
                rgba(139, 92, 246, 0.25),
                rgba(56, 189, 248, 0.14)
            ) !important;

        color:
            #E0F2FE !important;

        border-color:
            var(--pg-accent-2) !important;

        font-weight:
            700 !important;

        box-shadow:
            0 0 18px
            rgba(56, 189, 248, 0.20);
    }


    /* ============================================================
       BUTTONS
       ============================================================ */

    .stButton > button {

        background:
            linear-gradient(
                135deg,
                rgba(17, 20, 41, 0.92),
                rgba(12, 18, 38, 0.90)
            );

        color:
            #F1F5F9;

        border:
            1px solid
            rgba(139, 92, 246, 0.35);

        border-radius: 9px;

        font-weight: 700;

        font-family:
            var(--pg-font-body);

        font-size: 0.84rem;

        padding:
            0.52rem 1.15rem;

        transition:
            all 0.22s ease;

        position: relative;

        overflow: hidden;
    }


    .stButton > button::before {

        content: "";

        position: absolute;

        top: 0;

        left: -100%;

        width: 100%;

        height: 100%;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(255,255,255,0.08),
                transparent
            );

        transition:
            left 0.5s ease;
    }


    .stButton > button:hover {

        background:
            linear-gradient(
                135deg,
                #7C3AED,
                #38BDF8
            );

        color: #FFFFFF;

        border-color:
            #38BDF8;

        box-shadow:
            0 0 22px
            rgba(139, 92, 246, 0.42);

        transform:
            translateY(-2px);
    }


    .stButton > button:hover::before {

        left: 100%;
    }


    .stButton > button:active {

        transform:
            scale(0.97);
    }


    /* ============================================================
       INPUTS
       ============================================================ */

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stTextArea textarea {

        background:
            rgba(11, 16, 38, 0.82) !important;

        color:
            #F8FAFC !important;

        border:
            1px solid
            rgba(139, 92, 246, 0.25) !important;

        border-radius:
            9px !important;

        font-family:
            var(--pg-font-body) !important;

        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }


    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea textarea:focus {

        border-color:
            #38BDF8 !important;

        box-shadow:
            0 0 0 1px #38BDF8,
            0 0 15px
            rgba(56, 189, 248, 0.16) !important;
    }


    /* ============================================================
       SELECT BOX
       ============================================================ */

    [data-baseweb="select"] > div {

        background:
            rgba(11, 16, 38, 0.82) !important;

        border-color:
            rgba(139, 92, 246, 0.25) !important;

        color:
            #F8FAFC !important;

        border-radius:
            9px !important;
    }


    /* ============================================================
       EXPANDERS
       ============================================================ */

    div[data-testid="stExpander"] {

        background:
            rgba(11, 16, 38, 0.58);

        backdrop-filter:
            blur(14px);

        -webkit-backdrop-filter:
            blur(14px);

        border:
            1px solid
            var(--pg-border);

        border-radius:
            11px;

        margin-bottom:
            0.8rem;

        transition:
            border-color 0.25s ease,
            box-shadow 0.25s ease;
    }


    div[data-testid="stExpander"]:hover {

        border-color:
            rgba(56, 189, 248, 0.38);

        box-shadow:
            0 8px 24px
            rgba(0, 0, 0, 0.22);
    }


    div[data-testid="stExpander"] summary {

        font-weight: 700;

        color: #CBD5E1;

        font-family:
            var(--pg-font-body);
    }


    /* ============================================================
       DATAFRAME
       ============================================================ */

    div[data-testid="stDataFrame"] {

        border:
            1px solid
            var(--pg-border-strong);

        border-radius:
            10px;

        overflow:
            hidden;

        box-shadow:
            0 5px 22px
            rgba(0, 0, 0, 0.25);
    }


    /* ============================================================
       SLIDER
       ============================================================ */

    div[data-testid="stSlider"] [role="slider"] {

        background-color:
            #8B5CF6 !important;

        box-shadow:
            0 0 10px
            rgba(139, 92, 246, 0.65);

        border:
            2px solid
            #C4B5FD !important;
    }


    /* ============================================================
       CHECKBOX / RADIO
       ============================================================ */

    .stCheckbox label,
    .stRadio label {

        font-family:
            var(--pg-font-body) !important;

        color:
            #CBD5E1 !important;
    }


    /* ============================================================
       GLASS CARD
       ============================================================ */

    .pg-glass-card {

        background:
            linear-gradient(
                135deg,
                rgba(17, 24, 50, 0.62),
                rgba(8, 13, 31, 0.56)
            );

        backdrop-filter:
            blur(18px)
            saturate(150%);

        -webkit-backdrop-filter:
            blur(18px)
            saturate(150%);

        border:
            1px solid
            var(--pg-border);

        border-radius:
            14px;

        padding:
            16px 20px;

        margin-bottom:
            12px;

        box-shadow:
            0 5px 25px
            rgba(0, 0, 0, 0.45);

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease;

        position:
            relative;

        overflow:
            hidden;
    }


    .pg-glass-card::after {

        content: "";

        position:
            absolute;

        width:
            160px;

        height:
            160px;

        top:
            -100px;

        right:
            -80px;

        background:
            radial-gradient(
                circle,
                rgba(56, 189, 248, 0.09),
                transparent 70%
            );

        pointer-events:
            none;
    }


    .pg-glass-card:hover {

        transform:
            translateY(-4px);

        border-color:
            rgba(56, 189, 248, 0.44);

        box-shadow:
            0 18px 38px
            rgba(0, 0, 0, 0.42),
            0 0 24px
            rgba(139, 92, 246, 0.13);
    }


    .pg-glass-card.critical:hover {

        border-color:
            rgba(239, 68, 68, 0.58);

        box-shadow:
            0 15px 35px
            rgba(239, 68, 68, 0.20);
    }


    /* ============================================================
       SAAS CARD
       ============================================================ */

    .saas-card {

        background:
            rgba(11, 16, 38, 0.58);

        backdrop-filter:
            blur(14px);

        -webkit-backdrop-filter:
            blur(14px);

        border:
            1px solid
            var(--pg-border);

        border-radius:
            12px;

        padding:
            16px 20px;

        margin-bottom:
            14px;

        box-shadow:
            0 5px 20px
            rgba(0, 0, 0, 0.38);

        transition:
            transform 0.22s ease,
            box-shadow 0.22s ease,
            border-color 0.22s ease;
    }


    .saas-card:hover {

        transform:
            translateY(-3px);

        border-color:
            rgba(56, 189, 248, 0.35);

        box-shadow:
            0 14px 30px
            rgba(56, 189, 248, 0.13);
    }


    /* ============================================================
       BADGES
       ============================================================ */

    .saas-badge {

        display:
            inline-block;

        padding:
            3px 8px;

        font-size:
            0.70rem;

        font-weight:
            700;

        text-transform:
            uppercase;

        letter-spacing:
            0.07em;

        border-radius:
            5px;

        font-family:
            var(--pg-font-body);
    }


    /* Critical */

    .badge-critical {

        background-color:
            rgba(239, 68, 68, 0.15);

        color:
            #F87171;

        border:
            1px solid
            rgba(239, 68, 68, 0.4);

        animation:
            pg-pulse-critical 1.6s ease-in-out infinite,
            pg-pulse-glow-border 1.6s ease-in-out infinite;
    }


    /* High */

    .badge-high {

        background-color:
            rgba(249, 115, 22, 0.15);

        color:
            #FB923C;

        border:
            1px solid
            rgba(249, 115, 22, 0.4);
    }


    /* Medium */

    .badge-medium {

        background-color:
            rgba(234, 179, 8, 0.15);

        color:
            #FACC15;

        border:
            1px solid
            rgba(234, 179, 8, 0.4);
    }


    /* Low */

    .badge-low {

        background-color:
            rgba(56, 189, 248, 0.15);

        color:
            #60A5FA;

        border:
            1px solid
            rgba(56, 189, 248, 0.4);
    }


    /* Verified */

    .badge-verified {

        background-color:
            rgba(16, 185, 129, 0.15);

        color:
            #34D399;

        border:
            1px solid
            rgba(16, 185, 129, 0.4);
    }


    /* Neutral */

    .badge-neutral {

        background-color:
            rgba(148, 163, 184, 0.15);

        color:
            #94A3B8;

        border:
            1px solid
            rgba(148, 163, 184, 0.3);
    }


    /* ============================================================
       FADE + ENTRANCE ANIMATIONS
       ============================================================ */

    @keyframes pg-fade-slide-up {

        0% {

            opacity: 0;

            transform:
                translateY(18px);
        }

        100% {

            opacity: 1;

            transform:
                translateY(0);
        }
    }


    @keyframes pg-fade-slide-left {

        0% {

            opacity: 0;

            transform:
                translateX(-18px);
        }

        100% {

            opacity: 1;

            transform:
                translateX(0);
        }
    }


    @keyframes pg-fade-slide-right {

        0% {

            opacity: 0;

            transform:
                translateX(18px);
        }

        100% {

            opacity: 1;

            transform:
                translateX(0);
        }
    }


    .pg-fade-in {

        animation:
            pg-fade-slide-up
            0.55s
            cubic-bezier(
                0.16,
                1,
                0.3,
                1
            )
            both;
    }


    .pg-fade-in.d1 {
        animation-delay: 0.04s;
    }

    .pg-fade-in.d2 {
        animation-delay: 0.11s;
    }

    .pg-fade-in.d3 {
        animation-delay: 0.18s;
    }

    .pg-fade-in.d4 {
        animation-delay: 0.25s;
    }

    .pg-fade-in.d5 {
        animation-delay: 0.32s;
    }

    .pg-fade-in.d6 {
        animation-delay: 0.39s;
    }


    /* ============================================================
       LIVE INDICATOR
       ============================================================ */

    @keyframes pg-pulse-dot {

        0% {

            box-shadow:
                0 0 0 0
                rgba(52, 211, 153, 0.55);
        }

        70% {

            box-shadow:
                0 0 0 8px
                rgba(52, 211, 153, 0);
        }

        100% {

            box-shadow:
                0 0 0 0
                rgba(52, 211, 153, 0);
        }
    }


    .pg-live-dot {

        display:
            inline-block;

        width:
            8px;

        height:
            8px;

        border-radius:
            50%;

        background:
            #34D399;

        margin-right:
            6px;

        animation:
            pg-pulse-dot
            1.8s
            infinite;

        position:
            relative;

        top:
            -1px;
    }


    .pg-live-chip {

        display:
            inline-flex;

        align-items:
            center;

        font-size:
            0.67rem;

        font-weight:
            700;

        letter-spacing:
            0.09em;

        color:
            #34D399;

        background:
            rgba(16, 185, 129, 0.12);

        border:
            1px solid
            rgba(16, 185, 129, 0.35);

        padding:
            4px 10px 4px 8px;

        border-radius:
            999px;

        text-transform:
            uppercase;

        font-family:
            var(--pg-font-body);

        box-shadow:
            0 0 12px
            rgba(16, 185, 129, 0.08);
    }


    /* ============================================================
       CRITICAL PULSE
       ============================================================ */

    @keyframes pg-pulse-critical {

        0%,
        100% {

            box-shadow:
                0 0 0 0
                rgba(239, 68, 68, 0.45);
        }

        50% {

            box-shadow:
                0 0 0 7px
                rgba(239, 68, 68, 0);
        }
    }


    @keyframes pg-pulse-glow-border {

        0%,
        100% {

            border-color:
                rgba(239, 68, 68, 0.40);
        }

        50% {

            border-color:
                rgba(248, 113, 113, 0.90);
        }
    }


    /* ============================================================
       COSMIC BACKGROUND
       ============================================================ */

    """ + _COSMIC_BG_CSS.replace(
        "__STARS_SMALL__",
        _STARS_SMALL
    ).replace(
        "__STARS_MEDIUM__",
        _STARS_MEDIUM
    ).replace(
        "__STARS_LARGE__",
        _STARS_LARGE
    ).replace(
        "__STARS_TWINKLE__",
        _STARS_TWINKLE
    ) + """

    /* ============================================================
       REDUCED MOTION ACCESSIBILITY
       ============================================================ */

    @media (prefers-reduced-motion: reduce) {

        *,
        *::before,
        *::after {

            animation-duration:
                0.01ms !important;

            animation-iteration-count:
                1 !important;

            scroll-behavior:
                auto !important;

            transition-duration:
                0.01ms !important;
        }
    }


    /* ============================================================
       MOBILE OPTIMIZATION
       ============================================================ */

    @media (max-width: 900px) {

        .main .block-container {

            padding-left:
                1rem;

            padding-right:
                1rem;
        }

        .pg-glass-card {

            padding:
                14px 16px;
        }

        .stTabs [data-baseweb="tab"] {

            padding:
                8px 12px;

            font-size:
                0.76rem;
        }
    }


    @media (max-width: 600px) {

        h1 {

            font-size:
                1.45rem !important;
        }

        h2 {

            font-size:
                1.2rem !important;
        }

        h3 {

            font-size:
                1rem !important;
        }

        .pg-glass-card {

            border-radius:
                11px;

            padding:
                13px 14px;
        }

        .stButton > button {

            width:
                100%;
        }
    }

    </style>
    """

    st.markdown(
        css,
        unsafe_allow_html=True
    )


    render_cosmic_background()


def render_brand_header():
    st.markdown(
        """<div class="pg-fade-in d1" style="padding:6px 0 16px;border-bottom:1px solid rgba(139,92,246,.18);margin-bottom:18px"><div style="display:flex;align-items:baseline;gap:12px;flex-wrap:wrap"><span style="font-family:'Playfair Display',serif;font-size:2.875rem;font-weight:800;letter-spacing:.02em;background:linear-gradient(90deg,#F1F5F9 0%,#D4AF37 55%,#F1F5F9 120%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent">PREDICTGUARD</span><span class="pg-accent-text" style="font-size:.82rem;color:#38bdf8;letter-spacing:.04em;white-space:nowrap">Deep Space Intelligence</span><span class="pg-live-chip"><span class="pg-live-dot"></span>LIVE</span></div></div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_card(
    label: str,
    value: str,
    subtitle: str = "",
    border_color: str = "#1f293d"
):

    """
    Renders a sleek static intelligence-signal card.

    Typography:
    Label -> DM Sans
    Value -> Space Grotesk
    Subtitle -> DM Sans
    """

    st.markdown(
        f"""
        <div class="pg-glass-card">

            <div
                style="
                    color: #94a3b8;

                    font-size: 0.76rem;

                    font-weight: 700;

                    text-transform: uppercase;

                    letter-spacing: 0.06em;

                    font-family:
                        var(--pg-font-body);
                "
            >
                {label}
            </div>


            <div
                style="
                    color: #f8fafc;

                    font-size: 1.65rem;

                    font-weight: 700;

                    margin: 4px 0 2px 0;

                    font-family:
                        var(--pg-font-display);
                "
            >
                {value}
            </div>


            <div
                style="
                    color: #64748b;

                    font-size: 0.75rem;

                    font-family:
                        var(--pg-font-body);
                "
            >
                {subtitle}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


def render_animated_kpi_card(
    label: str,
    value: float,
    subtitle: str = "",
    prefix: str = "",
    suffix: str = "",
    decimals: int = 0,
    accent: str = "#38bdf8",
    delay_ms: int = 0,
    height: int = 118,
):

    """
    Renders a glassmorphic animated KPI card.

    Typography:
    Label -> DM Sans
    Value -> Space Grotesk
    Subtitle -> DM Sans
    """

    safe_label = html.escape(label)

    safe_subtitle = html.escape(
        subtitle
    )

    target = float(value)


    widget_html = f"""

    <div
        style="
            font-family:
                'DM Sans',
                sans-serif;
        "
    >

        <style>

            html,
            body {{

                background:
                    transparent;

                margin:
                    0;

                padding:
                    0;
            }}


            /* ====================================================
               KPI CARD
               ==================================================== */

            .card {{

                background:
                    rgba(11, 16, 38, 0.55);

                backdrop-filter:
                    blur(16px)
                    saturate(150%);

                -webkit-backdrop-filter:
                    blur(16px)
                    saturate(150%);

                border:
                    1px solid
                    rgba(139, 92, 246, 0.20);

                border-radius:
                    14px;

                padding:
                    14px 18px;

                box-shadow:
                    0 4px 20px -6px
                    rgba(0,0,0,0.45);

                transition:
                    transform 0.18s ease,
                    box-shadow 0.18s ease,
                    border-color 0.18s ease;

                opacity:
                    0;

                transform:
                    translateY(14px);

                animation:
                    fadeUp
                    0.5s
                    cubic-bezier(0.16,1,0.3,1)
                    {delay_ms}ms
                    forwards;

                box-sizing:
                    border-box;
            }}


            .card:hover {{

                transform:
                    translateY(-3px);

                border-color:
                    rgba(56, 189, 248, 0.45);

                box-shadow:
                    0 16px 32px -10px
                    rgba(139, 92, 246, 0.3);
            }}


            /* ====================================================
               ANIMATION
               ==================================================== */

            @keyframes fadeUp {{

                from {{

                    opacity:
                        0;

                    transform:
                        translateY(14px);
                }}

                to {{

                    opacity:
                        1;

                    transform:
                        translateY(0);
                }}

            }}


            /* ====================================================
               LABEL
               ==================================================== */

            .label {{

                color:
                    #94a3b8;

                font-size:
                    0.76rem;

                font-weight:
                    700;

                text-transform:
                    uppercase;

                letter-spacing:
                    0.06em;

                font-family:
                    'DM Sans',
                    sans-serif;
            }}


            /* ====================================================
               KPI VALUE
               ==================================================== */

            .value {{

                color:
                    #f8fafc;

                font-size:
                    1.7rem;

                font-weight:
                    700;

                margin:
                    4px 0 2px 0;

                font-family:
                    'Space Grotesk',
                    sans-serif;

                letter-spacing:
                    0.01em;
            }}


            /* ====================================================
               SUBTITLE
               ==================================================== */

            .subtitle {{

                color:
                    #64748b;

                font-size:
                    0.75rem;

                font-family:
                    'DM Sans',
                    sans-serif;
            }}

        </style>


        <!-- KPI CARD -->

        <div class="card">

            <div class="label">
                {safe_label}
            </div>


            <div
                class="value"
                id="val"
                style="
                    color:{accent};
                "
            >
            </div>


            <div class="subtitle">
                {safe_subtitle}
            </div>

        </div>


        <!-- COUNT-UP ANIMATION -->

        <script>

            (function() {{

                const el =
                    document.getElementById('val');

                const target =
                    {target};

                const decimals =
                    {decimals};

                const prefix =
                    {prefix!r};

                const suffix =
                    {suffix!r};

                const duration =
                    900;

                const start =
                    performance.now();


                function fmt(n) {{

                    return prefix +
                        n.toLocaleString(
                            undefined,
                            {{
                                minimumFractionDigits:
                                    decimals,

                                maximumFractionDigits:
                                    decimals
                            }}
                        ) +
                        suffix;
                }}


                function easeOutQuad(t) {{

                    return t * (2 - t);
                }}


                function tick(now) {{

                    const p =
                        Math.min(
                            1,
                            (now - start)
                            / duration
                        );


                    const eased =
                        easeOutQuad(p);


                    el.textContent =
                        fmt(
                            target * eased
                        );


                    if (p < 1) {{

                        requestAnimationFrame(
                            tick
                        );

                    }} else {{

                        el.textContent =
                            fmt(target);
                    }}

                }}


                requestAnimationFrame(
                    tick
                );

            }})();

        </script>

    </div>
    """


    components.html(
        widget_html,
        height=height
    )


def get_severity_badge_html(
    risk_score: float
) -> str:

    """
    Returns HTML for a risk badge based on score.
    """

    if risk_score >= 0.8:

        return (
            '<span '
            'class="saas-badge badge-critical">'
            'CRITICAL'
            '</span>'
        )

    elif risk_score >= 0.6:

        return (
            '<span '
            'class="saas-badge badge-high">'
            'HIGH'
            '</span>'
        )

    elif risk_score >= 0.3:

        return (
            '<span '
            'class="saas-badge badge-medium">'
            'MEDIUM'
            '</span>'
        )

    else:

        return (
            '<span '
            'class="saas-badge badge-low">'
            'LOW'
            '</span>'
        )