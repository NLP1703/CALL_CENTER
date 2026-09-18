#!/usr/bin/env python3
"""Client CLI pour KoboToolbox : deploiement de XLSForms et recuperation des donnees.

Usage :
    python kobo.py list
    python kobo.py deploy <fichier.xlsx> [--name "Nom du projet"]
    python kobo.py redeploy <uid> <fichier.xlsx>
    python kobo.py data <uid> [--out data/soumissions.json]
    python kobo.py export <uid> [--type xls|csv] [--out exports/]
    python kobo.py info <uid>
    python kobo.py media <uid> [image.png]
    python kobo.py langues <uid> [--nettoyer]
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parent


def charger_env():
    """Lit .env sans dependance externe."""
    fichier = BASE / ".env"
    if fichier.exists():
        for ligne in fichier.read_text(encoding="utf-8").splitlines():
            ligne = ligne.strip()
            if not ligne or ligne.startswith("#") or "=" not in ligne:
                continue
            cle, _, valeur = ligne.partition("=")
            os.environ.setdefault(cle.strip(), valeur.strip())

    url = os.environ.get("KOBO_URL", "https://kf.kobotoolbox.org").rstrip("/")
    token = os.environ.get("KOBO_TOKEN")
    if not token:
        sys.exit("Erreur : KOBO_TOKEN absent (definir dans .env ou en variable d'environnement).")
    return url, token


class Kobo:
    def __init__(self, url, token):
        self.url = url
        self.s = requests.Session()
        self.s.headers.update({"Authorization": f"Token {token}"})

    def _api(self, chemin):
        return f"{self.url}/api/v2/{chemin.lstrip('/')}"

    def get(self, chemin, **kw):
        r = self.s.get(self._api(chemin), **kw)
        r.raise_for_status()
        return r

    # -- projets ---------------------------------------------------------
    def lister(self):
        return self.get("assets.json?limit=200").json().get("results", [])

    def info(self, uid):
        return self.get(f"assets/{uid}.json").json()

    # -- import XLSForm --------------------------------------------------
    def importer(self, chemin_xlsx, nom=None, destination_uid=None):
        """Televerse un XLSForm : cree un projet, ou met a jour celui vise."""
        chemin_xlsx = Path(chemin_xlsx)
        donnees = {"library": "false"}
        if destination_uid:
            donnees["destination"] = self._api(f"assets/{destination_uid}/")
        else:
            donnees["name"] = nom or chemin_xlsx.stem

        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        with open(chemin_xlsx, "rb") as f:
            r = self.s.post(self._api("imports/"), data=donnees,
                            files={"file": (chemin_xlsx.name, f, mime)})
        if not r.ok:
            sys.exit(f"Echec import ({r.status_code}) : {r.text[:800]}")
        url_import = r.json()["url"]

        # L'import est asynchrone : on attend son aboutissement.
        for _ in range(60):
            time.sleep(1.5)
            etat = self.s.get(url_import).json()
            statut = etat.get("status")
            if statut == "complete":
                msg = etat.get("messages", {})
                cible = (msg.get("created") or msg.get("updated") or [{}])[0]
                return cible.get("uid") or destination_uid
            if statut == "error":
                sys.exit("Echec import :\n" + json.dumps(etat.get("messages", {}),
                                                        indent=2, ensure_ascii=False))
        sys.exit("Delai depasse : l'import n'a pas abouti.")

    # -- medias du formulaire --------------------------------------------
    def medias(self, uid):
        r = self.get(f"assets/{uid}/files.json?file_type=form_media")
        return r.json().get("results", [])

    def televerser_media(self, uid, chemin):
        """Attache une image au formulaire ; remplace celle du meme nom."""
        chemin = Path(chemin)
        for f in self.medias(uid):
            if (f.get("metadata") or {}).get("filename") == chemin.name:
                self.s.delete(f["url"])

        mimes = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                 ".gif": "image/gif", ".svg": "image/svg+xml"}
        with open(chemin, "rb") as fh:
            r = self.s.post(
                self._api(f"assets/{uid}/files/"),
                data={"file_type": "form_media", "description": "default",
                      "metadata": json.dumps({"filename": chemin.name})},
                files={"content": (chemin.name, fh,
                                   mimes.get(chemin.suffix.lower(), "application/octet-stream"))})
        if not r.ok:
            sys.exit(f"Echec televersement media ({r.status_code}) : {r.text[:800]}")
        return r.json()

    # -- traductions -----------------------------------------------------
    def langues(self, uid):
        return self.info(uid)["content"].get("translations") or []

    def nettoyer_langues(self, uid):
        """Retire les traductions sans nom laissees par un ancien import.

        Kobo fusionne les langues a chaque import : un formulaire passe de
        monolingue a bilingue garde un emplacement anonyme, et le formulaire
        refuse alors de s'ouvrir (« There is an unnamed translation »).
        """
        contenu = self.info(uid)["content"]
        langues = contenu.get("translations") or []
        vides = [i for i, nom in enumerate(langues) if not nom]
        if not vides:
            return langues, 0
        for section in ("survey", "choices"):
            for ligne in contenu.get(section, []):
                for cle in contenu.get("translated", []):
                    val = ligne.get(cle)
                    if isinstance(val, list) and len(val) == len(langues):
                        ligne[cle] = [v for i, v in enumerate(val) if i not in vides]
        contenu["translations"] = [n for i, n in enumerate(langues) if i not in vides]
        r = self.s.patch(self._api(f"assets/{uid}/"), json={"content": contenu})
        if not r.ok:
            sys.exit(f"Echec nettoyage ({r.status_code}) : {r.text[:800]}")
        return contenu["translations"], len(vides)

    # -- deploiement -----------------------------------------------------
    def deployer(self, uid):
        details = self.info(uid)
        url = self._api(f"assets/{uid}/deployment/")
        if details.get("has_deployment"):
            r = self.s.patch(url, data={"active": "true", "version_id": details["version_id"]})
        else:
            r = self.s.post(url, data={"active": "true"})
        if not r.ok:
            sys.exit(f"Echec deploiement ({r.status_code}) : {r.text[:800]}")
        return r.json()

    # -- donnees ---------------------------------------------------------
    def donnees(self, uid):
        """Recupere toutes les soumissions en suivant la pagination."""
        resultats, page = [], self._api(f"assets/{uid}/data.json?limit=500")
        while page:
            d = self.s.get(page).json()
            resultats.extend(d.get("results", []))
            page = d.get("next")
        return resultats

    def exporter(self, uid, type_export="xls", dossier="exports"):
        r = self.s.post(self._api(f"assets/{uid}/exports/"), data={
            "type": type_export,
            "fields_from_all_versions": "true",
            "lang": "_default",
            "hierarchy_in_labels": "false",
            "group_sep": "/",
            "multiple_select": "both",
        })
        if not r.ok:
            sys.exit(f"Echec creation export ({r.status_code}) : {r.text[:800]}")
        url_export = r.json()["url"]

        for _ in range(80):
            time.sleep(2)
            etat = self.s.get(url_export).json()
            if etat.get("status") == "complete":
                lien = etat["result"]
                Path(dossier).mkdir(parents=True, exist_ok=True)
                cible = Path(dossier) / lien.rsplit("/", 1)[-1]
                with self.s.get(lien, stream=True) as flux:
                    flux.raise_for_status()
                    with open(cible, "wb") as f:
                        for bloc in flux.iter_content(65536):
                            f.write(bloc)
                return cible
            if etat.get("status") == "error":
                sys.exit("Echec export : " + str(etat.get("messages")))
        sys.exit("Delai depasse : l'export n'a pas abouti.")


def main():
    p = argparse.ArgumentParser(description="Client KoboToolbox")
    sp = p.add_subparsers(dest="cmd", required=True)

    sp.add_parser("list", help="lister les projets")

    d = sp.add_parser("deploy", help="importer puis deployer un XLSForm")
    d.add_argument("xlsx")
    d.add_argument("--name")

    r = sp.add_parser("redeploy", help="mettre a jour un projet existant")
    r.add_argument("uid")
    r.add_argument("xlsx")

    i = sp.add_parser("info", help="details d'un projet")
    i.add_argument("uid")

    m = sp.add_parser("media", help="attacher une image au formulaire")
    m.add_argument("uid")
    m.add_argument("fichier", nargs="?")

    l = sp.add_parser("langues", help="lister (et nettoyer) les traductions")
    l.add_argument("uid")
    l.add_argument("--nettoyer", action="store_true",
                   help="retirer les traductions sans nom, puis redeployer")

    g = sp.add_parser("data", help="telecharger les soumissions (JSON)")
    g.add_argument("uid")
    g.add_argument("--out", default="data/soumissions.json")

    e = sp.add_parser("export", help="generer et telecharger un export")
    e.add_argument("uid")
    e.add_argument("--type", default="xls", choices=["xls", "csv", "geojson", "spss_labels"])
    e.add_argument("--out", default="exports")

    a = p.parse_args()
    k = Kobo(*charger_env())

    if a.cmd == "list":
        projets = k.lister()
        if not projets:
            print("Aucun projet sur ce compte.")
        for x in projets:
            print(f"{x['uid']}  {x['asset_type']:<10} deploye={str(x.get('has_deployment')):<5} "
                  f"soumissions={x.get('deployment__submission_count') or 0:<5} {x.get('name')}")

    elif a.cmd == "deploy":
        uid = k.importer(a.xlsx, nom=a.name)
        print(f"Projet importe : {uid}")
        k.deployer(uid)
        lien = (k.info(uid).get("deployment__links") or {}).get("url")
        print(f"Deploye.\n  Edition  : {k.url}/#/forms/{uid}\n  Collecte : {lien}")

    elif a.cmd == "redeploy":
        k.importer(a.xlsx, destination_uid=a.uid)
        k.deployer(a.uid)
        print(f"Projet {a.uid} mis a jour et redeploye.")

    elif a.cmd == "media":
        if a.fichier:
            k.televerser_media(a.uid, a.fichier)
        for f in k.medias(a.uid):
            meta = f.get("metadata") or {}
            print(f"{meta.get('filename')}  {meta.get('mimetype', '')}  "
                  f"{meta.get('size', '?')} octets")

    elif a.cmd == "langues":
        if a.nettoyer:
            langues, retirees = k.nettoyer_langues(a.uid)
            if retirees:
                k.deployer(a.uid)
                print(f"{retirees} traduction(s) sans nom retiree(s), projet redeploye.")
            else:
                print("Rien a nettoyer.")
        else:
            langues = k.langues(a.uid)
        for nom in langues:
            print(nom if nom else "(SANS NOM — le formulaire ne s'ouvrira pas)")

    elif a.cmd == "info":
        x = k.info(a.uid)
        print(json.dumps({
            "uid": x["uid"], "nom": x.get("name"), "deploye": x.get("has_deployment"),
            "version": x.get("version_id"),
            "questions": len(x.get("content", {}).get("survey") or []),
            "soumissions": x.get("deployment__submission_count"),
            "lien_collecte": (x.get("deployment__links") or {}).get("url"),
        }, indent=2, ensure_ascii=False))

    elif a.cmd == "data":
        lignes = k.donnees(a.uid)
        cible = Path(a.out)
        cible.parent.mkdir(parents=True, exist_ok=True)
        cible.write_text(json.dumps(lignes, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"{len(lignes)} soumission(s) -> {cible}")

    elif a.cmd == "export":
        print(f"Export genere : {k.exporter(a.uid, a.type, a.out)}")


if __name__ == "__main__":
    main()
