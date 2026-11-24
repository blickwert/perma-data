"""Inhalte der Version v2b (Kundenwünsche, Stand Dokument V5, 16. November 2026).

Quelle: PERMA_Mind_Academy_Homepagetexte_fuer_David_V5.docx, Abschnitte 1 bis 7 und 10.
Nur öffentliche Website-Texte. Umsetzungshinweise, "Button:"-Markierungen und die Abschnitte 8 bis 10
(Preise intern, SEO-Hinweise) gehören nicht in den Seitentext. Titel und Meta-Beschreibungen stehen
in META und landen im <head>.
Platzhalter in [eckigen Klammern] werden in der Vorschau gelb markiert.
"""

# --------------------------------------------------------------------------- Meta (Abschnitt 10)
META = {
    "index": {
        "file": "index.html",
        "title": "Positive Psychologie Ausbildung | PERMA Mind Academy",
        "desc": "Positive Psychologie lernen: seit 2014 international vernetzte Trainer, aktuelle Forschung und ECQA-Abschluss. Entdecke Basic, Advanced und Clinical Expert.",
    },
    "basic": {
        "file": "positive-psychologie-basic.html",
        "url": "/positive-psychologie-basic/",
        "title": "Positive Psychologie Basic | PERMA Mind Academy",
        "desc": "Positive Psychologie Basic: drei Module, eigenes Praxisprojekt und ECQA-Abschluss. Ohne Vorkenntnisse. Jetzt unverbindlich in die Interessentenliste eintragen.",
    },
    "advanced": {
        "file": "positive-psychologie-advanced.html",
        "url": "/positive-psychologie-advanced/",
        "title": "Positive Psychologie Advanced | PERMA Mind Academy",
        "desc": "Positive Psychologie Advanced ab Anfang 2028: 94 Einheiten für die professionelle Anwendung. Basic-Abschluss erforderlich. Unverbindliche Interessentenliste.",
    },
    "clinical": {
        "file": "klinische-positive-psychologie.html",
        "url": "/klinische-positive-psychologie/",
        "title": "Klinische Positive Psychologie | PERMA Mind Academy",
        "desc": "Klinische Positive Psychologie ab Frühjahr 2028: acht Module, 128 Seminareinheiten und ECQA-Abschluss. Jetzt in die unverbindliche Interessentenliste eintragen.",
    },
}

# Angebote (Reihenfolge = Reihenfolge der Karten, Akzentfarbe je Angebot)
OFFERS = [
    {"key": "basic", "accent": "blue", "name": "Positive Psychology Basic",
     "short": "Basic", "form_label": "Positive Psychology Basic",
     "card_text": "Du möchtest verstehen, wie Stärken, Beziehungen und Sinn zum Wohlbefinden beitragen? Basic vermittelt dir die Grundlagen, lässt dich Methoden selbst erproben und begleitet dein erstes Praxisprojekt. Der Einstieg ist ohne psychologische Vorkenntnisse möglich.",
     "card_meta": "Drei Module in Präsenz · Termine folgen · ECQA-Abschluss nach Erfüllung der Anforderungen",
     "card_button": "Zur Basic-Ausbildung", "list_button": "Zur Basic-Interessentenliste"},
    {"key": "advanced", "accent": "purple", "name": "Positive Psychology Advanced",
     "short": "Advanced", "form_label": "Positive Psychology Advanced",
     "card_text": "Du hast Basic abgeschlossen und möchtest Positive Psychologie professionell einsetzen? Advanced vertieft die Anwendung in Coaching, Bildung, Gesundheitsförderung und Führung. Du lernst, Interventionen auszuwählen und eigene Trainings zu entwickeln.",
     "card_meta": "Sechs Seminartage in drei Blöcken geplant · Beginn Anfang 2028 · Basic-Abschluss erforderlich",
     "card_button": "Zum Advanced-Lehrgang", "list_button": "Zur Advanced-Interessentenliste"},
    {"key": "clinical", "accent": "orange", "name": "PERMA Clinical Expert",
     "short": "Clinical Expert", "form_label": "PERMA Clinical Expert",
     "card_text": "Du arbeitest als klinische:r Psycholog:in oder Psychotherapeut:in? Vertiefe die Arbeit mit Stärken und Ressourcen in Diagnostik, Behandlungsplanung und Therapie. Fallarbeit und Supervision unterstützen die Übertragung in deine klinische Praxis.",
     "card_meta": "Acht zweitägige Module · Beginn Frühjahr 2028 · Auch einzelne Module buchbar",
     "card_button": "Zur Clinical-Expert-Fortbildung", "list_button": "Zur Clinical-Expert-Interessentenliste"},
]

