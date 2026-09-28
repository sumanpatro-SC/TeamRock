# MemoryMeet AI

Yon platfòm entèlijans atifisyèl pou reyinyon ki kapab sonje kontèks kliyan pase yo, angajman yo te pran, ak nòt istorik yo pou sentetize yon brèf egzekitif preparasyon reyinyon ki klè e aksyonab nan kèk segonn.

**Lyen Pwojè an Liy:** [https://memorymeet-ai-by-teamrock.onrender.com/](https://memorymeet-ai-by-teamrock.onrender.com/)  
**Depo GitHub:** [https://github.com/sumanpatro-SC/TeamRock](https://github.com/sumanpatro-SC/TeamRock)

---

## 1. Definisyon Pwoblèm nan (Problem Statement)
Ekip pwofesyonèl yo, responsab kont yo, ak konsiltan yo souvan antre nan reyinyon ak kliyan oswa patnè san yo pa sonje imedyatman angajman ki te pran anvan yo, risk ki ouvè yo, oswa kontèks pase a. Nòt reyinyon yo souvan gaye nan divès dokiman, nan sistèm CRM ki pa ajou, oswa yo pèdi nèt, sa ki lakòz:
* Patisipan reyinyon yo pa prepare epi yo bliye angajman anvan yo te pran ak kliyan an.
* Repetisyon kesyon ki diminye konfyans nivo egzekitif la.
* Neglijans sou risk pwojè a ak move aliyman sou atant yo.

---

## 2. Solisyon an: MemoryMeet AI
MemoryMeet AI bay yon sistèm memwa ak preparasyon reyinyon santralize:
1. **Anrejistreman Reyinyon ak Memwa Episodik:** Li stoke nòt ak angajman ki pa estriktire dirèkteman anba non patisipan yo ak konpayi yo grasa bank memwa vektè Hindsight la.
2. **Rapèl Semantik Konpòtmantal:** Li chèche epi li jwenn entèraksyon istorik yo, desizyon yo, ak ajanda anvan yo lè l sèvi avèk rechèch semantik nan langaj natirèl.
3. **Sentèz Egzekitif:** Li itilize motè enferans rapid Groq la (`openai/gpt-oss-120b`) pou l prepare brèf estriktire ki gen ladan istorik relasyon an, risk kritik yo, angajman ki rete ouvè yo, ak pwen diskisyon taktik yo.

---

## 3. Achitekti Sistèm nan ak Dyagram (Nivo 0 rive Nivo 3)

### Nivo 0: Dyagram Kontèks (Context Diagram)
```mermaid
graph LR
    User([Patisipan Reyinyon / Egzekitif]) -->|Anrejistre nòt & mande brèf| MMAI[Sistèm MemoryMeet AI]
    MMAI -->|Depo ak rechèch memwa alontèm| Hindsight[Motè Vektè Hindsight]
    MMAI -->|Sentèz kontèks ak jenerasyon| Groq[Motè LLM Groq]
    MMAI -->|Retounen brèf egzekitif fòmate| User

graph LR
    subgraph FastAPI Backend
        Router[Kontwolè Wout API]
        ModelValidator[Validasyon Schéma Pydantic]
        HindsightAdapter[Kliyan Hindsight Wrapper]
        LLMAdapter[Sèvis Konplesyon Groq]
    end

    Client[Kliyan Entèfas] -->|Demann Save / Brief| Router
    Router --> ModelValidator
    ModelValidator --> HindsightAdapter
    ModelValidator --> LLMAdapter
    
    HindsightAdapter -->|Ensèsyon & Rechèch Vektè| ExternalHindsight[(Bank Memwa Hindsight)]
    LLMAdapter -->|Jenerasyon Repons| ExternalGroq[(Klètè LLM Groq)]


Container Diagram

graph LR
    User([Navigatè Itilizatè]) -->|HTTPS / UI| SPA[Entèfas Sit Web HTML5/CSS3/JS]
    SPA -->|POST /api/save-meeting| API[Sèvè Backend FastAPI]
    SPA -->|POST /api/get-brief| API[Sèvè Backend FastAPI]
    
    subgraph Enfrastrikti Nwaj (Cloud)
        API -->|Apèl REST Retain / Recall| HindsightSDK[Sèvis Nwaj Hindsight]
        API -->|API Chat Completions| GroqLLM[Motè Enferans Groq]
    end

Component Diagram

graph LR
    subgraph FastAPI Backend
        Router[Kontwolè Wout API]
        ModelValidator[Validasyon Schéma Pydantic]
        HindsightAdapter[Kliyan Hindsight Wrapper]
        LLMAdapter[Sèvis Konplesyon Groq]
    end

    Client[Kliyan Entèfas] -->|Demann Save / Brief| Router
    Router --> ModelValidator
    ModelValidator --> HindsightAdapter
    ModelValidator --> LLMAdapter
    
    HindsightAdapter -->|Ensèsyon & Rechèch Vektè| ExternalHindsight[(Bank Memwa Hindsight)]
    LLMAdapter -->|Jenerasyon Repons| ExternalGroq[(Klètè LLM Groq)]

sequenceDiagram
    autonumber
    actor User as Itilizatè
    participant Frontend as Entèfas Sit Web
    participant FastAPI as FastAPI (/api/get-brief)
    participant Hindsight as Baz Done Vektè Hindsight
    participant Groq as Groq (gpt-oss-120b)

    User->>Frontend: Antre Patisipan, Konpayi, ak Nouvo Ajanda
    Frontend->>FastAPI: POST /api/get-brief {participant, company, agenda}
    FastAPI->>Hindsight: recall(query="Meeting history, decisions, commitments...")
    Hindsight-->>FastAPI: Retounen eleman memwa ki koresponn yo
    FastAPI->>FastAPI: Prepare prompt la ak kontèks memwa a ak enstriksyon yo
    FastAPI->>Groq: chat.completions.create(messages=[prompt])
    Groq-->>FastAPI: Retounen brèf egzekitif estriktire a
    FastAPI-->>Frontend: JSON {status: "success", brief: markdown}
    Frontend->>User: Afiche brèf la fòmate an Markdown grasa marked.js


4. Zouti Teknoloji yo Itilize (Tech Stack)
Backend: FastAPI, Pydantic, Uvicorn

Frontend: HTML5 responsif, Vanilla JavaScript, CSS Grid, Marked.js (pou afiche Markdown)

Memwa ak Depo: Kliyan Vektè Hindsight (hindsight-client)

Motè LLM: Groq Cloud (openai/gpt-oss-120b)

Konfigirasyon Anviwònman: Python Dotenv (python-dotenv)

Deplwaman: Render (Sèvis Web sou nwaj k ap kouri sou Uvicorn)

5. Referans API (Endpoints)
POST /api/save-meeting
Anrejistre nòt entèraksyon yo epi voye yo nan bank memwa pèmanan an.

{
  "participant": "Rahul Sharma",
  "company": "Acme Tech",
  "notes": "Te diskite sou rediksyon delè migrasyon AWS a pa de semèn. Te pwomèt dyagram achitekti a pou vandredi."
}


{
  "status": "success",
  "message": "Successfully retained memory for Rahul Sharma (Acme Tech)"
}


{
  "status": "success",
  "brief": "### Executive Brief...\n1. Executive Summary\n2. Critical Risks..."
}

6. Enstalasyon ak Egzolisyon Lokal
Kondisyon Preliminè
Python 3.10+

Git

Etap Enstalasyon yo
Klone depo a:

Bash
git clone [https://github.com/sumanpatro-SC/TeamRock.git](https://github.com/sumanpatro-SC/TeamRock.git)
cd TeamRock
Kreye epi aktive yon anviwònman virtyèl:

Bash
python -m venv venv
source venv/bin/activate    # Sou Windows: venv\Scripts\activate
Enstale modil ki nesesè yo:

Bash
pip install -r requirements.txt
Konfigire Varyab Anviwònman yo:
Kreye yon dosye .env nan rasin pwojè a:

Code snippet
HINDSIGHT_API_KEY=kle_hindsight_ou
HINDSIGHT_API_URL=[https://api.hindsight.vectorize.io](https://api.hindsight.vectorize.io)
HINDSIGHT_BANK_ID=Name: OpsMemory Incidents
GROQ_API_KEY=kle_groq_ou
Lanse sèvè lokal la:

Bash
uvicorn api.index:app --host 0.0.0.0 --port 8000 --reload
Louvri http://localhost:8000 nan navigatè w la.

7. Deplwaman an Pwodiksyon (Render)
Pwojè a deplwaye kòm yon Sèvis Web sou Render:

Lyen Sèvis an Liy: https://memorymeet-ai-by-teamrock.onrender.com/

Kòmand Konstriksyon (Build Command): pip install -r requirements.txt

Kòmand Demaraj (Start Command): uvicorn api.index:app --host 0.0.0.0 --port $PORT

Kalite Enstans: Plan Gratis (Sèvis web Python pèmanan ak sekirite SSL otomatik)