questions = [

    {
        'question': "Ho XSS sull'admin ma sul mio webhook non mi arriva il ping della fetch. DI CHI È LA COLPA??????",
        'answers': [
            'CORS',
            'CSP',
            'SOP',
            'Titto'
        ],
        'correct': 'CSP'
    },

    {
        'question': 'Qual è la differenza principale tra reflected e DOM-based XSS?',
        'answers':[
            "Nella reflected l'input passa per il server e non nella DOM-based",    
            "Nella DOM-based l'input passa per il server e non nella reflected",    
            "La reflected richiede che l'utente faccia una search in qualche endpoint", 
            "La DOM-based sfrutta errori del programmatore nell'utilizzo di jQuery "
        ],
        'correct': "Nella reflected l'input passa per il server e non nella DOM-based",
    },


    {
        'question': "Noto che il server è vulnerabile a XXE. Quale altra vulnerabilità posso chainare per ottenere un attacco completo?",
        'answers':[
            "SSRF",
            "SQLi",
            "XSS",
            "SSTI"
        ],
        'correct': "SSRF",
    },


    {
        'question': "Riesco a comunicare con un server fingendo di essere un altro server autorizzato, sto sfruttando una...",
        'answers':[
            "SSRF",
            "SSTI",
            "CORS",
            "ASLR"
        ],
        'correct': "SSRF",
    },


    {
        'question': "Quale di queste è una client-side vulnerability?",
        'answers':[
            "XSS",
            "SQLi",
            "XXE",
            "IDOR"
        ],
        'correct':"XSS" ,
    },

    # PWN

    {
        'question': "Che cos'è BOF?",
        'answers':[
            "Un modo per salutare le persone quando se ne vanno",
            "Un protocollo HTTP",
            "Balloons Over Flowers, un immaginario concetto utilizzato nell'industria florovolare per descrivere un evento annuale in cui palloncini da festa vengono liberati sopra vasti campi di fiori",
            "Un tipo attacco che si può applicare sui binari"
        ],
        'correct': "Un tipo attacco che si può applicare sui binari",
    },

    {
        'question': "Chi è più forte (secondo OpenECSC)",
        'answers':[
            "Titto",
            "Tommaso",
            "Lenadro",
            "Frank",
            "Kristoj",
            "Lorenzinco",
        ],
        'correct': "Frank",
    },

    {
        'question': "In quale schema di firma digitale viene utilizzato l'accoppiamento bilineare su curve ellittiche per verificare l'autenticità di un messaggio",
        'answers':[
            "DSA",
            "ECDSA",
            "BLS",
            "RSA",
        ],
        'correct': "BLS",
    },

    {
        'question': "Quale stringa da in output 97753866244e5cee785384941fef6edb8633364e se si fa lo sha1?",
        'answers':[
            "Grazie Dario",
            "Prego Dario",
            "Per favore Dario",
            "Un assaggino",
        ],
        'correct': "Un assaggino",
    },

    {
        'question': "Quale principio crittografico è essenziale per garantire che un messaggio non sia stato alterato durante il trasferimento?",
        'answers':[
            "Confidenzialità",
            "Integrità",
            "Non ripudio",
            "Controllo di Accesso",
        ],
        'correct': "Integrità",
    },

    {
        'question': "Cosa sono i 'nanomites' nel contesto delle tecniche di anti-debugging?",
        'answers':[
            "Un tipo di malware che infetta il codice a livello di nanometro.",
            "Piccoli dispositivi hardware usati per disturbare i debugger hardware.",
            "Un metodo di protezione del software che scompone le istruzioni eseguibili in piccole parti gestite da un dispatcher.",
            "Un software di monitoraggio che rileva e disabilita i debugger in esecuzione su un sistema.",
        ],
        'correct': "Un metodo di protezione del software che scompone le istruzioni eseguibili in piccole parti gestite da un dispatcher.",
    },

    # DOMANDE GAG

    {
        "question": "Quanti anni ha la Regina Elisabetta?",
        "answers": [
            "1200",
            "Fernando",
            "Falso",
            "Arrosticini"
        ],
        "correct": "90"
    },

    {
        "question": "Quale di questi è un nome di un cane?",
        "answers": [
            "Pistacchiosa",
            "Rex",
            "Anastasia",
            "Gatto"
        ],
        "correct": "Gatto"
    },

    {
        "question": "Qual è la risposta giusta?",
        "answers": [
            "B",
            "D",
            "A",
            "C"
        ],
        "correct": "Nessuna delle precedenti"
    }
]