# --------------------------------------------------------------------------- Startseite (Abschnitt 1)
HERO = {
    "h1": "Ausbildung in Positiver Psychologie mit wissenschaftlicher Tiefe",
    "paras": [
        "Verstehe, was Menschen stärkt, und lerne, dieses Wissen gezielt anzuwenden. In der PERMA Mind Academy verbindest du aktuelle Forschung zur Positiven Psychologie mit Übungen, Fallarbeit und eigenen Praxisprojekten. Für deine persönliche Entwicklung und für die Arbeit mit Menschen in Coaching, Bildung, Führung oder Therapie.",
        "Lerne bei Dr. Martin Wammerl und Mag. Michael Wohlkönig: seit 2014 im internationalen Fachaustausch, mit Erfahrung aus Forschung, klinischer Praxis und Ausbildung. Unsere ECQA-anerkannten Lehrgänge führen dich vom fundierten Einstieg bis zur vertieften beruflichen Anwendung.",
    ],
    "button_primary": "Passende Ausbildung finden",
    "button_secondary": "Zur Interessentenliste",
    "features": ["Seit 2014 international vernetzt", "Wissenschaftlich fundiert und praxisnah",
                 "Europäische Zertifizierung mit ECQA"],
}

WHY = {
    "title": "Warum PERMA Mind Academy?",
    "items": [
        ("blue", "globe", "Seit 2014 im Austausch mit der internationalen Forschung",
         "Unsere fachliche Entwicklung ist seit 2014 vom kontinuierlichen Austausch mit führenden Wissenschaftler:innen der Positiven Psychologie geprägt. Dazu zählen Begegnungen und fachlicher Austausch mit Martin Seligman, Mihály Csíkszentmihályi, Barbara Fredrickson, Kim Cameron und Tayyab Rashid sowie weiteren prägenden Persönlichkeiten des Fachs. Teile unserer Ausbildung haben wir direkt bei den Begründern der Positiven Psychologie absolviert."),
        ("purple", "flask", "Aktuelle Erkenntnisse für deine Praxis",
         "Wir nehmen seitdem regelmäßig an europäischen und internationalen Fachkonferenzen teil und verfolgen neue Forschungsergebnisse und fachliche Debatten. Diese Impulse fließen in unsere Ausbildung ein. Du lernst, was sich aus der Forschung für deine Arbeit ableiten lässt, welche Fragen offenbleiben und wo Methoden an Grenzen stoßen."),
        ("green", "badge", "Ein Abschluss mit europäischem Zertifizierungsrahmen",
         "Unsere ECQA-anerkannten Ausbildungen ermöglichen einen europäischen Kompetenznachweis durch eine externe Zertifizierungsstelle. Im Unterschied zu einer reinen Teilnahmebestätigung dokumentiert er Kenntnisse und Fähigkeiten anhand definierter Anforderungen. Damit kannst du deine Qualifikation gegenüber Auftraggeber:innen und Arbeitgeber:innen nachvollziehbar darstellen."),
    ],
}

COURSES = {"eyebrow": "Ausbildungen", "title": "Welche Ausbildung passt zu deinem nächsten Schritt?"}

UNDERSTAND = {
    "left_title": "Positive Psychologie verstehen und verantwortungsvoll anwenden",
    "left": [
        "Was hilft Menschen, sich zu entwickeln, tragfähige Beziehungen aufzubauen und auch unter Belastung Handlungsmöglichkeiten zu finden? Positive Psychologie untersucht diese Fragen wissenschaftlich. In unseren Ausbildungen lernst du, Erkenntnisse einzuordnen und passende Methoden auszuwählen. Schwierige Gefühle, psychische Erkrankungen und soziale Lebensbedingungen werden dabei berücksichtigt.",
        "Das PERMA-Modell bietet eine Orientierung mit fünf Bereichen des Wohlbefindens: positive Emotionen, Engagement, Beziehungen, Sinn und das Erreichen persönlich bedeutsamer Ziele. Wir verbinden dieses Modell mit weiteren Forschungsansätzen und fragen, was sich für die jeweilige Person und Situation daraus ableiten lässt.",
    ],
    "right_title": "Vom Verstehen zum Anwenden",
    "right": [
        "In kleinen Gruppen erprobst du Übungen zunächst selbst, arbeitest an Fällen und erhältst Rückmeldungen. Praxisprojekte helfen dir, das Gelernte in deinen Alltag oder Beruf zu übertragen. Dabei entwickelst du ein begründetes Vorgehen: Ziele klären, Methoden auswählen, Erfahrungen reflektieren und die Anwendung anpassen.",
    ],
}

NEXT_STEP = {
    "title": "Dein nächster Schritt",
    "text": "Du interessierst dich für eine unserer Ausbildungen? Trage dich unverbindlich in die Interessentenliste ein und wähle Basic, Advanced oder Clinical Expert. Sobald die jeweilige Ausschreibung vorliegt, erhältst du die Unterlagen für die verbindliche Anmeldung. Dein Eintrag ist kostenfrei und reserviert noch keinen Platz.",
}

