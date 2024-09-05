# Django Project

Questo progetto è sviluppato utilizzando Django e integra diverse tecnologie per creare un'applicazione web moderna e funzionale.

## Tecnologie utilizzate

- **Django**: Framework web di alto livello per lo sviluppo di applicazioni web in Python.
- **TailwindCSS**: Un framework CSS utility-first per creare velocemente interfacce personalizzate.
- **jQuery**: Libreria JavaScript per manipolazioni del DOM e richieste AJAX.
- **Crispy Forms**: Pacchetto per migliorare la resa delle form Django, utilizzando Bootstrap.
- **Requests**: Libreria Python per effettuare richieste HTTP.
- **BeautifulSoup4 (BS4)**: Libreria per il web scraping, utile per parsare HTML e XML.
- **Django Rest Framework**: Strumento potente per costruire API RESTful con Django.
- **Shapely**: Libreria per la manipolazione di oggetti geometrici (punti, poligoni, etc.).
- **PyJWT**: Implementazione JSON Web Token in Python per l'autenticazione basata su token.
- **Pillow**: Libreria Python per la manipolazione di immagini.
- **Geopy**: Libreria per la geocodifica e la manipolazione di informazioni geografiche.

## Installazione e configurazione

### Prerequisiti

Assicurati di avere installati i seguenti software:

- **Python 3.x**: Linguaggio di programmazione utilizzato da Django.
- **Node.js**: Necessario per gestire i pacchetti NPM (come TailwindCSS).
- **PostgreSQL** o un altro database supportato da Django (opzionale, puoi usare SQLite per sviluppo).

### Installazione del progetto

1. Clona il repository del progetto:

```bash
git clone https://github.com/tuo-progetto.git
cd tuo-progetto
```

2. Imposta l'ambiente virtuale e installa i requisiti:
```bash
python3 -m venv env
source env/bin/activate  # Su Windows: env\Scripts\activate
pip install -r requirements.txt
npm install
```

3. Migrazione Database:
```bash
python manage.py migrate
```

4. Esecuzione:
```bash
python .\manage.py tailwind start
python manage.py runserver
```

## Testing

```bash
python manage.py test
```