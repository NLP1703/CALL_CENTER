#!/usr/bin/env python3
"""Identite visuelle MDS partagee par les deux pages generees.

Couleurs relevees directement sur le logo de l'entreprise :
    navy  #1E428A  lettrage MDS et bandeau
    ambre #F6AE42  points de la courbe du logo
    cyan  #1EA8DE  extremite claire du degrade

Les couleurs de series (operateurs) restent celles validees pour la
lisibilite daltonienne : elles ne sont pas des couleurs de marque. Orange /
vert / bleu restent distincts en deuteranopie comme en protanopie.

Ce fichier est repris tel quel du projet JOB 001/26 (audit des agences) : seul
le tampon du bandeau change. Les deux questionnaires partagent la meme identite.
"""
from pathlib import Path

BASE = Path(__file__).resolve().parent

# Tampon du bandeau : identifie le job MDS sur les deux pages generees.
STAMP = "MDS JOB 002/26 · MS Ghost Check"

LOGO_BLANC = (BASE / "logo_mds_blanc.txt").read_text(encoding="utf-8").strip()
LOGO_COULEUR = (BASE / "logo_mds_couleur.txt").read_text(encoding="utf-8").strip()

POLICES = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=Archivo:wght@500;600;700&family=IBM+Plex+Mono:wght@500;600&'
    'family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">'
)

TOKENS = """
:root {
  /* --- identite MDS --- */
  --mds-navy:#1E428A; --mds-amber:#F6AE42; --mds-cyan:#1EA8DE;

  --plane:#EDF1F7; --card:#FBFCFE; --ink:#16233F; --ink-2:#3E4E70; --muted:#6B7A96;
  --rule:#D3DCE9; --rule-soft:#E4EAF3;
  --accent:#1E428A; --accent-soft:#E4EBF7; --accent-ink:#FFFFFF;
  --amber-ink:#8F5D06; --amber-soft:#FDF0DC;
  --band:#1E428A; --band-ink:#DCE6F5; --band-rule:rgba(255,255,255,.20);

  /* --- series (palette validee CVD, hors marque) --- */
  --op-orange:#eb6834; --op-mtn:#1baf7a; --op-camtel:#2a78d6;
  --op-wave:#b4508f;
  --vol:#1E428A; --vol-fill:rgba(30,66,138,.13);
  --st-good:#0ca30c; --st-warn:#fab219; --st-ser:#ec835a; --st-crit:#d03b3b;
  --ord-1:#86b6ef; --ord-2:#5598e7; --ord-3:#2a78d6; --ord-4:#1c5cab; --ord-5:#104281;
  --grid:#E1E6EF; --axis:#C6D0E0;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --plane:#0A1120; --card:#151C2B; --ink:#E6EBF5; --ink-2:#B6C2D8; --muted:#8797B2;
    --rule:#2A3448; --rule-soft:#202839;
    --accent:#6BA2E8; --accent-soft:#18233A; --accent-ink:#0A1120;
    --amber-ink:#F6AE42; --amber-soft:#2A2113;
    --band:#152A52; --band-ink:#D6E1F2; --band-rule:rgba(255,255,255,.16);

    --op-orange:#d95926; --op-mtn:#199e70; --op-camtel:#3987e5;
    --op-wave:#c76aa5;
    --vol:#8FB8EE; --vol-fill:rgba(143,184,238,.16);
    --ord-1:#184f95; --ord-2:#256abf; --ord-3:#3987e5; --ord-4:#6da7ec; --ord-5:#9ec5f4;
    --grid:#232C3D; --axis:#2E3950;
  }
}
:root[data-theme="dark"] {
  --plane:#0A1120; --card:#151C2B; --ink:#E6EBF5; --ink-2:#B6C2D8; --muted:#8797B2;
  --rule:#2A3448; --rule-soft:#202839;
  --accent:#6BA2E8; --accent-soft:#18233A; --accent-ink:#0A1120;
  --amber-ink:#F6AE42; --amber-soft:#2A2113;
  --band:#152A52; --band-ink:#D6E1F2; --band-rule:rgba(255,255,255,.16);

  --op-orange:#d95926; --op-mtn:#199e70; --op-camtel:#3987e5;
  --op-wave:#c76aa5;
  --vol:#8FB8EE; --vol-fill:rgba(143,184,238,.16);
  --ord-1:#184f95; --ord-2:#256abf; --ord-3:#3987e5; --ord-4:#6da7ec; --ord-5:#9ec5f4;
  --grid:#232C3D; --axis:#2E3950;
}
"""