# --------------------------------------------------------------------------- Angebotsseiten (Abschnitte 2 bis 4)
PAGES = {
    "basic": {
        "h1": "Basic-Ausbildung in Positiver Psychologie",
        "eyebrow": "Positive Psychology Basic",
        "lead": [
            "Wie kannst du Stärken erkennen, Beziehungen bewusst gestalten und persönlich bedeutsame Ziele verfolgen? In Basic erschließt du dir die wissenschaftlichen Grundlagen der Positiven Psychologie und erprobst konkrete Methoden. Dein eigenes Praxisprojekt verbindet die Ausbildung mit einer Frage aus deinem Alltag oder Beruf.",
            "Für Menschen, die Positive Psychologie persönlich oder beruflich nutzen möchten, etwa in Coaching, Beratung, Pädagogik, Führung und Gesundheitsberufen. Psychologische Vorkenntnisse sind nicht erforderlich.",
        ],
        "facts": [
            ("Voraussetzungen", "Keine psychologische Vorbildung erforderlich"),
            ("Aufbau", "Drei Module; neun Seminartage in drei Blöcken zu je drei Tagen geplant"),
            ("Format und Ort", "Präsenz, geplant im Raum Graz; genauer Ort wird bekannt gegeben"),
            ("Termine", "Die Termine der drei Module werden noch bekannt gegeben"),
            ("Abschluss", "ECQA-Zertifikat nach Erfüllung der Abschlussanforderungen"),
            ("Kosten", "1.997 € Frühbucherpreis / 2.397 € regulär",
             "Zuzüglich Zertifizierungsgebühren; Höhe wird noch bekannt gegeben. Frühbucherfrist folgt."),
        ],
        "content_title": "Inhalte und Ablauf",
        "modules": [
            ("Modul 1 Grundlagen der Positiven Psychologie",
             "Du lernst zentrale Modelle, das PERMA-Modell und erste positive Interventionen kennen. Verfahren zur Erfassung von Stärken, positiven Emotionen und Wohlbefinden helfen dir, Ausgangslagen zu verstehen. Gemeinsam ordnen wir Ergebnisse und wissenschaftliche Aussagen ein."),
            ("Modul 2 PERMA und die Bausteine des Wohlbefindens",
             "Du beschäftigst dich mit positiven Emotionen, Engagement und Charakterstärken, Beziehungen und Kommunikation sowie Sinn und persönlichen Zielen. Übungen zu Achtsamkeit und Resilienz machen erfahrbar, wie sich diese Themen im Alltag aufgreifen lassen."),
            ("Modul 3 Positive Psychologie in der Praxis",
             "Du überträgst das Gelernte auf Coaching, Bildung, Gesundheitsförderung oder Arbeitswelt. Dafür entwickelst und erprobst du ein eigenes Projekt. Peergruppen und Abschlusspräsentation geben Raum für Rückmeldungen und die Reflexion deiner Erfahrungen."),
        ],
        "scope_title": "Umfang und Abschluss",
        "scope": [
            "Das Curriculum umfasst 148 Einheiten à 45 Minuten: 100 Ausbildungseinheiten, 20 Einheiten Peergruppenarbeit, acht Einheiten Gruppencoaching und 20 Einheiten Praxisprojekt. Der genaue Zeitplan folgt mit der Ausschreibung.",
            "Für den ECQA-Abschluss erbringst du die vorgesehenen Ausbildungs- und Praxisleistungen, präsentierst dein Projekt und fasst es schriftlich zusammen. Dein Zertifikat dokumentiert die nachgewiesenen Kompetenzen in einem europäischen Rahmen. Der Basic-Abschluss eröffnet dir den Zugang zu Advanced.",
        ],
        "scope_link": ("advanced", "Zum Advanced-Lehrgang"),
        "list_title": "Unverbindliche Interessentenliste für Basic",
        "list_text": "Trage dich mit deinen Kontaktdaten unverbindlich ein. Sobald die Termine der drei Module und die Ausschreibung vorliegen, senden wir dir die Unterlagen für die verbindliche Anmeldung. Dein Eintrag ist kostenfrei und reserviert noch keinen Platz.",
    },
    "advanced": {
        "h1": "Advanced-Lehrgang in Positiver Psychologie",
        "eyebrow": "Positive Psychology Advanced",
        "lead": [
            "In Advanced vertiefst du die professionelle Anwendung der Positiven Psychologie. Du lernst, Interventionen passend auszuwählen, ihre Ergebnisse zu beurteilen und eigene Workshops und Trainings zu gestalten. Aktuelle Forschung und der internationale Fachaustausch unserer Trainer fließen in die Ausbildung ein.",
            "Der Lehrgang richtet sich an Coaches, Berater:innen, Pädagog:innen, Fachkräfte im Gesundheitsbereich, Führungskräfte und Trainer:innen. Voraussetzung ist eine abgeschlossene Basic-Ausbildung in Positiver Psychologie.",
        ],
        "facts": [
            ("Beginn", "Anfang 2028; einzelne Termine folgen"),
            ("Aufbau und Format", "Sechs Seminartage in drei Zweitagesblöcken in Präsenz geplant; Ort folgt"),
            ("Voraussetzung", "Abgeschlossene Basic-Ausbildung in Positiver Psychologie"),
            ("Abschluss", "ECQA-Zertifikat nach Erfüllung der Abschlussanforderungen"),
            ("Kosten", "1.398 € Frühbucherpreis / 1.596 € regulär",
             "Zuzüglich Zertifizierungsgebühren; Höhe wird noch bekannt gegeben. Frühbucherfrist folgt."),
        ],
        "content_title": "Inhalte und Arbeitsweise",
        "modules": [
            ("1 Beyond PERMA: Contemporary Positive Psychology",
             "Aktuelle Forschung zu Wohlbefinden, Belastung und kulturellen Unterschieden. Du prüfst, welche Erkenntnisse für deine Arbeit relevant sind und wo die Aussagekraft von Modellen und Methoden begrenzt ist."),
            ("2 Positive Coaching & Change",
             "Stärken, Werte und Ziele in Veränderungsprozessen nutzen. Du arbeitest mit Motivation und Ambivalenz, klärst Aufträge und beachtest die Grenze zwischen Coaching und Behandlung."),
            ("3 Positive Education & Development",
             "Stärken, Beziehungen und Lernmotivation in Bildungsprozessen fördern. Du entwickelst eine eigene Lernsequenz und setzt dich kritisch mit Ansätzen wie Growth Mindset auseinander."),
            ("4 Positive Health, Resilience & Recovery",
             "Stress, Erholung und Selbstmitgefühl in der Gesundheitsförderung aufgreifen. Du passt ressourcenorientierte Übungen an Zielgruppe und Belastungssituation an."),
            ("5 Positive Leadership & Organizations",
             "Positive Leadership, PERMA-Lead, psychologische Sicherheit und Feedback im Arbeitsalltag. Du entwickelst Maßnahmen für Teams und überlegst, wie sich ihre Ergebnisse beurteilen lassen."),
            ("6 Interventionen und Trainings gestalten",
             "Du planst, erprobst und reflektierst eigene Interventionen und Trainings. Kurze Übungssequenzen und Peerfeedback helfen dir, Inhalte verständlich anzuleiten und passend aufzubauen."),
        ],
        "scope_title": "Umfang und Abschluss",
        "scope": [
            "Geplant sind 94 Einheiten: 60 Seminareinheiten, vier Einheiten Coaching, 20 Einheiten Praxisprojekt und Selbststudium sowie zehn Einheiten Peergruppenarbeit. Dein Projekt führt von der Bedarfsanalyse bis zur Auswertung. Der ECQA-Abschluss setzt die vorgesehenen Ausbildungs-, Praxis- und Abschlussleistungen voraus. Zeitplan und genaue Anforderungen folgen mit der Ausschreibung.",
        ],
        # Ergänzung Martin Wammerl (November 2026): Qualifikation im Umfang-Abschnitt, Master-Trainer-Lehrgang als eigene Karte.
        "scope_more": ("Berufliche Qualifikation als Basic Trainer", [
            "Mit dem erfolgreichen Abschluss des Advanced-Curriculums erwirbst du die Qualifikation als „Basic Trainer“ für Positive Psychologie. Du kannst wissenschaftlich fundierte Inhalte und Methoden in deinem beruflichen Umfeld vermitteln, etwa in Workshops für dein Team oder in Fortbildungen für Kolleg:innen.",
        ]),
        "extras": [
            ("ECQA Master Trainer für Positive Psychologie (in Planung)", [
                "Für Absolvent:innen des Advanced-Curriculums planen wir einen weiterführenden Lehrgang, der an das Mastertraining der European Positive Psychology Academy (EUPPA) anknüpft. Er richtet sich an alle, die künftig selbst Basic- und Advanced-Curricula in Positiver Psychologie nach den Kriterien der ECQA anbieten und unterrichten möchten.",
                "Im Mittelpunkt steht die Frage, wie du einen ganzen Lehrgang gestaltest. Du erarbeitest ein eigenes Trainingskonzept, formulierst Lernziele und planst, wie die einzelnen Module aufeinander aufbauen. Du übst, aktuelle Forschung verständlich zu vermitteln, praktische Übungen anzuleiten und deren Erfahrungen mit der Gruppe auszuwerten. In der Supervision reflektierst du deine Rolle als Trainer:in und deinen Umgang mit unterschiedlichen Vorkenntnissen und herausfordernden Gruppensituationen.",
            ]),
        ],
        "scope_link": ("basic", "Zur Basic-Ausbildung"),
        "list_title": "Unverbindliche Interessentenliste für Advanced",
        "list_text": "Geplanter Beginn ist Anfang 2028. Trage dich unverbindlich in die Interessentenliste für Advanced ein. Sobald die Ausschreibung vorliegt, erhältst du die Unterlagen für die verbindliche Anmeldung. Der kostenfreie Eintrag reserviert noch keinen Platz.",
    },
    "clinical": {
        "h1": "Fortbildung in klinischer Positiver Psychologie",
        "eyebrow": "PERMA Clinical Expert",
        "lead": [
            "Erweitere deine klinische Arbeit um einen differenzierten Blick auf Stärken, Wohlbefinden und persönliche Entwicklung. PERMA Clinical Expert richtet sich an klinische Psycholog:innen und Psychotherapeut:innen, die Positive Psychologie in Diagnostik, Behandlungsplanung und Therapie integrieren möchten. Aktuelle Forschung, klinische Erfahrung und Fallarbeit bilden die Grundlage.",
        ],
        "facts": [
            ("Beginn und Format", "Frühjahr 2028; Präsenz im Raum Graz geplant. Einzeltermine und Ort folgen"),
            ("Aufbau und Buchung", "Acht zweitägige Module, insgesamt 16 Seminartage; einzeln oder zusammen buchbar"),
            ("Abschluss", "Mikrozertifikate für Einzelmodule vorgesehen; ECQA-Gesamtzertifikat nach Erfüllung aller Anforderungen"),
            ("Kosten", "370 € pro Modul / 2.960 € für alle acht Seminarmodule",
             "Zuzüglich Zertifizierungsgebühren für den Gesamtabschluss; Höhe wird noch bekannt gegeben. Supervision wird separat berechnet."),
        ],
        "content_title": "Inhalte und Ablauf",
        "modules": [
            ("1 Positive klinische Gesprächsführung",
             "Ressourcen, Hoffnung und Selbstwirksamkeit im Gespräch aufgreifen. Du übst, Entwicklungsmöglichkeiten zu erkunden und das Erleben von Belastung und Leid angemessen zu würdigen."),
            ("2 Positive klinische Diagnostik",
             "Stärken und Wohlbefinden ergänzend zur Symptomatik erfassen. Du nutzt die Ergebnisse für Fallverständnis, Behandlungsziele und Verlaufskontrolle."),
            ("3 Stärkenorientierte Behandlung und Psychotherapie",
             "Charakterstärken in die Behandlung integrieren und ihre Funktion im jeweiligen Kontext verstehen. Du berücksichtigst auch, wann eine Stärke übermäßig oder unpassend eingesetzt wird."),
            ("4 Achtsamkeit und Selbstmitgefühl",
             "Übungen zu Achtsamkeit und Selbstmitgefühl kennenlernen, anleiten und an individuelle Voraussetzungen und Belastungen anpassen."),
            ("5 Resilienzförderung und Ressourcenarbeit",
             "Persönliche, soziale und alltägliche Ressourcen erschließen. Das PERMA-Modell unterstützt die Planung konkreter Schritte zur Förderung von Wohlbefinden und Resilienz."),
            ("6 Positive Interventionen in der klinischen Praxis I",
             "Positive Interventionen anhand klinischer Ziele auswählen und verständlich vermitteln. Rückmeldungen der Patient:innen helfen dir, die Anwendung zu prüfen."),
            ("7 Positive Interventionen in der klinischen Praxis II",
             "Interventionen bei Schwierigkeiten anpassen und den Transfer in den Alltag unterstützen. Fallarbeit vertieft die klinische Entscheidungsfindung."),
            ("8 Möglichkeiten und Grenzen im störungsspezifischen Einsatz",
             "Indikation, Zeitpunkt und Grenzen positiv-psychologischer Interventionen reflektieren. Störungsbild, Schweregrad und individuelle Voraussetzungen bestimmen das Vorgehen."),
        ],
        "scope_title": "Umfang und Abschluss",
        "scope": [
            "Die acht zweitägigen Module umfassen insgesamt 128 Seminareinheiten an 16 Seminartagen, jeweils 16 Einheiten pro Modul. Hinzu kommen Praxis- und Supervisionsleistungen; deren genauer Umfang folgt mit der Ausschreibung. Für den ECQA-Gesamtabschluss sind alle Module sowie die vorgesehenen Praxis- und Supervisionsleistungen erforderlich. Für einzeln besuchte Module sind Mikrozertifikate vorgesehen.",
        ],
        "extras": [
            ("Anerkennung als Fortbildung", [
                "Die Anerkennung als Fortbildung nach dem Psychologengesetz und dem Psychotherapiegesetz ist in Arbeit. Über den aktuellen Stand informieren wir dich mit der Ausschreibung.",
            ]),
        ],
        "scope_link": None,
        "list_title": "Unverbindliche Interessentenliste für Clinical Expert",
        "list_text": "Geplanter Beginn ist Frühjahr 2028. Trage dich mit deinen Kontaktdaten unverbindlich in die Interessentenliste für Clinical Expert ein. Sobald die Ausschreibung vorliegt, erhältst du die Unterlagen für die verbindliche Anmeldung. Der Eintrag ist kostenfrei und reserviert noch keinen Platz.",
    },
}

