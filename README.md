# Fatturearuba

## Panoramica del Progetto

Il Sistema di Gestione delle Fatture è un'applicazione web sviluppata utilizzando Angular per il frontend e Django per il backend. Di seguito è riportata una suddivisione tecnica di questi aspetti:



### Frontend (Angular)

1. **Componenti**:
   - **Login**: Fornisce l'autenticazione dell'utente utilizzando OAuth 2.0.
   - **Dashboard**: Mostra un riepilogo delle fatture e collegamenti di navigazione.
   - **Elenco Fatture (ElencoFattureComponent)**: Elenca tutte le fatture, supporta il filtraggio e fornisce la navigazione ai dettagli di ogni singola fattura.
   - **Dettagli Fattura (DettaglioFatturaComponent)**: Visualizza informazioni dettagliate su una specifica fattura, compreso il file XML.
   - **Componente Aggiungi Fattura (AggiungiFatturaComponent)**: Consente agli utenti di creare nuove fatture.
2. **Autenticazione**:
   - OAuth 2.0 per l'autenticazione dell'utente.
   - In caso di autenticazione riuscita, viene ottenuto un token di accesso e memorizzato in modo sicuro (ai fini dell'esercizio esemplificato in localstorage).
3. **Integrazione Backend API**



### Backend (Django)

1. **OAuth 2.0**: Gestisce l'autenticazione dell'utente tramite OAuth 2.0, utilizzando **django-oauth-toolkit.**

2. **API delle Fatture**: Fornisce endpoint RESTful per la gestione delle fatture.

3. Abilitazione cross-origin

    

###  Autenticazione OAuth 2.0

Di seguito una spiegazione per far funzionare l'autenticazione OAuth 2.0 nel progetto:

Registrazione dell'Applicazione (vedi screen)**:

- È necessario registrare l'applicazione LATO SERVER
- Durante la registrazione, vengono generati un `CLIENT_ID` e un  `CLIENT_SECRET`

![1](/home/robertocaputo/Documenti/Personal/aruba/fatturearuba_be_bak/help/1.png)

 

### Backend (Django)

#### Prerequisiti

Prima di iniziare con il backend Django, assicurati di avere Python e pip installati sul tuo sistema.

#### Configurazione del Backend

1. **Clona il Codice Sorgente**

   ```bash
   git clone https://github.com/swimminsparrow/fatture-be.git
   ```

2. Ambiente Virtuale

   ```bash
   python -m venv myenv
   source myenv/bin/activate
   pip install -r requirements.txt
   ```

   

3. Migrazioni del Database**

```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Avvio del Server Django**

```
python manage.py runserver
```

collegati all'indirizzo http://localhost:8000. 



### Frontend (Angular)

#### Prerequisiti

Prima di iniziare con il frontend Angular, assicurati di avere Node.js e npm installati sul tuo sistema.

#### Configurazione del Frontend

1. **Clona il Codice Sorgente**: 

   ```
   git clone https://github.com/swimminsparrow/fatture-be.git
   ```

   

2. **Installazione delle Dipendenze**

```
npm install
```

**3. Avvio del Server di Sviluppo**

```bash
ng serve
```

indirizzo http://localhost:4200.

### Caso D'Uso

```bash
  .---------.               .---------.
  | Utente  |               |  [API]  |
  '---------'               '---------'
      |                         |
      | Effettua il login      |
      |------------------------>|
      |                         |
      |<-- Risponde con       |
      |    token OAuth        |
      |------------------------|
      |                         |
      | Visualizza elenco      |
      |   fatture              |
      |------------------------>|
      |                         |
      |<-- Restituisce         |
      |    elenco fatture     |
      |------------------------|
      |                         |
      | Visualizza dettaglio   |
      |   fattura              |
      |------------------------>|
      |                         |
      |<-- Restituisce dettaglio|
      |------------------------|
      |                         |
      | Aggiungi nuova        |
      |   fattura              |
      |------------------------>|
      |                         |
      |<-- Restituisce         |
      |    conferma            |
      |------------------------|
      |                         |
      | Aggiorna dati         |
      |   fattura              |
      |------------------------>|
      |                         |
      |<-- Restituisce         |
      |    conferma            |
      |------------------------|
      |                         |
      | Effettua il logout     |
      |------------------------>|

```

# API

## Autenticazione

### Login
- **URL**: `{{host}}/o/token/`
- **Metodo**: POST
- **Richiesta**:
  - `username` (stringa)
  - `password` (stringa)
  - `grant_type` (stringa)
- **Descrizione**: Endpoint per l'autenticazione e il recupero del token di accesso.

## Fatture

### Ottieni Tutte le Fatture
- **URL**: `{{api}}/invoices/`
- **Metodo**: GET
- **Autenticazione**: Token di Accesso Bearer
- **Descrizione**: Ottiene l'elenco di tutte le fatture presenti nel sistema.

### Crea Fattura
- **URL**: `{{api}}/invoices/`
- **Metodo**: POST
- **Autenticazione**: Token di Accesso Bearer
- **Richiesta**:
  ```json
  {
    "issue_date": "YYYY-MM-DD",
    "due_date": "YYYY-MM-DD",
    "emitter_full_name": "John Doe",
    "emitter_email": "john@example.com",
    "destination_full_name": "Alice Smith",
    "destination_email": "alice@example.com",
    "total_amount": 100.50,
    "status": "Inviata",
    "emitter_user": 1,
    "destination_user": 2
  }
  ```
- **Descrizione**: Crea una nuova fattura con i dettagli forniti.

### Ottieni Fattura per ID
- **URL**: `{{api}}/invoices/invoice_number/{invoice_number}`
- **Metodo**: GET
- **Autenticazione**: Token di Accesso Bearer
- **Descrizione**: Ottiene i dettagli di una fattura specificata per numero di fattura.

### Aggiorna Fattura per ID
- **URL**: `{{api}}/invoices/invoice_number/{invoice_number}`
- **Metodo**: PATCH
- **Autenticazione**: Token di Accesso Bearer
- **Richiesta**:
  ```json
  {
    "sdi_identifier": "test2"
  }
  ```
- **Descrizione**: Aggiorna il campo identificativo SDI di una fattura.

### Ottieni XML della Fattura per ID
- **URL**: `{{api}}/invoices/xml/invoice_number/{invoice_number}`
- **Metodo**: GET
- **Autenticazione**: Token di Accesso Bearer
- **Descrizione**: Ottiene il file XML associato a una fattura.

### Carica XML per Fattura per ID
- **URL**: `{{api}}/invoices/xml/invoice_number/{invoice_number}`
- **Metodo**: POST
- **Autenticazione**: Token di Accesso Bearer
- **Richiesta**: Form Data (xml_file)
- **Descrizione**: Carica un nuovo file XML per la fattura specificata.

### Ottieni Stato della Fattura per Identificativo SDI
- **URL**: `{{api}}/invoices/sdi_identifier/{sdi_identifier}/status/`
- **Metodo**: GET
- **Autenticazione**: Token di Accesso Bearer
- **Descrizione**: Ottiene lo stato corrente di una fattura in base all'identificativo SDI.

### Ottieni Fattura per Identificativo SDI
- **URL**: `{{api}}/invoices/sdi_identifier/{sdi_identifier}`
- **Metodo**: GET
- **Autenticazione**: Token di Accesso Bearer
- **Descrizione**: Ottiene i dettagli di una fattura in base all'identificativo SDI.



## Note Aggiuntive

- Per autenticarsi e ottenere un token di accesso, è possibile utilizzare il flusso OAuth2 con le credenziali appropriate.
- Assicurarsi di includere il token di accesso nell'header "Authorization" di ogni richiesta alle API.
- Per ulteriori dettagli sulle richieste e sulle risposte, consultare la documentazione specifica delle API.# fatture-be

## Alcuni Limiti

- Attualmente, l'applicativo non supporta la definizione e la gestione di ruoli utente. Questo significa che tutti gli utenti hanno accesso alle stesse funzionalità, senza distinzioni di privilegi.
- L'applicativo non dispone di un meccanismo di indicizzazione per le fatture.
- Nella presente implementazione, i due microservizi di autenticazione e gestione delle fatture sono combinati in un unico.
- Modulare le componenti del backend: L'attuale struttura del backend non prevede una suddivisione modulare delle views, dei modelli e dei serializzatori in file separati. Questa mancanza di modularità potrebbe rendere più difficile la manutenzione e l'estensione del codice nel tempo.