BASE_CSS = """
* { box-sizing:border-box; }
body {
  margin:0; background:var(--plane); color:var(--ink);
  font-family:"IBM Plex Sans","Segoe UI",system-ui,sans-serif;
  font-size:15px; line-height:1.55; -webkit-font-smoothing:antialiased;
}
a { color:var(--accent); }
:focus-visible { outline:2px solid var(--mds-amber); outline-offset:2px; }

/* --- bandeau de marque --- */
.band { background:var(--band); color:var(--band-ink); padding:22px 26px 20px;
        border-bottom:3px solid var(--mds-amber); }
.band-in { max-width:1240px; margin:0 auto; display:flex; flex-wrap:wrap;
           justify-content:space-between; align-items:flex-end; gap:20px; }
.band-id { display:flex; align-items:center; gap:18px; }
.logo { height:52px; width:auto; flex:none; display:block; }
.band-sep { width:1px; align-self:stretch; background:var(--band-rule); flex:none; }
.stamp { font-family:"IBM Plex Mono",monospace; font-size:10.5px; font-weight:600;
         letter-spacing:.15em; text-transform:uppercase; color:var(--mds-amber);
         border:1px solid currentColor; padding:3px 8px; border-radius:2px;
         display:inline-block; }
.band h1 { font-family:Archivo,"Arial Narrow",sans-serif; font-weight:700;
           font-size:clamp(22px,3.2vw,32px); margin:10px 0 2px; letter-spacing:-.015em;
           line-height:1.1; text-wrap:balance; }
.band .role { margin:0; font-size:13.5px; opacity:.78; }
.band-side { font-family:"IBM Plex Mono",monospace; font-size:11.5px; text-align:right;
             opacity:.85; line-height:1.85; }
.band-side b { font-weight:600; opacity:.6; text-transform:uppercase; letter-spacing:.1em; }
@media (max-width:640px) {
  .band-side { text-align:left; }
  .logo { height:42px; }
}

.card { background:var(--card); border:1px solid var(--rule); border-radius:4px; }
table { width:100%; border-collapse:collapse; font-size:13px; }
th { text-align:left; font-size:10.5px; letter-spacing:.09em; text-transform:uppercase;
     color:var(--muted); font-weight:600; padding:0 10px 7px 0;
     border-bottom:1px solid var(--rule); }
td { padding:7px 10px 7px 0; border-bottom:1px solid var(--rule-soft); vertical-align:top; }
tr:last-child td { border-bottom:none; }
.num { text-align:right; font-variant-numeric:tabular-nums;
       font-family:"IBM Plex Mono",monospace; white-space:nowrap; }
.mono { font-family:"IBM Plex Mono",monospace; font-size:12px; white-space:nowrap; }
@media (prefers-reduced-motion:reduce) { *, *::before, *::after { transition:none !important;
                                                                  animation:none !important; } }
"""


def bandeau(titre, role, cotes):
    """Bandeau de marque commun. `cotes` : liste de couples (etiquette, valeur)."""
    lignes = "".join(f"<div><b>{k}</b> {v}</div>" for k, v in cotes)
    return f"""<header class="band">
  <div class="band-in">
    <div class="band-id">
      <img class="logo" src="{LOGO_BLANC}" alt="MDS — Marketing &amp; Distribution Services">
      <div class="band-sep"></div>
      <div>
        <span class="stamp">{STAMP}</span>
        <h1>{titre}</h1>
        <p class="role">{role}</p>
      </div>
    </div>
    <div class="band-side">{lignes}</div>
  </div>
</header>"""