# --------------------------------------------------------------------------- Über uns und Zertifizierung (Abschnitt 5)
ABOUT = {
    "eyebrow": "Über uns",
    "title": "Lerne bei Martin Wammerl und Michael Wohlkönig",
    "intro": "Dr. Martin Wammerl und Mag. Michael Wohlkönig sind zertifizierte Master-Trainer der Positiven Psychologie. Seit 2014 stehen sie im kontinuierlichen Austausch mit der internationalen Fachwelt. In der PERMA Mind Academy verbinden sie diesen Zugang zur Forschung mit klinischer Erfahrung, Coaching und Erwachsenenbildung. So lernst du wissenschaftliche Grundlagen und deren durchdachte Anwendung bei denselben Trainern.",
    "accordions": [
        ("Direkter Zugang zu den Menschen hinter den Modellen",
         ["Zu unserer fachlichen Entwicklung gehören persönliche Begegnungen und Austausch mit Martin Seligman, Mihály Csíkszentmihályi, Barbara Fredrickson, Kim Cameron und Tayyab Rashid. Teile unserer Ausbildung haben wir direkt bei den Begründern der Positiven Psychologie absolviert. Der seit 2014 bestehende Kontakt zur internationalen Forschungsgemeinschaft setzt sich in regelmäßigem Fachaustausch und der Teilnahme an europäischen und internationalen Konferenzen fort."]),
        ("Wissenschaftliche Aktualität als Teil der Ausbildung",
         ["Wir nutzen diesen Austausch, um neue Befunde einzuordnen und unsere Lehrinhalte weiterzuentwickeln. Im Seminar verbinden wir Forschungswissen mit Fragen aus der Anwendung: Für wen passt eine Intervention? Welche Ziele unterstützt sie? Welche Voraussetzungen und Grenzen sind zu beachten? So erhältst du Orientierung für fachlich begründete Entscheidungen."]),
    ],
    "trainers": [
        {"name": "Dr. Martin Wammerl MA MSc", "role": "Master-Trainer",
         "photo": "[Foto Dr. Martin Wammerl]", "alt": "Dr. Martin Wammerl, Trainer der PERMA Mind Academy",
         "teaser": "Klinischer Psychologe, Gesundheitspsychologe und Psychotherapeut für Verhaltenstherapie. Lehrtherapeut mit voller Lehrbefugnis sowie hypnosystemischer Coach und Supervisor.",
         "profile": [
             "Er verbindet psychiatrische und psychotherapeutische Praxis mit Forschung und Hochschullehre. Wissenschaftlich beschäftigt er sich mit der Messung von Wohlbefinden und der Evaluation positiv-psychologischer Programme, darunter PERMA.teach. Er ist Mitautor des Buches „Einführung in die Positive Psychologie“, das 2025 im facultas Verlag erschienen ist.",
         ],
         "quote": ("„Dies ist das umfassendste Buch zur Positiven Psychologie. Es sollte auf dem Schreibtisch aller Therapeut:innen, Coaches und Forscher:innen der Positiven Psychologie liegen.“",
                   "Martin Seligman über das Buch"),
         "after": [
             "In der Academy macht er wissenschaftliche Ergebnisse für die Praxis zugänglich. Seine Schwerpunkte sind die Grundlagen der Positiven Psychologie, Positive Education sowie klinische und psychotherapeutische Anwendungen. Du lernst, Forschungsbefunde kritisch zu lesen und für konkrete Fragestellungen zu nutzen.",
         ]},
        {"name": "Mag. Michael Wohlkönig", "role": "Master-Trainer",
         "photo": "[Foto Mag. Michael Wohlkönig]", "alt": "Mag. Michael Wohlkönig, Trainer der PERMA Mind Academy",
         "teaser": "Klinischer Psychologe, Gesundheitspsychologe, Sportpsychologe und Mentaltrainer.",
         "profile": [
             "Sein fachlicher Hintergrund umfasst Arbeits- und Organisationspsychologie sowie Weiterbildungen in systemischem und hypnosystemischem Coaching und Neuer Autorität.",
             "Seit 2013 wirkt er an der Entwicklung der Positiven Psychologie in Österreich und an Ausbildungsprogrammen mit. Seit 2014 ist er in der klinisch-psychologischen Behandlung tätig und arbeitet in seiner Praxis in Graz mit Erwachsenen, Kindern und Jugendlichen.",
         ],
         "quote": None,
         "after": [
             "Seine Schwerpunkte sind stärkenorientiertes Coaching, Resilienz, Positive Leadership und Neurodivergenz, insbesondere ADHS und Autismus. In der Academy bringt er Beispiele aus Beratung, Arbeitsleben, Familie und Sport ein. Sein Fokus liegt darauf, Methoden an unterschiedliche Menschen und Lebenssituationen anzupassen.",
         ]},
    ],
}

