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
     "card_meta": "Start Herbst 2027 · Präsenz im Raum Graz · 1.997 € Frühbucher / 2.397 € regulär",
     "card_button": "Zur Basic-Ausbildung", "list_button": "Zur Basic-Interessentenliste"},
    {"key": "advanced", "accent": "purple", "name": "Positive Psychology Advanced",
     "short": "Advanced", "form_label": "Positive Psychology Advanced",
     "card_text": "Du hast Basic oder eine gleichwertige Ausbildung abgeschlossen und möchtest Positive Psychologie professionell einsetzen? Advanced vertieft die Anwendung in Coaching, Bildung, Gesundheitsförderung und Führung. Du lernst, Interventionen auszuwählen und eigene Trainings zu entwickeln.",
     "card_meta": "Start Anfang 2028 · Basic-Abschluss oder anerkannter gleichwertiger Abschluss erforderlich · 1.398 € Frühbucher / 1.596 € regulär",
     "card_button": "Zum Advanced-Lehrgang", "list_button": "Zur Advanced-Interessentenliste"},
    {"key": "clinical", "accent": "orange", "name": "PERMA Clinical Expert",
     "short": "Clinical Expert", "form_label": "PERMA Clinical Expert",
     "card_text": "Du arbeitest als klinische:r Psycholog:in oder Psychotherapeut:in? Vertiefe die Arbeit mit Stärken und Ressourcen in Diagnostik, Behandlungsplanung und Therapie. Fallarbeit und Supervision unterstützen die Übertragung in deine klinische Praxis.",
     "card_meta": "Start Frühjahr 2028 · Präsenz im Raum Graz · 370 € je Modul / 2.960 € für acht Module",
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
# Übergabe 22.11.2026: Formulierung für mehrteilige Lehrgänge
RATEN = "Für mehrteilige Lehrgänge bieten wir auf Anfrage Ratenzahlung an. Die Höhe der Raten und die Zahlungstermine teilen wir dir vor der verbindlichen Anmeldung schriftlich mit."

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
            ("Beginn", "Herbst 2027; die Termine der drei Module werden noch bekannt gegeben"),
            ("Aufbau", "Neun Seminartage in drei Blöcken"),
            ("Format und Ort", "Präsenz im Raum Graz; genauer Ort wird bekannt gegeben"),
            ("Umfang", "148 Einheiten à 45 Minuten"),
            ("Abschluss", "ECQA-Zertifikat nach Erfüllung der Abschlussanforderungen"),
            ("Kosten", "1.997 € Frühbucherpreis / 2.397 € regulär",
             "Frühbucherpreis bis acht Wochen vor dem ersten Modul. Zuzüglich Zertifizierungsgebühr; Höhe folgt. Ratenzahlung auf Anfrage."),
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
            "Voraussichtlicher Start im Herbst 2027. Die Ausbildung findet in Präsenz im Raum Graz statt und umfasst neun Seminartage in drei Blöcken. Die Termine der drei Module und den genauen Veranstaltungsort geben wir noch bekannt.",
            "Die Ausbildung umfasst 148 Einheiten à 45 Minuten. Der Seminarteil umfasst 100 Einheiten. Hinzu kommen 20 Einheiten Peergruppenarbeit, acht Einheiten Gruppencoaching und 20 Einheiten für dein Praxisprojekt. Für den ECQA-Abschluss sind mindestens 80 % Anwesenheit in den Seminareinheiten erforderlich. Du fasst das Projekt schriftlich zusammen und präsentierst es zum Abschluss. Der Basic-Abschluss eröffnet dir den Zugang zu Advanced.",
            "Der Frühbucherpreis gilt bis acht Wochen vor dem ersten Modul. Das konkrete Datum folgt mit der Ausschreibung. " + RATEN,
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
            "Der Lehrgang richtet sich an Coaches, Berater:innen, Pädagog:innen, Fachkräfte im Gesundheitsbereich, Führungskräfte und Trainer:innen. Voraussetzung ist der Basic-Abschluss oder ein anerkannter gleichwertiger Abschluss.",
        ],
        "facts": [
            ("Beginn", "Anfang 2028; Termine folgen"),
            ("Aufbau und Format", "Drei Zweitagesblöcke in Präsenz geplant; Ort folgt"),
            ("Voraussetzung", "Basic-Abschluss der PERMA Mind Academy, EUPPA-Basic-Abschluss oder zertifizierte:r Anwender:in der Positiven Psychologie DACH-PP (Level 1)",
             "Andere Abschlüsse prüfen wir einzeln auf Gleichwertigkeit. Schick uns dafür deinen Abschlussnachweis mit Angaben zu Inhalt und Umfang."),
            ("Umfang", "94 Einheiten à 45 Minuten"),
            ("Abschluss", "ECQA-Zertifikat nach Erfüllung der Abschlussanforderungen"),
            ("Kosten", "1.398 € Frühbucherpreis / 1.596 € regulär",
             "Frühbucherpreis bis acht Wochen vor dem ersten Modul. Zuzüglich Zertifizierungsgebühr; Höhe folgt. Ratenzahlung auf Anfrage."),
        ],
        "content_title": "Inhalte und Arbeitsweise",
        "modules": [
            ("1 Beyond PERMA: Contemporary Positive Psychology",
             "Jemand berichtet im Coaching von beruflicher Überlastung. Ist eine Stärkenübung jetzt sinnvoll? Du lernst die Positive Psychologie 2.0 kennen und untersuchst, wie Wohlbefinden und schwierige Gefühle zusammenhängen. An einer Studie zu Stärkenübungen prüfst du, wer teilgenommen hat und was sich aus den Ergebnissen für den Fall ableiten lässt. Du begründest schriftlich, ob und wie du die Übung einsetzen würdest, und beziehst Arbeitsbedingungen und kulturelles Umfeld ein."),
            ("2 Positive Coaching & Change",
             "Wie begleitest du jemanden, der sich Veränderung wünscht und zugleich am Gewohnten festhält? Du klärst den Coachingauftrag, arbeitest mit Stärken und Werten und leitest einen machbaren nächsten Schritt ab. In Dreiergruppen übst du Coachinggespräche mit wechselnden Rollen und erhältst Rückmeldung. Dabei besprecht ihr auch, wo die Grenze zwischen Coaching und Behandlung liegt."),
            ("3 Positive Education & Development",
             "Du lernst das österreichische Programm PERMA.teach und das Positive-Education-Projekt der australischen Geelong Grammar School kennen. Du vergleichst, wie Lehrkräfte vorbereitet werden und wie Positive Psychologie im Unterricht und im Schulleben verankert wird. Am Beispiel von Growth Mindset prüfst du, welche Schlüsse die Forschung für den Unterricht zulässt. Für eine Bildungseinrichtung entwirfst du einen Einführungsplan mit einer konkreten Lernsequenz. Du legst fest, wie du die Umsetzung dokumentierst und das Wohlbefinden von Lernenden und Lehrenden vor und nach der Einführung erhebst."),
            ("4 Positive Health, Resilience & Recovery",
             "Für die Gesundheitsförderung lernst du Übungen zur Stressregulation, zur Erholung und zum Selbstmitgefühl kennen. An einem Praxisfall entwickelst du eine Präventionsmaßnahme und legst fest, wie du ihren Nutzen überprüfst. Du klärst, was eine Übung leisten kann und wann sich Rahmenbedingungen ändern sollten oder Unterstützung durch eine Fachstelle sinnvoll ist."),
            ("5 Positive Leadership & Organizations",
             "Im Mittelpunkt steht Positive Leadership nach Kim Cameron. An einem Teamfall vergleichst du Camerons Ansatz mit PERMA-Lead nach Markus Ebner und untersuchst, wie Führungskräfte Arbeitsbeziehungen stärken und Sinn in der Arbeit vermitteln können. Aus Camerons Ansatz leitest du eine konkrete Maßnahme für das Team ab. Im Rollenspiel übst du, kritisches Feedback klar und wertschätzend zu geben."),
            ("6 Interventionen und Trainings gestalten",
             "Du entwickelst eine Intervention oder ein Training für eine Zielgruppe aus deinem Berufsfeld. Du planst, was die Teilnehmenden lernen oder ausprobieren sollen und welche Methoden dazu passen. Im Seminar leitest du eine kurze Sequenz an und überarbeitest sie anhand der Rückmeldungen. Du legst fest, wie du den Transfer in den Arbeitsalltag überprüfst."),
        ],
        "scope_title": "Umfang und Abschluss",
        "scope": [
            "Advanced umfasst 94 Einheiten à 45 Minuten. Dazu zählen 60 Seminareinheiten, vier Einheiten Gruppencoaching, 20 Einheiten Praxisarbeit und Selbststudium sowie zehn Einheiten Peergruppenarbeit. Für den Abschluss sind mindestens 80 % Anwesenheit in den Seminaren erforderlich. Gruppencoaching, Peergruppenarbeit und Praxisnachweis sind vollständig zu absolvieren.",
            "Als Praxisnachweis dokumentierst du entweder zwei praktische Anwendungsfälle oder ein selbst durchgeführtes Praxisprojekt. In beiden Varianten reflektierst du dein Vorgehen schriftlich und präsentierst deine Arbeit zum Abschluss. Der ECQA-Abschluss setzt eine positive Beurteilung und die Erfüllung der Abschlussanforderungen voraus.",
            "Der Frühbucherpreis gilt bis acht Wochen vor dem ersten Modul. Das konkrete Datum folgt mit der Ausschreibung. " + RATEN,
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
            ("Zielgruppe", "Klinische Psycholog:innen und Psychotherapeut:innen"),
            ("Beginn und Format", "Frühjahr 2028; Präsenz im Raum Graz geplant. Termine und Ort folgen"),
            ("Aufbau und Buchung", "Acht zweitägige Module zu je 16 Einheiten; einzeln oder als Lehrgang buchbar"),
            ("Abschluss", "ECQA-Gesamtabschluss mit Supervision und Falldokumentation; Mikrozertifikat je Modul"),
            ("Kosten", "370 € je Modul / 2.960 € für alle acht Module",
             "Supervision wird gesondert verrechnet. Alle Module plus 25 Gruppensupervisionseinheiten: 4.460 € zuzüglich Zertifizierungsgebühr. Ratenzahlung auf Anfrage."),
        ],
        "content_title": "Inhalte und Ablauf",
        "modules": [
            ("1 Positive klinische Gesprächsführung",
             "Wie lassen sich Stärken und Hoffnung im klinischen Gespräch ansprechen, wenn zunächst das Leiden im Vordergrund steht? Du übst, Belastungen anzuerkennen, widersprüchliche Gefühle aufzugreifen und Fragen zu stellen, die Raum für die Sichtweise deines Gegenübers lassen. Dabei erkundest du frühere Bewältigungserfahrungen, hilfreiche Beziehungen und persönliche Handlungsspielräume. In Gesprächsübungen erhältst du Rückmeldung dazu, wie deine Fragen und Zusammenfassungen ankommen.",
             ["Belastende Erfahrungen und Ambivalenz in eigenen Worten zusammenfassen und im Gespräch prüfen, ob sich dein Gegenüber verstanden fühlt.",
              "Nach Ressourcen und Ausnahmen fragen und dabei herausarbeiten, was die Person selbst beigetragen hat und was durch Unterstützung oder äußere Umstände möglich wurde.",
              "Mit Patient:innen aus einem persönlichen Anliegen ein Behandlungsziel formulieren und klären, wie zuversichtlich sie sind, einen ersten Schritt zu setzen."]),
            ("2 Positive klinische Diagnostik",
             "Du lernst, die klinische Diagnostik um Charakterstärken, Hoffnung, Selbstwirksamkeit und unterschiedliche Aspekte des Wohlbefindens zu erweitern. Ein VIA-Stärkenprofil gibt dir einen Zugang zu selbst eingeschätzten Charakterstärken. Mit dem PERMA-Profiler betrachtest du positive Emotionen, Engagement, Beziehungen, Sinnerleben und das Erreichen persönlicher Ziele. Du vergleichst diese Zugänge mit der Skala zur Allgemeinen Selbstwirksamkeitserwartung und mit Interviewfragen zur Hoffnung: Welche Wege zu einem Ziel sieht eine Person, und inwieweit traut sie sich zu, diese zu verfolgen?",
             ["Aus einer klinischen Fragestellung ableiten, welches Merkmal du erfassen möchtest und ob sich dafür Interview, Verhaltensbeobachtung oder Fragebogen eignet. Bei einem Fragebogen kannst du Sprachfassung, Vergleichswerte und Grenzen der Interpretation beurteilen.",
              "Ein Stärkenprofil verständlich rückmelden, die Rangfolge als relative Selbsteinschätzung erklären und mit Erfahrungen aus unterschiedlichen Lebensbereichen abgleichen.",
              "Ressourcen, Symptombelastung und Funktionsniveau in einer klinischen Fallformulierung zusammenführen. Daraus kannst du ein Behandlungsziel ableiten und passende Kriterien für die Verlaufskontrolle wählen."]),
            ("3 Stärkenorientierte Behandlung und Psychotherapie",
             "Im Mittelpunkt steht die Frage, wie Patient:innen ihre Charakterstärken für ein Behandlungsziel nutzen können. Du untersuchst, welche Funktion der Einsatz einer Stärke im jeweiligen Lebenskontext hat. Auch eine vertraute Stärke kann je nach Situation zu selten, zu häufig oder wenig passend eingesetzt werden. Du lernst, solche Muster gemeinsam zu erkennen und neue Handlungsmöglichkeiten in der Sitzung vorzubereiten und im Alltag zu erproben.",
             ["Charakterstärken anhand konkreter Handlungen herausarbeiten und mit Patient:innen klären, welche Bedeutung diese Stärken für ihr Selbstbild und ihre Ziele haben.",
              "Erkennen, in welchen Situationen eine Stärke Handlungsspielraum eröffnet oder ein belastendes Muster aufrechterhält, und einen flexibleren Einsatz mit der Person erarbeiten.",
              "Ein Verhaltensexperiment zum Einsatz einer Stärke planen, eine überprüfbare Erwartung formulieren und die beobachteten Folgen für die weitere Behandlung nutzen."]),
            ("4 Achtsamkeit und Selbstmitgefühl",
             "Du erprobst zwei unterschiedliche therapeutische Zugänge. Achtsamkeitsübungen richten die Aufmerksamkeit darauf, wie Gedanken, Gefühle und körperliche Empfindungen im gegenwärtigen Moment erlebt werden. Bei Übungen zum Selbstmitgefühl steht die Frage im Mittelpunkt, wie Menschen sich in belastenden Momenten selbst begegnen. In Selbsterfahrung und angeleiteter Praxis lernst du, beide Zugänge verständlich zu vermitteln und die Intensität einer Übung auf die Person abzustimmen.",
             ["Aus dem Behandlungsziel ableiten, ob das bewusste Wahrnehmen innerer Vorgänge oder ein hilfreicherer Umgang mit Selbstkritik im Vordergrund stehen soll.",
              "Kurze Übungen anleiten und Wahlmöglichkeiten eröffnen. Bei Unbehagen kannst du die Aufmerksamkeit auf die äußere Umgebung lenken, die Übung verkürzen oder sie gemeinsam beenden.",
              "Mit Patient:innen eine selbstmitfühlende Antwort in ihrer eigenen Sprache entwickeln und im Verlauf prüfen, wie sich diese auf Selbstkritik und weiteres Handeln auswirkt."]),
            ("5 Resilienzförderung und Ressourcenarbeit",
             "In der klinischen Ressourcenarbeit geht es auch darum, welche Unterstützung unter anhaltender Belastung tatsächlich erreichbar ist. Du erarbeitest eine Ressourcenlandkarte, die persönliche Fähigkeiten, soziale Beziehungen und praktische Hilfen sichtbar macht. Das PERMA-Modell dient dir als Gesprächsrahmen, um etwa nach Zugehörigkeit, Sinnerleben und Erfahrungen von Kompetenz zu fragen. Du beziehst äußere Belastungsfaktoren in die Planung ein und klärst, wo Veränderungen im Umfeld nötig sind.",
             ["Vorhandene und nutzbare Ressourcen unterscheiden und mit Patient:innen herausarbeiten, was den Zugang zu Unterstützung erleichtert oder erschwert.",
              "Einen realistischen Plan zur Entlastung entwickeln, der eigene Handlungsmöglichkeiten, Beiträge des Umfelds und Alternativen bei absehbaren Hindernissen berücksichtigt.",
              "Frühzeichen zunehmender Überlastung erheben und mit der Person überprüfen, welche Maßnahmen im Alltag tragen und wo zusätzliche Unterstützung gebraucht wird."]),
            ("6 Positive Interventionen in der klinischen Praxis I",
             "In diesem Modul lernst du, positiv-psychologische Interventionen für ein konkretes klinisches Behandlungsziel auszuwählen und erstmals anzuleiten. Du vergleichst etwa das bewusste Auskosten angenehmer Erfahrungen (Savoring) mit dem schriftlichen Rückblick auf hilfreiche Alltagsmomente. Dabei arbeitest du heraus, worauf die jeweilige Übung die Aufmerksamkeit richtet, was sie von Patient:innen verlangt und wie du ihren Zweck vermittelst. Auch ausbleibende oder unangenehme Reaktionen haben in der Nachbesprechung Platz.",
             ["Aus einem Behandlungsziel ableiten, ob eine Intervention etwa die Wahrnehmung angenehmer Erfahrungen, soziale Verbundenheit oder das Erleben eigener Handlungsmöglichkeiten ansprechen soll.",
              "Die Auswahl begründen, eine Übung im Einverständnis mit der Person anleiten und Dauer und Anforderungen an Konzentration, Energie und Alltag anpassen.",
              "Eine erste Anwendung zwischen den Sitzungen vereinbaren und eine Beobachtungsfrage formulieren, mit der die Person ihre tatsächliche Erfahrung festhalten kann."]),
            ("7 Positive Interventionen in der klinischen Praxis II",
             "Hier steht der Verlauf einer bereits begonnenen Intervention im Mittelpunkt. Du lernst, Rückmeldungen aus Sitzungen, Beobachtungen aus dem Alltag und Veränderungen der Symptomatik gemeinsam auszuwerten. Wenn der erwartete Nutzen ausbleibt, prüfst du, ob das Behandlungsziel noch passt, die Übung umsetzbar war oder unerwünschte Wirkungen aufgetreten sind. Dazu gehört auch, Leistungsdruck oder Selbstabwertung anzusprechen, die durch einen Übungsauftrag entstehen können.",
             ["Anhand von Rückmeldungen und Verlaufsdaten einschätzen, ob die Durchführung schwierig war, der erhoffte Nutzen ausgeblieben ist oder die Person die Übung als belastend erlebt hat.",
              "Mit Patient:innen entscheiden, ob ihr die Anleitung, die Häufigkeit oder den Zeitpunkt anpasst, eine andere Intervention wählt oder die Übung beendet.",
              "Für den nächsten Behandlungsschritt ein Beobachtungskriterium und einen Zeitpunkt zur Auswertung festlegen sowie die Entscheidung für Dokumentation und Supervision begründen."]),
            ("8 Möglichkeiten und Grenzen im störungsspezifischen Einsatz",
             "Du setzt dich mit der Frage auseinander, wann positiv-psychologische Interventionen eine störungsspezifische Behandlung sinnvoll ergänzen. Unter anderem vergleichst du ihren möglichen Stellenwert bei depressiven Störungen und Angststörungen. Du prüfst, wie gut sich Forschungsbefunde auf die jeweilige klinische Fragestellung übertragen lassen. Für deine Entscheidung berücksichtigst du die Funktion der Symptome, den Schweregrad, die Behandlungsphase und die Präferenzen der Patient:innen.",
             ["Begründen, welches störungsspezifische Behandlungsziel eine Intervention unterstützen kann und welche Voraussetzungen für ihren Einsatz erfüllt sein sollten.",
              "Hinweise auf Vermeidung, Überforderung oder akute Gefährdung einordnen und erkennen, wann Risikoabklärung, Krisenintervention oder andere Behandlungsschritte Vorrang haben.",
              "Nutzen, Grenzen und Alternativen mit Patient:innen besprechen, die gemeinsame Entscheidung dokumentieren und festlegen, wann die Indikation erneut geprüft wird."]),
        ],
        "scope_title": "Gesamtabschluss und Mikrozertifikate",
        "scope": [
            "Die Fortbildung richtet sich an klinische Psycholog:innen und Psychotherapeut:innen. Acht zweitägige Module mit je 16 Einheiten ergeben insgesamt 128 Seminareinheiten à 45 Minuten. Die Module können einzeln oder als Lehrgang gebucht werden. Die Mindestanwesenheit beträgt 80 % in jedem Modul.",
            "Für den Gesamtabschluss absolvierst du alle acht Module und 25 Supervisionseinheiten à 45 Minuten. Einzel- und Gruppensupervision kannst du kombinieren. Jede absolvierte Einheit zählt gleich. Du dokumentierst und anonymisierst zwei Fälle aus deiner eigenen klinischen Praxis schriftlich und besprichst mindestens einen davon in der Supervision. Der Lehrgang umfasst 153 Seminar- und Supervisionseinheiten. Die Falldokumentation kommt hinzu.",
            "Für ein Mikrozertifikat eines Einzelmoduls brauchst du mindestens 80 % Anwesenheit im jeweiligen Modul und eine kurze schriftliche Transferaufgabe. Darin beschreibst du, wie du eine Methode aus dem Modul in deiner Praxis einsetzen würdest. Abgeschlossene Module sind auf den Gesamtlehrgang anrechenbar.",
            "Die ECQA-Zertifizierung ist für Basic, Advanced sowie für den Clinical-Expert-Gesamtabschluss und die Mikrozertifikate bestätigt. Bis zur Ausgabe der ECQA-Mikrozertifikate stellt die Academy die Mikrozertifikate selbst aus. Die gesetzliche Fortbildungsanerkennung nach dem Psychologengesetz und dem Psychotherapiegesetz ist in Arbeit.",
        ],
        "extras": [
            ("Preise und Supervision", [
                "Einzeln gebuchtes Seminarmodul: 370 €<br>Alle acht Seminarmodule: 2.960 €<br>Einzelsupervision à 45 Minuten: 120 €<br>Gruppensupervision à 45 Minuten, maximal vier Personen: 60 € je Person<br>Alle Seminarmodule plus 25 Gruppensupervisionseinheiten: 4.460 € zuzüglich Zertifizierungsgebühr",
                "Der Gruppentarif von 60 € pro Person ist ein Fixpreis. Bei kombinierter oder reiner Einzelsupervision hängt der Gesamtpreis von der gewählten Aufteilung ab. Für den Erwerb eines Mikrozertifikats pro Modul ist keine Supervision vorgesehen. " + RATEN,
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
    # Fotos von den IPPA-Weltkongressen unter den Trainerprofilen (Martin Wammerl, 24.11.2026)
    "research": {
        "title": "Aus unserer Forschungsarbeit",
        "figures": [
            ("ippa-orlando-2015.webp", "Martin Wammerl und Michael Wohlkönig vor ihrem Poster zum PERMA-Profiler und Positive Psychotherapy Inventory",
             "Orlando, USA, 25. bis 28. Juni 2015",
             "Martin Wammerl und Michael Wohlkönig beim 4. IPPA-Weltkongress in Lake Buena Vista bei Orlando. Der PERMA-Profiler und das Positive Psychotherapy Inventory waren in ihren deutschsprachigen Fassungen die ersten beiden multifaktoriellen Verfahren, mit denen die PERMA-Theorie des Wohlbefindens im deutschen Sprachraum empirisch überprüft wurde."),
            ("ippa-montreal-2017.webp", "Martin Wammerl und Michael Wohlkönig vor ihrem Poster zur Burnoutprävention mit PERMA",
             "Montreal, Kanada, 13. bis 16. Juli 2017",
             "Martin Wammerl und Michael Wohlkönig beim 5. IPPA-Weltkongress. Der Posterbeitrag stellte das erste Burnoutpräventionsprogramm im deutschen Sprachraum vor, das auf den fünf PERMA-Bausteinen aufbaute. Das Programm richtete sich an Fachkräfte in psychosozialen Berufen."),
        ],
    },
    "trainers": [
        {"name": "Dr. Martin Wammerl MA MSc", "role": "Master-Trainer",
         "photo": "[Foto Dr. Martin Wammerl]", "alt": "Dr. Martin Wammerl, Trainer der PERMA Mind Academy",
         "image": "trainer-martin-wammerl.webp",
         "figure": ("martin-wammerl-martin-seligman-2014.webp", "Martin Wammerl und Martin Seligman",
                    "Martin Wammerl und Martin Seligman in Rosenheim, Deutschland, 2014"),
         "teaser": "Klinischer Psychologe, Gesundheitspsychologe und Psychotherapeut für Verhaltenstherapie. Lehrtherapeut mit voller Lehrbefugnis sowie hypnosystemischer Coach und Supervisor.",
         "profile": [
             "Er verbindet psychiatrische und psychotherapeutische Praxis mit Forschung und Hochschullehre. Wissenschaftlich beschäftigt er sich mit der Messung von Wohlbefinden und der Evaluation positiv-psychologischer Programme, darunter PERMA.teach. Er ist Mitautor des Buches „Einführung in die Positive Psychologie“, das 2025 im facultas Verlag erschienen ist.",
         ],
         "quote": ("„Dies ist das umfassendste Buch zur Positiven Psychologie. Es sollte auf dem Schreibtisch aller Therapeut:innen, Coaches und Forscher:innen der Positiven Psychologie liegen.“",
                   "Martin Seligman über „Einführung in die Positive Psychologie“, facultas Verlag, 2025"),
         "after": [
             "In der Academy macht er wissenschaftliche Ergebnisse für die Praxis zugänglich. Seine Schwerpunkte sind die Grundlagen der Positiven Psychologie, Positive Education sowie klinische und psychotherapeutische Anwendungen. Du lernst, Forschungsbefunde kritisch zu lesen und für konkrete Fragestellungen zu nutzen.",
         ]},
        {"name": "Mag. Michael Wohlkönig", "role": "Master-Trainer",
         "photo": "[Foto Mag. Michael Wohlkönig]", "alt": "Mag. Michael Wohlkönig, Trainer der PERMA Mind Academy",
         "image": "trainer-michael-wohlkoenig.webp",
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
         "Gegenüber einer reinen Teilnahmebestätigung weist das ECQA-Zertifikat überprüfte Kompetenzen nach. Gegenüber einem rein institutseigenen Abschluss kommt eine unabhängige Zertifizierungsstelle mit festgelegten Anforderungen hinzu. Der europäisch ausgerichtete Nachweis unterstützt dich dabei, deine Qualifikation gegenüber Arbeitgeber:innen und Auftraggeber:innen zu erläutern. Die ECQA-Zertifizierung ist für Basic, Advanced sowie für den Clinical-Expert-Gesamtabschluss und die Mikrozertifikate bestätigt. Die Höhe der Zertifizierungsgebühren wird noch bekannt gegeben."),
        ("Welche Ausbildung passt zu mir?",
         "Basic ist dein Einstieg, wenn du Positive Psychologie verstehen und persönlich oder beruflich anwenden möchtest. Advanced baut auf dem Basic-Abschluss oder einem anerkannten gleichwertigen Abschluss auf und vertieft die professionelle Arbeit einschließlich eigener Trainings. Clinical Expert richtet sich gezielt an klinische Psycholog:innen und Psychotherapeut:innen."),
        ("Welche Voraussetzung gilt für Advanced?",
         "Zum Einstieg berechtigen der Basic-Abschluss der PERMA Mind Academy, der bisherige EUPPA-Basic-Abschluss der European Positive Psychology Academy oder der Abschluss als zertifizierte:r Anwender:in der Positiven Psychologie DACH-PP (Level 1). Andere Abschlüsse prüfen wir einzeln auf Gleichwertigkeit. Kontaktiere uns dafür mit deinem Abschlussnachweis und Angaben zu Inhalt und Umfang deiner Ausbildung."),
        ("Wann starten die Lehrgänge?",
         "Basic startet voraussichtlich im Herbst 2027, Advanced Anfang 2028 und PERMA Clinical Expert im Frühjahr 2028. Die genauen Termine folgen mit der Ausschreibung."),
        ("Wo finden die Ausbildungen statt?",
         "Die Lehrgänge sind als Präsenzveranstaltungen geplant. Basic und Clinical Expert sollen im Raum Graz stattfinden. Für Advanced wird der Veranstaltungsort noch bekannt gegeben. Die genauen Angaben erhältst du mit der Ausschreibung."),
        ("Kann ich einzelne Module buchen?",
         "Bei Clinical Expert kannst du einzelne Module buchen. Für jedes Modul erhältst du nach Erfüllung der Anforderungen ein Mikrozertifikat, und abgeschlossene Module sind auf den Gesamtlehrgang anrechenbar. Für den Gesamtabschluss kommen Supervision und Falldokumentation hinzu. Basic und Advanced sind zusammenhängende Lehrgänge."),
        ("Wie funktioniert die Anmeldung?",
         "Trage dich zunächst unverbindlich in die Interessentenliste ein. Sobald die Ausschreibung vorliegt, senden wir dir Termine, Konditionen und Unterlagen für die verbindliche Anmeldung. Der Eintrag reserviert noch keinen Platz. Nach verbindlicher Anmeldung erfolgt die Zahlung per Überweisung. Für mehrteilige Lehrgänge bieten wir auf Anfrage Ratenzahlung an. Die Höhe der Raten und die Zahlungstermine teilen wir dir vor der verbindlichen Anmeldung schriftlich mit."),
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

# Social Media (Footer). Leere Adresse = Symbol wird nicht angezeigt.
SOCIAL = [
    ("instagram", "https://www.instagram.com/permamindacademy/"),
    ("facebook", "https://www.facebook.com/profile.php?id=61593453518327"),
    ("linkedin", "https://www.linkedin.com/company/145489665/"),
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
