#!/usr/bin/env python3
"""Generate SVG placeholder "covers" for publications.

Each placeholder is the long-term fallback shown by research.html when a real
front-page PNG (rendered from a PDF by generate-paper-thumbs.sh) is missing.
Output: img/papers/placeholders/<basename>.svg

Edit the PAPERS table below and re-run:  python3 scripts/generate-paper-placeholders.py
"""

import html
import os

# (basename, title, [subtitle lines], authors, journal, year, bg-color)
PAPERS = [
    ("averett-2026-cdctc-fertility", "Child-Care Subsidies",
     ["Fertility & Birth", "Outcomes — Evidence", "from the CDCTC"],
     "with Yating Gong & Yang Wang",
     "Rev. Economics of the Household", "forthcoming", "#1f3d2b"),

    ("averett-2026-lgbtq-stem", "Not Thriving",
     ["LGBTQ+ Women in", "STEM Work"],
     "with Mary A. Armstrong",
     "J. Women & Minorities in Sci. & Eng.", "forthcoming", "#660000"),

    ("averett-2026-cdctc-health", "Child Care Credit",
     ["Long-Term Health Effects", "of Early Childhood", "Exposure"],
     "with Yating Gong & Yang Wang",
     "Health Economics", "forthcoming", "#1b3a5b"),

    ("averett-2025-one-child-fertility", "One-Child Policy",
     ["Fertility among Chinese", "Immigrants to the US"],
     "with Siyuan Lin & Laura M. Argys",
     "Rev. Economics of the Household", "2025", "#1f3d2b"),

    ("averett-2025-instate-tuition", "In-State Tuition",
     ["Undocumented Immigrants'", "Enrollment, Graduation", "& Employment"],
     "with Bansak, Condon & Dziadula",
     "J. Migration & Human Security", "2025", "#3d1f3d"),

    ("averett-2025-circadian", "Living in Sync",
     ["with the Sun — Sleep &", "Mental Health and", "Circadian Misalignment"],
     "with Laura M. Argys & Muzhe Yang",
     "Amer. J. of Health Economics", "2025", "#2f2f3a"),

    ("averett-2021-brain-gain", "Brain Gain or",
     ["Brain Drain? Student-", "Migrant Flows & Growth"],
     "with J. D. Rasamoelison & D. Stifel",
     "Applied Economics", "2021", "#3d1f3d"),

    ("averett-2021-minwage-immigrant-children", "Minimum Wages",
     ["Health & Access to Care", "of Immigrants' Children"],
     "with Julie K. Smith & Yang Wang",
     "Applied Economics Letters", "2021", "#5a3210"),

    ("averett-2021-light-pollution", "Light Pollution",
     ["Sleep Deprivation in", "Pregnancy & Infant Health"],
     "with Laura M. Argys & Muzhe Yang",
     "Southern Economic Journal", "2021", "#660000"),

    ("averett-2021-conscientious-woman", "Conscientious",
     ["Woman — Behind Every", "High-Earning Man"],
     "with Cynthia Bansak & Julie K. Smith",
     "J. Family & Economic Issues", "2021", "#1b3a5b"),

    ("averett-2020-aviation-noise", "Residential Noise",
     ["Aviation Noise &", "Birth Outcomes"],
     "with Laura M. Argys & Muzhe Yang",
     "J. Environ. Econ. & Management", "2020", "#1f3d2b"),

    ("averett-2020-hospitals-drg", "Do Hospitals",
     ["Respond to Incentives?", "Medicare DRG Reform"],
     "with Amanda Cook",
     "Journal of Health Economics", "2020", "#2f2f3a"),

    ("averett-2019-con-pennsylvania", "Taking the CON",
     ["out of Pennsylvania —", "Hip/Knee Replacement"],
     "with Sabrina Terrizzi & Yang Wang",
     "Health Policy & Technology", "2019", "#1f3d2b"),

    ("averett-2019-medicaid-opioid", "Medicaid Expansion",
     ["and Opioid Deaths"],
     "with Julie K. Smith & Yang Wang",
     "Health Economics", "2019", "#1b3a5b"),

    ("averett-2019-marijuana-opioid", "Medical Marijuana",
     ["Laws & Opioid-Related", "Mortality"],
     "with Emily Smith",
     "Economics Bulletin", "2019", "#660000"),
]

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 440" width="340" height="440" role="img" aria-label="{aria}">
  <rect width="340" height="440" fill="{bg}"/>
  <rect x="14" y="14" width="312" height="412" fill="none" stroke="rgba(255,255,255,0.18)" stroke-width="1"/>
  <g font-family="Georgia, 'Times New Roman', serif" fill="#ffffff">
    <text x="30" y="80" font-size="23" font-weight="700">{title}</text>
    <text x="30" y="118" font-size="14" font-style="italic" fill="rgba(255,255,255,0.85)">
{subtitle}
    </text>
    <text x="30" y="252" font-size="13" font-family="'Roboto', Arial, sans-serif" fill="rgba(255,255,255,0.75)">
      {authors}
    </text>
  </g>
  <rect x="0" y="370" width="340" height="70" fill="rgba(0,0,0,0.28)"/>
  <g font-family="Georgia, 'Times New Roman', serif" fill="#ffffff">
    <text x="30" y="398" font-size="14" font-style="italic">{journal}</text>
    <text x="30" y="420" font-size="13" fill="rgba(255,255,255,0.7)">{year}</text>
  </g>
</svg>
"""


def subtitle_tspans(lines):
    out = []
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else 20
        out.append(f'      <tspan x="30" dy="{dy}">{html.escape(line)}</tspan>')
    return "\n".join(out)


def main():
    root = os.path.join(os.path.dirname(__file__), "..")
    outdir = os.path.join(root, "img", "papers", "placeholders")
    os.makedirs(outdir, exist_ok=True)
    for base, title, subs, authors, journal, year, bg in PAPERS:
        svg = TEMPLATE.format(
            aria=html.escape(f"{title} — {journal}, {year}"),
            bg=bg,
            title=html.escape(title),
            subtitle=subtitle_tspans(subs),
            authors=html.escape(authors),
            journal=html.escape(journal),
            year=html.escape(year),
        )
        path = os.path.join(outdir, f"{base}.svg")
        with open(path, "w") as f:
            f.write(svg)
        print(f"wrote {os.path.relpath(path, root)}")


if __name__ == "__main__":
    main()