CERT = {
    "eyebrow": "Zertifizierung",
    "title": "Europäische Zertifizierung mit ECQA",
    "paras": [
        "Mit einem ECQA-Abschluss erhältst du ein europäisch ausgerichtetes Zertifikat, das deine nachgewiesenen Kompetenzen dokumentiert. Die Zertifizierung erfolgt in einem externen Rahmen mit definierten fachlichen Anforderungen. Für dich entsteht ein Nachweis, dessen Grundlage über die Bewertung durch unsere Academy hinausgeht.",
        "Bei der Wahl einer Ausbildung lohnt sich ein Blick auf den Abschluss: Eine reine Teilnahmebestätigung bescheinigt den Besuch eines Lehrgangs. Ein institutseigenes Zertifikat folgt den Anforderungen des jeweiligen Anbieters und kann ebenfalls eine Prüfung voraussetzen. ECQA ergänzt die Ausbildung um die Zertifizierung durch eine unabhängige Stelle anhand festgelegter Kompetenzen und Bewertungskriterien.",
    ],
    "logo_placeholder": "[ECQA-Logo nach Freigabe]",
    "accordions": [
        ("Dein Vorteil gegenüber einem rein internen Abschluss", [
            "Du kannst deine Qualifikation nachvollziehbar darstellen: Gegenüber Arbeitgeber:innen und Auftraggeber:innen verweist du auf einen externen Kompetenznachweis. Das ist besonders hilfreich, wenn dein Gegenüber den Ausbildungsanbieter noch nicht kennt.",
            "Du erkennst, was der Abschluss voraussetzt: Definierte Kompetenzen und Bewertungskriterien machen die Anforderungen transparent. Deine Kenntnisse und Fähigkeiten werden überprüft; die bloße Teilnahme reicht für das ECQA-Zertifikat nicht aus.",
            "Du erhältst einen europäisch ausgerichteten Nachweis: ECQA arbeitet über einzelne Bildungsanbieter und Länder hinweg. Das erleichtert es, den Abschluss auch in internationalen beruflichen Zusammenhängen zu erläutern. Eine automatische berufliche Zulassung in anderen Ländern ist damit nicht verbunden.",
        ]),
        ("Vom Lernen zum nachgewiesenen Können", [
            "Die Vorbereitung auf den Abschluss ist mit der Ausbildung verbunden. Du setzt dich mit wissenschaftlichen Grundlagen auseinander, übst ihre Anwendung und bearbeitest die vorgesehenen Praxisaufgaben. Bei Basic steht dabei dein eigenes Projekt im Mittelpunkt, bei Advanced die vertiefte Anwendung und Trainingsgestaltung, bei Clinical Expert die klinische Praxis einschließlich Supervision.",
            "Die Zertifizierungsgebühren sind im Lehrgangspreis nicht enthalten. Ihre Höhe wird noch bekannt gegeben. Die konkreten Abschlussanforderungen erhältst du mit der Ausschreibung.",
        ]),
    ],
    "button": "Ausbildungen und Abschlüsse vergleichen",
}

