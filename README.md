
## Auto-héberger le bot

- Cloner le projet

```bash
  git clone https://github.com/AliceVancypher/INSA-bot.git
```

- Aller dans le dossier du projet
```bash
  cd INSA-bot
```

- Installer les dépendances (voir plus bas)

- Créer les fichiers de configuration nécessaire
```bash
  mkdir data
  cd data
  touch config
  touch id_insa.json
  touch message_role.json
  touch notes.json
```
- Dans le fichier config
```bash
TOKEN=<YOUR-DISCORD-BOT-TOKEN>
OWNER_ID=<YOUR-DISCORD-ID>
```
- Dans le fichier id_insa.json
```bash
{"login" : "<login insa>", "mdp" : "<mdp insa>"}
```
Si vous ne voulez pas utiliser la fonctionnalité des notes, allez dans main.py et commentez la ligne
```bash
await bot.add_cog(Notes(bot))
```

Lancer le bot

```bash
  python main.py
```

