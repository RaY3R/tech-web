# tech-web
Progetto DJANGO tecnologie web

# Avviare un ambiente virtuale Python e un progetto Django
## Creare un ambiente virtuale Python
- Assicurarsi di avere Python installato
- Aprire il terminale
- Navigare alla directory del progetto
- Creare l'ambiente virtuale
  - `python -m venv nome_ambiente`
- Attivare l'ambiente virtuale
  - Windows: `.\nome_ambiente\Scripts\activate`
  - Mac/Linux: `source nome_ambiente/bin/activate`

## Installare i pacchetti necessari
- Assicurarsi che l'ambiente virtuale sia attivo
- Installare i pacchetti con pip
  - `pip install -r requirements.txt`

## Creare un nuovo progetto Django
- Utilizzare il comando Django-admin per creare un nuovo progetto
  - `django-admin startproject nome_progetto`

## Avviare il server di sviluppo Django
- Navigare nella directory del progetto
  - `cd nome_progetto`
- Avviare il server di sviluppo
  - `python manage.py runserver`

## Creare una nuova app Django (opzionale)
- Utilizzare il comando manage.py per creare una nuova app
  - `python manage.py startapp nome_app`