# --------------------------------------------------------------------------- FAQ, Newsletter, Kontakt (Abschnitt 6)
FAQ = {
    "eyebrow": "Fragen",
    "title": "Häufige Fragen zur Ausbildung in Positiver Psychologie",
    "items": [
        ("Was zeichnet die PERMA Mind Academy aus?",
         "Unsere Trainer verbinden den kontinuierlichen internationalen Fachaustausch seit 2014 mit eigener Forschungs- und Praxiserfahrung. Teile ihrer Ausbildung haben sie direkt bei den Begründern der Positiven Psychologie absolviert. Diese Verbindung prägt die Inhalte und ihre Vermittlung. Hinzu kommt der ECQA-Abschluss als europäischer Kompetenznachweis."),
        ("Welchen Nutzen hat die ECQA-Zertifizierung?",
         "Gegenüber einer reinen Teilnahmebestätigung weist das ECQA-Zertifikat überprüfte Kompetenzen nach. Gegenüber einem rein institutseigenen Abschluss kommt eine unabhängige Zertifizierungsstelle mit festgelegten Anforderungen hinzu. Der europäisch ausgerichtete Nachweis unterstützt dich dabei, deine Qualifikation gegenüber Arbeitgeber:innen und Auftraggeber:innen zu erläutern. Die Höhe der zusätzlichen Zertifizierungsgebühren wird noch bekannt gegeben."),
        ("Welche Ausbildung passt zu mir?",
         "Basic ist dein Einstieg, wenn du Positive Psychologie verstehen und persönlich oder beruflich anwenden möchtest. Advanced baut auf dem abgeschlossenen Basic auf und vertieft die professionelle Arbeit einschließlich eigener Trainings. Clinical Expert richtet sich gezielt an klinische Psycholog:innen und Psychotherapeut:innen."),
        ("Welche Voraussetzung gilt für Advanced?",
         "Eine abgeschlossene Basic-Ausbildung in Positiver Psychologie ist Voraussetzung. Vergleichbare Vorkenntnisse allein ersetzen diesen Abschluss nicht."),
        ("Wann starten die Lehrgänge?",
         "Die Termine der drei Basic-Module folgen. Advanced beginnt voraussichtlich Anfang 2028, PERMA Clinical Expert im Frühjahr 2028."),
        ("Wo finden die Ausbildungen statt?",
         "Die Lehrgänge sind als Präsenzveranstaltungen geplant. Basic und Clinical Expert sollen im Raum Graz stattfinden. Für Advanced wird der Veranstaltungsort noch bekannt gegeben. Die genauen Angaben erhältst du mit der Ausschreibung."),
        ("Kann ich einzelne Module buchen?",
         "Bei Clinical Expert kannst du einzelne Module buchen und auf das Gesamtzertifikat anrechnen lassen. Dafür sind zusätzlich die Praxis- und Supervisionsleistungen erforderlich. Basic und Advanced sind zusammenhängende Lehrgänge."),
        ("Wie funktioniert die Anmeldung?",
         "Trage dich zunächst unverbindlich in die Interessentenliste ein. Sobald die Ausschreibung vorliegt, senden wir dir Termine, Konditionen und Unterlagen für die verbindliche Anmeldung. Der Eintrag reserviert noch keinen Platz. Nach verbindlicher Anmeldung erfolgt die Zahlung per Überweisung."),
    ],
}

