# 📚 Οδηγός Πηγών, Μελέτης & Τεχνικής Τεκμηρίωσης (Knowledge Map & Learning Resources)
## Anytime.gr Hybrid Knowledge RAG Chatbot System

> **Σκοπός:** Αυτό το αρχείο αποτελεί τον **Πλήρη Εκπαιδευτικό Χάρτη (Learning Blueprint)** με όλες τις επίσημες πηγές, βιβλιογραφία, documentation και tutorials για κάθε τεχνολογία, αρχιτεκτονική αρχή και αλγόριθμο που χρησιμοποιείται στο έργο.

---

## 📑 Πίνακας Περιεχομένων

1. [Αρχιτεκτονική & Αρχές Σχεδιασμού (Uncle Bob & Clean Architecture)](#1-αρχιτεκτονική--αρχές-σχεδιασμού-uncle-bob--clean-architecture)
2. [Java 21 LTS & Spring Boot 3.3.4](#2-java-21-lts--spring-boot-334)
3. [Gradle 8.10 (Groovy DSL) & Build Automation](#3-gradle-810-groovy-dsl--build-automation)
4. [Angular 22 Signals & Modern Frontend](#4-angular-22-signals--modern-frontend)
5. [Bootstrap 5.3 & Responsive CSS Grid](#5-bootstrap-53--responsive-css-grid)
6. [Information Retrieval, BM25 & Greek Text Processing](#6-information-retrieval-bm25--greek-text-processing)
7. [Πρωτόκολλα Επικοινωνίας: Real-Time WebSockets (RFC 6455)](#7-πρωτόκολλα-επικοινωνίας-real-time-websockets-rfc-6455)
8. [Προτεινόμενο Μονοπάτι Μελέτης Βήμα-προς-Βήμα (Step-by-Step Learning Path)](#8-προτεινόμενο-μονοπάτι-μελέτης-βήμα-προς-βήμα)

---

## 1. Αρχιτεκτονική & Αρχές Σχεδιασμού (Uncle Bob & Clean Architecture)

Η αρχιτεκτονική του Backend βασίζεται 100% στις διδαχές του **Robert C. Martin (Uncle Bob)** και στο πρότυπο **Ports & Adapters (Hexagonal Architecture)**.

### 📖 Βασική Βιβλιογραφία:
* 📕 **«Clean Architecture: A Craftsman's Guide to Software Structure and Design»** — Robert C. Martin (Prentice Hall).  
  * *Τι να διαβάσετε:* Κεφάλαια 19-22 (The Dependency Rule, Entity Layer, Use Cases, Presenters & Controllers).
* 📗 **«Clean Code: A Handbook of Agile Software Craftsmanship»** — Robert C. Martin.  
  * *Τι να διαβάσετε:* Meaningful Names, Functions (Do One Thing), Classes (Single Responsibility).

### 🌐 Επίσημα Άρθρα & Online Resources:
* 🔗 [The Clean Architecture (Επίσημο Blog Uncle Bob / Clean Coder)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)  
  * Το θεμελιώδες άρθρο με το διάγραμμα των ομόκεντρων κύκλων (Entities $\to$ Use Cases $\to$ Interface Adapters $\to$ Frameworks).
* 🔗 [S.O.L.I.D. Principles Guide (Baeldung)](https://www.baeldung.com/solid-principles)  
  * Αναλυτικά παραδείγματα σε Java για Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.
* 🔗 [Hexagonal Architecture (Alistair Cockburn)](https://alistair.cockburn.us/hexagonal-architecture/)  
  * Πώς τα Inbound και Outbound Ports απομονώνουν την επιχειρησιακή λογική από τις βάσεις δεδομένων και τα UI.

### 📍 Αντιστοίχιση στον Κώδικά μας:
* **Domain Models:** [`FaqItem.java`](file:///g:/WIDGET-UI/BACKEND_JAVA/src/main/java/com/anytime/chatbot/domain/model/FaqItem.java), [`PassageChunk.java`](file:///g:/WIDGET-UI/BACKEND_JAVA/src/main/java/com/anytime/chatbot/domain/model/PassageChunk.java)
* **Inbound/Outbound Ports:** [`SearchKnowledgeUseCase.java`](file:///g:/WIDGET-UI/BACKEND_JAVA/src/main/java/com/anytime/chatbot/usecase/port/in/SearchKnowledgeUseCase.java), [`KnowledgeRepositoryPort.java`](file:///g:/WIDGET-UI/BACKEND_JAVA/src/main/java/com/anytime/chatbot/usecase/port/out/KnowledgeRepositoryPort.java)
* **Use Case Service:** [`SearchKnowledgeService.java`](file:///g:/WIDGET-UI/BACKEND_JAVA/src/main/java/com/anytime/chatbot/usecase/impl/SearchKnowledgeService.java)

---

## 2. Java 21 LTS & Spring Boot 3.3.4

Το Backend χρησιμοποιεί τη σύγχρονη έκδοση **Java 21 LTS** και το **Spring Boot 3.3.4**.

### 🌐 Επίσημο Documentation:
* 🔗 [Oracle Java 21 Official Documentation](https://docs.oracle.com/en/java/javase/21/)  
  * Ειδικά τα **Java Records (JEP 395)**: Αμετάβλητες δομές δεδομένων χωρίς getters/setters boilerplate.
  * **Pattern Matching for switch (JEP 441)** και **Virtual Threads / Project Loom (JEP 444)**.
* 🔗 [Spring Boot 3.3.x Reference Guide](https://docs.spring.io/spring-boot/reference/index.html)  
  * Ενσωματωμένος Tomcat Server, Configuration Properties, Dependency Injection (`@Service`, `@RestController`).
* 🔗 [Spring Framework WebSocket Support](https://docs.spring.io/spring-framework/reference/web/websocket.html)  
  * Υλοποίηση `TextWebSocketHandler` και `WebSocketConfigurer` για real-time streaming.
* 🔗 [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/) & [Mockito Documentation](https://site.mockito.org/)  
  * Σύνταξη unit tests με `@ExtendWith(MockitoExtension.class)` και `@Mock`.

### 📍 Αντιστοίχιση στον Κώδικά μας:
* **WebSocket Config:** [`WebSocketConfig.java`](file:///g:/WIDGET-UI/BACKEND_JAVA/src/main/java/com/anytime/chatbot/config/WebSocketConfig.java)
* **WebSocket Handler:** [`ChatWebSocketHandler.java`](file:///g:/WIDGET-UI/BACKEND_JAVA/src/main/java/com/anytime/chatbot/controller/ChatWebSocketHandler.java)
* **Unit Tests:** [`SearchKnowledgeServiceTest.java`](file:///g:/WIDGET-UI/BACKEND_JAVA/src/test/java/com/anytime/chatbot/usecase/impl/SearchKnowledgeServiceTest.java)

---

## 3. Gradle 8.10 (Groovy DSL) & Build Automation

Το έργο χτίζεται αποκλειστικά με το **Gradle** χρησιμοποιώντας **Groovy DSL**.

### 🌐 Επίσημο Documentation:
* 🔗 [Gradle User Manual (Official)](https://docs.gradle.org/current/userguide/userguide.html)  
  * Πώς λειτουργεί το Incremental Build, το Gradle Daemon, και το Task execution.
* 🔗 [Spring Boot Gradle Plugin Reference](https://docs.spring.io/spring-boot/gradle-plugin/index.html)  
  * Εντολές `bootRun` (εκκίνηση dev server) και `bootJar` (παραγωγή αυτόνομου εκτελέσιμου JAR).
* 🔗 [Gradle Java Toolchains](https://docs.gradle.org/current/userguide/toolchains.html)  
  * Αυτόματη ανίχνευση και δέσμευση της έκδοσης Java 21 (`JavaLanguageVersion.of(21)`).

### 📍 Αντιστοίχιση στον Κώδικά μας:
* **Build Script:** [`build.gradle`](file:///g:/WIDGET-UI/BACKEND_JAVA/build.gradle)
* **Settings:** [`settings.gradle`](file:///g:/WIDGET-UI/BACKEND_JAVA/settings.gradle)
* **Wrapper:** `gradlew.bat` / `gradlew`

---

## 4. Angular 22 Signals & Modern Frontend

Το Frontend είναι ένα αυτόνομο Web Widget γραμμένο σε **Angular 22** με **Angular Signals**.

### 🌐 Επίσημο Documentation:
* 🔗 [Angular.dev (Επίσημο Νέο Documentation)](https://angular.dev/)  
  * **Angular Signals:** `signal()`, `computed()`, `effect()` — fine-grained αντιδραστικότητα.
  * **Standalone Components:** `standalone: true` χωρίς την ανάγκη για παλιά `NgModule`.
  * **New Control Flow Syntax:** Χρήση των νέων οδηγιών `@if`, `@else`, `@for (item of list; track item.id)`.
* 🔗 [TypeScript Handbook (v5.5+)](https://www.typescriptlang.org/docs/handbook/intro.html)  
  * Αυστηρά types (`interfaces`, `enums`, `union types`).

### 📍 Αντιστοίχιση στον Κώδικά μας:
* **Component Logic & Signals:** [`chat-widget.component.ts`](file:///g:/WIDGET-UI/UI/src/app/components/chat-widget/chat-widget.component.ts)
* **Component Template (@for / @if):** [`chat-widget.component.html`](file:///g:/WIDGET-UI/UI/src/app/components/chat-widget/chat-widget.component.html)
* **WebSocket Service:** [`websocket-chat.service.ts`](file:///g:/WIDGET-UI/UI/src/app/services/websocket-chat.service.ts)
* **Domain DTOs:** [`chat.models.ts`](file:///g:/WIDGET-UI/UI/src/app/models/chat.models.ts)

---

## 5. Bootstrap 5.3 & Responsive CSS Grid

Για την εμφάνιση χρησιμοποιείται συνδυασμός **Bootstrap 5.3 Utility Flexbox** και **Modern CSS Grid**.

### 🌐 Επίσημο Documentation:
* 🔗 [Bootstrap 5.3 Official Documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/)  
  * **Grid & Flexbox:** `.d-flex`, `.flex-column`, `.row`, `.col`, `.gap-2`, `.align-items-center`.
* 🔗 [MDN Web Docs: CSS Grid Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout)  
  * `display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px;` — Πώς κατασκευάστηκε το συμπαγές 4x2 categories grid.
* 🔗 [Glassmorphism CSS Generator & Guide](https://css.glass/)  
  * `backdrop-filter: blur(12px)`, ημιδιαφανή backgrounds και gradient borders.

### 📍 Αντιστοίχιση στον Κώδικά μας:
* **Widget SCSS Styles:** [`chat-widget.component.scss`](file:///g:/WIDGET-UI/UI/src/app/components/chat-widget/chat-widget.component.scss)
* **Global Theme:** [`styles.scss`](file:///g:/WIDGET-UI/UI/src/styles.scss)

---

## 6. Information Retrieval, BM25 & Greek Text Processing

Η καρδιά του συστήματος είναι η **100% Extractive Μηχανή Ανάκτησης**.

### 📖 Θεμελιώδης Βιβλιογραφία:
* 📕 **«Introduction to Information Retrieval»** — Christopher D. Manning, Prabhakar Raghavan, Hinrich Schütze (Cambridge University Press).  
  * *Διαθέσιμο δωρεάν online:* [https://nlp.stanford.edu/IR-book/](https://nlp.stanford.edu/IR-book/)  
  * *Τι να διαβάσετε:* Κεφάλαιο 6 (Scoring, term weighting & the Vector Space Model), Κεφάλαιο 11 (Probabilistic Information Retrieval & Okapi BM25).

### 🌐 Αλγόριθμοι & Ελληνική Γλώσσα:
* 🔗 [Okapi BM25 Algorithm Overview (Wikipedia / Stanford NLP)](https://en.wikipedia.org/wiki/Okapi_BM25)  
  * Πώς υπολογίζεται η συχνότητα όρων (TF) και η αντίστροφη συχνότητα εγγράφων (IDF).
* 🔗 [Unicode Greek and Coptic Character Block](https://en.wikipedia.org/wiki/Greek_and_Coptic)  
  * Επεξήγηση τόνων (οξεία, διαλυτικά) και μετατροπή τελικού σίγμα (`ς` U+03C2 $\to$ `σ` U+03C3).

### 📍 Αντιστοίχιση στον Κώδικά μας:
* **Greek Text Normalizer:** [`TextNormalizer.java`](file:///g:/WIDGET-UI/BACKEND_JAVA/src/main/java/com/anytime/chatbot/domain/service/TextNormalizer.java)
* **Snippet Slicer & Phone Intent:** [`SnippetExtractor.java`](file:///g:/WIDGET-UI/BACKEND_JAVA/src/main/java/com/anytime/chatbot/domain/service/SnippetExtractor.java)
* **BM25 Search Engine:** [`PureJavaHybridSearchEngine.java`](file:///g:/WIDGET-UI/BACKEND_JAVA/src/main/java/com/anytime/chatbot/infrastructure/adapter/PureJavaHybridSearchEngine.java)

---

## 7. Πρωτόκολλα Επικοινωνίας: Real-Time WebSockets (RFC 6455)

Το σύστημα λειτουργεί σε **Stealth / Zero HTTP Exposure Mode** χρησιμοποιώντας **αποκλειστικά WebSocket επικοινωνία**.

### 🌐 Επίσημα Standards & Guides:
* 🔗 [RFC 6455: The WebSocket Protocol (IETF)](https://datatracker.ietf.org/doc/html/rfc6455)  
  * Αμφίδρομη, full-duplex επικοινωνία σε πραγματικό χρόνο πάνω από μία σύνδεση TCP χωρίς HTTP overhead.
* 🔗 [MDN Web Docs: Writing WebSocket client applications](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_client_applications)  
  * Πώς διαχειριζόμαστε `onopen`, `onmessage`, `onclose`, και αυτόματο επανασυντονισμό (auto-reconnection).
* 🔗 [Spring Framework WebSocket Reference Guide](https://docs.spring.io/spring-framework/reference/web/websocket.html)  
  * Υλοποίηση καθαρού `TextWebSocketHandler` και `WebSocketConfigurer` σε Spring Boot 3.

### 📍 Αντιστοίχιση στον Κώδικά μας:
* **WebSocket Controller:** [`ChatWebSocketHandler.java`](file:///g:/WIDGET-UI/BACKEND_JAVA/src/main/java/com/anytime/chatbot/controller/ChatWebSocketHandler.java)
* **WebSocket Configuration:** [`WebSocketConfig.java`](file:///g:/WIDGET-UI/BACKEND_JAVA/src/main/java/com/anytime/chatbot/config/WebSocketConfig.java)
* **Frontend WebSocket Service:** [`websocket-chat.service.ts`](file:///g:/WIDGET-UI/UI/src/app/services/websocket-chat.service.ts)

---

## 8. Προτεινόμενο Μονοπάτι Μελέτης Βήμα-προς-Βήμα

Αν θέλετε να κατανοήσετε πλήρως πώς λειτουργεί το σύστημα και να αποκτήσετε τη γνώση να χτίζετε παρόμοια enterprise συστήματα:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ΒΗΜΑΤΑ ΕΚΜΑΘΗΣΗΣ ΤΟΥ ΣΥΣΤΗΜΑΤΟΣ (ROADMAP)                │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. ΔΙΑΒΑΣΤΕ ΤΟ DOMAIN LAYER:                                                │
│    Ανοίξτε το TextNormalizer.java & SnippetExtractor.java για να δείτε      │
│    πώς καθαρίζεται το ελληνικό κείμενο χωρίς καμία εξωτερική βιβλιοθήκη.    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. ΜΕΛΕΤΗΣΤΕ ΤΟ USE CASE & TA PORTS (Uncle Bob):                            │
│    Δείτε πώς το SearchKnowledgeService.java εξαρτάται μόνο από interfaces   │
│    (KnowledgeRepositoryPort & SearchEnginePort) και πώς ελέγχεται με mock.  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. ΕΞΕΡΕΥΝΗΣΤΕ ΤΗΝ PURE JAVA SEARCH ENGINE:                                 │
│    Δείτε πώς υλοποιείται ο BM25 αλγόριθμος και τα category weights στο      │
│    PureJavaHybridSearchEngine.java.                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. ΔΕΙΤΕ ΤΗ ΣΥΝΔΕΣΗ WEBSOCKET & MVC CONTROLLER:                             │
│    Δείτε πώς το ChatWebSocketHandler.java στέλνει JSON πίσω στο UI.         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. ΜΕΛΕΤΗΣΤΕ ΤΟ ANGULAR 22 SIGNALS COMPONENT:                               │
│    Ανοίξτε το chat-widget.component.ts & .html για να δείτε πώς τα Signals  │
│    ενημερώνουν αυτόματα το UI χωρίς περιττά re-renders.                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

© 2026 Anytime.gr Knowledge Retrieval System. All Rights Reserved.  
*Educational & Technical Knowledge Map.*
