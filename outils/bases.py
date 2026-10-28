"""Clients des cinq bases, appelés par `docker compose exec` (aucun port publié).

Chaque fonction renvoie un objet Resultat : code retour, sortie, lignes de résultat et valeur
(quand le résultat tient en une seule cellule). Le projet Compose est lu dans COMPOSE_PROJECT_NAME.
"""
import os
import re
import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
BASES = ("postgres", "mongo", "redis", "cassandra", "neo4j")


@dataclass
class Resultat:
    code: int
    sortie: str
    erreur: str
    lignes: list = field(default_factory=list)

    @property
    def ok(self):
        return self.code == 0

    @property
    def valeur(self):
        """La cellule unique du résultat, sans guillemets, ou None."""
        if len(self.lignes) != 1:
            return None
        return self.lignes[0].strip().strip('"')


def compose(*args, entree=None, timeout=600):
    env = dict(os.environ)
    env.setdefault("COMPOSE_PROJECT_NAME", "felicia")
    p = subprocess.run(["docker", "compose", "-f", str(RACINE / "compose.yaml"), *args],
                       input=entree, capture_output=True, text=True, cwd=RACINE, env=env, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def exec_(service, *cmd, entree=None, timeout=600):
    return compose("exec", "-T", service, *cmd, entree=entree, timeout=timeout)


def postgres(requete=None, fichier_texte=None, base="felicia"):
    cmd = ["psql", "-U", "felicia", "-d", base, "-v", "ON_ERROR_STOP=1", "-q", "-At", "-F", "|"]
    if requete is not None:
        code, out, err = exec_("postgres", *cmd, "-c", requete)
    else:
        code, out, err = exec_("postgres", *cmd, "-1", "-f", "-", entree=fichier_texte)
    return Resultat(code, out, err, [l for l in out.splitlines() if l.strip()])


ENVELOPPE_MONGO = """
let __r = (%s);
if (__r && typeof __r.toArray === 'function') { __r = __r.toArray(); }
if (Array.isArray(__r)) { print('@@LIGNES ' + __r.length); __r.forEach(d => print(EJSON.stringify(d))); }
else { print('@@VALEUR ' + ((__r !== null && typeof __r === 'object') ? EJSON.stringify(__r) : String(__r))); }
"""


def mongo(requete=None, fichier_texte=None):
    """Une requête est une expression JavaScript : curseur, tableau ou valeur."""
    if requete is not None:
        code, out, err = exec_("mongo", "mongosh", "--quiet", "felicia", "--eval", ENVELOPPE_MONGO % requete)
        lignes = []
        for i, l in enumerate(out.splitlines()):
            if l.startswith("@@LIGNES "):
                lignes = [x for x in out.splitlines()[i + 1:] if x.strip()]
                break
            if l.startswith("@@VALEUR "):
                lignes = [l[len("@@VALEUR "):]]
                break
        return Resultat(code, out, err, lignes)
    code, out, err = exec_("mongo", "mongosh", "--quiet", "felicia", "--file", "/dev/stdin", entree=fichier_texte)
    return Resultat(code, out, err, [l for l in out.splitlines() if l.strip()])


def redis(requete=None, fichier_texte=None):
    if requete is not None:
        code, out, err = exec_("redis", "redis-cli", "-e", *shlex.split(requete))
    else:
        code, out, err = exec_("redis", "redis-cli", "-e", entree=fichier_texte)
    return Resultat(code, out, err, [l for l in out.splitlines() if l.strip()])


def _lignes_cqlsh(out):
    """Extrait les lignes de données d'une sortie de cqlsh (tableau puis « (N rows) »)."""
    lignes, dedans = [], False
    for l in out.splitlines():
        if re.match(r"^-+(\+-+)*$", l.strip()):
            dedans = True
            continue
        if re.match(r"^\(\d+ rows?\)$", l.strip()):
            dedans = False
            continue
        if dedans and l.strip():
            lignes.append(" | ".join(c.strip() for c in l.split("|")))
    return lignes


def cassandra(requete=None, fichier_texte=None):
    cmd = ["cqlsh", "--request-timeout=120", "-k", "felicia"]
    if requete is not None:
        code, out, err = exec_("cassandra", *cmd, "-e", requete)
    else:
        code, out, err = exec_("cassandra", *cmd, entree=fichier_texte)
    return Resultat(code, out, err, _lignes_cqlsh(out))


def neo4j(requete=None, fichier_texte=None):
    cmd = ["cypher-shell", "-u", "neo4j", "-p", "felicia-neo4j", "--format", "plain"]
    if requete is not None:
        code, out, err = exec_("neo4j", *cmd, requete)
        lignes = [l for l in out.splitlines() if l.strip()][1:]   # la première ligne est l'en-tête
    else:
        code, out, err = exec_("neo4j", *cmd, entree=fichier_texte)
        lignes = [l for l in out.splitlines() if l.strip()]
    return Resultat(code, out, err, lignes)


CLIENTS = {"postgres": postgres, "mongo": mongo, "redis": redis, "cassandra": cassandra, "neo4j": neo4j}