NEWSLETTER = {
    "eyebrow": "Newsletter",
    "title": "Neuigkeiten aus der PERMA Mind Academy",
    "text": "Bleib über neue Ausbildungsangebote, Termine und Entwicklungen der PERMA Mind Academy informiert. Abonniere unseren Newsletter unabhängig von einer Lehrgangsanmeldung. Du kannst dich jederzeit wieder abmelden.",
    "consent": "Ich möchte den Newsletter der PERMA Mind Academy erhalten. Ich kann mich jederzeit wieder abmelden. Informationen zur Verarbeitung meiner Angaben finde ich in der Datenschutzerklärung.",
    "button": "Newsletter abonnieren",
    "done": "Bitte bestätige deine Newsletter-Anmeldung über den Link in unserer E-Mail.",
}

# Social Media (Footer). Leere Adresse = Symbol wird nicht angezeigt (LinkedIn folgt laut Besprechung 19.11.2026).
SOCIAL = [
    ("instagram", "https://www.instagram.com/permamindacademy/"),
    ("facebook", "https://www.facebook.com/profile.php?id=61593453518327"),
    ("linkedin", ""),
]

CONTACT = {
    "title": "Kontakt",
    "text": "Du möchtest klären, welcher Lehrgang zu deinem beruflichen Hintergrund passt? Schreib uns über das Kontaktformular. Wenn du über den Start informiert werden möchtest, trage dich unverbindlich in die Interessentenliste für die gewünschte Ausbildung ein.",
    "button": "Nachricht senden",
    "done": "Danke für deine Nachricht. Wir melden uns per E-Mail bei dir.",
}

