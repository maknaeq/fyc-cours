# Installer et vérifier son environnement

Au premier TP, un appel au modèle échoue. Est-ce votre code, ou votre machine ?
Impossible de le savoir si l'environnement n'a jamais été vérifié. Ce guide vous
fait installer quatre choses, puis les contrôler une par une, avant la séance 1.
Comptez 30 minutes, plus le temps de téléchargement du modèle.

- **Docker Desktop** : fait tourner les TP et la base de données dans des
  conteneurs. Vous n'avez pas besoin d'installer PHP ni Composer : les dépôts
  de TP les embarquent ([Laravel Sail](https://laravel.com/docs/13.x/sail)).
- **Ollama** : fait tourner un modèle d'IA sur votre ordinateur. C'est gratuit,
  sans compte, et c'est le choix conseillé pour tous les TP.
- **PostgreSQL avec pgvector** : la base qui stockera les « embeddings » (des
  textes transformés en listes de nombres, pour chercher par ressemblance),
  utilisée dès la séance 2.
- **Une clé d'accès à une IA en ligne** : facultative, pour comparer avec un
  fournisseur en ligne.

Les commandes ci-dessous sont celles de Windows (PowerShell). Sous macOS et sous
Linux, les étapes sont les mêmes sans WSL : voir la fin de ce guide.

## 1. Docker Desktop

Sous Windows, Docker Desktop s'appuie sur WSL 2, la couche qui fait tourner
Linux dans Windows. Il demande Windows 10 22H2 ou Windows 11 23H2 ou plus (éditions Pro, Entreprise
ou Éducation d'après sa page d'installation), 8 Go de RAM au moins, et la virtualisation activée dans le BIOS
([Docker Desktop sur Windows](https://docs.docker.com/desktop/setup/install/windows-install/)).

1. Ouvrez PowerShell en administrateur, puis installez WSL et redémarrez :

   ```powershell
   wsl --install
   ```

   ([Installer WSL, Microsoft](https://learn.microsoft.com/en-us/windows/wsl/install))
2. Installez Docker Desktop depuis la page ci-dessus, lancez-le, puis ouvrez
   *Settings → Resources → WSL Integration* et activez l'intégration pour votre
   distribution Ubuntu.
3. Vérifiez :

   ```powershell
   docker run --rm hello-world
   ```

Docker affiche un message de bienvenue : l'étape est bonne. Si rien ne
démarre, la cause la plus fréquente est la virtualisation désactivée dans le
BIOS (voir la page Docker Desktop ci-dessus).

## 2. Ollama et un modèle

1. Téléchargez Ollama sur [ollama.com/download](https://ollama.com/download) et
   installez-le. Il se lance en tâche de fond, et son API répond sur
   `http://localhost:11434` ([Ollama sur Windows](https://docs.ollama.com/windows)).
   Si vous avez une carte NVIDIA, Ollama demande un pilote en version 551.61 ou
   plus récente.
2. Téléchargez le modèle des TP (2,0 Go, il gère les appels d'outils dont
   la séance 2 a besoin) :

   ```powershell
   ollama pull llama3.2:3b
   ```

   ([llama3.2, Ollama](https://ollama.com/library/llama3.2))
3. Vérifiez que l'API répond. Dans PowerShell, écrivez `curl.exe` et non
   `curl`, qui y désigne une autre commande :

   ```powershell
   curl.exe http://localhost:11434/api/tags
   ```

   La réponse est du JSON qui liste `llama3.2:3b`.
4. Faites un premier appel, qui charge le modèle en mémoire :

   ```powershell
   ollama run llama3.2:3b "Dis bonjour en une phrase."
   ```

**Le premier appel est lent.** Ollama charge le modèle à la première requête,
ce qui peut dépasser le délai d'attente d'une application. Après 5 minutes sans
requête, il le décharge ([FAQ Ollama](https://docs.ollama.com/faq)). Avant
chaque TP, refaites l'appel de l'étape 4.

### Régler la fenêtre de contexte

La **fenêtre de contexte** est la quantité de texte (en *tokens*, des morceaux
de mots) que le modèle garde en mémoire pendant un échange. Ollama la fixe à
4 096 tokens par défaut ([FAQ Ollama](https://docs.ollama.com/faq)), et à 4 k
aussi sur une carte de moins de 24 Go de mémoire
([Context length, Ollama](https://docs.ollama.com/context-length)). C'est peu
dès qu'on envoie des documents ou des outils : le modèle perd alors le début
sans prévenir.

On la règle avec la variable d'environnement `OLLAMA_CONTEXT_LENGTH`.
Sous Windows ([FAQ Ollama](https://docs.ollama.com/faq)) :

1. Quittez Ollama (icône dans la barre des tâches).
2. Ouvrez les paramètres Windows, cherchez *variables d'environnement*, puis
   *Modifier les variables d'environnement pour votre compte*.
3. Créez la variable `OLLAMA_CONTEXT_LENGTH` avec la valeur `8192`.
4. Relancez Ollama depuis le menu Démarrer.

8 192 est un point de départ pour les TP. Un contexte plus grand consomme plus
de mémoire : la doc d'Ollama recommande au moins 64 000 tokens pour les agents,
ce que la plupart des machines ne tiennent pas avec un modèle de cette taille.
Contrôlez ce qui est réellement alloué :

```powershell
ollama ps
```

La colonne `CONTEXT` donne la taille de la fenêtre et la colonne `PROCESSOR`
indique si le modèle tourne sur le GPU ou sur le processeur.

### Machine moins puissante

Sans carte graphique compatible, Ollama utilise le processeur : tout marche,
mais plus lentement, donc davantage de premiers appels qui dépassent le délai.
Sur une machine de moins de 16 Go de RAM, prenez le modèle plus léger
`llama3.2:1b` (1,3 Go), et dites-le aux TP dans le fichier `.env` :

```powershell
ollama pull llama3.2:1b
```

```dotenv
LLM_OLLAMA_MODEL=llama3.2:1b
```

Plus petit, il répond en général moins bien : les TP sont réglés pour le modèle
à 3 milliards de paramètres. Dernière solution : n'utiliser que
l'IA en ligne (étape 4), sans Ollama.

## 3. PostgreSQL avec pgvector

L'extension **pgvector** ajoute à PostgreSQL un type de colonne pour les
vecteurs et la recherche par ressemblance. On l'utilise à partir de la
séance 2, mais on la vérifie maintenant.

Créez un dossier `fyc-env` et enregistrez-y le fichier `docker-compose.yml`
fourni avec ce guide :

```yaml
services:
  db:
    image: pgvector/pgvector:0.8.7-pg18
    container_name: fyc-pgvector
    ports:
      - "${FORWARD_DB_PORT:-5432}:5432"
    environment:
      POSTGRES_DB: noteflow
      POSTGRES_USER: noteflow
      POSTGRES_PASSWORD: secret
    volumes:
      - fyc-pgdata:/var/lib/postgresql
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "noteflow", "-d", "noteflow"]
      interval: 5s
      timeout: 5s
      retries: 10

volumes:
  fyc-pgdata:
```

La version de l'image est **épinglée** (`0.8.7-pg18`, pgvector 0.8.7 sur
PostgreSQL 18) : un `latest` changerait sous vos pieds, et les résultats du
cours ne seraient plus reproductibles
([pgvector](https://github.com/pgvector/pgvector)). Le mot de passe `secret`
convient à une base locale de test, jamais à autre chose.

```powershell
cd fyc-env
docker compose up -d
docker compose exec db psql -U noteflow -d noteflow -c "CREATE EXTENSION IF NOT EXISTS vector;" -c "SELECT extversion FROM pg_extension WHERE extname = 'vector';"
```

La requête doit renvoyer `0.8.7`. Si le port 5432 est déjà pris sur votre
machine (une autre base), changez-le :
`$env:FORWARD_DB_PORT = "5433"` avant `docker compose up -d`.

## 4. Une clé d'accès en ligne (facultatif)

Un fournisseur en ligne permet de comparer avec Ollama. Les TP utilisent Mistral
par défaut (`mistral-small-2603`). Créez un compte sur
[console.mistral.ai](https://console.mistral.ai), puis une clé d'API, et
placez-la dans le `.env` du TP :

```dotenv
LLM_PROVIDER=http
LLM_HTTP_API_KEY=votre_clé
```

Ne l'enregistrez jamais dans Git (le `.env` est ignoré par les dépôts de TP).
Le coût dépend de votre compte : Mistral décrit un mode gratuit, par défaut, aux
limites basses, et des paliers payants au-delà
([limites de débit, Mistral](https://help.mistral.ai/en/articles/698531-why-am-i-hitting-api-rate-limits-and-how-do-i-increase-them)).
Lisez ses conditions sur l'usage des données avant d'envoyer autre chose que des
notes de test. Sans clé, tous les TP restent faisables avec Ollama.

## 5. Vérifier que tout est en place

Quatre contrôles, un par brique. Chacun doit réussir avant la séance 1.

1. **Docker** : `docker run --rm hello-world` affiche le message de bienvenue.
2. **Ollama** : `curl.exe http://localhost:11434/api/tags` liste votre modèle.
3. **Ollama vu depuis un conteneur**, le chemin qu'empruntera l'application des TP :

   ```powershell
   docker run --rm curlimages/curl http://host.docker.internal:11434/api/tags
   ```

   Même réponse qu'au point 2. Si elle échoue alors que le point 2 réussit,
   Docker ne joint pas Ollama : relancez Ollama, puis Docker Desktop.
4. **pgvector** : la requête de l'étape 3 renvoie `0.8.7`.

<!-- À brancher (FYC-38) : le script de vérification remplace ces quatre
contrôles par une seule commande, avec un message clair par point. -->

## macOS et Linux

Les étapes sont les mêmes, sans WSL. Sur macOS, installez Docker Desktop et
Ollama depuis leurs pages de téléchargement. Sur Linux, installez Docker Engine
et Ollama selon leurs pages officielles. Ce guide a été vérifié sur Windows
uniquement : le contrôle 3 n'a pas été éprouvé sous Linux, où un service local
n'est pas forcément joignable depuis un conteneur.

## Pour aller plus loin

Si vous préférez PHP et Composer installés sur votre machine plutôt que dans des
conteneurs, Laravel 13 demande PHP 8.3 au moins
([Laravel 13.x : notes de version](https://laravel.com/docs/13.x/releases)).
Les TP n'en ont pas besoin.