# --------------------------------------------------------------------------- Interessentenliste (Abschnitt 7)
LIST = {
    "title": "Unverbindliche Interessentenliste",
    "intro": "Trage dich unverbindlich für Basic, Advanced oder Clinical Expert ein. Du kannst auch mehrere Ausbildungen auswählen. Sobald die jeweilige Ausschreibung vorliegt, informieren wir dich über die Termine und senden dir die Unterlagen für die verbindliche Anmeldung.",
    "intro2": "Der Eintrag ist kostenfrei und reserviert noch keinen Ausbildungsplatz. Den Newsletter erhältst du nur, wenn du ihn zusätzlich abonnierst.",
    "interest_legend": "Ich interessiere mich für",
    "hint": "Mit deinem Eintrag nehmen wir dich in die Interessentenliste für deine ausgewählten Ausbildungen auf. Du erhältst dazu Informationen und später die Unterlagen für die verbindliche Anmeldung per E-Mail.",
    "newsletter": "Ja, ich möchte zusätzlich den Newsletter der PERMA Mind Academy mit Informationen zu Ausbildungen und Seminarterminen erhalten. Ich kann mich jederzeit wieder abmelden.",
    "button": "Unverbindlich eintragen",
    "done": "Danke für dein Interesse an der PERMA Mind Academy. Du bist unverbindlich in der Interessentenliste für deine ausgewählten Ausbildungen eingetragen. Sobald die jeweilige Ausschreibung vorliegt, senden wir dir die Unterlagen für die verbindliche Anmeldung. Dein Eintrag reserviert noch keinen Platz.",
}

PRIVACY_NOTE = "Informationen zur Verarbeitung deiner Angaben findest du in unserer {link}."
